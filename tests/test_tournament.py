from app.models.tournament import Tournament

def test_create_tournament(auth_headers, client):
    response = client.post('/api/tournament/create', 
        headers=auth_headers,
        json={'name': 'Test Tournament'}
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data['tournament']['name'] == 'Test Tournament'
    assert data['tournament']['status'] == 'waiting'

def test_get_active_tournaments(auth_headers, client):
    client.post('/api/tournament/create', 
        headers=auth_headers,
        json={'name': 'Tourney 1'}
    )
    response = client.get('/api/tournament/active', headers=auth_headers)
    assert response.status_code == 200
    assert len(response.get_json()['tournaments']) >= 1

def test_join_tournament(auth_headers, client):
    client.post('/api/tournament/create', 
        headers=auth_headers,
        json={'name': 'Joinable'}
    )
    response = client.post('/api/tournament/1/join', headers=auth_headers)
    assert response.status_code == 200

def test_join_tournament_twice(auth_headers, client):
    client.post('/api/tournament/create', 
        headers=auth_headers,
        json={'name': 'Double Join'}
    )
    client.post('/api/tournament/1/join', headers=auth_headers)
    response = client.post('/api/tournament/1/join', headers=auth_headers)
    assert response.status_code == 400

def test_get_tournament_bracket(auth_headers, client):
    client.post('/api/tournament/create', 
        headers=auth_headers,
        json={'name': 'Bracket Test'}
    )
    response = client.get('/api/tournament/1/bracket', headers=auth_headers)
    assert response.status_code == 200

def test_get_nonexistent_tournament(auth_headers, client):
    response = client.get('/api/tournament/999/bracket', headers=auth_headers)
    assert response.status_code == 404