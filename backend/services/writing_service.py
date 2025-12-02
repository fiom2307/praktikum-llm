from services.gemini_service import generate_from_prompt
from database import SessionLocal
from models import WritingHistory

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
        f"Korrigieren sie den text auf grammatik und still: {user_text}"
        "\nDanach gib eine kurze Erklärung AUF DEUTSCH (nur Erklärung, nichts mehr)."
        "Am Ende gib einen kurzen, positiven Kommentar AUF DEUTSCH zur Motivation des Schülers."
        "Wiederhole den user Text NICHT noch einmal."
        "\nGib am Ende einen positiven Kommentar, der den Schüler motiviert, egal ob er gut oder schlecht abschneidet."
    )

    corrected = generate_from_prompt(prompt)

    save_writing_history(
        user_id=user_id,
        user_answer=user_text,
        llm_feedback=corrected
    )

    return {"corrected_text": corrected}
