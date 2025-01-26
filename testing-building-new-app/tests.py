import unittest
from app import create_app
from app.extensions import db
from app.models import User, PasswordReset
from datetime import datetime, timedelta
from flask_login import current_user

class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    WTF_CSRF_ENABLED = False
    SECRET_KEY = 'test-secret-key'
    GOOGLE_CLIENT_ID = 'test-client-id'
    GOOGLE_CLIENT_SECRET = 'test-client-secret'

class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = User(username='test', email='test@example.com')
        u.set_password('cat')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))

    def test_password_reset(self):
        u = User(username='test', email='test@example.com')
        db.session.add(u)
        db.session.commit()
        token = 'test-token'
        pr = PasswordReset(user_id=u.id, token=token, expires_at=datetime.utcnow() + timedelta(hours=1))
        db.session.add(pr)
        db.session.commit()
        self.assertIsNotNone(PasswordReset.query.filter_by(token=token).first())

    def test_user_role(self):
        u = User(username='test', email='test@example.com', role='user')
        self.assertEqual(u.role, 'user')
        u.role = 'admin'
        self.assertEqual(u.role, 'admin')

class UserManagementTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def register(self, username, email, password):
        return self.client.post('/auth/register', data=dict(
            username=username,
            email=email,
            password=password,
            password2=password
        ), follow_redirects=True)

    def login(self, email, password):
        return self.client.post('/auth/login', data=dict(
            email=email,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.client.get('/auth/logout', follow_redirects=True)

    def test_register(self):
        response = self.register('test', 'test@example.com', 'cat')
        self.assertIn(b'Congratulations, you are now a registered user!', response.data)

    def test_login_logout(self):
        self.register('test', 'test@example.com', 'cat')
        response = self.login('test@example.com', 'cat')
        self.assertIn(b'Welcome, test!', response.data)
        response = self.logout()
        self.assertIn(b'Sign In', response.data)

    def test_invalid_login(self):
        response = self.login('test@example.com', 'wrong_password')
        self.assertIn(b'Invalid email or password', response.data)

    def test_duplicate_registration(self):
        self.register('test', 'test@example.com', 'cat')
        response = self.register('test', 'test@example.com', 'dog')
        self.assertIn(b'Please use a different email address', response.data)

    def test_password_reset_request(self):
        self.register('test', 'test@example.com', 'cat')
        response = self.client.post('/auth/reset_password_request', data=dict(
            email='test@example.com'
        ), follow_redirects=True)
        self.assertIn(b'Check your email for the instructions to reset your password', response.data)

if __name__ == '__main__':
    unittest.main(verbosity=2)
