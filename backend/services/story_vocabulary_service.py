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

    # 1. All exercises for the city
    exercises = (
        db.query(StoryVocabularyExercise)
        .filter(StoryVocabularyExercise.city_id == city_id)
        .all()
    )

    if not exercises:
        return None

    exercise_ids = [e.id for e in exercises]

    # 2. Last attempt per exercise for this user
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

    # 3. Exercises NOT completed yet
    not_completed = [
        e for e in exercises
        if not history_map.get(e.id, {}).get("completed", False)
    ]

    if not_completed:
        chosen = random.choice(not_completed)
    else:
        # 4. Exercises completed but answered incorrectly
        incorrect = [
            e for e in exercises
            if history_map.get(e.id, {}).get("completed") is True
            and history_map.get(e.id, {}).get("correct") is False
        ]

        # All exercises completed and correct
        if not incorrect:
            return {
                "status": "done"
            }

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
    
        prompt = f"""
            You are an automatic feedback generator for a vocabulary recall item. 

CONTEXT 

The student saw hints and typed a target word. Do NOT show the correct answer. If the student is wrong, the same word will reappear in a later round. Feedback should help the next attempt without giving away the solution. 

INPUT 

- Hints / task shown to the student: {json.dumps(clues, ensure_ascii=False)}

- Target answer (FOR YOU ONLY, never reveal): {word}

- Student answer: {answer}

HARD RULES 

1) Output ONLY the four lines in the exact format below (same labels, same order, same blank line after "Tu respuesta: ..."). No extra text. 

2) "Tu respuesta" must reproduce the student's answer EXACTLY as given. 

3) "Valutazione" must be EXACTLY one of: corretto | parzialmente corretto | falso 

4) "Già corretto" and "Piccola miglioria" must be in German. 

5) Never reveal the target answer. Never print the correct word. Never spell it. Never give enough information that uniquely identifies the target (do NOT give letter sequences; do NOT combine multiple identifiers such as first letter + length + ending). 

6) Total output must be < 50 words (whitespace tokens). Keep "Già corretto" and "Piccola miglioria" short (preferably 1 sentence each). 

7) Never use technical terms in the output: do NOT output “INVALID” and do NOT output “WORD_COUNT”. 

8) The <Label> must be in German. 

INPUT RATING 

- corretto: matches target (ignore trivial case/whitespace). 

- parzialmente corretto: clearly close (minor spelling/inflection/diacritic) or partially aligned. 

- falso: not close, empty, or irrelevant 

SCORING (NON-NEGOTIABLE) 

- If the user's text is empty/in a different language /inappropriate ->Pizze guadagnate = 0. 
- For falso / parzialmente -> Pizze guadagnate = 0. 

- For corretto -> Pizze guadagnate = 1. 

CONTENT RULES FOR "Già corretto" (German) 

- Must be based on the student's input (not generic praise). 

- If corretto: confirm fully (e.g., "Tutto corretto."). 

- If parzialmente corretto: name ONE specific aspect that is already right without revealing the answer, such as: 

* correct direction/meaning implied by the hints 

* plausible word form or category (noun/verb/adjective) for the task 

* a part of the spelling seems consistent (beginning / stem / ending is close) WITHOUT quoting letters 

- If falso and nothing is defensible: be supportive but minimal (e.g., "Guter Versuch."). 

CONTENT RULES FOR "Piccola miglioria" (German) 

- Exactly ONE small, actionable cue for the next round, tailored to the student's input. 

- The cue should point to the biggest error type you infer, but must NOT disclose the solution. 

- Allowed cue types (choose ONE): 

* spelling focus: ending / vowels / double consonants / accent (general, no letters) 

* grammar focus: article/genus or inflection (only if relevant to the task) 

* strategy focus: re-check the hints and commit to one spelling 

- Do NOT combine multiple cues. Do NOT give the correct word, letters, or the full ending. 

OUTPUT FORMAT (MANDATORY)

{{"status":"<correct|almost|incorrect>","hint":"<Italian hint or empty>"}}

Example 1:
{{"status":"almost", "hint":"Attenzione all’ortografia: controlla le doppie consonanti."}}

Example 2 (incorrect guess):
{{"status":"incorrect","hint":""}}

Example 3 (almost guess):
{{"status":"almost", "hint":"Manca l’accento finale sulla parola."}}

Example 4 (correct guess):
Word: {word}
Student answer: {word}

Output: 
{{"status":"correct", "hint":""}}
"""


        raw_response = generate_from_prompt(prompt)
        clean_text = re.sub(r"```json|```", "", raw_response).strip()

        try:
            result = json.loads(clean_text)
        except json.JSONDecodeError:
            result = raw_response

        is_correct = result.get("status") == "correct"
        is_completed = is_correct or attempt >= 3
        
        print(is_correct)

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