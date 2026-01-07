# from services.city_service import get_city_by_key

# def get_city_reading_exercise_for_user(user_id: int, city_key: str):
#     city = get_city_by_key(city_key)

import random
from database import SessionLocal
from models.city_model import City
from models import StoryReadingExercise, StoryReadingHistory
from models import User
from services.openai_service import generate_from_prompt
from services.reading_service import extract_pizzas, extract_indexes, clean_llm_output

def save_reading_story_history(user_id, exercise_id, user_answer, llm_feedback, correct_question_indexes):
    db = SessionLocal()
    try:
        entry = StoryReadingHistory(
            user_id=user_id,
            exercise_id=exercise_id,
            user_answer=user_answer,
            llm_feedback=llm_feedback,
            correct_question_indexes=correct_question_indexes
        )
        db.add(entry)
        db.commit()
        db.refresh(entry)
        return entry
    finally:
        db.close()

def get_city_reading_text_for_user(user_id: int, city_key: str):
    db = SessionLocal()
    try:
        # 1️⃣ Resolver ciudad (city_key = name en minúsculas)
        city = (
            db.query(City)
            .filter(City.name.ilike(city_key))
            .first()
        )
        if not city:
            return {"reading_text": "❌ Città non valida."}

        # 2️⃣ Traer ejercicios de lectura de ESA ciudad
        exercises = (
            db.query(StoryReadingExercise)
            .filter(StoryReadingExercise.city_id == city.id)
            .all()
        )
        if not exercises:
            return {"reading_text": "❌ Nessun esercizio disponibile per questa città."}

        exercise_ids = [e.id for e in exercises]

        # 3️⃣ Traer historial del usuario para esos ejercicios
        histories = (
            db.query(StoryReadingHistory)
            .filter(
                StoryReadingHistory.user_id == user_id,
                StoryReadingHistory.exercise_id.in_(exercise_ids)
            )
            .all()
        )

        # 4️⃣ Unir preguntas correctas por ejercicio
        correct_by_exercise = {}
        for h in histories:
            correct_by_exercise.setdefault(h.exercise_id, set())
            if h.correct_question_indexes:
                correct_by_exercise[h.exercise_id].update(h.correct_question_indexes)

        # 5️⃣ Determinar ejercicios válidos y preguntas restantes
        ALL_QUESTIONS = {0, 1, 2, 3, 4}
        candidates = []

        for ex in exercises:
            correct = correct_by_exercise.get(ex.id, set())
            remaining = sorted(list(ALL_QUESTIONS - correct))

            if remaining:  # aún quedan preguntas
                candidates.append((ex, remaining))

        if not candidates:
            return {
                "reading_text": "🎉 **Hai completato tutti gli esercizi di lettura di questa città!**"
            }

        # 6️⃣ Elegir ejercicio random
        ex, remaining_indexes = random.choice(candidates)

        # 7️⃣ Construir MARKDOWN FINAL
        questions_md = "\n".join(
            [f"{i+1}. {ex.questions[i]}" for i in remaining_indexes]
        )

        reading_text_md = f"""

{ex.text}

---

{questions_md}
"""

        return {
            "exercise_id": ex.id, 
            "reading_text": reading_text_md
        }

    finally:
        db.close()
        
def correct_story_answers_ai(user_id: int, generated_text: str, user_text: str, exercise_id: int):
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
            "Wenn der Text des Nutzers leer ist, werden automatisch 0 Punkte vergeben."
            "Am Ende musst du mir die Nummern der Fragen zurückgeben, die korrekt waren, in dieser Form: \"Indexes: 1, 3, 5\" fängt mit 0 an"
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
            ""
            "Beantworte nur im oben beschriebenen Format, ohne zusätzliche Erklärungen, ohne Einleitung und ohne zusätzlichen Text.\n\n"
            "Nutze dafür den folgenden Ausgangstext:\n"
            f"{generated_text}\n\n"
            "Dies sind die Antworten des Schülers:\n"
            f"{user_text}\n\n"
            "Wenn der Text des Nutzers leer ist, werden automatisch 0 Punkte vergeben."
            "Am Ende musst du mir die Nummern der Fragen zurückgeben, die korrekt waren, in dieser Form: \"Indexes: 1, 3, 5\" fängt mit 0 an"
        )

        prompt = prompt_control if user.user_group == "control" else prompt_treatment

    finally:
        db.close()

    corrected = generate_from_prompt(prompt)
    pizzas = extract_pizzas(corrected)
    indexes = extract_indexes(corrected)
    corrected = clean_llm_output(corrected)

    save_reading_story_history(
        user_id=user_id,
        exercise_id=exercise_id,
        user_answer=user_text,
        llm_feedback=corrected,
        correct_question_indexes=indexes
    )

    return {"corrected_answers": corrected,"pizzas": pizzas}
