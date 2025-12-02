from database import SessionLocal
from models import User

def increment_pizza_count(user_id, inc):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return None

        user.pizza_count = (user.pizza_count or 0) + inc

        db.commit()
        db.refresh(user)

        return user.pizza_count
    finally:
        db.close()
