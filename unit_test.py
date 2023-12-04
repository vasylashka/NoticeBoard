import json
import pytest
from flask import Flask
from flask_migrate import Migrate
from controllers.note_routes import blp as note_blp
from controllers.user_routes import blp as user_blp

from database import db


@pytest.fixture(scope="session")
def app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    migrate = Migrate(app, db)

    app.register_blueprint(user_blp, url_prefix='/api/v1/users')
    app.register_blueprint(note_blp, url_prefix='/api/v1/notes')

    with app.app_context():
        db.create_all()

    yield app

    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


# User tests

def test_create_user_successful(client):
    data = {
        "email": "test@example.com",
        "username": "testuser"
    }

    response = client.post('/api/v1/users/create', json=data)
    assert response.status_code == 201

    data = json.loads(response.data)
    assert "message" in data
    assert "user_id" in data


def test_get_all_users_successful(client):
    response = client.get('/api/v1/users')
    assert response.status_code == 200

    data = json.loads(response.data)
    assert "users" in data


def test_get_user_by_id(client):
    response = client.get('/api/v1/users/1')
    assert response.status_code == 200

    data = json.loads(response.data)
    assert "user" in data


def test_get_user_by_id_404(client):  # User not found
    response = client.get('/api/v1/users/5')
    assert response.status_code == 404

    data = json.loads(response.data)
    assert data["error"] == "User not found"


def test_update_user_successful(client):
    data = {
        "email": "updated@example.com",
        "username": "updateduser"
    }

    response = client.put('/api/v1/users/1', json=data)
    assert response.status_code == 200

    data = json.loads(response.data)
    assert "message" in data


def test_update_user_404(client):  # User not found
    data = {
        "email": "updated@example.com",
        "username": "updateduser"
    }

    response = client.put('/api/v1/users/5', json=data)
    assert response.status_code == 404

    data = json.loads(response.data)
    assert data["error"] == "User not found"


def test_delete_user_successful(client):
    response = client.delete('/api/v1/users/1')
    assert response.status_code == 200

    data = json.loads(response.data)
    assert "message" in data


def test_delete_user_404(client):
    response = client.delete('/api/v1/users/5')
    assert response.status_code == 404

    data = json.loads(response.data)
    assert data["error"] == "User not found"


# to check correctness of notes
def test_create_user(client):
    data1 = {
        "email": "test@example.com",
        "username": "testuser"
    }
    data2 = {
        "email": "test1@example.com",
        "username": "testuser1"
    }

    response = client.post('/api/v1/users/create', json=data1)
    assert response.status_code == 201
    response1 = client.post('/api/v1/users/create', json=data2)
    assert response1.status_code == 201


# Notes tests

def test_create_note_successful(client):
    data = {
        "title": "Test Note",
        "text": "This is a test note",
        "user_id": 1
    }

    response = client.post('/api/v1/notes/create', json=data)
    assert response.status_code == 201

    data = json.loads(response.data)
    assert "message" in data
    assert "note_id" in data


def test_create_note_404(client):
    data = {
        "title": "Test Note",
        "text": "This is a test note",
        "user_id": 123
    }

    response = client.post('/api/v1/notes/create', json=data)
    assert response.status_code == 404

    data = json.loads(response.data)
    assert data["error"] == "User not found"


def test_get_all_notes_successful(client):
    response = client.get('/api/v1/notes')
    assert response.status_code == 200

    data = json.loads(response.data)
    assert "notes" in data


def test_get_note_by_id_successful(client):
    response = client.get('/api/v1/notes/1')
    assert response.status_code == 200

    data = json.loads(response.data)
    assert "note" in data


def test_get_note_by_id_404(client):
    response = client.get('/api/v1/notes/645338')
    assert response.status_code == 404

    data = json.loads(response.data)
    assert data["error"] == "Note not found"


def test_get_all_notes_by_user_id_successful(client):
    response = client.get('/api/v1/users/1/notes')
    assert response.status_code == 200

    data = json.loads(response.data)
    assert "Notes by user" in data


def test_get_all_notes_by_user_id_404(client):
    response = client.get('/api/v1/users/123/notes')
    assert response.status_code == 404

    data = json.loads(response.data)
    assert data["error"] == "User not found"


def test_update_note_successful(client):
    data = {
        "title": "Updated Note",
        "text": "This note has been updated"
    }

    response = client.put('/api/v1/notes/1/1', json=data)
    assert response.status_code == 200

    data = json.loads(response.data)
    assert "message" in data


def test_update_note_404_1(client):  # Note not found
    data = {
        "title": "Updated Note",
        "text": "This note has been updated"
    }

    response = client.put('/api/v1/notes/123/1', json=data)
    assert response.status_code == 404

    data = json.loads(response.data)
    assert data["error"] == "Note not found"


def test_update_note_404_2(client):  # User not found
    data = {
        "title": "Updated Note",
        "text": "This note has been updated"
    }

    response = client.put('/api/v1/notes/1/123', json=data)
    assert response.status_code == 404

    data = json.loads(response.data)
    assert data["error"] == "User not found"


def test_update_note_403(client):  # Access forbidden
    data = {
        "title": "Updated Note",
        "text": "This note has been updated"
    }

    response = client.put('/api/v1/notes/1/2', json=data)
    assert response.status_code == 403

    data = json.loads(response.data)
    assert data["error"] == "You are not allowed to perform this action"


def test_delete_note_404_1(client):  # Note not found
    response = client.delete('/api/v1/notes/123/1')
    assert response.status_code == 404

    data = json.loads(response.data)
    assert data["error"] == "Note not found"


def test_delete_note_404_2(client):  # User not found
    response = client.delete('/api/v1/notes/1/123')
    assert response.status_code == 404

    data = json.loads(response.data)
    assert data["error"] == "User not found"


def test_delete_note_403(client):  # Access denied
    response = client.delete('/api/v1/notes/1/2')
    assert response.status_code == 403

    data = json.loads(response.data)
    assert data["error"] == "You are not allowed to perform this action"


def test_delete_note_successful(client):
    response = client.delete('/api/v1/notes/1/1')
    assert response.status_code == 200

    data = json.loads(response.data)
    assert "message" in data
