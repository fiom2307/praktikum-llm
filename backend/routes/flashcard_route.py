from flask import Blueprint, request, jsonify
from services.flashcard_service import save_flashcard, get_flashcards
from models import flashcard_to_dict

flashcard_routes = Blueprint("flashcard_routes", __name__)

@flashcard_routes.route("/flashcards/<int:user_id>", methods=["POST"])
def add_user_flashcard(user_id):
    data = request.get_json()
    word = data.get("word")
    definition = data.get("definition", "")

    new_card = save_flashcard(user_id, word, definition)
    return jsonify({
        "success": True,
        "flashcard": flashcard_to_dict(new_card)
    })

@flashcard_routes.route("/flashcards/<int:user_id>", methods=["GET"])
def get_user_flashcards(user_id):
    
    flashcards = get_flashcards(user_id)
    
    return jsonify({
        "success": True,
        "flashcards": [flashcard_to_dict(card) for card in flashcards]
    })