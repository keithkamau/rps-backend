from app import db
from app.models.statistics import UserStatistics
from app.models.user import User

class StatisticsService:
    
    @staticmethod
    def record_game(user_id, won, choice):
        stats = UserStatistics.query.filter_by(user_id=user_id).first()
        if not stats:
            return
        
        stats.games_played += 1
        
        if won:
            stats.games_won += 1
            stats.current_streak += 1
            if stats.current_streak > stats.best_streak:
                stats.best_streak = stats.current_streak
        else:
            stats.games_lost += 1
            stats.current_streak = 0
        
        if choice == 'rock':
            stats.rock_count += 1
        elif choice == 'paper':
            stats.paper_count += 1
        elif choice == 'scissors':
            stats.scissors_count += 1
        
        db.session.commit()
    
    @staticmethod
    def get_leaderboard():
        stats = UserStatistics.query.join(User).filter(
            User.is_active == True
        ).order_by(UserStatistics.games_won.desc()).limit(20).all()
        
        leaderboard = []
        for rank, stat in enumerate(stats, 1):
            user = User.query.get(stat.user_id)
            leaderboard.append({
                'rank': rank,
                'username': user.username,
                'games_won': stat.games_won,
                'win_rate': round(stat.games_won / stat.games_played * 100, 1) if stat.games_played > 0 else 0,
                'tournaments_won': stat.tournaments_won,
                'best_streak': stat.best_streak
            })
        
        return leaderboard
    
    @staticmethod
    def record_tournament_win(user_id):
        stats = UserStatistics.query.filter_by(user_id=user_id).first()
        if stats:
            stats.tournaments_won += 1
            db.session.commit()