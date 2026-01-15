from database import SessionLocal
from models import User, City, UserCityProgress
from services.city_service import get_city_by_key

def increment_pizza_count(user_id, amount, game_mode, city_key=None):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return None
        
        final_amount = amount
        
        if user.current_multiplier_value:
            value = user.current_multiplier_value

            if value == 10 and not (game_mode == "vocabulary"):
                if ((game_mode == "reading" and amount >= 4) or
                    (game_mode == "writing" and amount >= 7)):
                    final_amount *= 10
            else:
                final_amount *= value

            user.current_multiplier_value = None

        user.pizza_count = (user.pizza_count or 0) + final_amount

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
                        city_id=city.id
                    )
                    db.add(progress)

                if(game_mode == "reading"):
                    if (progress.reading_pizzas_earned < 5):
                        progress.reading_pizzas_earned += amount
                    if(progress.reading_tasks_done == 0):
                        progress.reading_tasks_done += 1
                elif(game_mode == "vocabulary"):
                    if (progress.vocabulary_pizzas_earned < 10):
                        progress.vocabulary_pizzas_earned += amount
                    if(progress.vocabulary_tasks_done < 10):
                        progress.vocabulary_tasks_done += 1
                elif(game_mode == "writing"):
                    if (progress.writing_pizzas_earned < 7):
                        progress.writing_pizzas_earned += amount
                    if(progress.writing_tasks_done == 0):
                        progress.writing_tasks_done += 1
                        
                if (progress.reading_pizzas_earned >= 5 and progress.reading_tasks_done >= 1) and (progress.vocabulary_pizzas_earned >= 10 and progress.vocabulary_tasks_done >= 10) and (progress.writing_pizzas_earned >= 7 and progress.writing_tasks_done >= 1):
                    if city.id == user.current_city_id:
                        print("next city")
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
            unlocked=True
        )
        db.add(progress)
    else:
        progress.unlocked = True

    user = db.query(User).filter(User.id == user_id).first()
    user.current_city_id = next_city.id
