from flask import Blueprint, request, jsonify
from services.city_service import get_city_by_key
from models import UserCityProgress
from database import SessionLocal

user_city_progress_routes = Blueprint("user_city_progress_routes", __name__)

@user_city_progress_routes.route("/add_task_to_user_city_progress/<int:user_id>", methods=["POST"])
def add_task_to_user_city_progress(user_id):
    data = request.get_json()
    city_key = data.get("cityKey")
    page_type = data.get("pageType")

    if not city_key or not page_type:
        return jsonify({"error": "Missing cityKey or pageType"}), 400

    db = SessionLocal()

    city = get_city_by_key(city_key)
    if not city:
        return jsonify({"error": "City not found"}), 404

    progress = (
        db.query(UserCityProgress)
        .filter(
            UserCityProgress.user_id == user_id,
            UserCityProgress.city_id == city.id
        )
        .first()
    )

    if not progress:
        return jsonify({"error": "User city progress not found"}), 404

    # 🔒 LIMITS
    if page_type == "vocabulary":
        if progress.vocabulary_tasks_done >= city.vocabulary_task_count:
            return jsonify({"success": True, "reached_limit": True})
        progress.vocabulary_tasks_done += 1

    elif page_type == "reading":
        if progress.reading_tasks_done >= city.reading_task_count:
            return jsonify({"success": True, "reached_limit": True})
        progress.reading_tasks_done += 1

    elif page_type == "writing":
        if progress.writing_tasks_done >= city.writing_task_count:
            return jsonify({"success": True, "reached_limit": True})
        progress.writing_tasks_done += 1

    else:
        return jsonify({"error": "Invalid pageType"}), 400

    db.commit()

    return jsonify({
        "success": True,
        "reached_limit": False
    })