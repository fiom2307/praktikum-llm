from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, func, ForeignKey
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password_hashed = Column(Text, nullable=False)
    user_group = Column(String)
    pizza_count = Column(Integer, default=0)
    current_multiplier_value = Column(Integer, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    current_costume_id = Column(Integer, default=0, nullable=False)
    current_city_id = Column(Integer, ForeignKey("cities.id"))


def user_to_dict(user):
    if user is None:
        return None
    return {
        "id": user.id,
        "username": user.username,
        "pizza_count": user.pizza_count,
        "current_costume_id": user.current_costume_id,
        "current_multiplier_value": user.current_multiplier_value,
        "created_at": user.created_at.isoformat() if user.created_at else None,
    }
