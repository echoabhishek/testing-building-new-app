import unittest
from app import app, db
from app.models import User, PasswordReset
from datetime import datetime, timedelta

class UserModelCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

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

class UserManagementTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.client = app.test_client()
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_register(self):
        response = self.client.post('/register', data=dict(
            username='test',
            email='test@example.com',
            password='cat',
            password2='cat'
        ), follow_redirects=True)
        self.assertIn(b'Congratulations, you are now a registered user!', response.data)

    def test_login_logout(self):
        # Register a user
        self.client.post('/register', data=dict(
            username='test',
            email='test@example.com',
            password='cat',
            password2='cat'
        ), follow_redirects=True)

        # Login
        response = self.client.post('/login', data=dict(
            email='test@example.com',
            password='cat'
        ), follow_redirects=True)
        self.assertIn(b'Welcome, test!', response.data)

        # Logout
        response = self.client.get('/logout', follow_redirects=True)
        self.assertIn(b'Sign In', response.data)

if __name__ == '__main__':
    unittest.main(verbosity=2)
