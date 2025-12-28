from database import SessionLocal
from models import User, City, UserCityProgress
from services.city_service import get_city_by_key

def increment_pizza_count(user_id, amount, city_key=None):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return None

        user.pizza_count = (user.pizza_count or 0) + amount

        if city_key:
            city = get_city_by_key(city_key)
            if city:
                progress = (
                    db.query(UserCityProgress)
                    .filter(
                        UserCityProgress.user_id == user_id,
                        UserCityProgress.city_id == city.id
                    )
                    .first()
                )

                if not progress:
                    progress = UserCityProgress(
                        user_id=user_id,
                        city_id=city.id,
                        pizzas_earned=0,
                        unlocked=True
                    )
                    db.add(progress)

                progress.pizzas_earned += amount

                if progress.pizzas_earned >= city.min_pizzas_to_unlock:
                    if city.id == user.current_city_id:
                        unlock_next_city(db, user_id, city)

        db.commit()
        return user.pizza_count

    finally:
        db.close()

def unlock_next_city(db, user_id, city):
    next_city = (
        db.query(City)
        .filter(City.order_index == city.order_index + 1)
        .first()
    )

    if not next_city:
        return

    progress = (
        db.query(UserCityProgress)
        .filter(
            UserCityProgress.user_id == user_id,
            UserCityProgress.city_id == next_city.id
        )
        .first()
    )

    if not progress:
        progress = UserCityProgress(
            user_id=user_id,
            city_id=next_city.id,
            pizzas_earned=0,
            unlocked=True
        )
        db.add(progress)
    else:
        progress.unlocked = True

    user = db.query(User).filter(User.id == user_id).first()
    user.current_city_id = next_city.id
