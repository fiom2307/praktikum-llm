from services.gemini_service import generate_from_prompt
from database import SessionLocal
from models import WritingHistory
import re

def save_writing_history(user_id, user_answer, llm_feedback):
    db = SessionLocal()
    try:
        entry = WritingHistory(
            user_id=user_id,
            user_answer=user_answer,
            llm_feedback=llm_feedback
        )
        db.add(entry)
        db.commit()
        db.refresh(entry)
        return entry
    finally:
        db.close()

def correct_text_with_ai(user_id: int, user_text: str):

    prompt = (
        f"Analysiere den folgenden Text auf Italienisch und erkläre die vorhandenen Fehler "
        f"zu Grammatik und Stil AUF DEUTSCH: {user_text}\n"
        "Gib NUR eine Erklärung der Fehler zurück.\n"
        "Wiederhole oder korrigiere den Text NICHT.\n"
        "Füge KEINE zusätzlichen Kommentare oder Motivation hinzu.\n"
        "Am Ende gib eine Punktzahl zwischen 0 und 10 als „Pizzas X” an (nur ganze Zahlen).\n"
        "Falls der Text nicht auf Italienisch ist oder nicht zwischen 50 und 150 Wörtern liegt, gib „Pizzas 0” aus."
    )

    corrected = generate_from_prompt(prompt)
    
    pizzas = extract_pizzas(corrected)
    
    save_writing_history(
        user_id=user_id,
        user_answer=user_text,
        llm_feedback=corrected
    )

    return {"corrected_text": corrected, "pizzas": pizzas}

def extract_pizzas(text: str) -> int:
    match = re.search(r"Pizzas\s+(-?\d+)", text)
    if match:
        return int(match.group(1))
    return 0