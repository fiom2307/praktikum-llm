from flask import Blueprint, request, jsonify
from services.vocabulary_service import generate_word_and_clues_with_ai, check_word_with_ai, get_last_vocabulary_entry
from services.story_vocabulary_service import generate_word_and_clues_for_story, get_last_vocabulary_entry_from_city, story_vocabulary_history_to_dict, check_word_with_ai_in_story
from models import free_vocabulary_history_to_dict

vocabulary_routes = Blueprint("vocabulary_routes", __name__)

@vocabulary_routes.route("/generate_word_and_clues", methods=["POST"])
def generate_word_and_clues():
    data = request.get_json()
    user_id = data.get("userId")
    city_key = data.get("cityKey")

    if city_key:
        response = generate_word_and_clues_for_story(user_id, city_key)
    else:
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
    exercise_id = data.get("exerciseId", 0)

    if (exercise_id == 0):
        result = check_word_with_ai(userId, word, clues, answer, attempt)
    else:
        result = check_word_with_ai_in_story(userId, exercise_id, answer, attempt)
    return jsonify(result)

@vocabulary_routes.route("/vocabulary/last/<int:user_id>", methods=["GET"])
def get_last_vocabulary(user_id):

    entry = get_last_vocabulary_entry(user_id)

    if entry is None:
        return jsonify({"exists": False, "message": "No history entries found"})

    return jsonify({
        "exists": True,
        "history": free_vocabulary_history_to_dict(entry)
    })

@vocabulary_routes.route("/vocabulary/last/<string:city_key>/<int:user_id>", methods=["GET"])
def get_last_vocabulary_from_city(city_key, user_id):

    entry = get_last_vocabulary_entry_from_city(user_id, city_key)

    if entry is None:
        return jsonify({
            "exists": False,
            "message": "No history entries found for this city"
        })

    return jsonify({
        "exists": True,
        "history": story_vocabulary_history_to_dict(entry)
    })
