# 3rd-party packages
from flask import Flask, render_template, request, redirect, url_for
from flask_mail import Mail, Message
from flask_mongoengine import MongoEngine
from flask_login import (
    LoginManager,
    current_user,
    login_user,
    logout_user,
    login_required,
)
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename

# stdlib
import os
from datetime import datetime

app = Flask(__name__)
app.config["MONGODB_HOST"] = "mongodb://localhost:27017/p5"
app.config["SECRET_KEY"] = b'k\x89,\x95C\xa9\xaa\x0e,t\xae%\xad\x95\x81Z'
mail_settings = {
    "MAIL_SERVER": 'smtp.mail.yahoo.com',
    "MAIL_PORT": 587,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": os.environ['EMAIL_USER'],
    "MAIL_PASSWORD": "Password1Password@"
}

app.config.update(mail_settings)
mail = Mail(app)

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
)

db = MongoEngine(app)
"""*******Temp comment till login written"""
login_manager = LoginManager(app)
login_manager.login_view = "login"
bcrypt = Bcrypt(app)

from . import routes
