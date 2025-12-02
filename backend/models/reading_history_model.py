from sqlalchemy import Column, Integer, Text, TIMESTAMP, ForeignKey, func
from database import Base

class ReadingHistory(Base):
    __tablename__ = "reading_history"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    llm_question = Column(Text)
    user_answer = Column(Text)
    llm_feedback = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())
