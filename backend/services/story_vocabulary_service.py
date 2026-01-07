import random
from sqlalchemy import desc

from services.city_service import get_city_by_key
from models import StoryVocabularyExercise, StoryVocabularyHistory
from database import SessionLocal


def generate_word_and_clues_for_story(user_id: int, city_key: str):
    db = SessionLocal()

    city = get_city_by_key(city_key)
    city_id = city.id

    # 1. Todos los ejercicios de la ciudad
    exercises = db.query(StoryVocabularyExercise)\
        .filter(StoryVocabularyExercise.city_id == city_id)\
        .all()

    if not exercises:
        return None

    exercise_ids = [e.id for e in exercises]

    # 2. Último intento por ejercicio del usuario
    subquery = (
        db.query(
            StoryVocabularyHistory.exercise_id,
            StoryVocabularyHistory.completed,
            StoryVocabularyHistory.correct
        )
        .filter(
            StoryVocabularyHistory.user_id == user_id,
            StoryVocabularyHistory.exercise_id.in_(exercise_ids)
        )
        .order_by(
            StoryVocabularyHistory.exercise_id,
            desc(StoryVocabularyHistory.created_at)
        )
        .distinct(StoryVocabularyHistory.exercise_id)
        .subquery()
    )

    history_map = {
        row.exercise_id: {
            "completed": row.completed,
            "correct": row.correct
        }
        for row in db.query(subquery).all()
    }

    # 3. Ejercicios NO completados
    not_completed = [
        e for e in exercises
        if not history_map.get(e.id, {}).get("completed", False)
    ]

    if not_completed:
        chosen = random.choice(not_completed)
    else:
        # 4. Ejercicios completados pero incorrectos
        incorrect = [
            e for e in exercises
            if history_map.get(e.id, {}).get("completed") is True
            and history_map.get(e.id, {}).get("correct") is False
        ]

        if not incorrect:
            return None  # o lanzar excepción

        chosen = random.choice(incorrect)

    return {
        "word": chosen.word,
        "clues": chosen.clues,
        "exercise_id": chosen.id
    }
