from flask import Blueprint, request, jsonify
from services.admin_service import reset_user_password

admin_routes = Blueprint("admin_routes", __name__)


@admin_routes.route("/admin/reset-password", methods=["POST"])
def reset_password():
    data = request.get_json()

    admin_username = data.get("admin_username")
    child_username = data.get("child_username")
    new_password = data.get("new_password")

    if not admin_username or not child_username or not new_password:
        return jsonify({
            "success": False,
            "message": "Missing required data"
        }), 400

    response, status = reset_user_password(
        admin_username,
        child_username,
        new_password
    )

    return jsonify(response), status
