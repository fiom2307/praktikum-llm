from database import SessionLocal
from models.city_model import City

def seed_cities():
    db = SessionLocal()

    cities = [
        {
            "id": 1,
            "name": "Napoli",
            "order_index": 1,
            "vocabulary_pizza_goal": 10,
            "vocabulary_task_count": 10,
            "reading_pizza_goal": 5,
            "reading_task_count": 1,
            "writing_pizza_goal": 7,
            "writing_task_count": 1,
        },
        {
            "id": 2,
            "name": "Palermo",
            "order_index": 2,
            "vocabulary_pizza_goal": 10,
            "vocabulary_task_count": 10,
            "reading_pizza_goal": 5,
            "reading_task_count": 1,
            "writing_pizza_goal": 7,
            "writing_task_count": 1,
        },
        {
            "id": 3,
            "name": "Roma",
            "order_index": 3,
            "vocabulary_pizza_goal": 10,
            "vocabulary_task_count": 10,
            "reading_pizza_goal": 5,
            "reading_task_count": 1,
            "writing_pizza_goal": 7,
            "writing_task_count": 1,
        },
        {
            "id": 4,
            "name": "Siena",
            "order_index": 4,
            "vocabulary_pizza_goal": 10,
            "vocabulary_task_count": 10,
            "reading_pizza_goal": 5,
            "reading_task_count": 1,
            "writing_pizza_goal": 7,
            "writing_task_count": 1,
        },
        {
            "id": 5,
            "name": "Venezia",
            "order_index": 5,
            "vocabulary_pizza_goal": 10,
            "vocabulary_task_count": 10,
            "reading_pizza_goal": 5,
            "reading_task_count": 1,
            "writing_pizza_goal": 7,
            "writing_task_count": 1,
        },
        {
            "id": 6,
            "name": "Torino",
            "order_index": 6,
            "vocabulary_pizza_goal": 10,
            "vocabulary_task_count": 10,
            "reading_pizza_goal": 5,
            "reading_task_count": 1,
            "writing_pizza_goal": 7,
            "writing_task_count": 1,
        },
    ]

    for city_data in cities:
        city = db.query(City).filter(City.id == city_data["id"]).first()

        if city:
            # UPDATE if it exists
            for key, value in city_data.items():
                setattr(city, key, value)
        else:
            # INSERT if it does not exist
            db.add(City(**city_data))

    db.commit()
    db.close()