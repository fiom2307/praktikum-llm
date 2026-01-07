import random
from sqlalchemy import desc
from sqlalchemy.orm import Session
import re
import json
from services.openai_service import generate_from_prompt
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


def get_last_vocabulary_entry_from_city(user_id: int, city_key: str):
    db = SessionLocal()
    try:
        city = get_city_by_key(city_key)
        if not city:
            return None

        entry = (
            db.query(StoryVocabularyHistory)
            .join(
                StoryVocabularyExercise,
                StoryVocabularyHistory.exercise_id == StoryVocabularyExercise.id
            )
            .filter(
                StoryVocabularyHistory.user_id == user_id,
                StoryVocabularyExercise.city_id == city.id
            )
            .order_by(StoryVocabularyHistory.created_at.desc())
            .first()
        )

        return entry
    finally:
        db.close()


def story_vocabulary_history_to_dict(entry):
    db = SessionLocal()
    try:
        exercise = (
            db.query(StoryVocabularyExercise)
            .filter(StoryVocabularyExercise.id == entry.exercise_id)
            .first()
        )

        return {
            "id": entry.id,
            "user_id": entry.user_id,
            "exercise_id": entry.exercise_id,
            "word": exercise.word if exercise else None,
            "clues": exercise.clues if exercise else [],
            "user_answer": entry.user_answer,
            "attempt_number": entry.attempt_number,
            "completed": entry.completed,
            "correct": entry.correct,
            "created_at": entry.created_at.isoformat() if entry.created_at else None,
        }
    finally:
        db.close()

def check_word_with_ai_in_story(userId: int, exercise_id: str, answer: str, attempt: int):
    db = SessionLocal()

    try:
        exercise = (
            db.query(StoryVocabularyExercise)
            .filter(StoryVocabularyExercise.id == exercise_id)
            .first()
        )

        if not exercise:
            return {"status": "error", "hint": "Exercise not found"}

        word = exercise.word
        clues = exercise.clues
    
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

        try:
            result = json.loads(clean_text)
        except json.JSONDecodeError:
            result = raw_response

        is_correct = result.get("status") == "correct"
        is_completed = is_correct or attempt >= 3

        save_story_vocabulary_history(
            user_id=userId,
            exercise_id=exercise_id,
            answer=answer,
            attempt=attempt,
            completed=is_completed,
            correct=is_correct,
            db=db
        )
        return result
    
    finally:
        db.close()

def save_story_vocabulary_history(
    user_id: int,
    exercise_id: int,
    answer: str,
    attempt: int,
    completed: bool,
    correct: bool, 
    db: Session
):
    entry = StoryVocabularyHistory(
        user_id=user_id,
        exercise_id=exercise_id,
        user_answer=answer,
        attempt_number=attempt,
        completed=completed,
        correct=correct,
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)

    return entry