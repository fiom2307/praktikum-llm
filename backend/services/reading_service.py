from services.gemini_service import generate_from_prompt
from database import SessionLocal
from models import FreeReadingHistory
import re
from models import User
from typing import List

def save_reading_history(user_id, llm_question, user_answer, llm_feedback):
    db = SessionLocal()
    try:
        entry = FreeReadingHistory(
            user_id=user_id,
            llm_question=llm_question,
            user_answer=user_answer,
            llm_feedback=llm_feedback
        )
        db.add(entry)
        db.commit()
        db.refresh(entry)
        return entry
    finally:
        db.close()

def correct_answers_ai(user_id: int, generated_text: str, user_text: str):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return {"corrected_answers": "", "pizzas": 0}

        prompt_control = (
            "Vergleiche diese Antworten mit den zuvor erstellten Fragen zum Text und markiere, welche richtig sind. "
            "Gib NUR folgendes Format aus und halte dich strikt daran:\n\n"
            "**Frage 1:** richtige Antwort\n"
            "--------------------\n"
            "**Erklärung:** Korrektur der Schülerantwort\n\n"
            "**Richtige Antwort:** Antwort der Frage\n"
            "**Frage 2:** richtige Antwort\n"
            "--------------------\n"
            "**Erklärung:** Korrektur der Schülerantwort\n\n"
            "**Richtige Antwort:** Antwort der Frage\n"
            "(… und so weiter für alle Fragen …)\n\n"
            "Am Ende gib:\n"
            "- Einen kurzen, motivierenden Kommentar für den Schüler, egal ob er gut oder schlecht abgeschnitten hat.\n"
            "- Eine Punktzahl von 0 bis 5 im Format: Pizzas X\n\n"
            "Beantworte nur im oben beschriebenen Format, ohne zusätzliche Erklärungen, ohne Einleitung und ohne zusätzlichen Text.\n\n"
            "Nutze dafür den folgenden Ausgangstext:\n"
            f"{generated_text}\n\n"
            "Dies sind die Antworten des Schülers:\n"
            f"{user_text}\n\n"
            "Se lo studente dice qualcosa di inappropriato o di scortese, assegnagli un punteggio di -5 e non rispondere."
        )

        prompt_treatment = (
            "Vergleiche diese Antworten mit den zuvor erstellten Fragen zum Text und markiere, welche richtig sind. "
            "Gib NUR folgendes Format aus und halte dich strikt daran:\n\n"
            "**Frage 1:** richtige Antwort\n"
            "--------------------\n"
            "**Erklärung:** Korrektur der Schülerantwort\n\n"
            "**Richtige Antwort:** Antwort der Frage\n"
            "**Frage 2:** richtige Antwort\n"
            "--------------------\n"
            "**Erklärung:** Korrektur der Schülerantwort\n\n"
            "**Richtige Antwort:** Antwort der Frage\n"
            "(… und so weiter für alle Fragen …)\n\n"
            "Am Ende gib:\n"
            "- Einen kurzen, motivierenden Kommentar für den Schüler, egal ob er gut oder schlecht abgeschnitten hat.\n"
            "- Eine Punktzahl von 0 bis 5 im Format: Pizzas X\n\n"
            "Beantworte nur im oben beschriebenen Format, ohne zusätzliche Erklärungen, ohne Einleitung und ohne zusätzlichen Text.\n\n"
            "Nutze dafür den folgenden Ausgangstext:\n"
            f"{generated_text}\n\n"
            "Dies sind die Antworten des Schülers:\n"
            f"{user_text}\n\n"
            "Se lo studente dice qualcosa di inappropriato o di scortese, assegnagli un punteggio di -5 e non rispondere."
        )

        prompt = prompt_control if user.user_group == "control" else prompt_treatment

    finally:
        db.close()

    corrected = generate_from_prompt(prompt)
    pizzas = extract_pizzas(corrected)
    corrected = clean_llm_output(corrected)

    save_reading_history(
        user_id=user_id,
        llm_question=generated_text,
        user_answer=user_text,
        llm_feedback=corrected
    )

    return {"corrected_answers": corrected,"pizzas": pizzas}

def extract_pizzas(text: str) -> int:
    match = re.search(r"Pizzas\s+(-?\d+)", text)
    if match:
        return int(match.group(1))
    return 0

def extract_indexes(text: str) -> List[int]:
    match = re.search(r"Indexes\s*:\s*\[?([0-9,\s-]+)\]?", text)
    if not match:
        return []

    raw_indexes = match.group(1)
    return [int(i.strip()) for i in raw_indexes.split(",") if i.strip()]

def clean_llm_output(text: str) -> str:
    return re.sub(
        r"(Pizzas\s+-?\d+|Indexes\s*:?\s*\[?[0-9,\s-]+\]?)",
        "",
        text,
        flags=re.IGNORECASE
    ).strip()


def generate_reading_text_from_ai(user_id: int):
    db = SessionLocal()
    try:
        histories = (
            db.query(FreeReadingHistory)
            .filter(FreeReadingHistory.user_id == user_id)
            .order_by(FreeReadingHistory.created_at.desc())
            .limit(5)
            .all()
        )

        previous_texts = [h.llm_question for h in histories if h.llm_question]

        previous_texts_str = "\n\n---\n\n".join(previous_texts)

    finally:
        db.close()
    
    prompt = (
        "Schreibe einen kurzen Text im Italienisch von etwa 150 Wörtern über eines der folgenden Themen, whälen sie den Thema random aus: "
        "Ferien, Schule und Freizeit, Identität und Zukunftspläne, kulturelle Unterschiede zwischen "
        "Nord- und Süditalien, Liebe und Freundschaft, italienische Feste und Jugendkultur, Lesen und "
        "Literatur oder italienische Feiertage und Traditionen. "
        "Erstelle danach fünf Fragen zu deinem Text. Schreibe einfach den Text auf Italienisch die Fragen auch, ohne zu "
        "sagen, über welche Themen er handelt, und ohne jegliche zusätzliche Interaktion. Beachte, dass das Italienisch-Niveau A2 sein muss."
        "WICHTIG:\n"
        "- Der neue Text darf thematisch und inhaltlich NICHT sehr ähnlich zu den folgenden vorherigen Texten sein.\n"
        "- Vermeide gleiche Feste, gleiche Beispiele oder sehr ähnliche Fragestellungen.\n\n"
        "Vorherige Texte (nur zur Orientierung, NICHT wiederverwenden):\n"
        f"{previous_texts_str}\n\n"
    )
    
    text = generate_from_prompt(prompt)
    return {
        "exercise_id": 0,
        "reading_text": text
    }