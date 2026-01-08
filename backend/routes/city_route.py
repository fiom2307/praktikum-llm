from flask import Blueprint, jsonify
from services.city_service import get_all_city_progress_for_user, get_city_by_key, get_user_progress_for_city

city_routes = Blueprint("city_routes", __name__)

@city_routes.route("/cities/progress/<int:user_id>", methods=["GET"])
def get_cities_progress(user_id):
    data = get_all_city_progress_for_user(user_id)
    return jsonify({
        "success": True,
        "cities": data
    }), 200


@city_routes.route("/cities/<string:city_key>/<int:user_id>", methods=["GET"])
def get_city(city_key, user_id):
    city = get_city_by_key(city_key)
    if not city:
        return jsonify({"success": False}), 404

    progress = get_user_progress_for_city(user_id, city.id)

    if not progress or not progress.unlocked:
        return jsonify({
            "success": False,
            "error": "City locked"
        }), 403

    return jsonify({
        "success": True,
        "city": {
            "key": city.name.lower(),
            "name": city.name,
            "level": city.order_index,
            "vocabulary_pizza_goal": city.vocabulary_pizza_goal,
            "vocabulary_pizzas_earned": progress.vocabulary_pizzas_earned,
            "reading_pizza_goal": city.reading_pizza_goal,
            "reading_pizzas_earned": progress.reading_pizzas_earned,
            "writing_pizza_goal": city.writing_pizza_goal,
            "writing_pizzas_earned": progress.writing_pizzas_earned,

            "vocabulary_task_count": city.vocabulary_task_count,
            "vocabulary_tasks_done": progress.vocabulary_tasks_done,
            "reading_task_count": city.reading_task_count,
            "reading_tasks_done": progress.reading_tasks_done,
            "writing_task_count": city.writing_task_count,
            "writing_tasks_done": progress.writing_tasks_done
        }
    }), 200