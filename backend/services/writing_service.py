from services.openai_service import generate_from_prompt
from database import SessionLocal
from models import WritingHistory
import re
from models import User

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
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return {"corrected_text": "", "pizzas": 0}
        
        histories = (
            db.query(WritingHistory)
            .filter(WritingHistory.user_id == user_id)
            .order_by(WritingHistory.created_at.desc())
            .limit(5)
            .all()
        )

        previous_feedbacks = [
            h.llm_feedback for h in histories if h.llm_feedback
        ]

        previous_feedbacks_str = "\n\n---\n\n".join(previous_feedbacks)

        prompt_1 = (
            f"Analysiere den folgenden Text auf Italienisch und erkläre die vorhandenen Fehler "
            f"zu Grammatik und Stil AUF DEUTSCH: {user_text}\n"
            "Gib NUR eine Erklärung der Fehler zurück.\n"
            "Wiederhole oder korrigiere den Text NICHT.\n"
            "Füge KEINE zusätzlichen Kommentare oder Motivation hinzu.\n"
            "Am Ende gib eine Punktzahl zwischen 0 und 10 als „Pizzas X” an (nur ganze Zahlen).\n"
            "Falls der Text nicht auf Italienisch ist oder nicht zwischen 50 und 150 Wörtern liegt, gib „Pizzas 0” aus."
        )

        prompt_2 = (
            f"Analysiere den folgenden Text auf Italienisch und erkläre die vorhandenen Fehler."
            f"zu Grammatik und Stil AUF DEUTSCH: {user_text}\n"
            "Gib NUR eine Erklärung der Fehler zurück.\n"
            "Wiederhole oder korrigiere den Text NICHT.\n"
            "Füge KEINE zusätzlichen Kommentare oder Motivation hinzu.\n"
            "Am Ende gib eine Punktzahl zwischen 0 und 10 als „Pizzas X” an (nur ganze Zahlen). Das erwartete Niveau des user ist A2.\n"
            "Falls der Text nicht auf Italienisch ist oder nicht zwischen 50 und 150 Wörtern liegt, gib „Pizzas 0” aus."
            "ZUSÄTZLICH:\n"
            "Analysiere die folgenden früheren Rückmeldungen des Schülers. "
            "Suche nach Fehlern, die sich mehrfach wiederholen (z.B. gleiche Grammatikprobleme, "
            "falsche Verbformen, Präpositionen, Artikel oder Satzstellung).\n\n"
            "Wenn es wiederkehrende Fehler gibt, füge GANZ AM ENDE einen kurzen Abschnitt hinzu mit:\n"
            "- einer Liste der häufigsten wiederholten Fehler\n"
            "- einem kurzen, konkreten Rat, wie der Schüler diese Fehler verbessern oder vermeiden kann\n\n"
            "Frühere Rückmeldungen (nur zur Analyse, NICHT zitieren oder wiederholen):\n"
            f"{previous_feedbacks_str}"
        )

        if user.user_group == "control":
            prompt = prompt_1
        else: 
            prompt = prompt_2

    finally:
        db.close()

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