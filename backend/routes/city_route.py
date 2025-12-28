from flask import Blueprint, jsonify
from services.city_service import get_city_progress_for_user, get_city_by_key, get_user_city_progress

city_routes = Blueprint("city_routes", __name__)

@city_routes.route("/cities/progress/<int:user_id>", methods=["GET"])
def get_cities_progress(user_id):
    data = get_city_progress_for_user(user_id)
    return jsonify({
        "success": True,
        "cities": data
    }), 200


@city_routes.route("/cities/<string:city_key>/<int:user_id>", methods=["GET"])
def get_city(city_key, user_id):
    city = get_city_by_key(city_key)
    if not city:
        return jsonify({"success": False}), 404

    progress = get_user_city_progress(user_id, city.id)

    return jsonify({
        "success": True,
        "city": {
            "key": city.name.lower(),
            "name": city.name,
            "level": city.order_index,
            "min_pizzas_to_unlock": city.min_pizzas_to_unlock,
            "pizzas_earned": progress.pizzas_earned if progress else 0
        }
    }), 200