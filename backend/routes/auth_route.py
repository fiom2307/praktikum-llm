from flask import Blueprint, jsonify, request
from services.auth_service import authenticate_user
from services.user_service import get_user

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
    

@auth_routes.route("/history/<string:username>", methods=["GET"])
def get_user_history(username):
    # 
    
    user = get_user(username)

    if not user:
        return jsonify({"message": f"User {username} not found"}), 404
    
    # 
    history_data = user.get("history", []) 
    
    return jsonify({"username": username, "history": history_data}), 200

    
