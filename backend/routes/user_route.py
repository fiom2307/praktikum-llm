from flask import Blueprint, request, jsonify
from services.user_service import equip_costume 

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