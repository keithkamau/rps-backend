def test_signup_success(client):
    response = client.post('/api/auth/signup', json={
        'username': 'newuser',
        'email': 'new@test.com',
        'password': 'Test1234'
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data['user']['username'] == 'newuser'
    assert 'token' in data

def test_signup_duplicate_username(client):
    client.post('/api/auth/signup', json={
        'username': 'user1',
        'email': 'user1@test.com',
        'password': 'Test1234'
    })
    response = client.post('/api/auth/signup', json={
        'username': 'user1',
        'email': 'user2@test.com',
        'password': 'Test1234'
    })
    assert response.status_code == 409

def test_signup_duplicate_email(client):
    client.post('/api/auth/signup', json={
        'username': 'userA',
        'email': 'same@test.com',
        'password': 'Test1234'
    })
    response = client.post('/api/auth/signup', json={
        'username': 'userB',
        'email': 'same@test.com',
        'password': 'Test1234'
    })
    assert response.status_code == 409

def test_signup_missing_fields(client):
    response = client.post('/api/auth/signup', json={})
    assert response.status_code == 400

def test_signup_weak_password(client):
    response = client.post('/api/auth/signup', json={
        'username': 'test',
        'email': 'test@test.com',
        'password': 'short'
    })
    assert response.status_code == 400

def test_login_success(client):
    client.post('/api/auth/signup', json={
        'username': 'loginuser',
        'email': 'login@test.com',
        'password': 'Test1234'
    })
    response = client.post('/api/auth/login', json={
        'username': 'loginuser',
        'password': 'Test1234'
    })
    assert response.status_code == 200
    assert 'token' in response.get_json()

def test_login_wrong_password(client):
    client.post('/api/auth/signup', json={
        'username': 'loginuser2',
        'email': 'login2@test.com',
        'password': 'Test1234'
    })
    response = client.post('/api/auth/login', json={
        'username': 'loginuser2',
        'password': 'WrongPass1'
    })
    assert response.status_code == 401

def test_login_nonexistent_user(client):
    response = client.post('/api/auth/login', json={
        'username': 'nobody',
        'password': 'Test1234'
    })
    assert response.status_code == 401

def test_get_me(auth_headers, client):
    response = client.get('/api/auth/me', headers=auth_headers)
    assert response.status_code == 200
    assert response.get_json()['user']['username'] == 'testuser'

def test_get_me_no_token(client):
    response = client.get('/api/auth/me')
    assert response.status_code == 401