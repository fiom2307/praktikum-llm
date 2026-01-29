from database import SessionLocal
from models import User, user_to_dict
from passlib.context import CryptContext
import random
from sqlalchemy import func
from models import City, UserCityProgress
import re

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
PASSWORD_REGEX = r"^(?=.*[A-Z])(?=.*[!@#$%^&*()\-_+=\[\]{};:'\",.<>/?]).{6,16}$"

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

def reset_own_password(username, old_password, new_password):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == username).first()

        if not user:
            return {
                "success": False,
                "message": "Utente non trovato"
            }, 404

        if not pwd_context.verify(old_password, user.password_hashed):
            return {
                "success": False,
                "message": "La password attuale non è corretta"
            }, 403


        if not new_password:
            return {
                "success": False,
                "message": "La nuova password è obbligatoria"
            }, 400

        if len(new_password) < 6:
            return {
                "success": False,
                "message": "La password deve contenere almeno 6 caratteri"
            }, 400

        if len(new_password) > 16:
            return {
                "success": False,
                "message": "La password non può superare i 16 caratteri"
            }, 400

        if not re.match(PASSWORD_REGEX, new_password):
            return {
                "success": False,
                "message": "La password deve contenere almeno una lettera maiuscola e un carattere speciale"
            }, 400

        user.password_hashed = pwd_context.hash(new_password)
        db.commit()

        return {
            "success": True,
            "message": "Password aggiornata con successo"
        }, 200

    finally:
        db.close()
