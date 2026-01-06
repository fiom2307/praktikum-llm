from database import SessionLocal
from models import User, user_to_dict
from passlib.context import CryptContext
import random
from sqlalchemy import func
from models import City, UserCityProgress

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

        cities = db.query(City).order_by(City.order_index).all()

        for city in cities:
            db.add(UserCityProgress(
                user_id=user.id,
                city_id=city.id,
                unlocked=(city.order_index == 1)
            ))

        user.current_city_id = cities[0].id

        db.commit()

        user_data = user_to_dict(user)
        return user_data
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


