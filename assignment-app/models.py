from mongoengine import Document, StringField, ReferenceField, connect
from flask_login import UserMixin

# Connect to MongoDB (can also be done via init_app in app.py)
# connect(db="assignment-app", host="your_mongo_uri") -- optional here

class User(UserMixin, Document):
    email = StringField(required=True, unique=True)
    password = StringField(required=True)
    role = StringField(required=True)  # teacher or student

class Assignment(Document):
    title = StringField(required=True)
    teacher = ReferenceField(User)

class Submission(Document):
    student = ReferenceField(User)
    assignment = ReferenceField(Assignment)
    content = StringField()
