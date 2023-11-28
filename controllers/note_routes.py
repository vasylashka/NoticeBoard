from flask import request, jsonify, Blueprint
from datetime import datetime
from ORM.note import Note
from ORM.user import User
from decorator import get_note_and_user


blp = Blueprint("Note", __name__, url_prefix="/api/v1/note")


@blp.route('create', methods=['POST'])
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


@blp.route('get/all', methods=['GET'])
def get_all_notes():
    notes = Note.objects()
    return jsonify({"notes": [note.to_json() for note in notes]}), 200


@blp.route('get/one/<note_id>', methods=['GET'])
def get_node_by_id(note_id):
    note = Note.objects(id=note_id).first()

    if not note:
        return jsonify({"error": "Note not found"}), 404

    return jsonify({"user": note.to_json()}), 200

@blp.route('get/<user_id>', methods=['GET'])
def get_all_notes_by_user_id(user_id):
    user = User.objects(id=user_id).first()
    if not user:
        return jsonify({"error": "User not found"}), 404
    notes = Note.objects(user_id=user)
    return jsonify({"users": [note.to_json() for note in notes]}), 200


@blp.route('update/<note_id>/<user_id>', methods=['PUT'])
@get_note_and_user()
def update_note(note, user):
    data = request.json
    new_title = data.get('title')
    new_text = data.get('text')

    note.title = new_title
    note.text = new_text
    note.save()

    return jsonify({"message": "Note updated successfully"}), 200


@blp.route('delete/<note_id>/<user_id>', methods=['DELETE'])
@get_note_and_user()
def delete_note(note, user):
    note.delete()
    return jsonify({"message": "Note deleted successfully"}), 200