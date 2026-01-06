from database import SessionLocal
from models.story_vocabulary_exercise_model import StoryVocabularyExercise

def seed_story_vocabulary_exercises():
    db = SessionLocal()

    exercises_by_city = {
        1: [  # Napoli
            {"word": "impressione", "clues": ["impression"]},
            {"word": "caotico", "clues": ["chaotic"]},
            {"word": "vivace", "clues": ["lively"]},
            {"word": "accogliente", "clues": ["welcoming"]},
            {"word": "centro storico", "clues": ["historic centre"]},
            {"word": "esperienza", "clues": ["experience"]},
            {"word": "ordinato", "clues": ["orderly"]},
            {"word": "moderno", "clues": ["modern"]},
            {"word": "industria", "clues": ["industry"]},
            {"word": "confronto", "clues": ["comparison"]},
        ],
        2: [
            {"word": "identità", "clues": ["identity"]},
            {"word": "ricordo", "clues": ["memory"]},
            {"word": "speranza", "clues": ["hope"]},
            {"word": "orgoglio", "clues": ["pride"]},
            {"word": "difficoltà", "clues": ["difficulty"]},
            {"word": "energia", "clues": ["energy", "liveliness"]},
            {"word": "quotidiano", "clues": ["everyday life"]},
            {"word": "abitante", "clues": ["inhabitant"]},
            {"word": "emozione", "clues": ["emotion"]},
            {"word": "appartenenza", "clues": ["sense of belonging"]},
        ],
        3: [
            {"word": "rumore", "clues": ["noise"]},
            {"word": "concentrazione", "clues": ["concentration"]},
            {"word": "progetto", "clues": ["project"]},
            {"word": "curiosità", "clues": ["curiosity"]},
            {"word": "discutere", "clues": ["to discuss"]},
            {"word": "equilibrio", "clues": ["balance"]},
            {"word": "vita quotidiana", "clues": ["daily life"]},
            {"word": "ascoltare di nascosto", "clues": ["to eavesdrop"]},
            {"word": "calmarsi", "clues": ["to calm down"]},
            {"word": "accordo", "clues": ["agreement"]},
        ],
        4: [
            {"word": "opinione", "clues": ["opinion"]},
            {"word": "emozione", "clues": ["emotion"]},
            {"word": "dubbio", "clues": ["doubt"]},
            {"word": "impressione", "clues": ["impression"]},
            {"word": "orgoglio", "clues": ["pride"]},
            {"word": "paura", "clues": ["fear"]},
            {"word": "necessario che", "clues": ["it is necessary that"]},
            {"word": "importante che", "clues": ["it is important that"]},
            {"word": "rimanere", "clues": ["to remain", "to stay"]},
            {"word": "desiderio", "clues": ["desire"]},
        ],
        5: [
            {"word": "triste", "clues": ["sad"]},
            {"word": "capire", "clues": ["to understand"]},
            {"word": "parlare con calma", "clues": ["to talk calmly"]},
            {"word": "essere arrabbiato/a", "clues": ["to be angry"]},
            {"word": "avere l’impressione che", "clues": ["to have the impression that"]},
            {"word": "prendere sul serio", "clues": ["to take seriously"]},
            {"word": "sentimento", "clues": ["feeling"]},
            {"word": "restare uniti", "clues": ["to stay united"]},
            {"word": "trovare un accordo", "clues": ["to find an agreement"]},
            {"word": "dialogo", "clues": ["dialogue", "communication"]},
        ],
        6: [
            {"word": "mare", "clues": ["sea"]},
            {"word": "atmosfera calorosa", "clues": ["warm atmosphere"]},
            {"word": "spontaneo", "clues": ["spontaneous"]},
            {"word": "rumoroso", "clues": ["noisy"]},
            {"word": "viale", "clues": ["boulevard", "wide street"]},
            {"word": "edificio industriale", "clues": ["industrial building"]},
            {"word": "organizzato", "clues": ["organized"]},
            {"word": "silenzioso", "clues": ["quiet"]},
            {"word": "differenza", "clues": ["difference"]},
            {"word": "storia", "clues": ["history", "background"]},
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