from flask import Flask
from config import Config
from app.extensions import db, login, mail
from flask_dance.contrib.google import make_google_blueprint

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login.init_app(app)
    mail.init_app(app)

    login.login_view = 'auth.login'

    google_bp = make_google_blueprint(
        client_id=app.config['GOOGLE_CLIENT_ID'],
        client_secret=app.config['GOOGLE_CLIENT_SECRET'],
        scope=['profile', 'email']
    )
    app.register_blueprint(google_bp, url_prefix='/login')

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    with app.app_context():
        from app import models
        db.create_all()

    return app
