import re
import json
from services.gemini_service import generate_from_prompt
from database import SessionLocal
from models import VocabularyHistory

def generate_word_and_clues_with_ai():
    prompt = (
        "Generate one Italian vocabulary word that would be appropriate for a 14-year-old student "
        "with an A2 level of Italian. Then, write three short clues in Italian (maximum 5 words each) "
        "that help the student guess the word. "
        "Each clue should be simple and clear, avoiding long sentences or rare words. "
        "Return *only* valid JSON, without explanations or code block formatting. Example:\n"
        '{"word": "gatto", "clues": ["È un animale.", "Fa miao.", "Ama dormire."]}'
    )

    raw_response = generate_from_prompt(prompt)

    clean_text = re.sub(r"```json|```", "", raw_response).strip()

    try:
        return json.loads(clean_text)
    except json.JSONDecodeError:
        return {"raw_response": raw_response}
    
def save_vocabulary_history(user_id: int, word: str, clues: list, answer: str, attempt: int):
    db = SessionLocal()
    try:
        entry = VocabularyHistory(
            user_id=user_id,
            word=word,
            clues=clues,
            user_answer=answer,
            user_attempt=attempt
        )
        db.add(entry)
        db.commit()
        return entry
    finally:
        db.close()
    

def check_word_with_ai(userId: int, word: str, clues: list, answer: str, attempt: int):

    prompt = (
        f"Word: {word}\n"
        f"User answer: {answer}\n"
        f"Clues: {json.dumps(clues, ensure_ascii=False)}\n\n"
        "Compare the user's answer with the correct word in Italian.\n"
        "If it matches exactly, return:\n"
        '{"status": "correct", "hint": ""}\n'
        "If it's close (e.g. small spelling mistake or a synonym), return:\n"
        '{"status": "almost", "hint": "brief explanation in Italian"}\n'
        "If it's wrong, return:\n"
        '{"status": "incorrect", "hint": ""}\n'
        "Return only valid JSON, no extra text."
    )

    raw_response = generate_from_prompt(prompt)
    clean_text = re.sub(r"```json|```", "", raw_response).strip()

    save_vocabulary_history(
        user_id=userId,
        word=word,
        clues=clues,
        answer=answer,
        attempt=attempt,
    )

    try:
        return json.loads(clean_text)
    except json.JSONDecodeError:
        return {"raw_response": raw_response}

def get_last_vocabulary_entry(user_id: int):
    db = SessionLocal()
    try:
        entry = (
            db.query(VocabularyHistory)
        .filter(VocabularyHistory.user_id == user_id)
        .order_by(VocabularyHistory.created_at.desc())
        .first()
        )

        return entry
    finally:
        db.close()
