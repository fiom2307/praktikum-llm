from flask import Blueprint, request, jsonify
from services.reading_service import correct_answers_ai
from services.reading_service import generate_reading_text_from_ai


reading_routes = Blueprint("reading_routes", __name__)

@reading_routes.route("/correct_answers", methods=["POST"])
def correct_answer():
    data = request.get_json()
    user_text = data.get("text", "")
    generated_text = data.get("generatedText", "")

    response = correct_answers_ai(generated_text, user_text)

    return jsonify(response)

@reading_routes.route("/create_reading_text", methods=["POST"])
def create_reading_text():

    response = generate_reading_text_from_ai()

    return jsonify(response)