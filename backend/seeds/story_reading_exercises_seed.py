from database import SessionLocal
from models.story_reading_exercise_model import StoryReadingExercise

def seed_story_reading_exercises():
    db = SessionLocal()

    exercises_by_city = {
        1: [  # Napoli
            {"text": "", "questions": [], "answers": []},
            {"text": "", "questions": [], "answers": []},
        ],
        2: [  # Palermo
            {"text": "", "questions": [], "answers": []},
            {"text": "", "questions": [], "answers": []},
        ],
        3: [  # Roma
            {"text": "", "questions": [], "answers": []},
            {"text": "", "questions": [], "answers": []},
        ],
        4: [  # Siena
            {"text": "", "questions": [], "answers": []},
            {"text": "", "questions": [], "answers": []},
        ],
        5: [  # Venezia
            {"text": "", "questions": [], "answers": []},
            {"text": "", "questions": [], "answers": []},
        ],
        6: [  # Torino
            {"text": "", "questions": [], "answers": []},
            {"text": "", "questions": [], "answers": []},
        ],
    }

    exercise_id = 1

    for city_id, exercises in exercises_by_city.items():
        for exercise_data in exercises:
            existing = db.query(StoryReadingExercise).filter(
                StoryReadingExercise.id == exercise_id
            ).first()

            data = {
                "id": exercise_id,
                "city_id": city_id,
                "text": exercise_data["text"],
                "questions": exercise_data["questions"],
                "answers": exercise_data["answers"],
            }

            if existing:
                for key, value in data.items():
                    setattr(existing, key, value)
            else:
                db.add(StoryReadingExercise(**data))

            exercise_id += 1

    db.commit()
    db.close()
