from database import db
from datetime import datetime


class Note(db.Model):
    __tablename__ = 'notes'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    text = db.Column(db.String(404))
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('User', back_populates='notes')

    def __init__(self, title, text, user_id):
        self.title = title
        self.text = text
        self.user_id = user_id


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    notes = db.relationship('Note', back_populates='user', cascade='all, delete-orphan')

    def __init__(self, username, email):
        self.username = username
        self.email = email
