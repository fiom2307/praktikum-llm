from flask import Blueprint, jsonify, request
import json

login_routes = Blueprint("login_routes", __name__)

@login_routes.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username", "").strip().lower()

    with open("data/users.json", "r") as f:
        users = json.load(f)

    user = next((u for u in users if u["username"].lower() == username), None)

    if user:
        return jsonify({"exists": True, "user": user})
    else:
        return jsonify({"exists": False})
