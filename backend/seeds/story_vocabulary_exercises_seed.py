from database import SessionLocal
from models.story_vocabulary_exercise_model import StoryVocabularyExercise

def seed_story_vocabulary_exercises():
    db = SessionLocal()

    exercises_by_city = {
    1: [# Napoli
        {"word": "la veduta", "clues": ["ciò che si può vedere da un punto alto", "panorama davanti agli occhi", "immagine di un paesaggio"]},
        {"word": "torinese", "clues": ["persona o cosa di Torino", "che viene da Torino", "legato alla città di Torino"]},
        {"word": "napoletano, -a", "clues": ["persona o cosa di Napoli", "che viene da Napoli", "tipico di Napoli"]},
        {"word": "il / la pizzaiolo, –a", "clues": ["persona che prepara la pizza", "lavora in pizzeria", "esperto di pizza"]},
        {"word": "settentrionale", "clues": ["che si trova a nord", "relativo al nord dell’Italia", "opposto di meridionale"]},
        {"word": "meridionale", "clues": ["che si trova a sud", "relativo al sud dell’Italia", "opposto di settentrionale"]},
        {"word": "caotico,-a", "clues": ["con molta confusione", "poco ordinato", "difficile da gestire"]},
        {"word": "industializzato, –a", "clues": ["con molte fabbriche", "sviluppato dal punto di vista industriale", "legato all’industria"]},
        {"word": "l‘automobile (f)", "clues": ["mezzo di trasporto", "veicolo con quattro ruote", "si usa per viaggiare su strada"]},
        {"word": "l‘impressione (f)", "clues": ["idea che nasce subito", "sensazione iniziale", "opinione personale"]}
        ],
    2: [
        {"word": "il/la residente", "clues": ["persona che vive stabilmente in un luogo", "abitante di una città o paese", "non turista"]},
        {"word": "il nord", "clues": ["parte alta della mappa", "zona settentrionale", "opposto di sud"]},
        {"word": "il sud", "clues": ["parte bassa della mappa", "zona meridionale", "opposto di nord"]},
        {"word": "quotidiano, –a", "clues": ["di tutti i giorni", "abituale", "legato alla routine"]},
        {"word": "l‘energia", "clues": ["forza per agire", "voglia di fare", "dinamismo"]},
        {"word": "per quanto riguarda", "clues": ["parlando di", "in relazione a", "a proposito di"]},
        {"word": "la speranza", "clues": ["pensiero positivo sul futuro", "attesa di qualcosa di buono", "desiderio che qualcosa accada"]},
        {"word": "l‘identità (f)", "clues": ["ciò che definisce una persona", "senso di sé", "caratteristiche personali"]},
        {"word": "l‘imbarazzo della scelta", "clues": ["avere troppe possibilità", "difficoltà nel decidere", "molte opzioni disponibili"]},
        {"word": "l‘appuntamento", "clues": ["incontro fissato", "momento stabilito per vedersi", "riunione programmata"]}
    ],
    3: [
        {"word": "il sentimento", "clues": ["emozione che si prova", "stato interiore", "sensazione profonda"]},
        {"word": "la melodia", "clues": ["insieme di suoni", "parte musicale di una canzone", "musica facile da ricordare"]},
        {"word": "indimenticabile", "clues": ["che non si può dimenticare", "molto speciale", "lascia un forte ricordo"]},
        {"word": "il chiacchierone/ l chiacchierona", "clues": ["persona che parla molto", "ama fare conversazione", "non sta mai in silenzio"]},
        {"word": "la paura", "clues": ["sensazione di timore", "emozione negativa", "reazione a un pericolo"]},
        {"word": "lasciare in pace", "clues": ["non disturbare", "non dare fastidio", "lasciare tranquillo"]},
        {"word": "augurarsi", "clues": ["desiderare qualcosa", "sperare che accada", "fare un desiderio"]},
        {"word": "interrompere", "clues": ["fermarsi mentre qualcuno parla", "tagliare una conversazione", "non lasciare finire"]},
        {"word": "la conversazione", "clues": ["dialogo tra persone", "scambio di parole", "parlare insieme"]},
        {"word": "andare (bene) d‘accordo", "clues": ["avere un buon rapporto", "non litigare", "stare bene insieme"]}
    ],
    4: [
        {"word": "l‘opinione", "clues": ["idea personale", "ciò che si pensa di qualcosa", "punto di vista"]},
        {"word": "vivo,-a", "clues": ["che ha vita", "non morto", "pieno di energia"]},
        {"word": "il dubbio", "clues": ["incertezza", "non essere sicuri", "domanda nella mente"]},
        {"word": "sperare", "clues": ["desiderare qualcosa di buono", "pensare positivamente al futuro", "augurarsi"]},
        {"word": "necessario,-a", "clues": ["indispensabile", "che serve per forza", "non si può evitare"]},
        {"word": "possibile", "clues": ["che può accadere", "realizzabile", "non impossibile"]},
        {"word": "impossibile", "clues": ["che non può accadere", "non realizzabile", "molto difficile"]},
        {"word": "pensare", "clues": ["usare la mente", "avere un’idea", "riflettere su qualcosa"]},
        {"word": "credere", "clues": ["pensare che qualcosa sia vero", "avere fiducia", "non dubitare"]},
        {"word": "contento,-a", "clues": ["felice", "soddisfatto", "di buon umore"]}
    ],
    5: [
        {"word": "Il disordine", "clues": ["mancanza di ordine", "confusione", "situazione poco organizzata"]},
        {"word": "la manifestazione", "clues": ["evento pubblico", "incontro con molte persone", "azione collettiva in strada"]},
        {"word": "all‘aperto", "clues": ["fuori dagli edifici", "non al chiuso", "in uno spazio esterno"]},
        {"word": "aver(e) luogo", "clues": ["succedere", "svolgersi in un posto", "accadere in un momento preciso"]},
        {"word": "spettacolare", "clues": ["molto impressionante", "che colpisce gli occhi", "bello da vedere"]},
        {"word": "il portafortuna", "clues": ["oggetto che porta fortuna", "si tiene per avere buona sorte", "simbolo di fortuna"]},
        {"word": "la sfortuna", "clues": ["mancanza di fortuna", "evento negativo", "brutta sorte"]},
        {"word": "parlare con calma", "clues": ["parlare tranquillamente", "senza arrabbiarsi", "con tono sereno"]},
        {"word": "prendere sul serio", "clues": ["considerare importante", "non scherzare", "dare valore a qualcosa"]},
        {"word": "restare uniti", "clues": ["stare insieme", "non separarsi", "aiutarsi a vicenda"]}
    ],
    6: [
        {"word": "rumoroso,-a", "clues": ["con molto rumore", "non silenzioso", "pieno di suoni forti"]},
        {"word": "il patrono/ la patrona", "clues": ["santo protettore di una città", "figura che protegge", "persona importante per una comunità"]},
        {"word": "Il sangue", "clues": ["liquido rosso nel corpo", "scorre nelle vene", "importante per la vita"]},
        {"word": "sciogliersi", "clues": ["diventare liquido", "non essere più solido", "perdere la forma"]},
        {"word": "la maschera", "clues": ["oggetto per coprire il viso", "si usa a carnevale", "serve per nascondersi"]},
        {"word": "Il cappuccio", "clues": ["parte del giubbotto", "copre la testa", "protezione contro freddo o pioggia"]},
        {"word": "nascondere", "clues": ["mettere fuori dalla vista", "non far vedere", "tenere segreto"]},
        {"word": "Il viso", "clues": ["parte della testa", "dove ci sono occhi e bocca", "mostra le emozioni"]},
        {"word": "Innamorato, –a", "clues": ["pieno d’amore", "che ama qualcuno", "con forti sentimenti"]},
        {"word": "spontaneo", "clues": ["senza preparazione", "naturale", "non pianificato"]}
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