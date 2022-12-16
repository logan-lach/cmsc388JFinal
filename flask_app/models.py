from flask_login import UserMixin
from datetime import datetime
from . import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.objects(username=user_id).first()


class User(db.Document, UserMixin):
    username = db.StringField(unique=True, required=True, min_length = 1, max_length=40)
    email = db.EmailField(unique=True, required=True)
    password = db.StringField(required=True)
    profile_pic = db.ImageField()


    # Returns unique string identifying our object
    def get_id(self):
        return self.username

# Review.objects(class_name = class_name)
# Review.objects(professor = professor)

class Review(db.Document):
    commenter = db.StringField() # Who wrote the review (Only for full reviews)
    text = db.StringField(min_length=5, max_length=500) # Content of the review (Only for full reviews)
    date = db.StringField() # Only required for reviews that have text (ie only full reviews)
    full_review = db.StringField(required=True, min_length=4, max_length = 5) # Marks if its a full review or an anonymous review
    type_review = db.StringField(required=True, min_length=5, max_length=9) # Marks "class" or "professor", helps with umd.io calls
    about = db.StringField(required=True, min_length=1, max_length=40) # Who the review was written for (always required)
    gpa = db.StringField() # GPA (Only thing an anonymous review can enter)
    stars = db.StringField(required=True)
    

