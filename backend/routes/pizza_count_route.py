from flask import Blueprint, jsonify, request
from services.pizza_count_service import increment_pizza_count

pizza_count_routes = Blueprint("pizza_count_routes", __name__)

@pizza_count_routes.route("/pizza_count/<int:user_id>", methods=["POST"])
def increment_pizzas(user_id):
    data = request.get_json()
    inc = data.get("inc", 1)

    new_pizza_count = increment_pizza_count(user_id, inc)

    return jsonify({ "success": True, "pizzaCount": new_pizza_count })

    
