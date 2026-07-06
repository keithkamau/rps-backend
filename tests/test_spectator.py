def test_spectate_match_not_found(auth_headers, client):
    response = client.get('/api/spectator/match/999', headers=auth_headers)
    assert response.status_code == 404

def test_active_matches_empty(auth_headers, client):
    response = client.get('/api/spectator/active-matches', headers=auth_headers)
    assert response.status_code == 200
    assert response.get_json()['matches'] == []
