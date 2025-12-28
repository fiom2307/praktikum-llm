from flask import Blueprint, jsonify, request
from services.pizza_count_service import increment_pizza_count

pizza_count_routes = Blueprint("pizza_count_routes", __name__)

@pizza_count_routes.route("/pizza_count", methods=["POST"])
def increment_pizzas():
    data = request.get_json()

    user_id = data.get("user_id")
    amount = data.get("amount", 1)
    city_key = data.get("city_key")  # puede ser None

    if not user_id:
        return jsonify({
            "success": False,
            "message": "user_id is required"
        }), 400

    new_pizza_count = increment_pizza_count(
        user_id=user_id,
        amount=amount,
        city_key=city_key
    )

    return jsonify({
        "success": True,
        "pizzaCount": new_pizza_count
    }), 200

