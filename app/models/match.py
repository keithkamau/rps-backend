from app import db
from datetime import datetime

class Match(db.Model):
    __tablename__ = 'matches'
    
    id = db.Column(db.Integer, primary_key=True)
    tournament_id = db.Column(db.Integer, db.ForeignKey('tournaments.id'))
    round_number = db.Column(db.Integer, nullable=False)
    player1_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    player2_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    winner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    status = db.Column(db.String(20), default='pending')  # pending, active, completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    player1 = db.relationship('User', foreign_keys=[player1_id])
    player2 = db.relationship('User', foreign_keys=[player2_id])
    winner = db.relationship('User', foreign_keys=[winner_id])
    rounds = db.relationship('Round', backref='match')
    
    def to_dict(self):
        return {
            'id': self.id,
            'tournament_id': self.tournament_id,
            'round_number': self.round_number,
            'player1': self.player1.username if self.player1 else None,
            'player2': self.player2.username if self.player2 else None,
            'winner': self.winner.username if self.winner else None,
            'status': self.status
        }

class Round(db.Model):
    __tablename__ = 'rounds'
    
    id = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.Integer, db.ForeignKey('matches.id'))
    round_number = db.Column(db.Integer, nullable=False)
    player1_choice = db.Column(db.String(10))
    player2_choice = db.Column(db.String(10))
    winner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    def to_dict(self):
        return {
            'id': self.id,
            'match_id': self.match_id,
            'round_number': self.round_number,
            'player1_choice': self.player1_choice,
            'player2_choice': self.player2_choice,
            'winner_id': self.winner_id
        }