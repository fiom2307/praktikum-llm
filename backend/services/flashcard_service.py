from database import SessionLocal
from models import Flashcard

def save_flashcard(user_id, word, definition=None):
    db = SessionLocal()
    try:
        # check duplicates
        existing = (
            db.query(Flashcard)
            .filter(Flashcard.user_id == user_id, Flashcard.word == word)
            .first()
        )

        if existing:
            return existing

        new_card = Flashcard(
            user_id=user_id,
            word=word,
            definition=definition or ""
        )

        db.add(new_card)
        db.commit()
        db.refresh(new_card)

        return new_card
    finally:
        db.close()

def get_flashcards(user_id):
    db = SessionLocal()
    try:
        return db.query(Flashcard).filter(Flashcard.user_id == user_id).all()
    finally:
        db.close()