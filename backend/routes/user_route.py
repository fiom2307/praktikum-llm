from flask import Blueprint, request, jsonify
from services.user_service import equip_costume
from models.user_model import User
from services.user_service import get_current_multiplier

user_routes = Blueprint('user', __name__)

@user_routes.route("/user/equip", methods=["POST"])
def equip_costume_route():
    data = request.get_json()
    username = data.get("username")
    item_id = data.get("item_id")

    if not username or item_id is None:
        return jsonify({"success": False, "message": "Missing username or item_id"}), 400

    try:
        item_id = int(item_id)
    except ValueError:
        return jsonify({"success": False, "message": "Invalid item_id format"}), 400

    new_costume_id, error = equip_costume(username, item_id)
    
    if error:
        return jsonify({"success": False, "message": error}), 400

    return jsonify({
        "success": True, 
        "current_costume_id": new_costume_id
    }), 200
    

@user_routes.route("/user/<username>/multiplier", methods=["GET"])
def get_current_multiplier_route(username):
    value, error = get_current_multiplier(username)

    if error:
        return jsonify({"error": error}), 404

    return jsonify({
        "current_multiplier_value": value
    })
