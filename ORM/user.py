from flask_mongoengine import Document
from mongoengine import EmailField, StringField


class User(Document):
    email = EmailField(required=True, unique=True)
    username = StringField(max_length=50)
