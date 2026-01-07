from database import SessionLocal
from models.story_vocabulary_exercise_model import StoryVocabularyExercise

def seed_story_vocabulary_exercises():
    db = SessionLocal()

    exercises_by_city = {
    1: [  # Napoli
        {"word": "impressione", "clues": ["sensazione iniziale", "idea che nasce subito", "percezione personale"]},
        {"word": "caotico", "clues": ["poco ordinato", "con molta confusione", "difficile da gestire"]},
        {"word": "vivace", "clues": ["pieno di energia", "con molta attività", "mai tranquillo"]},
        {"word": "accogliente", "clues": ["fa sentire a proprio agio", "amichevole con gli altri", "trasmette calore umano"]},
        {"word": "centro storico", "clues": ["parte antica della città", "zona con edifici storici", "luogo ricco di tradizione"]},
        {"word": "esperienza", "clues": ["qualcosa che si vive", "evento personale", "situazione che lascia un ricordo"]},
        {"word": "ordinato", "clues": ["ben organizzato", "senza confusione", "con regole chiare"]},
        {"word": "moderno", "clues": ["legato al presente", "con idee nuove", "non tradizionale"]},
        {"word": "industria", "clues": ["settore del lavoro", "produzione di beni", "attività economica"]},
        {"word": "confronto", "clues": ["paragone tra due cose", "analisi delle differenze", "mettere a confronto"]},
    ],
    2: [
        {"word": "identità", "clues": ["ciò che definisce una persona", "senso di sé", "parte profonda dell’individuo"]},
        {"word": "ricordo", "clues": ["immagine del passato", "memoria personale", "pensiero legato a un evento"]},
        {"word": "speranza", "clues": ["pensiero positivo sul futuro", "attesa di qualcosa di buono", "desiderio che qualcosa accada"]},
        {"word": "orgoglio", "clues": ["sentirsi fieri", "stima di sé", "valore personale"]},
        {"word": "difficoltà", "clues": ["problema da affrontare", "situazione complicata", "ostacolo"]},
        {"word": "energia", "clues": ["forza interiore", "voglia di fare", "dinamismo"]},
        {"word": "quotidiano", "clues": ["di tutti i giorni", "abituale", "legato alla routine"]},
        {"word": "abitante", "clues": ["persona che vive in un luogo", "residente", "non turista"]},
        {"word": "emozione", "clues": ["sentimento intenso", "reazione interiore", "stato dell’animo"]},
        {"word": "appartenenza", "clues": ["sentirsi parte di qualcosa", "legame con un gruppo", "connessione profonda"]},
    ],
    3: [
        {"word": "rumore", "clues": ["suono forte", "disturbo acustico", "assenza di silenzio"]},
        {"word": "concentrazione", "clues": ["attenzione totale", "focus mentale", "pensare senza distrazioni"]},
        {"word": "progetto", "clues": ["idea da realizzare", "attività pianificata", "lavoro con un obiettivo"]},
        {"word": "curiosità", "clues": ["voglia di sapere", "interesse per il nuovo", "desiderio di scoprire"]},
        {"word": "discutere", "clues": ["parlare di un problema", "scambiare opinioni", "confrontarsi verbalmente"]},
        {"word": "equilibrio", "clues": ["situazione stabile", "assenza di eccessi", "armonia"]},
        {"word": "vita quotidiana", "clues": ["attività di ogni giorno", "routine personale", "vita normale"]},
        {"word": "ascoltare di nascosto", "clues": ["sentire senza farsi notare", "osservare in silenzio", "non partecipare apertamente"]},
        {"word": "calmarsi", "clues": ["tornare tranquilli", "ridurre la tensione", "rilassarsi"]},
        {"word": "accordo", "clues": ["decisione comune", "intesa finale", "soluzione condivisa"]},
    ],
    4: [
        {"word": "opinione", "clues": ["idea personale", "punto di vista", "ciò che si pensa"]},
        {"word": "emozione", "clues": ["reazione emotiva", "sentimento interno", "stato interiore"]},
        {"word": "dubbio", "clues": ["incertezza", "non essere sicuri", "domanda senza risposta"]},
        {"word": "impressione", "clues": ["sensazione immediata", "idea iniziale", "percezione personale"]},
        {"word": "orgoglio", "clues": ["sentirsi fieri", "valore di sé", "soddisfazione personale"]},
        {"word": "paura", "clues": ["sentimento di timore", "emozione negativa", "ansia"]},
        {"word": "necessario che", "clues": ["indica obbligo", "non opzionale", "condizione importante"]},
        {"word": "importante che", "clues": ["esprime valore", "sottolinea priorità", "indica rilevanza"]},
        {"word": "rimanere", "clues": ["non andare via", "continuare a essere", "restare nello stesso luogo"]},
        {"word": "desiderio", "clues": ["volontà profonda", "sogno personale", "ciò che si vuole"]},
    ],
    5: [
        {"word": "triste", "clues": ["con poca gioia", "stato emotivo negativo", "sentirsi giù"]},
        {"word": "capire", "clues": ["comprendere un’idea", "afferrare il senso", "rendere chiaro"]},
        {"word": "parlare con calma", "clues": ["senza litigare", "con tono tranquillo", "in modo pacato"]},
        {"word": "essere arrabbiato/a", "clues": ["provare rabbia", "non essere sereni", "reagire male"]},
        {"word": "avere l’impressione che", "clues": ["pensare che", "sentire interiormente", "credere senza certezza"]},
        {"word": "prendere sul serio", "clues": ["dare importanza", "non sottovalutare", "considerare attentamente"]},
        {"word": "sentimento", "clues": ["emozione interna", "stato del cuore", "reazione emotiva"]},
        {"word": "restare uniti", "clues": ["non dividersi", "mantenere il gruppo", "stare insieme"]},
        {"word": "trovare un accordo", "clues": ["raggiungere una soluzione", "decidere insieme", "risolvere un conflitto"]},
        {"word": "dialogo", "clues": ["comunicazione aperta", "scambio di parole", "parlare per capirsi"]},
    ],
    6: [
        {"word": "mare", "clues": ["acqua salata", "vicino alla costa", "luogo di spiagge"]},
        {"word": "atmosfera calorosa", "clues": ["ambiente umano", "sensazione di accoglienza", "clima emotivo positivo"]},
        {"word": "spontaneo", "clues": ["naturale", "non forzato", "senza pianificazione"]},
        {"word": "rumoroso", "clues": ["con molti suoni", "poco silenzioso", "pieno di rumori"]},
        {"word": "viale", "clues": ["strada larga", "spesso con alberi", "via principale"]},
        {"word": "edificio industriale", "clues": ["costruzione per il lavoro", "non residenziale", "legato alla produzione"]},
        {"word": "organizzato", "clues": ["ben strutturato", "con ordine", "gestito con metodo"]},
        {"word": "silenzioso", "clues": ["con poco rumore", "tranquillo", "calmo"]},
        {"word": "differenza", "clues": ["ciò che non è uguale", "contrasto", "variazione"]},
        {"word": "storia", "clues": ["passato di un luogo", "eventi precedenti", "contesto storico"]},
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