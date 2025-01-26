from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from backend.models.user import User
from backend.models.password_reset import PasswordReset
from backend.app import db, mail, bcrypt, limiter
from flask_mail import Message
import secrets
from datetime import datetime, timedelta
from flask_dance.contrib.google import google
import re

auth = Blueprint('auth', __name__)

def validate_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def validate_password(password):
    return len(password) >= 8 and any(c.isalpha() for c in password) and any(c.isdigit() for c in password)

@auth.route('/register', methods=['POST'])
@limiter.limit("5 per minute")
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({"message": "Username, email, and password are required"}), 400

    if not validate_email(email):
        return jsonify({"message": "Invalid email format"}), 400

    if not validate_password(password):
        return jsonify({"message": "Password must be at least 8 characters long and contain both letters and numbers"}), 400

    if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
        return jsonify({"message": "Username or email already exists"}), 400

    new_user = User(username=username, email=email)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    current_app.logger.info(f"New user registered: {username}")
    return jsonify({"message": "User created successfully"}), 201

@auth.route('/login', methods=['POST'])
@limiter.limit("10 per minute")
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if user and bcrypt.check_password_hash(user.password_hash, password):
        access_token = create_access_token(identity=str(user.id))
        current_app.logger.info(f"User logged in: {username}")
        return jsonify(access_token=access_token), 200
    
    current_app.logger.warning(f"Failed login attempt for user: {username}")
    return jsonify({"message": "Invalid username or password"}), 401

@auth.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    user = User.query.get(int(current_user_id))
    if not user:
        current_app.logger.error(f"Protected route accessed with invalid user ID: {current_user_id}")
        return jsonify({"message": "User not found"}), 404
    current_app.logger.info(f"Protected route accessed by user: {user.username}")
    return jsonify(logged_in_as=user.username), 200

@auth.route('/admin/dashboard', methods=['GET'])
@jwt_required()
def admin_dashboard():
    current_user_id = get_jwt_identity()
    user = User.query.get(int(current_user_id))
    if not user:
        current_app.logger.error(f"Admin dashboard accessed with invalid user ID: {current_user_id}")
        return jsonify({"message": "User not found"}), 404
    if user.role != 'admin':
        current_app.logger.warning(f"Unauthorized admin dashboard access attempt by user: {user.username}")
        return jsonify({"message": "Access denied"}), 403
    current_app.logger.info(f"Admin dashboard accessed by user: {user.username}")
    return jsonify({"message": "Welcome to the admin dashboard"}), 200

@auth.route('/forgot-password', methods=['POST'])
@limiter.limit("3 per hour")
def forgot_password():
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({"message": "Email is required"}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        current_app.logger.warning(f"Forgot password attempt for non-existent email: {email}")
        return jsonify({"message": "Email not found"}), 404

    token = secrets.token_urlsafe(32)
    reset = PasswordReset(user_id=user.id, token=token, expires_at=datetime.utcnow() + timedelta(hours=1))
    db.session.add(reset)
    db.session.commit()

    msg = Message("Password Reset Request",
                  sender="noreply@example.com",
                  recipients=[user.email])
    msg.body = f"Click the following link to reset your password: http://yourdomain.com/reset-password/{token}"
    
    if current_app.config['TESTING']:
        current_app.config['EMAIL_SENT'] = msg.body
    else:
        mail.send(msg)

    current_app.logger.info(f"Password reset requested for user: {user.username}")
    return jsonify({"message": "Password reset email sent"}), 200

@auth.route('/reset-password/<token>', methods=['POST'])
@limiter.limit("3 per hour")
def reset_password(token):
    data = request.get_json()
    new_password = data.get('new_password')

    if not new_password:
        return jsonify({"message": "New password is required"}), 400

    reset = PasswordReset.query.filter_by(token=token).first()
    if not reset or reset.expires_at < datetime.utcnow():
        current_app.logger.warning(f"Password reset attempt with invalid or expired token: {token}")
        return jsonify({"message": "Invalid or expired token"}), 400

    user = User.query.get(reset.user_id)
    user.set_password(new_password)
    db.session.delete(reset)
    db.session.commit()

    current_app.logger.info(f"Password reset successful for user: {user.username}")
    return jsonify({"message": "Password reset successful"}), 200

@auth.route('/google-login')
def google_login():
    if not google.authorized:
        return jsonify({"message": "Not authorized"}), 401
    resp = google.get("/oauth2/v2/userinfo")
    if not resp.ok:
        return jsonify({"message": "Failed to fetch user info"}), 400
    user_info = resp.json()
    user = User.query.filter_by(email=user_info['email']).first()
    if not user:
        user = User(username=user_info['email'].split('@')[0], email=user_info['email'])
        db.session.add(user)
        db.session.commit()
    access_token = create_access_token(identity=str(user.id))
    return jsonify(access_token=access_token), 200

