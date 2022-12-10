# 3rd-party packages
from flask import render_template, request, redirect, url_for, flash
from flask_mongoengine import MongoEngine
import io
import base64
# from flask_login import (
#     LoginManager,
#     current_user,
#     login_user,
#     logout_user,
#     login_required,
# )
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename
from .forms import ReviewForm, GPA_CHOICES
# stdlib
from datetime import datetime

# local
from . import app, bcrypt, client
# from .forms import (
# from .models import User, Review, load_user
# from .utils import current_time

""" ************ View functions ************ """


@app.route("/", methods=["GET", "POST"])
def index():
	return render_template("welcome_page.html")

@app.route('/test',methods=["GET", "POST"])
def review():
	form = ReviewForm()
	if form.validate_on_submit():
		return render_template("welcome_page.html")
	return render_template("test.html", form=form)