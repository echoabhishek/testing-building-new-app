from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db, google
from app.forms import RegistrationForm, LoginForm, PasswordResetRequestForm, PasswordResetForm
from app.models import User, PasswordReset, role_required
from app.email import send_password_reset_email
from datetime import datetime, timedelta
import secrets

@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password')
            return redirect(url_for('login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = secrets.token_urlsafe(32)
            reset = PasswordReset(user_id=user.id, token=token, expires_at=datetime.utcnow() + timedelta(hours=1))
            db.session.add(reset)
            db.session.commit()
            send_password_reset_email(user, token)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html', title='Reset Password', form=form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    reset = PasswordReset.query.filter_by(token=token).first()
    if not reset or reset.expires_at < datetime.utcnow():
        return redirect(url_for('index'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        user = User.query.get(reset.user_id)
        user.set_password(form.password.data)
        db.session.delete(reset)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)

@app.route('/login/google')
def google_login():
    if not google.authorized:
        return redirect(url_for('google.login'))
    resp = google.get('/oauth2/v2/userinfo')
    assert resp.ok, resp.text
    email = resp.json()['email']
    user = User.query.filter_by(email=email).first()
    if not user:
        username = resp.json()['name']
        user = User(username=username, email=email)
        db.session.add(user)
        db.session.commit()
    login_user(user)
    return redirect(url_for('index'))

@app.route('/admin')
@login_required
@role_required('admin')
def admin():
    return render_template('admin.html', title='Admin Panel')

@app.route('/login/google')
def google_login():
    if not google.authorized:
        return redirect(url_for('google.login'))
    resp = google.get('/oauth2/v2/userinfo')
    assert resp.ok, resp.text
    email = resp.json()['email']
    user = User.query.filter_by(email=email).first()
    if not user:
        username = resp.json()['name']
        user = User(username=username, email=email)
        db.session.add(user)
        db.session.commit()
    login_user(user)
    return redirect(url_for('index'))

@app.route('/admin')
@login_required
@role_required('admin')
def admin():
    return render_template('admin.html', title='Admin Panel')
@role_required('admin')
def admin():
    return render_template('admin.html', title='Admin Panel')
