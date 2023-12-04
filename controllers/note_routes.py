from flask import request, jsonify, Blueprint
from models import Note, User
from decorator import get_note_and_user
from database import db
from schemas import NoteSchema

note_schema = NoteSchema()
blp = Blueprint("Note", __name__, url_prefix="/api/v1/notes")


@blp.route('create', methods=['POST'])
def create_note():
    data = request.json
    title = data.get('title')
    text = data.get('text')
    user_id = data.get('user_id')

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    note = Note(title=title, text=text, user_id=user_id)
    db.session.add(note)
    db.session.commit()
    return jsonify({"message": "Note created successfully", "note_id": str(note.id)}), 201


@blp.route('', methods=['GET'])
def get_all_notes():
    notes = Note.query.all()
    result = note_schema.dump(notes, many=True)
    return jsonify({"notes": result}), 200


@blp.route('<note_id>', methods=['GET'])
def get_node_by_id(note_id):
    note = Note.query.get(note_id)
    if not note:
        return jsonify({"error": "Note not found"}), 404
    result = note_schema.dump(note)
    return jsonify({"note": result}), 200


@blp.route('<note_id>/<user_id>', methods=['PUT'])
@get_note_and_user()
def update_note(note, user):
    data = request.json
    new_title = data.get('title')
    new_text = data.get('text')

    note.title = new_title
    note.text = new_text
    db.session.commit()

    return jsonify({"message": "Note updated successfully"}), 200


@blp.route('<note_id>/<user_id>', methods=['DELETE'])
@get_note_and_user()
def delete_note(note, user):
    db.session.delete(note)
    db.session.commit()
    return jsonify({"message": "Note deleted successfully"}), 200
