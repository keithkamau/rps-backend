from app import db
from datetime import datetime

class Tournament(db.Model):
    __tablename__ = 'tournaments'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), default='waiting')  # waiting, active, completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    players = db.relationship('TournamentPlayer', backref='tournament')
    matches = db.relationship('Match', backref='tournament')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'status': self.status,
            'player_count': len(self.players),
            'created_at': self.created_at.isoformat()
        }

class TournamentPlayer(db.Model):
    __tablename__ = 'tournament_players'
    
    id = db.Column(db.Integer, primary_key=True)
    tournament_id = db.Column(db.Integer, db.ForeignKey('tournaments.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    seed = db.Column(db.Integer)
    eliminated = db.Column(db.Boolean, default=False)
    
    user = db.relationship('User')