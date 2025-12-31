from models.shop_history_model import ShopHistoryModel
from database import SessionLocal
from sqlalchemy.exc import SQLAlchemyError
from models.user_model import User
from data.shop_items import SHOP_ITEMS as ITEMS_LIST

SHOP_ITEMS_DICT = {item["id"]: item for item in ITEMS_LIST}

def purchase_item(username, item_id, item_cost):
    db = SessionLocal()
    try:

        item = SHOP_ITEMS_DICT.get(item_id) 
        
        if not item:
            return None, "Item not found."
        
        if item['cost'] != item_cost:
            return None, f"Price mismatch. Server price is {item['cost']}."
            
        user = db.query(User).filter(User.username == username).first()
        if not user:
            return None, "User not found."
        
        if item_id > 100:
            if user.current_multiplier_value:
                return None, "Multiplier already active."

            user.active_multiplier_id = item_id
            user.current_multiplier_value = item["value"]
        
        if item.get("is_costume") or item_id in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]:
            existing_item = db.query(ShopHistoryModel).filter(
                ShopHistoryModel.user_id == user.id,
                ShopHistoryModel.item_id == item_id
            ).first()

            if existing_item:
                return None, "Hai già acquistato questo oggetto! (You already own this item)"
            
        if user.pizza_count < item_cost:
            return None, f"Insufficient pizza count. You have {user.pizza_count}, need {item_cost}."
            
        user.pizza_count -= item_cost
        
        new_purchase = ShopHistoryModel(
            user_id=user.id,
            item_id=item_id,
            item_name=item['name'], 
            item_cost=item_cost
        )
        db.add(new_purchase)
        
        db.commit()
        
        return user.pizza_count, None
        
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Database error: {e}")
        return None, "Database error occurred."
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        return None, "An internal error occurred."
    finally:
        db.close()

def get_user_inventory(username):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == username).first()
        if not user:
            return []

        inventory_records = db.query(ShopHistoryModel).filter(
            ShopHistoryModel.user_id == user.id
        ).order_by(ShopHistoryModel.purchased_at.desc()).all()
        
        inventory = []
        for r in inventory_records:
            item_info = SHOP_ITEMS_DICT.get(r.item_id)
            emoji = item_info.get('emoji', "📦")

            
            inventory.append({
                "id": r.id, 
                "item_id": r.item_id, 
                "item_name": r.item_name,
                "emoji": emoji,
                "purchased_at": r.purchased_at.isoformat() 
            })
        
        return inventory
    finally:
        db.close()

    