from flask import Blueprint, request, jsonify
from services.reading_service import correct_answers_ai, generate_reading_text_from_ai
from services.story_reading_service import get_city_reading_text_for_user


reading_routes = Blueprint("reading_routes", __name__)

@reading_routes.route("/correct_answers", methods=["POST"])
def correct_answer():
    data = request.get_json()
    user_id = data.get("userId")
    user_text = data.get("text", "")
    generated_text = data.get("generatedText", "")

    response = correct_answers_ai(user_id, generated_text, user_text)

    return jsonify(response)

@reading_routes.route("/create_reading_text", methods=["POST"])
def create_reading_text():
    data = request.get_json()
    user_id = data.get("userId")
    city_key = data.get("cityKey")

    if city_key:
        response = get_city_reading_text_for_user(user_id, city_key)
    else:
        response = generate_reading_text_from_ai(user_id)

    return jsonify(response)