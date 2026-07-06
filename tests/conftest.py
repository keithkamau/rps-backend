import pytest
from app import create_app, db

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SECRET_KEY': 'test-secret',
        'JWT_SECRET_KEY': 'test-jwt-secret',
    })
    
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
    # Create user and get token
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