from app import socketio
from flask import request
from flask_socketio import join_room, leave_room, emit

# Store active matches and their timers
active_matches = {}

@socketio.on('connect')
def handle_connect():
    print(f'Client connected: {request.sid}')

@socketio.on('disconnect')
def handle_disconnect():
    print(f'Client disconnected: {request.sid}')
    # Clean up any matches this client was in
    for match_id in list(active_matches.keys()):
        match_data = active_matches[match_id]
        if request.sid in match_data['players']:
            # Handle player disconnect - treat as forfeit
            socketio.emit('player_disconnected', {
                'match_id': match_id,
                'player_sid': request.sid
            }, room=f'match_{match_id}')

@socketio.on('join_match')
def handle_join_match(data):
    match_id = data.get('match_id')
    user_id = data.get('user_id')
    
    room = f'match_{match_id}'
    join_room(room)
    
    if match_id not in active_matches:
        active_matches[match_id] = {
            'players': {},
            'round': 1,
            'choices': {},
            'scores': {'player1': 0, 'player2': 0},
            'countdown': None
        }
    
    active_matches[match_id]['players'][request.sid] = user_id
    
    # Notify room
    player_count = len(active_matches[match_id]['players'])
    emit('player_joined', {
        'match_id': match_id,
        'player_count': player_count
    }, room=room)
    
    # Start match when 2 players join
    if player_count == 2:
        emit('match_ready', {
            'match_id': match_id,
            'countdown': 5
        }, room=room)

@socketio.on('submit_choice')
def handle_submit_choice(data):
    match_id = data.get('match_id')
    round_number = data.get('round_number')
    choice = data.get('choice')
    
    if match_id not in active_matches:
        return
    
    match_data = active_matches[match_id]
    match_data['choices'][request.sid] = choice
    
    # Notify opponent (without revealing choice)
    emit('opponent_chose', {
        'message': 'Opponent has made their choice'
    }, room=f'match_{match_id}', include_self=False)
    
    # If both players chose, determine winner
    if len(match_data['choices']) == 2:
        from .game_logic import GameLogic
        
        choices = list(match_data['choices'].values())
        sids = list(match_data['choices'].keys())
        
        result = GameLogic.determine_winner(choices[0], choices[1])
        
        # Send result to both players
        result_data = {
            'round_number': round_number,
            'player1_choice': choices[0] if result == 'player1' else choices[1],
            'player2_choice': choices[1] if result == 'player1' else choices[0],
            'result': result,
            'your_choice': match_data['choices'][request.sid]
        }
        
        emit('round_result', result_data, room=f'match_{match_id}')
        
        # Update scores
        if result == 'player1':
            match_data['scores']['player1'] += 1
        elif result == 'player2':
            match_data['scores']['player2'] += 1
        
        # Check if match is over (best of 3)
        if match_data['scores']['player1'] == 2 or match_data['scores']['player2'] == 2:
            winner = 'player1' if match_data['scores']['player1'] == 2 else 'player2'
            emit('match_over', {
                'winner': winner,
                'scores': match_data['scores']
            }, room=f'match_{match_id}')
            
            # Clean up
            del active_matches[match_id]
        else:
            # Reset for next round
            match_data['round'] += 1
            match_data['choices'] = {}
            
            emit('next_round', {
                'round_number': match_data['round'],
                'scores': match_data['scores'],
                'countdown': 5
            }, room=f'match_{match_id}')

@socketio.on('join_tournament_room')
def handle_join_tournament(data):
    tournament_id = data.get('tournament_id')
    room = f'tournament_{tournament_id}'
    join_room(room)
    emit('joined_tournament', {'tournament_id': tournament_id})

@socketio.on('spectate_match')
def handle_spectate(data):
    match_id = data.get('match_id')
    room = f'match_{match_id}'
    join_room(room)
    
    if match_id in active_matches:
        emit('spectate_update', {
            'match_id': match_id,
            'scores': active_matches[match_id]['scores'],
            'round': active_matches[match_id]['round']
        })