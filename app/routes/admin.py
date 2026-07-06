from flask import Blueprint, jsonify
from app.models.user import User
from app.models.tournament import Tournament
from app.services.statistics_service import StatisticsService
from app.utils.decorators import token_required

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/stats', methods=['GET'])
@token_required
def get_platform_stats(user_id):
    total_users = User.query.count()
    active_tournaments = Tournament.query.filter_by(status='active').count()
    waiting_tournaments = Tournament.query.filter_by(status='waiting').count()
    completed_tournaments = Tournament.query.filter_by(status='completed').count()
    
    return jsonify({
        'total_users': total_users,
        'active_tournaments': active_tournaments,
        'waiting_tournaments': waiting_tournaments,
        'completed_tournaments': completed_tournaments
    }), 200

@admin_bp.route('/leaderboard', methods=['GET'])
@token_required
def get_leaderboard(user_id):
    leaderboard = StatisticsService.get_leaderboard()
    return jsonify({'leaderboard': leaderboard}), 200

@admin_bp.route('/tournaments', methods=['GET'])
@token_required
def get_all_tournaments(user_id):
    tournaments = Tournament.query.order_by(Tournament.created_at.desc()).all()
    return jsonify({'tournaments': [t.to_dict() for t in tournaments]}), 200