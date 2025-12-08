from flask import Blueprint, request, jsonify
from services.shop_service import purchase_item, get_user_inventory

shop_bp = Blueprint('shop', __name__)

@shop_bp.route('/shop/buy', methods=['POST'])
def buy_item():
    
    data = request.get_json()

    username = data.get('username')
    item_id = data.get('item_id')
    item_cost = data.get('item_cost')

    if not username:
        return jsonify({"message": "Missing username"}), 400

    if item_id is None or item_cost is None:
        return jsonify({"message": "Missing item_id or item_cost"}), 400

    new_pizza_count, error = purchase_item(username, item_id, item_cost)

    if error:
        status_code = 403 if "Insufficient" in error else 400 
        return jsonify({"message": error}), status_code

    return jsonify({
        "message": "Purchase successful",
        "new_pizza_count": new_pizza_count 
    }), 200


@shop_bp.route('/shop/inventory', methods=['GET'])
def get_inventory():
   
    username = request.args.get('username')
    
    if not username:
        return jsonify({"message": "Missing username param"}), 400

    inventory = get_user_inventory(username)
    
    return jsonify({"inventory": inventory}), 200