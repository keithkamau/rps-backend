import pytest
from app import create_app, db
from app.config import TestConfig

@pytest.fixture
def app():
    app = create_app(TestConfig)
    
    with app.app_context():
        db.create_all()
    
    yield app
    
    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def auth_headers(client):
    client.post('/api/auth/signup', json={
        'username': 'testuser',
        'email': 'test@test.com',
        'password': 'Test1234'
    })
    response = client.post('/api/auth/login', json={
        'username': 'testuser',
        'password': 'Test1234'
    })
    token = response.get_json()['token']
    return {'Authorization': f'Bearer {token}'}
