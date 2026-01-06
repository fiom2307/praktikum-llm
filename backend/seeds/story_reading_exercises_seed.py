from database import SessionLocal
from models.city_model import City

def seed_cities():
    db = SessionLocal()

    cities = [
        {"id": 1, "name": "Napoli", "order_index": 1},
        {"id": 2, "name": "Palermo", "order_index": 2},
        {"id": 3, "name": "Roma", "order_index": 3},
        {"id": 4, "name": "Siena", "order_index": 4},
        {"id": 5, "name": "Venezia", "order_index": 5},
        {"id": 6, "name": "Torino", "order_index": 6},
    ]

    for city in cities:
        exists = db.query(City).filter(City.id == city["id"]).first()
        if not exists:
            db.add(City(**city))

    db.commit()
    db.close()
