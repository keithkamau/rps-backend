from app import db

class UserStatistics(db.Model):
    __tablename__ = 'user_statistics'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)
    games_played = db.Column(db.Integer, default=0)
    games_won = db.Column(db.Integer, default=0)
    games_lost = db.Column(db.Integer, default=0)
    tournaments_won = db.Column(db.Integer, default=0)
    rock_count = db.Column(db.Integer, default=0)
    paper_count = db.Column(db.Integer, default=0)
    scissors_count = db.Column(db.Integer, default=0)
    current_streak = db.Column(db.Integer, default=0)
    best_streak = db.Column(db.Integer, default=0)
    
    def to_dict(self):
        total_moves = self.rock_count + self.paper_count + self.scissors_count
        return {
            'user_id': self.user_id,
            'games_played': self.games_played,
            'games_won': self.games_won,
            'games_lost': self.games_lost,
            'win_rate': round(self.games_won / self.games_played * 100, 1) if self.games_played > 0 else 0,
            'tournaments_won': self.tournaments_won,
            'favorite_move': max([
                ('rock', self.rock_count),
                ('paper', self.paper_count),
                ('scissors', self.scissors_count)
            ], key=lambda x: x[1])[0] if total_moves > 0 else None,
            'current_streak': self.current_streak,
            'best_streak': self.best_streak
        }