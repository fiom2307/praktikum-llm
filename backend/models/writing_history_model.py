from sqlalchemy import Column, Integer, Text, TIMESTAMP, ForeignKey, func
from database import Base

class WritingHistory(Base):
    __tablename__ = "writing_history"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    user_answer = Column(Text)
    llm_feedback = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())
