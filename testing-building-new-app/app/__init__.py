from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from config import Config
from flask_dance.contrib.google import make_google_blueprint, google

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = 'login'
mail = Mail(app)

google_bp = make_google_blueprint(
    client_id=app.config['GOOGLE_CLIENT_ID'],
    client_secret=app.config['GOOGLE_CLIENT_SECRET'],
    scope=['profile', 'email']
)
app.register_blueprint(google_bp, url_prefix='/login')

from app import routes, models

@login.user_loader
def load_user(id):
    return models.User.query.get(int(id))
