from database import SessionLocal
from models.story_writing_exercise_model import StoryWritingExercise

def seed_story_writing_exercises():
    db = SessionLocal()

    exercises_by_city = {
        1: [  # Napoli
            {"text": "Scrivi 5-6 frasi in italiano in cui parli delle tue prime impressioni di Napoli e di Torino. Descrivi le tue emozioni ed immagini quando pensi alle due città."},
        ],
        2: [  # Palermo
            {"text": "Scrivi 5-6 frasi in italiano in cui parli di Napoli. Immagina: sei un/una residente di Napoli e parli delle tue emozioni, dell‘atmosfera e della tua identità. Non parli del turismo."},
        ],
        3: [  # Roma    
            {"text": "Scrivi 5-6 frasi in italiano in cui parli di un conflitto quotidiano a casa, in famiglia o con gli amici e quale è una tua soluzione."},
        ],
        4: [  # Siena
            {"text": "Scrivi 5-6 frasi in cui parli di un viaggio con degli amici in una città italiana. Usa anche tre delle seguenti espressioni. \n\n “penso che…“		“non so se…“		“ho dubbi se …“	“è importante che…““è possibile che…“		“credo che…“		“non sono sicuro/sicura se …“"},
        ],
        5: [  # Venezia
            {"text": "Scrivi 5-6 frasi in cui parli di un conflitto con un amico o con un‘amica. Quali sono o sono state possibili soluzioni? Usa minimo tre espressioni diverse per parlare delle vostre emozioni."},
        ],
        6: [  # Torino
            {"text": "Scrivi un‘e-mail di circa 90-110 parole ad un tuo amico/ una tua amica in Italia. Volete fare un viaggio insieme ma lui/lei vuole andare in una città italiana (quale?) dove tu non vuoi andare. Preferisci andare a Napoli! Parla della tua impressione di Napoli e di che cosa bisogna assolutamente vedere e fare a Napoli."},
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
