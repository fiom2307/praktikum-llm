from sqlalchemy import Column, Integer, Boolean, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.sql import func
from database import Base

class UserCityProgress(Base):
    __tablename__ = "user_city_progress"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    city_id = Column(Integer, ForeignKey("cities.id", ondelete="CASCADE"), nullable=False)

    vocabulary_pizzas_earned = Column(Integer, nullable=False, default=0)
    vocabulary_tasks_done = Column(Integer, nullable=False, default=0)

    reading_pizzas_earned = Column(Integer, nullable=False, default=0)
    reading_tasks_done = Column(Integer, nullable=False, default=0)

    writing_pizzas_earned = Column(Integer, nullable=False, default=0)
    writing_tasks_done = Column(Integer, nullable=False, default=0)
    
    unlocked = Column(Boolean, nullable=False, default=False)

    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        UniqueConstraint("user_id", "city_id", name="uq_user_city"),
    )
