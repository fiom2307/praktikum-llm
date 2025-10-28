from flask import Blueprint, jsonify, request
from services.auth_service import find_user

auth_routes = Blueprint("auth_routes", __name__)

@auth_routes.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username", "")

    user = find_user(username)
    if user:
        return jsonify({"exists": True, "user": user})
    return jsonify({"exists": False}), 404 # not found
