def test_get_match_not_found(auth_headers, client):
    response = client.get('/api/game/match/999', headers=auth_headers)
    assert response.status_code == 404

def test_submit_invalid_choice(auth_headers, client):
    response = client.post('/api/game/match/1/round/1/choice',
        headers=auth_headers,
        json={'choice': 'lizard'}
    )
    assert response.status_code == 404  # Match doesn't exist yet
