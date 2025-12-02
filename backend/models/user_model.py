from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, func
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password_hashed = Column(Text, nullable=False)
    user_group = Column(String)
    pizza_count = Column(Integer, default=0)
    created_at = Column(TIMESTAMP, server_default=func.now())


def user_to_dict(user):
    if user is None:
        return None
    return {
        "id": user.id,
        "username": user.username,
        "user_group": user.user_group,
        "pizza_count": user.pizza_count,
        "created_at": user.created_at.isoformat() if user.created_at else None,
    }
