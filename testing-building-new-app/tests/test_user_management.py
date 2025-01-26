import pytest
from src.app import app, db, User, bcrypt

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    client = app.test_client()

    with app.app_context():
        db.create_all()

    yield client

    with app.app_context():
        db.drop_all()

def test_user_registration(client):
    response = client.post('/register', json={
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'testpassword'
    })
    assert response.status_code == 201
    assert b"User registered successfully" in response.data

def test_user_login(client):
    # Register a user first
    client.post('/register', json={
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'testpassword'
    })

    # Try to login
    response = client.post('/login', json={
        'username': 'testuser',
        'password': 'testpassword'
    })
    assert response.status_code == 200
    assert b"Logged in successfully" in response.data

def test_invalid_login(client):
    response = client.post('/login', json={
        'username': 'nonexistent',
        'password': 'wrongpassword'
    })
    assert response.status_code == 401
    assert b"Invalid credentials" in response.data

def test_password_reset_request(client):
    # Register a user first
    client.post('/register', json={
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'testpassword'
    })

    # Request password reset
    response = client.post('/reset-password', json={
        'email': 'testuser@example.com'
    })
    assert response.status_code == 200
    assert b"Password reset instructions sent" in response.data

def test_password_reset_request_invalid_email(client):
    response = client.post('/reset-password', json={
        'email': 'nonexistent@example.com'
    })
    assert response.status_code == 404
    assert b"User not found" in response.data

def test_admin_access(client):
    # Register an admin user
    client.post('/register', json={
        'username': 'adminuser',
        'email': 'admin@example.com',
        'password': 'adminpassword'
    })

    # Set the user's role to admin (this would typically be done through a separate admin interface)
    with app.app_context():
        user = User.query.filter_by(username='adminuser').first()
        user.role = 'admin'
        db.session.commit()

    # Login as admin
    client.post('/login', json={
        'username': 'adminuser',
        'password': 'adminpassword'
    })

    # Access admin route
    response = client.get('/admin')
    assert response.status_code == 200
    assert b"Welcome to the admin panel" in response.data

def test_admin_access_unauthorized(client):
    # Register a regular user
    client.post('/register', json={
        'username': 'regularuser',
        'email': 'regular@example.com',
        'password': 'regularpassword'
    })

    # Login as regular user
    client.post('/login', json={
        'username': 'regularuser',
        'password': 'regularpassword'
    })

    # Try to access admin route
    response = client.get('/admin')
    assert response.status_code == 403
    assert b"Unauthorized" in response.data

