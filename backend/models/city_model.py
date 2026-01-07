from sqlalchemy import Column, Integer, String
from database import Base

class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    order_index = Column(Integer, nullable=False)
    vocabulary_pizza_goal = Column(Integer, nullable=False)
    vocabulary_task_count = Column(Integer, nullable=False)
    reading_pizza_goal = Column(Integer, nullable=False)
    reading_task_count = Column(Integer, nullable=False)
    writing_pizza_goal = Column(Integer, nullable=False)
    writing_task_count = Column(Integer, nullable=False)