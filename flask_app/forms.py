from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename
from wtforms import StringField, IntegerField, SubmitField, TextAreaField, PasswordField,SelectField
from wtforms.validators import (
    InputRequired,
    DataRequired,
    NumberRange,
    Length,
    Email,
    EqualTo,
    ValidationError,
)
GPA_CHOICES = [('A', 'A'), ('B', 'B'), ('C','C'),('D','D'), ('F','F'), ('W', 'W')]
CLASS_OR_PROF_CHOICE = ['Course', 'Professor']
ONE_TO_FIVE_RATING_CHOICES = (
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
)

from .models import User

class ReviewForm(FlaskForm):
    type_review = SelectField(u"Type of Review", choices=CLASS_OR_PROF_CHOICE,)
    about = StringField("About", validators=[InputRequired(), Length(min=1, max=40)])
    specific = TextAreaField(
        "Comment", validators=[InputRequired(), Length(min=5, max=500)]
    )
    gpa = SelectField(u"GPA", choices=GPA_CHOICES,)
    star_rating = SelectField(u"Star Rating", choices=ONE_TO_FIVE_RATING_CHOICES,)
    submit = SubmitField("Submit")

class AnonReviewForm(FlaskForm):
    type_review = SelectField(u"Review About", choices=CLASS_OR_PROF_CHOICE,)
    about = StringField("About", validators=[InputRequired(), Length(min=1, max=40)])
    star_rating = SelectField(u"Star Rating", choices=ONE_TO_FIVE_RATING_CHOICES,)
    submit = SubmitField("Submit")

class RegistrationForm(FlaskForm):
    username = StringField(
        "Username", validators=[InputRequired(), Length(min=1, max=40)]
    )
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired()])
    confirm_password = PasswordField(
        "Confirm Password", validators=[InputRequired(), EqualTo("password")]
    )
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.objects(username=username.data).first()
        if user is not None:
            raise ValidationError("Username is taken")

    def validate_email(self, email):
        user = User.objects(email=email.data).first()
        if user is not None:
            raise ValidationError("Email is taken")

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=1, max=40)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=1)])
    submit = SubmitField("Login")

class SearchForm(FlaskForm):
    class_or_prof =  SelectField(u"Search For", choices=CLASS_OR_PROF_CHOICE,)
    search_query = StringField(validators=[InputRequired(), Length(min=1, max=40)])
    submit = SubmitField('Search')

class RemovalForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=1, max=40)])
    about = StringField(validators=[InputRequired(), Length(min=1, max=40)])
    specific = TextAreaField(
        "Why you feel we should remove their comment", validators=[InputRequired(), Length(min=5, max=500)]
    )
    submit = SubmitField('Send Email')
    
