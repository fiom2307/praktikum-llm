from database import SessionLocal
from models import User
from passlib.context import CryptContext
import random
from sqlalchemy import func

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

        group = assign_group(db)

        user = User(
            username=username, 
            password_hashed=hashed, 
            user_group=group)
        
        db.add(user)
        db.commit()
        db.refresh(user)

        return user
    finally:
        db.close()

def assign_group(db):    
    treatment_count = db.query(func.count(User.id))\
        .filter(User.user_group == "treatment")\
        .scalar()

    control_count = db.query(func.count(User.id))\
        .filter(User.user_group == "control")\
        .scalar()

    if treatment_count < control_count:
        return "treatment"
    elif control_count < treatment_count:
        return "control"
    else:
        return random.choice(["treatment", "control"])


