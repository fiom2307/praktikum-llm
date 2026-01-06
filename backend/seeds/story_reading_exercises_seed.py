from database import SessionLocal
from models.story_reading_exercise_model import StoryReadingExercise

def seed_story_reading_exercises():
    db = SessionLocal()

    exercises_by_city = {
        1: [  # Napoli
            {
                "text": "In classe gli studenti parlano di due città italiane: Napoli e Torino. Alcuni studenti collegano Napoli al mare, al sole e alla vita vivace nelle strade. Altri invece pensano al traffico e al rumore della città. Una studentessa racconta di esserci stata una volta: dice che il centro storico è affollato, ma le persone sono molto accoglienti. Di Torino gli studenti immaginano una città più ordinata e moderna, collegata all’industria e al lavoro. L’insegnante ricorda alla classe che ogni città può avere più di una faccia e che le prime impressioni non sempre raccontano tutta la realtà.",
                "questions": [
                    "Quali immagini positive sono associate a Napoli?",
                    "Quali aspetti negativi di Napoli vengono menzionati da alcuni studenti?",
                    "Che esperienza racconta una studentessa dopo aver visitato Napoli?",
                    "Come immaginano gli studenti la città di Torino?",
                    "Quale messaggio dà l’insegnante alla fine del testo?"
                ],
            }
        ],
        2: [  # Palermo
            {
                "text": "Per molti abitanti, Napoli non è solo una città. Nel centro storico le strade sono strette e piene di persone, i balconi sono colorati e la gente parla ad alta voce. Per qualcuno questo sembra caotico, ma per altri è un segno di energia e di vita. Alcuni giovani dicono che la città sia difficile, ma allo stesso tempo la sentono come una parte della propria identità. Per questo Napoli può apparire diversa a seconda di chi la guarda: un turista, uno studente o chi ci vive ogni giorno.",
                "questions": [
                    "Quali elementi della vita quotidiana a Napoli vengono descritti nel testo?",
                    "Perché alcune persone vedono la città come caotica?",
                    "Perché altre persone vedono gli stessi aspetti come qualcosa di positivo?",
                    "Che cosa dice il testo sul rapporto tra l’identità dei giovani e la città?",
                    "Perché Napoli può apparire diversa a persone diverse?"
                ],
            },
        ],

        3: [  # Roma
            {
                "text": "È sera in un appartamento nel centro di Napoli. Carlo sta studiando nella sua stanza, ma dal soggiorno si sente molta musica. Il padre entra e dice che in casa c’è troppo rumore. Alla porta della stanza c’è anche la sorellina di Carlo, che ascolta tutto con curiosità e ride perché vuole sapere cosa succede. Carlo è un po’ nervoso, ma alla fine tutti parlano insieme e trovano una soluzione per stare tranquilli.",
                "questions": [
                    "Dove si svolge la storia?",
                    "Che cosa sta facendo Carlo nella storia?",
                    "Perché il padre è infastidito?",
                    "Che cosa fa la sorellina di Carlo?",
                    "Come finisce la situazione?"
                ],
            }
        ],
        4: [  # Siena
            {
                "text": "Gli amici di Carlo stanno parlando del loro viaggio. Luca dice che pensa che Napoli sia una città molto viva, ma ha paura che ci sia troppo traffico nel centro. Tiziana spera che il tempo sia bello, perché vuole visitare la città a piedi. Marco non è sicuro che tutti possano partecipare, ma è contento che il gruppo sia motivato. Per loro il viaggio non è solo organizzazione: è anche emozione, speranza e un po’ di dubbio.",
                "questions": [
                    "Che cosa pensa Luca di Napoli?",
                    "Di che cosa ha paura Luca?",
                    "Che cosa spera Tiziana?",
                    "Di che cosa non è sicuro Marco?",
                    "Che cosa rende Marco positivo alla fine?"
                ],
            }
        ],
        5: [  # Venezia
            {
                "text": "Due amici parlano dopo una discussione. Giulia dice che è triste che Marco non capisca quanto per lei sia importante il viaggio. Marco pensa che sia meglio parlare con calma, ma ha l’impressione che Giulia sia ancora arrabbiata. Lei spera che lui prenda sul serio i suoi sentimenti, e lui desidera che il gruppo resti unito. Alla fine entrambi capiscono che non è facile trovare un accordo, ma sono contenti che ci sia ancora dialogo.",
                "questions": [
                    "Perché Giulia è triste?",
                    "Che cosa pensa Marco sia meglio fare?",
                    "Che impressione ha Marco di Giulia?",
                    "Che cosa spera Giulia?",
                    "Che cosa rende entrambi positivi alla fine?"
                ],
            }
        ],
        6: [  # Torino
            {
                "text": "Per molti studenti Napoli e Torino sono due città molto diverse. Napoli è vicina al mare, la vita nelle strade è più rumorosa e spontanea, e molte persone dicono che l’atmosfera sia calorosa. Torino invece è una città del nord, con grandi viali e molti edifici industriali. Alcuni pensano che sia più organizzata e silenziosa. Non significa che una città sia migliore dell’altra: ognuna ha la propria storia, e chi le visita impara a vedere le differenze.",
                "questions": [
                    "Che cosa rende Napoli diversa secondo il testo?",
                    "Come viene descritta l’atmosfera a Napoli?",
                    "Quali caratteristiche vengono menzionate per Torino?",
                    "Che cosa pensano alcune persone di Torino?",
                    "Qual è il messaggio finale del testo?"
                ],
            }
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
            }

            if existing:
                for key, value in data.items():
                    setattr(existing, key, value)
            else:
                db.add(StoryReadingExercise(**data))

            exercise_id += 1

    db.commit()
    db.close()
