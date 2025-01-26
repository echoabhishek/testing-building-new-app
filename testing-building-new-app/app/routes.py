from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app.extensions import db
from app.forms import RegistrationForm, LoginForm, PasswordResetRequestForm, PasswordResetForm
from app.models import User, PasswordReset
from app.email import send_password_reset_email
from datetime import datetime, timedelta
import secrets
from flask import current_app as app
from flask_dance.contrib.google import google

# ... (rest of the routes remain the same)
