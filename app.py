from flask import Flask, request, jsonify, json, render_template
from flask_mongoengine import MongoEngine
from flask_swagger_ui import get_swaggerui_blueprint
from datetime import datetime

from werkzeug.exceptions import HTTPException

from ORM.note import Note
from ORM.user import User
from decorator import get_note_and_user

app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
    'db': 'NoticeBoard',
    'host': 'mongodb://localhost:27017/NoticeBoard'
}

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "NoticeBoard API"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

db = MongoEngine(app)


@app.errorhandler(Exception)
def handle_error(e):
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    return jsonify(error=str(e)), code


@app.route('/api/v1/create/user', methods=['POST'])
def create_user():
    data = request.json
    email = data.get('email')
    username = data.get('username')

    user = User(email=email, username=username)
    user.save()

    return jsonify({"message": "User created successfully", "user_id": str(user.id)}), 201


@app.route('/api/v1/get/users', methods=['GET'])
def get_all_users():
    users = User.objects()
    return jsonify({"users": [user.to_json() for user in users]}), 200


@app.route('/api/v1/get/user/<user_id>', methods=['GET'])
def get_user_by_id(user_id):
    user = User.objects(id=user_id).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({"user": user.to_json()}), 200



@app.route('/api/v1/update/user/<user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    new_username = data.get('username')
    new_email = data.get('email')

    user = User.objects(id=user_id).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    user.username = new_username
    user.email = new_email
    user.save()

    return jsonify({"message": "User updated successfully"}), 200


@app.route('/api/v1/delete/user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.objects(id=user_id).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    user.delete()
    return jsonify({"message": "User deleted successfully"}), 200


@app.route('/api/v1/create/note', methods=['POST'])
def create_note():
    data = request.json
    title = data.get('title')
    text = data.get('text')
    user_id = data.get('user_id')

    user = User.objects(id=user_id).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    note = Note(title=title, text=text, creation_date=datetime.utcnow(), user_id=user_id)
    note.save()

    return jsonify({"message": "Note created successfully", "note_id": str(note.id)}), 201


@app.route('/api/v1/get/notes', methods=['GET'])
def get_all_notes():
    notes = Note.objects()
    return jsonify({"notes": [note.to_json() for note in notes]}), 200


@app.route('/api/v1/get/note/<note_id>', methods=['GET'])
def get_node_by_id(note_id):
    note = Note.objects(id=note_id).first()

    if not note:
        return jsonify({"error": "Note not found"}), 404

    return jsonify({"user": note.to_json()}), 200

@app.route('/api/v1/get/notes/<user_id>', methods=['GET'])
def get_all_notes_by_user_id(user_id):
    user = User.objects(id=user_id).first()
    if not user:
        return jsonify({"error": "User not found"}), 404
    notes = Note.objects(user_id=user)
    return jsonify({"users": [note.to_json() for note in notes]}), 200


@app.route('/api/v1/update/note/<note_id>/<user_id>', methods=['PUT'])
@get_note_and_user()
def update_note(note, user):
    data = request.json
    new_title = data.get('title')
    new_text = data.get('text')

    note.title = new_title
    note.text = new_text
    note.save()

    return jsonify({"message": "Note updated successfully"}), 200


@app.route('/api/v1/delete/note/<note_id>/<user_id>', methods=['DELETE'])
@get_note_and_user()
def delete_note(note, user):
    note.delete()
    return jsonify({"message": "Note deleted successfully"}), 200


if __name__ == '__main__':
    app.run(debug=True)
