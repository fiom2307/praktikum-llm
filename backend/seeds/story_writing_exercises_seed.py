from database import SessionLocal
from models.story_writing_exercise_model import StoryWritingExercise

def seed_story_writing_exercises():
    db = SessionLocal()

    exercises_by_city = {
        1: [  # Napoli
            {"text": ""},
        ],
        2: [  # Palermo
            {"text": ""},
        ],
        3: [  # Roma
            {"text": ""},
        ],
        4: [  # Siena
            {"text": ""},
        ],
        5: [  # Venezia
            {"text": ""},
        ],
        6: [  # Torino
            {"text": ""},
        ],
    }

    exercise_id = 1

    for city_id, exercises in exercises_by_city.items():
        for exercise_data in exercises:
            existing = db.query(StoryWritingExercise).filter(
                StoryWritingExercise.id == exercise_id
            ).first()

            data = {
                "id": exercise_id,
                "city_id": city_id,
                "text": exercise_data["text"],
            }

            if existing:
                for key, value in data.items():
                    setattr(existing, key, value)
            else:
                db.add(StoryWritingExercise(**data))

            exercise_id += 1

    db.commit()
    db.close()
