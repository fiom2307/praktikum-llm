from flask import Blueprint, request, jsonify
from services.flashcard_service import save_flashcard, get_flashcards

flashcard_routes = Blueprint("flashcard_routes", __name__)

@flashcard_routes.route("/save_flashcard", methods=["POST"])
def save_current_vocab():
    data = request.get_json()
    username = data.get("username")
    word = data.get("word")

    saved_word = save_flashcard(username, word)
    return jsonify(saved_word)

@flashcard_routes.route("/get_flashcards", methods=["POST"])
def get_current_vocab():
    data = request.get_json()
    username = data.get("username")

    flashcards = get_flashcards(username)
    
    return jsonify(flashcards)