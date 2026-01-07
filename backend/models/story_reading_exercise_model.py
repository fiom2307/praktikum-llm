from sqlalchemy import Column, Integer, Text, ForeignKey, ARRAY
from database import Base

class StoryReadingExercise(Base):
    __tablename__ = "story_reading_exercises"

    id = Column(Integer, primary_key=True)
    city_id = Column(Integer, ForeignKey("cities.id", ondelete="CASCADE"))
    text = Column(Text)
    questions = Column(ARRAY(Text))
