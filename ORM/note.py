from flask_mongoengine import Document
from mongoengine import StringField, DateTimeField, ReferenceField

from ORM.user import User


class Note(Document):
    title = StringField(max_length=50)
    text = StringField(max_length=404)
    creation_date = DateTimeField()
    user_id = ReferenceField(User, reverse_delete_rule=2)  # set NULL
