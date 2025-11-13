from flask import Blueprint, jsonify, request
from services.pizza_count_service import increment_pizza_count

pizza_count_routes = Blueprint("pizza_count_routes", __name__)

@pizza_count_routes.route("/increment_pizza_count", methods=["POST"])
def increment_pizzas():
    data = request.get_json()
    username = data["username"]
    inc = data["inc"]

    new_pizza_count = increment_pizza_count(username, inc)

    return jsonify({"pizzaCount": new_pizza_count})

    
