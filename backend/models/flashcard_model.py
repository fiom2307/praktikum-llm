from sqlalchemy import Column, Integer, Text, TIMESTAMP, ForeignKey, func
from database import Base

class Flashcard(Base):
    __tablename__ = "flashcards"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    word = Column(Text)
    definition = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())

def flashcard_to_dict(card):
    return {
        "id": card.id,
        "word": card.word,
        "definition": card.definition,
        "user_id": card.user_id,
        "created_at": card.created_at.isoformat() if card.created_at else None
    }
