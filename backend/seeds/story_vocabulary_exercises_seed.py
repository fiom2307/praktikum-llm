from database import SessionLocal
from models.story_vocabulary_exercise_model import StoryVocabularyExercise

def seed_story_vocabulary_exercises():
    db = SessionLocal()

    exercises_by_city = {
        1: [  # Napoli
            {"word": "", "clues": []},
            {"word": "", "clues": []},
            {"word": "", "clues": []},
            {"word": "", "clues": []},
            {"word": "", "clues": []},
            {"word": "", "clues": []},
            {"word": "", "clues": []},
            {"word": "", "clues": []},
            {"word": "", "clues": []},
            {"word": "", "clues": []},
        ],
        2: [  # Palermo
            {"word": "", "clues": []},
            {"word": "", "clues": []},
            {"word": "", "clues": []},
            {"word": "", "clues": []},
            {"word": "", "clues": []},
            {"word": "", "clues": []},
            {"word": "", "clues": []},
            {"word": "", "clues": []},
            {"word": "", "clues": []},
            {"word": "", "clues": []},
        ],
        3: [  # Roma
            {"word": "", "clues": []},
            {"word": "", "clues": []},
            {"word": "", "clues": []},
            {"word": "", "clues": []},
            {"word": "", "clues": []},
            {"word": "", "clues": []},
            {"word": "", "clues": []},
            {"word": "", "clues": []},
            {"word": "", "clues": []},
            {"word": "", "clues": []},
        ],
        4: [  # Siena
            {"word": "", "clues": []},
            {"word": "", "clues": []},
            {"word": "", "clues": []},
            {"word": "", "clues": []},
            {"word": "", "clues": []},
            {"word": "", "clues": []},
            {"word": "", "clues": []},
            {"word": "", "clues": []},
            {"word": "", "clues": []},
            {"word": "", "clues": []},
        ],
        5: [  # Venezia
            {"word": "", "clues": []},
            {"word": "", "clues": []},
            {"word": "", "clues": []},
            {"word": "", "clues": []},
            {"word": "", "clues": []},
            {"word": "", "clues": []},
            {"word": "", "clues": []},
            {"word": "", "clues": []},
            {"word": "", "clues": []},
            {"word": "", "clues": []},
        ],
        6: [  # Torino
            {"word": "", "clues": []},
            {"word": "", "clues": []},
            {"word": "", "clues": []},
            {"word": "", "clues": []},
            {"word": "", "clues": []},
            {"word": "", "clues": []},
            {"word": "", "clues": []},
            {"word": "", "clues": []},
            {"word": "", "clues": []},
            {"word": "", "clues": []},
        ],
    }

    exercise_id = 1

    for city_id, exercises in exercises_by_city.items():
        for exercise_data in exercises:
            existing = db.query(StoryVocabularyExercise).filter(
                StoryVocabularyExercise.id == exercise_id
            ).first()

            data = {
                "id": exercise_id,
                "city_id": city_id,
                "word": exercise_data["word"],
                "clues": exercise_data["clues"],
            }

            if existing:
                for key, value in data.items():
                    setattr(existing, key, value)
            else:
                db.add(StoryVocabularyExercise(**data))

            exercise_id += 1

    db.commit()
    db.close()