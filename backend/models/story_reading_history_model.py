from sqlalchemy import Column, Integer, Text, TIMESTAMP, ForeignKey, func, ARRAY
from database import Base

class StoryReadingHistory(Base):
    __tablename__ = "story_reading_history"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    exercise_id = Column(Integer, ForeignKey("story_reading_exercises.id", ondelete="CASCADE"))
    user_answer = Column(Text)
    llm_feedback = Column(Text)
    correct_question_indexes = Column(ARRAY(Integer))
    created_at = Column(TIMESTAMP, server_default=func.now())
