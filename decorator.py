from functools import wraps
from flask import jsonify

from models import Note, User



def get_note_and_user(note_id_param='note_id', user_id_param='user_id'):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            note_id = kwargs.get(note_id_param)
            user_id = kwargs.get(user_id_param)

            note = Note.query.get(note_id)
            user = User.query.get(user_id)

            if not user:
                return jsonify({"error": "User not found"}), 404

            if not note:
                return jsonify({"error": "Note not found"}), 404

            if str(note.user_id) != str(user_id):
                return jsonify({"error": "You are not allowed to perform this action"}), 403

            return func(note, user)

        return wrapper

    return decorator

