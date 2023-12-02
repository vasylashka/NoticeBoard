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

    app.register_blueprint(user_blp, url_prefix='/api/v1/user')
    app.register_blueprint(note_blp, url_prefix='/api/v1/note')

    with app.app_context():
        db.create_all()

    yield app

    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

#User tests

def test_create_user_succesful(client):
    data = {
        "email": "test@example.com",
        "username": "testuser"
    }

    response = client.post('/api/v1/user/create', json=data)
    assert response.status_code == 201

    data = json.loads(response.data)
    assert "message" in data
    assert "user_id" in data


def test_get_all_users(client):
    response = client.get('/api/v1/user/get/all')
    assert response.status_code == 200

    data = json.loads(response.data)
    assert "users" in data

def test_get_user_by_id(client):
    response = client.get('/api/v1/user/get/1')
    assert response.status_code == 200

    data = json.loads(response.data)
    assert "user" in data

def test_get_user_by_id_404(client): #User not found
    response = client.get('/api/v1/user/get/5')
    assert response.status_code == 404

    data = json.loads(response.data)
    assert "message" in data

def test_update_user(client):
    data = {
        "email": "updated@example.com",
        "username": "updateduser"
    }

    response = client.put('/api/v1/user/update/1', json=data)
    assert response.status_code == 200

    data = json.loads(response.data)
    assert "message" in data

def test_update_user_404(client): #User not found
    data = {
        "email": "updated@example.com",
        "username": "updateduser"
    }

    response = client.put('/api/v1/user/update/5', json=data)
    assert response.status_code == 404

    data = json.loads(response.data)
    assert "error" in data

def test_delete_user(client):
    response = client.delete('/api/v1/user/delete/1')
    assert response.status_code == 200

    data = json.loads(response.data)
    assert "message" in data

def test_delete_user_404(client):
    response = client.delete('/api/v1/user/delete/5')
    assert response.status_code == 404

    data = json.loads(response.data)
    assert "error" in data

#to check correctness of notes
def test_create_user(client):
    data1 = {
        "email": "test@example.com",
        "username": "testuser"
    }
    data2 = {
        "email": "test1@example.com",
        "username": "testuser1"
    }

    response = client.post('/api/v1/user/create', json=data1)
    assert response.status_code == 201
    response1 = client.post('/api/v1/user/create', json=data2)
    assert response1.status_code == 201


#Notes tests

def test_create_note_succesful(client):
    data = {
        "title": "Test Note",
        "text": "This is a test note",
        "user_id": 1
    }

    response = client.post('/api/v1/note/create', json=data)
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

    response = client.post('/api/v1/note/create', json=data)
    assert response.status_code == 404

    data = json.loads(response.data)
    assert "message" in data

def test_get_all_notes(client):
    response = client.get('/api/v1/note/get/all')
    assert response.status_code == 200

    data = json.loads(response.data)
    assert "notes" in data

def test_get_note_by_id_succesful(client):
    response = client.get('/api/v1/note/get/one/1')
    assert response.status_code == 200

    data = json.loads(response.data)
    assert "note" in data

def test_get_note_by_id_404(client):
    response = client.get('/api/v1/note/get/one/645338')
    assert response.status_code == 404

    data = json.loads(response.data)
    assert "message" in data
def test_get_all_notes_by_user_id_succesful(client):
    response = client.get('/api/v1/note/get/1')
    assert response.status_code == 200

    data = json.loads(response.data)
    assert "notes by user" in data

def test_get_all_notes_by_user_id_404(client):
    response = client.get('/api/v1/note/get/123')
    assert response.status_code == 404

    data = json.loads(response.data)
    assert "message" in data

def test_update_note_succesful(client):
    data = {
        "title": "Updated Note",
        "text": "This note has been updated"
    }

    response = client.put('/api/v1/note/update/1/1', json=data)
    assert response.status_code == 200

    data = json.loads(response.data)
    assert "message" in data

def test_update_note_404_1(client): #Note not found
    data = {
        "title": "Updated Note",
        "text": "This note has been updated"
    }

    response = client.put('/api/v1/note/update/123/1', json=data)
    assert response.status_code == 404

    data = json.loads(response.data)
    assert "error" in data

def test_update_note_404_2(client): #User not found
    data = {
        "title": "Updated Note",
        "text": "This note has been updated"
    }

    response = client.put('/api/v1/note/update/1/123', json=data)
    assert response.status_code == 404

    data = json.loads(response.data)
    assert "error" in data

def test_update_note_403(client): #Access forbidden
    data = {
        "title": "Updated Note",
        "text": "This note has been updated"
    }

    response = client.put('/api/v1/note/update/1/2', json=data)
    assert response.status_code == 403

    data = json.loads(response.data)
    assert "error" in data



def test_delete_note_404_1(client): #Note not found
    response = client.delete('/api/v1/note/delete/123/1')
    assert response.status_code == 404

    data = json.loads(response.data)
    assert "error" in data

def test_delete_note_404_2(client): #User not found
    response = client.delete('/api/v1/note/delete/1/123')
    assert response.status_code == 404

    data = json.loads(response.data)
    assert "error" in data

def test_delete_note_403(client): #Access denied
    response = client.delete('/api/v1/note/delete/1/2')
    assert response.status_code == 403

    data = json.loads(response.data)
    assert "error" in data

def test_delete_note_succesful(client):
    response = client.delete('/api/v1/note/delete/1/1')
    assert response.status_code == 200

    data = json.loads(response.data)
    assert "message" in data