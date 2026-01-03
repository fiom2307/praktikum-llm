from flask import Blueprint, request, jsonify
from services.vocabulary_service import generate_word_and_clues_with_ai, check_word_with_ai, get_last_vocabulary_entry
from models import vocabulary_to_dict

vocabulary_routes = Blueprint("vocabulary_routes", __name__)

@vocabulary_routes.route("/generate_word_and_clues", methods=["POST"])
def generate_word_and_clues():
    data = request.get_json()
    user_id = data.get("userId")
    response = generate_word_and_clues_with_ai(user_id)
    return jsonify(response)

@vocabulary_routes.route("/check_word", methods=["POST"])
def check_word():
    data = request.get_json()
    word = data.get("word", "").strip()
    clues = data.get("clues", [])
    answer = data.get("answer", "").strip()
    userId = data.get("userId")
    attempt = data.get("attempt")

    result = check_word_with_ai(userId, word, clues, answer, attempt)
    return jsonify(result)

@vocabulary_routes.route("/vocabulary/last/<int:user_id>", methods=["GET"])
def get_last_vocabulary(user_id):

    entry = get_last_vocabulary_entry(user_id)

    if entry is None:
        return jsonify({"exists": False, "message": "No history entries found"})

    return jsonify({
        "exists": True,
        "history": vocabulary_to_dict(entry)
    })
