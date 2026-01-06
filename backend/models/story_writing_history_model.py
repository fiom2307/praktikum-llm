from sqlalchemy import Column, Integer, Text, TIMESTAMP, ForeignKey, func
from database import Base

class StoryWritingHistory(Base):
    __tablename__ = "story_writing_history"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    exercise_id = Column(Integer, ForeignKey("story_writing_exercises.id", ondelete="CASCADE"))
    user_answer = Column(Text)
    llm_feedback = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())
