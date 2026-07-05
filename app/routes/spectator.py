from flask import Blueprint, request, jsonify
from app import db
from app.models.match import Match
from app.utils.decorators import token_required

spectator_bp = Blueprint('spectator', __name__)

@spectator_bp.route('/match/<int:match_id>', methods=['GET'])
@token_required
def spectate_match(user_id, match_id):
    match = Match.query.get(match_id)
    
    if not match:
        return jsonify({'error': 'Match not found'}), 404
    
    # Anyone can spectate active matches
    if match.status not in ['active', 'completed']:
        return jsonify({'error': 'Match is not available for spectating'}), 400
    
    return jsonify({
        'match': match.to_dict(),
        'rounds': [r.to_dict() for r in match.rounds]
    }), 200

@spectator_bp.route('/active-matches', methods=['GET'])
@token_required
def get_active_matches(user_id):
    matches = Match.query.filter_by(status='active').all()
    
    return jsonify({
        'matches': [m.to_dict() for m in matches]
    }), 200