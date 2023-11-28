from flask import request, jsonify, Blueprint

from ORM.user import User

blp = Blueprint("User", __name__, url_prefix="/api/v1/user")


@blp.route('create', methods=['POST'])
def create_user():
    data = request.json
    email = data.get('email')
    username = data.get('username')

    user = User(email=email, username=username)
    user.save()

    return jsonify({"message": "User created successfully", "user_id": str(user.id)}), 201


@blp.route('get/all', methods=['GET'])
def get_all_users():
    users = User.objects()
    return jsonify({"users": [user.to_json() for user in users]}), 200


@blp.route('get/<user_id>', methods=['GET'])
def get_user_by_id(user_id):
    user = User.objects(id=user_id).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({"user": user.to_json()}), 200


@blp.route('update/<user_id>', methods=['PUT'])
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


@blp.route('delete/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.objects(id=user_id).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    user.delete()
    return jsonify({"message": "User deleted successfully"}), 200
