from database import SessionLocal
from models import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def authenticate_user(username, password):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == username).first()
        if not user:
            return None

        if pwd_context.verify(password, user.password_hashed):
            return user
        
        return None

    finally:
        db.close()

def register_user(username, password):
    db = SessionLocal()
    try:        
        hashed = pwd_context.hash(password)

        user = User(username=username, password_hashed=hashed)
        db.add(user)
        db.commit()
        db.refresh(user)

        return user
    finally:
        db.close()


