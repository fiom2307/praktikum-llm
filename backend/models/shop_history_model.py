from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base 

class ShopHistoryModel(Base):
    __tablename__ = 'shop_history'

    id = Column(Integer, primary_key=True, index=True)
    
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    item_id = Column(Integer, nullable=False)       
    item_name = Column(String(100), nullable=False) 
    item_cost = Column(Integer, nullable=False)     
    
    # record purchase time
    purchased_at = Column(DateTime, default=func.now())
