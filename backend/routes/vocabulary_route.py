from flask import Blueprint, request, jsonify
from services.vocabulary_service import generate_word_and_clues_with_ai, check_word_with_ai, get_current_vocabulary, save_current_vocabulary 

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
    username = data.get("username")

    result = check_word_with_ai(username, word, clues, answer)
    return jsonify(result)

@vocabulary_routes.route("/get_current_vocabulary", methods=["POST"])
def get_current_vocab():
    data = request.get_json()
    username = data.get("username")

    current_vocabulary = get_current_vocabulary(username)

    if current_vocabulary is None:
        return jsonify({"error": "User not found"}), 404
    
    return jsonify(current_vocabulary)

@vocabulary_routes.route("/save_current_vocabulary", methods=["POST"])
def save_current_vocab():
    data = request.get_json()
    username = data["username"]
    word = data["word"]
    clues = data["clues"]
    attempts = data["attempts"]
    completed = data["completed"]

    vocabulary = save_current_vocabulary(username, word, clues, attempts, completed)
    return jsonify(vocabulary)
