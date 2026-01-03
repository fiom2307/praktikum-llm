from sqlalchemy import Column, Integer, Text, TIMESTAMP, ForeignKey, ARRAY, func, Boolean
from database import Base

class VocabularyHistory(Base):
    __tablename__ = "vocabulary_history"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    clues = Column(ARRAY(Text))
    word = Column(Text)
    user_answer = Column(Text)
    user_attempt = Column(Integer)
    completed = Column(Boolean, default=False, nullable=False)
    corrected = Column(Boolean, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())

def vocabulary_to_dict(entry):
    if entry is None:
        return None
    
    completed = (
        entry.user_attempt == 3 or
        (entry.user_answer is not None and entry.word == entry.user_answer)

    )

    return {
        "word": entry.word,
        "clues": entry.clues,
        "attempt": entry.user_attempt,
        "user_answer": entry.user_answer,
        "completed": completed,
        "corrected": entry.corrected,
        "created_at": entry.created_at.isoformat() if entry.created_at else None
    }
