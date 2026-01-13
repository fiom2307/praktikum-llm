from flask import Blueprint, request, jsonify
from services.writing_service import correct_text_with_ai, generate_exercise_with_ai
from services.story_writing_service import correct_story_text_with_ai, fetch_writing_text_service

writing_routes = Blueprint("writing_routes", __name__)

@writing_routes.route("/correct_text", methods=["POST"])
def correct_text():
    data = request.get_json()
    user_text = data.get("text", "")
    userId = data.get("userId")
    exerciseId = data.get("exerciseId")
    
    if(exerciseId == 0):
        result = correct_text_with_ai(userId, user_text)
    else:
        result = correct_story_text_with_ai(userId, user_text, exerciseId)

    return jsonify(result)

@writing_routes.route("/fetch_writing_text", methods=["POST"])
def fetch_reading_text():
    data = request.get_json()
    city_key=data.get("cityKey")
    
    if(city_key != ""):
        print("story")
        return jsonify(
            fetch_writing_text_service(
                user_id=data.get("userId"),
                city_key=city_key
            )
        )
    else:
        print("free")
        return jsonify(
            generate_exercise_with_ai(
                user_id=data.get("userId"),
            )
        )
