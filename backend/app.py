from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_dance.contrib.google import make_google_blueprint

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()
mail = Mail()
limiter = Limiter(key_func=get_remote_address)

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user_management.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Change this in production
    app.config['MAIL_SERVER'] = 'smtp.example.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'your-email@example.com'
    app.config['MAIL_PASSWORD'] = 'your-email-password'
    app.config['SECRET_KEY'] = 'your-secret-key'  # Change this in production
    app.config['GOOGLE_OAUTH_CLIENT_ID'] = 'your-google-client-id'
    app.config['GOOGLE_OAUTH_CLIENT_SECRET'] = 'your-google-client-secret'

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)
    limiter.init_app(app)

    google_bp = make_google_blueprint(
        client_id=app.config['GOOGLE_OAUTH_CLIENT_ID'],
        client_secret=app.config['GOOGLE_OAUTH_CLIENT_SECRET'],
        scope=['profile', 'email']
    )
    app.register_blueprint(google_bp, url_prefix='/login')

    from backend.routes.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    @app.before_first_request
    def create_tables():
        db.create_all()

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
