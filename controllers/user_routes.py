from flask import request, jsonify, Blueprint

from controllers.note_routes import note_schema
from database import db
from models import User
from schemas import UserSchema

blp = Blueprint("User", __name__, url_prefix="/api/v1/users")
user_schema = UserSchema()


@blp.route('create', methods=['POST'])
def create_user():
    data = request.json
    email = data.get('email')
    username = data.get('username')

    user = User(email=email, username=username)
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User created successfully", "user_id": str(user.id)}), 201


@blp.route('', methods=['GET'])
def get_all_users():
    users = User.query.all()
    result = user_schema.dump(users, many=True)
    return jsonify({"users": result}), 200


@blp.route('<user_id>', methods=['GET'])
def get_user_by_id(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    result = user_schema.dump(user)
    return jsonify({"user": result}), 200


@blp.route('<user_id>/notes', methods=['GET'])
def get_all_notes_by_user_id(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    notes = user.notes
    result = note_schema.dump(notes, many=True)
    return jsonify({"Notes by user": result}), 200


@blp.route('<user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    new_username = data.get('username')
    new_email = data.get('email')

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    user.username = new_username
    user.email = new_email
    db.session.commit()

    return jsonify({"message": "User updated successfully"}), 200


@blp.route('<user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "User deleted successfully"}), 200
