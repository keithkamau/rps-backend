from app import db
from app.models.tournament import Tournament, TournamentPlayer
from app.models.match import Match, Round
import random

class TournamentService:
    
    @staticmethod
    def create_tournament(name):
        tournament = Tournament(name=name, status='waiting')
        db.session.add(tournament)
        db.session.commit()
        return tournament
    
    @staticmethod
    def join_tournament(tournament_id, user_id):
        tournament = Tournament.query.get(tournament_id)
        if not tournament:
            return None, "Tournament not found"
        
        if tournament.status != 'waiting':
            return None, "Tournament has already started"
        
        existing = TournamentPlayer.query.filter_by(
            tournament_id=tournament_id, 
            user_id=user_id
        ).first()
        
        if existing:
            return None, "Already joined"
        
        player = TournamentPlayer(tournament_id=tournament_id, user_id=user_id)
        db.session.add(player)
        db.session.commit()
        
        player_count = TournamentPlayer.query.filter_by(tournament_id=tournament_id).count()
        
        if player_count >= 4:
            TournamentService.start_tournament(tournament_id)
        
        return tournament, None
    
    @staticmethod
    def start_tournament(tournament_id):
        tournament = Tournament.query.get(tournament_id)
        if not tournament or tournament.status != 'waiting':
            return
        
        players = TournamentPlayer.query.filter_by(tournament_id=tournament_id).all()
        
        if len(players) < 4:
            return
        
        random.shuffle(players)
        for i, player in enumerate(players):
            player.seed = i + 1
        
        TournamentService.generate_matches(tournament, players)
        
        tournament.status = 'active'
        db.session.commit()
    
    @staticmethod
    def generate_matches(tournament, players):
        round_number = 1
        
        existing = Match.query.filter_by(tournament_id=tournament.id).all()
        if existing:
            round_number = max(m.round_number for m in existing) + 1
        
        for i in range(0, len(players), 2):
            if i + 1 < len(players):
                match = Match(
                    tournament_id=tournament.id,
                    round_number=round_number,
                    player1_id=players[i].user_id,
                    player2_id=players[i+1].user_id,
                    status='pending'
                )
                db.session.add(match)
        
        db.session.commit()
    
    @staticmethod
    def advance_winner(match_id, winner_id):
        match = Match.query.get(match_id)
        if not match or match.status != 'active':
            return
        
        match.winner_id = winner_id
        match.status = 'completed'
        
        tournament = Tournament.query.get(match.tournament_id)
        round_matches = Match.query.filter_by(
            tournament_id=tournament.id,
            round_number=match.round_number
        ).all()
        
        round_complete = all(m.status == 'completed' for m in round_matches)
        
        if round_complete:
            winners = [m.winner_id for m in round_matches if m.winner_id]
            
            all_players = TournamentPlayer.query.filter_by(
                tournament_id=tournament.id,
                eliminated=False
            ).all()
            
            for player in all_players:
                if player.user_id not in winners:
                    player.eliminated = True
            
            if len(winners) == 1:
                tournament.status = 'completed'
                from app.services.statistics_service import StatisticsService
                StatisticsService.record_tournament_win(winners[0])
            elif len(winners) >= 2:
                next_players = TournamentPlayer.query.filter_by(
                    tournament_id=tournament.id,
                    eliminated=False
                ).all()
                TournamentService.generate_matches(tournament, next_players)
        
        db.session.commit()
    
    @staticmethod
    def get_bracket(tournament_id):
        tournament = Tournament.query.get(tournament_id)
        if not tournament:
            return None
        
        matches = Match.query.filter_by(tournament_id=tournament_id).order_by(
            Match.round_number, Match.id
        ).all()
        
        rounds = {}
        for match in matches:
            round_key = f"round_{match.round_number}"
            if round_key not in rounds:
                rounds[round_key] = []
            
            match_data = match.to_dict()
            match_data['rounds'] = [r.to_dict() for r in match.rounds]
            rounds[round_key].append(match_data)
        
        return {
            'tournament': tournament.to_dict(),
            'rounds': rounds
        }