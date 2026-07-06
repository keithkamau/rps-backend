def test_admin_stats(auth_headers, client):
    response = client.get('/api/admin/stats', headers=auth_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert 'total_users' in data
    assert 'active_tournaments' in data

def test_admin_leaderboard(auth_headers, client):
    response = client.get('/api/admin/leaderboard', headers=auth_headers)
    assert response.status_code == 200
    assert 'leaderboard' in response.get_json()

def test_admin_tournaments(auth_headers, client):
    response = client.get('/api/admin/tournaments', headers=auth_headers)
    assert response.status_code == 200
    assert 'tournaments' in response.get_json()
