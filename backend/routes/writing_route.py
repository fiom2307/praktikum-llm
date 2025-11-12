from flask import Blueprint, request, jsonify
from services.writing_service import correct_text_with_ai

writing_routes = Blueprint("writing_routes", __name__)

@writing_routes.route("/correct_text", methods=["POST"])
def correct_text():
    data = request.get_json()
    user_text = data.get("text", "")

    result = correct_text_with_ai(user_text)

    return jsonify(result)
