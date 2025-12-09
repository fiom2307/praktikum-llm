from database import SessionLocal
from models import User
from models.shop_history_model import ShopHistoryModel

def get_user_by_username(username):
    db = SessionLocal()
    try:
        return db.query(User).filter(User.username == username).first()
    finally:
        db.close()

def equip_costume(username, item_id):
    
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == username).first()
        if not user:
            return None, "User not found."
        
        if item_id == 0:
            user.current_costume_id = 0
            db.commit()
            return 0, None

        has_item = db.query(ShopHistoryModel).filter(
            ShopHistoryModel.user_id == user.id,
            ShopHistoryModel.item_id == item_id
        ).first()

        if not has_item:
            return None, "Item not owned by user."

        user.current_costume_id = item_id
        db.commit()

        return item_id, None
        
    except Exception as e:
        db.rollback()
        print(f"Error equipping costume: {e}")
        return None, "Database error during equip."
    finally:
        db.close()