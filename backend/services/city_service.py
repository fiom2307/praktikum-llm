from database import SessionLocal
from models import City, UserCityProgress
from sqlalchemy import func

def get_city_progress_for_user(user_id: int):
    db = SessionLocal()
    try:
        rows = (
            db.query(City, UserCityProgress)
            .join(
                UserCityProgress,
                (UserCityProgress.city_id == City.id)
            )
            .filter(UserCityProgress.user_id == user_id)
            .order_by(City.order_index)
            .all()
        )

        result = []

        for city, progress in rows:
            result.append({
                "key": city.name.lower(),
                "unlocked": progress.unlocked,
                "pizzas_earned": progress.pizzas_earned,
                "min_pizzas_to_unlock": city.min_pizzas_to_unlock
            })

        return result

    finally:
        db.close()


def get_city_by_key(city_key):
    db = SessionLocal()
    try:
        return db.query(City).filter(func.lower(City.name) == city_key.lower()).first()
    finally:
        db.close()

def get_user_city_progress(user_id, city_id):
    db = SessionLocal()
    try:
        return (
            db.query(UserCityProgress)
            .filter(
                UserCityProgress.user_id == user_id,
                UserCityProgress.city_id == city_id
            )
            .first()
        )
    finally:
        db.close()

