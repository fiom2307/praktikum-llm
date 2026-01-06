# from services.city_service import get_city_by_key

# def get_city_reading_exercise_for_user(user_id: int, city_key: str):
#     city = get_city_by_key(city_key)

import random
from database import SessionLocal
from models.city_model import City
from models import StoryReadingExercise, StoryReadingHistory


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

        return {"reading_text": reading_text_md}

    finally:
        db.close()
