# 3rd-party packages
from flask import render_template, request, redirect, url_for, flash
from flask_mongoengine import MongoEngine
import io
import base64
"""*******Temp comment till login written"""
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
from .models import Review
from .utils import current_time

""" ************ View functions ************ """


@app.route("/", methods=["GET", "POST"])
def index():
	reviews = Review.objects()
	return render_template("welcome_page.html", reviews=reviews)

@app.route('/test',methods=["GET", "POST"])
def review():
	form = ReviewForm()
	if form.validate_on_submit():
		feedback = Review(
            #commenter=current_user._get_current_object(),
            text=form.text.data,
            date=current_time(),
            class_name=form.class_name.data,
			professor=form.professor.data,
			stars=form.stars.data,
			gpa=form.gpa.data)
			
		feedback.save()
		
	reviews = Review.objects()
	return render_template("test.html", form=form, reviews=reviews)