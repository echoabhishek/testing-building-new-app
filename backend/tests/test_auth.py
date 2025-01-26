import pytest
from backend.app import create_app, db, limiter
from backend.models.user import User
from backend.models.password_reset import PasswordReset
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False
    limiter.enabled = False  # Disable rate limiting for tests
    return app

@pytest.fixture
def client(app):
    with app.app_context():
        db.create_all()
    
    yield app.test_client()
    
    with app.app_context():
        db.session.remove()
        db.drop_all()

# ... (previous test functions remain the same)

def test_google_login(client, app):
    mock_google = MagicMock()
    mock_google.authorized = True
    mock_resp = MagicMock()
    mock_resp.ok = True
    mock_resp.json.return_value = {
        'email': 'googleuser@example.com'
    }
    mock_google.get.return_value = mock_resp

    with patch('backend.routes.auth.google', mock_google):
        with app.app_context():
            response = client.get('/auth/google-login')
            assert response.status_code == 200
            assert 'access_token' in response.json

            # Verify that a new user was created
            user = User.query.filter_by(email='googleuser@example.com').first()
            assert user is not None
            assert user.username == 'googleuser'

