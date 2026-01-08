from database import SessionLocal
from models import Flashcard
from services.openai_service import generate_from_prompt

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

        # generate definition + eselsbrücke
        if not definition:
            prompt = (
                f"Erkläre sehr kurz das italienische Wort '{word}'.\n"
                "Regeln:\n"
                "- Verwende eine sehr kurze und einfache Definition.\n"
                "- Füge eine Eselsbrücke (Merkhilfe) hinzu.\n"
                "- Schreibe NUR im folgenden Format:\n\n"
                "Definition: ...\n"
                "Eselsbrücke: ..."
            )

            definition = generate_from_prompt(prompt).strip()

        new_card = Flashcard(
            user_id=user_id,
            word=word,
            definition=definition
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