from database import SessionLocal
from models import User

def get_user_by_username(username):
    db = SessionLocal()
    try:
        return db.query(User).filter(User.username == username).first()
    finally:
        db.close()