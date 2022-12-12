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
# from .models import User

class ReviewForm(FlaskForm):
    classes = StringField(
        "Course", validators=[InputRequired(), Length(min=1, max=40)]
    )
    text = TextAreaField(
        "Comment", validators=[InputRequired(), Length(min=5, max=500)]
    )
    gpa =  SelectField(u"GPA", choices=GPA_CHOICES,)
    submit = SubmitField("Submit")
