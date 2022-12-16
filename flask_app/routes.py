# 3rd-party packages
from flask import render_template, request, redirect, url_for, flash
from flask_mongoengine import MongoEngine
import requests
import io
import base64
"""*******Temp comment till login written"""
from flask_login import (
     LoginManager,
     current_user,
     login_user,
     logout_user,
     login_required,
)
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename
from .forms import ReviewForm, RegistrationForm, LoginForm, AnonReviewForm, SearchForm,  GPA_CHOICES
# stdlib
from datetime import datetime

# local
from . import app, bcrypt
# from .forms import (
from .models import User, Review, load_user
from datetime import datetime


def current_time() -> str:
    return datetime.now().strftime("%B %d, %Y at %H:%M:%S")


""" ************ View functions ************ """


@app.route("/", methods=["GET", "POST"])
def index():
	big_query = Review.objects(full_review="True")
	reviews = big_query.order_by("-date")[:3]
	return render_template("welcome_page.html", reviews=reviews, size=len(big_query))

@app.route("/review", methods=["GET", "POST"])
def write_review():
	form = ReviewForm()
	if current_user.is_authenticated:
		try: 
			if request.method == "POST":
				if form.validate_on_submit():
					review = Review(
						full_review="True",
						type_review= form.type_review.data, 
						commenter=str(current_user.username),
						about = form.about.data, 
						text = form.specific.data, 
						date = current_time(), 
						gpa = form.gpa.data, 
						stars = form.star_rating.data )
					review.save()
					# return redirect(url_for("reviews", about=form.about.data))
					return redirect(url_for("index"))
				print("Did not validate")
				
		except Exception as e:
			print(e)
			return render_template("review.html", error_msg=str(e), form=form)
		return render_template("review.html", form=form)
	else:
		form = AnonReviewForm()
		try:
			if request.method == "POST":
				if form.validate_on_submit():
					review = Review(
						full_review="False",
						type_review = form.type_review.data,
						about = form.about.data,
						stars = form.star_rating.data
					)
					review.save()
					return redirect(url_for("index"))
		except Exception as e:
			print(e)
			return render_template("anonreview.html", error_msg=str(e), form=form)
	return render_template("anonreview.html", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('login'))
	form = RegistrationForm()
	try: 
		if request.method == "POST":
			if form.validate_on_submit():
				print('we validated!')
				hashed = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
				user = User(username=form.username.data, 
							email=form.email.data, password=hashed)
				user.save()
				return redirect(url_for('login'))
			else:
				flash("Invalid registration. Please try again")
	except ValueError as e:
		return render_template("register.html", title="Register", error_message=e, form=form)
	return render_template("register.html", title="Register", form = form)

@app.route("/about", methods=["GET", "POST"])
def about():
	return render_template("about.html")

@app.route("/login", methods=["GET", "POST"])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	
	form = LoginForm()
	try:
		if request.method == "POST":
			if form.validate_on_submit():
				user = User.objects(username=form.username.data).first()

				if user is not None and bcrypt.check_password_hash(user.password, form.password.data) :
					login_user(user)
					return redirect(url_for('index'))
				else:
					flash ("Incorrect username or password")
	except ValueError as e:
		return render_template('login.html', title="login", form=form, error_message = e)
	return render_template('login.html', title="login", form=form)

@app.route('/test2', methods=["GET", "POST"])
def test2():
	return "hello" + current_user.username

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# let this reprsent the search page
@app.route('/search', methods=['GET', 'POST'])
def search_form():
    form = SearchForm()
    
    if request.method == "POST":
        if form.validate_on_submit():
            return redirect(url_for('query', type = form.class_or_prof.data,
                                    query=form.search_query.data))

    return render_template('search.html', form=form)


# this is the action once a search has been submited
@app.route('/search/<type>/<query>', methods=['GET'])
def search_results(type, query):
    result = None
    
    #1. Search for class/professor with user input info on form
    try:
        if type == 'Course':
            result = Review.objects.get(class_name = query)
        else:
            result = Review.objects.get(professor = query)
    
    
    #2. If there is an error while searching reload serach page with error
    except Exception as e:
        return render_template('search.html', error_msg=e)

    #3. If no results are found reload the search page for new search
    if result == None:     
        print('No Results for "{}" were not Found!'.format(query))
        return redirect(url_for('/search'))   
    
    # 4. Load class page 'query_results.html' /**** Change redirction to reviews once review is done ***/
    return redirect(url_for('/about')) 
