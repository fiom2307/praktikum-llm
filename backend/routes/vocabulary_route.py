from flask import Blueprint, request, jsonify
from services.vocabulary_service import generate_word_and_clues_with_ai, check_word_with_ai

vocabulary_routes = Blueprint("vocabulary_routes", __name__)

@vocabulary_routes.route("/generate_word_and_clues", methods=["POST"])
def generate_word_and_clues():
    data = generate_word_and_clues_with_ai()
    return jsonify(data)

@vocabulary_routes.route("/check_word", methods=["POST"])
def check_word():
    data = request.get_json()
    word = data.get("word", "").strip()
    clues = data.get("clues", [])
    answer = data.get("answer", "").strip()

    result = check_word_with_ai(word, clues, answer)
    return jsonify(result)