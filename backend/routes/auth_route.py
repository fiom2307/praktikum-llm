from flask import Blueprint, jsonify, request
from services.auth_service import authenticate_user

auth_routes = Blueprint("auth_routes", __name__)

@auth_routes.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"exists": False, "message": "Missing username or password"}),400

    user = authenticate_user(username, password)

    if user:
        return jsonify({"exists": True, "user": user})
    else:
        return jsonify({"exists": False, "message": "Invalid credentials"}), 401

    
