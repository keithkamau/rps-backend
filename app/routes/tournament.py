from flask import Blueprint, request, jsonify
from app import db
from app.models.tournament import Tournament, TournamentPlayer
from app.services.tournament_service import TournamentService
from app.utils.decorators import token_required

tournament_bp = Blueprint('tournament', __name__)

@tournament_bp.route('/create', methods=['POST'])
@token_required
def create_tournament(user_id):
    data = request.get_json()
    name = data.get('name', 'New Tournament')
    
    tournament = TournamentService.create_tournament(name)
    
    return jsonify({
        'message': 'Tournament created',
        'tournament': tournament.to_dict()
    }), 201

@tournament_bp.route('/active', methods=['GET'])
@token_required
def get_active_tournaments(user_id):
    tournaments = Tournament.query.filter(
        Tournament.status.in_(['waiting', 'active'])
    ).order_by(Tournament.created_at.desc()).all()
    
    return jsonify({
        'tournaments': [t.to_dict() for t in tournaments]
    }), 200

@tournament_bp.route('/<int:tournament_id>/join', methods=['POST'])
@token_required
def join_tournament(user_id, tournament_id):
    tournament, error = TournamentService.join_tournament(tournament_id, user_id)
    
    if error:
        return jsonify({'error': error}), 400
    
    return jsonify({
        'message': 'Joined tournament',
        'tournament': tournament.to_dict()
    }), 200

@tournament_bp.route('/<int:tournament_id>/bracket', methods=['GET'])
@token_required
def get_bracket(user_id, tournament_id):
    bracket = TournamentService.get_bracket(tournament_id)
    
    if not bracket:
        return jsonify({'error': 'Tournament not found'}), 404
    
    return jsonify(bracket), 200

@tournament_bp.route('/<int:tournament_id>', methods=['GET'])
@token_required
def get_tournament(user_id, tournament_id):
    tournament = Tournament.query.get(tournament_id)
    
    if not tournament:
        return jsonify({'error': 'Tournament not found'}), 404
    
    players = TournamentPlayer.query.filter_by(tournament_id=tournament_id).all()
    
    return jsonify({
        'tournament': tournament.to_dict(),
        'players': [{
            'id': p.user_id,
            'username': p.user.username,
            'seed': p.seed,
            'eliminated': p.eliminated
        } for p in players]
    }), 200