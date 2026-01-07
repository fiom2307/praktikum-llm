from database import SessionLocal
from models.story_writing_exercise_model import StoryWritingExercise

def seed_story_writing_exercises():
    db = SessionLocal()

    exercises_by_city = {
        1: [  # Napoli
            {"text": "Scrivi 5–6 frasi in italiano. Confronta le tue prime impressioni di Napoli e Torino. Non valutare: descrivi sensazioni, immagini e associazioni."},
        ],
        2: [  # Palermo
            {"text": "Scrivi 5–6 frasi in italiano. Descrivi Napoli dal punto di vista di una persona che ci vive. Concentrati su emozioni, atmosfera e identità, non sul turismo."},
        ],
        3: [  # Roma    
            {"text": "Scrivi 5–6 frasi in italiano. Descrivi un piccolo conflitto quotidiano a casa o in classe. Concentrati su emozioni, reazioni e su come la situazione si risolve."},
        ],
        4: [  # Siena
            {"text": "Scrivi 4–5 frasi in italiano. Esprimi i tuoi sentimenti o le tue opinioni su una città o un luogo. Usa almeno due delle seguenti strutture: “penso che…”, “credo che…”, “ho paura che…”, “è importante che…”."},
        ],
        5: [  # Venezia
            {"text": "Scrivi 5–6 frasi in italiano su un conflitto con un amico e su come cerchi di risolverlo. Usa almeno due espressioni di opinione o di emozione."},
        ],
        6: [  # Torino
            {"text": "Scrivi una breve email (70–90 parole) in cui confronti due città. Usa almeno due espressioni di contrasto."},
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
