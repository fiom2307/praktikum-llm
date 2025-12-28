from sqlalchemy import Column, Integer, String
from database import Base

class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    order_index = Column(Integer, nullable=False)
    min_pizzas_to_unlock = Column(Integer, nullable=False)