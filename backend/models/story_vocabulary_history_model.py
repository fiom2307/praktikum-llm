from sqlalchemy import Column, Integer, Text, TIMESTAMP, ForeignKey, func, Boolean
from database import Base

class StoryVocabularyHistory(Base):
    __tablename__ = "free_vocabulary_history"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    exercise_id = Column(Integer, ForeignKey("story_vocabulary_exercises.id", ondelete="CASCADE"))
    user_answer = Column(Text)
    attempt_number = Column(Integer)
    completed = Column(Boolean, default=False, nullable=False)
    correct = Column(Boolean, default=False, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
