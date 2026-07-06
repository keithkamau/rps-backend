from flask import Blueprint, request, jsonify
from app import db
from app.models.match import Match, Round
from app.services.game_logic import GameLogic
from app.services.statistics_service import StatisticsService
from app.utils.decorators import token_required

game_bp = Blueprint('game', __name__)

@game_bp.route('/match/<int:match_id>', methods=['GET'])
@token_required
def get_match(user_id, match_id):
    match = Match.query.get(match_id)
    
    if not match:
        return jsonify({'error': 'Match not found'}), 404
    
    if user_id != match.player1_id and user_id != match.player2_id:
        return jsonify({'error': 'Not your match'}), 403
    
    return jsonify({
        'match': match.to_dict(),
        'rounds': [r.to_dict() for r in match.rounds]
    }), 200

@game_bp.route('/match/<int:match_id>/start-round', methods=['POST'])
@token_required
def start_round(user_id, match_id):
    match = Match.query.get(match_id)
    
    if not match:
        return jsonify({'error': 'Match not found'}), 404
    
    if user_id != match.player1_id and user_id != match.player2_id:
        return jsonify({'error': 'Not your match'}), 403
    
    if match.status == 'pending':
        match.status = 'active'
    
    round_count = Round.query.filter_by(match_id=match_id).count()
    
    new_round = Round(
        match_id=match_id,
        round_number=round_count + 1
    )
    
    db.session.add(new_round)
    db.session.commit()
    
    return jsonify({
        'message': 'Round started',
        'round': new_round.to_dict(),
        'countdown': 5
    }), 201

@game_bp.route('/match/<int:match_id>/round/<int:round_id>/choice', methods=['POST'])
@token_required
def submit_choice(user_id, match_id, round_id):
    match = Match.query.get(match_id)
    
    if not match:
        return jsonify({'error': 'Match not found'}), 404
    
    if match.status != 'active':
        return jsonify({'error': 'Match is not active'}), 400
    
    data = request.get_json()
    choice = data.get('choice')
    
    if not GameLogic.validate_choice(choice):
        return jsonify({'error': 'Invalid choice. Must be rock, paper, or scissors'}), 400
    
    round_record = Round.query.get(round_id)
    if not round_record:
        return jsonify({'error': 'Round not found'}), 404
    
    if user_id == match.player1_id:
        if round_record.player1_choice:
            return jsonify({'error': 'Choice already submitted'}), 400
        round_record.player1_choice = choice
    elif user_id == match.player2_id:
        if round_record.player2_choice:
            return jsonify({'error': 'Choice already submitted'}), 400
        round_record.player2_choice = choice
    else:
        return jsonify({'error': 'Not your match'}), 403
    
    db.session.commit()
    
    if round_record.player1_choice and round_record.player2_choice:
        result = GameLogic.determine_winner(
            round_record.player1_choice,
            round_record.player2_choice
        )
        
        if result == 'player1':
            round_record.winner_id = match.player1_id
        elif result == 'player2':
            round_record.winner_id = match.player2_id
        
        # Update statistics
        player1_won = result == 'player1'
        player2_won = result == 'player2'
        
        StatisticsService.record_game(match.player1_id, player1_won, round_record.player1_choice)
        StatisticsService.record_game(match.player2_id, player2_won, round_record.player2_choice)
        
        db.session.commit()
        
        return jsonify({
            'round': round_record.to_dict(),
            'result': result
        }), 200
    
    return jsonify({
        'message': 'Choice recorded, waiting for opponent',
        'round': round_record.to_dict()
    }), 200