from sqlalchemy import Column, Integer, Text, ForeignKey, ARRAY
from database import Base

class StoryVocabularyExercise(Base):
    __tablename__ = "story_reading_exercises"

    id = Column(Integer, primary_key=True)
    city_id = Column(Integer, ForeignKey("cities.id", ondelete="CASCADE"))
    word = Column(Text)
    clues = Column(ARRAY(Text))
