from database import SessionLocal
from models import User
from models.shop_history_model import ShopHistoryModel
from sqlalchemy.orm.attributes import flag_modified

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
        

def get_current_multiplier(username):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == username).first()
        if not user:
            return None, "User not found"
        return user.current_multiplier_value, None
    finally:
        db.close()

def mark_tutorial_seen(username, task_type):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == username).first()
        if not user:
            return None, "User not found."

        progress = dict(user.tutorial_progress) if user.tutorial_progress else {"reading": False, "vocabulary": False, "writing": False}
        
        if task_type in progress:
            progress[task_type] = True
            user.tutorial_progress = progress
            
            flag_modified(user, "tutorial_progress")
            
            db.commit()
            return True, None
        else:
            return None, f"Unknown task type: {task_type}"
            
    except Exception as e:
        db.rollback()
        return None, str(e)
    finally:
        db.close()