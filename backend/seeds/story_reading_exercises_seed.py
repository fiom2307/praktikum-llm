from database import SessionLocal
from models.story_reading_exercise_model import StoryReadingExercise

def seed_story_reading_exercises():
    db = SessionLocal()

    exercises_by_city = {
        1: [  # Napoli
            {
                "text": "Si presentano due città italiane di cui non si è ancora parlato in classe: Napoli e Torino. Le foto delle città fanno vedere che sia Napoli sia Torino sono belle città grandi in due ambienti molto diversi. Vicino a Torino troviamo le Alpi mentre la veduta su di Napoli con il Vesuvio fa vedere anche il mare. Nelle foto si vedono alcune specialità famosi in tutto il mondo, cioè i grissini torinesi e la pizza napoletana. Vediamo anche un pizzaiolo in azione. Torino è una città settentrionale e il traffico nelle larghe vie nel centro è molto meno caotico di quello meridionale nelle strette vie nel centro storico di Napoli. Tutti e due le città sono industrializzate e un prodotto tipico di Torino e di Napoli sono le automobili: vicino a Torino troviamo la FIAT e vicino a Napoli l‘Alfa Romeo. L’insegnante ricorda alla classe che ogni città può avere più di una faccia e che le prime impressioni non sempre raccontano tutta la realtà",
                "questions": [
                    "In quanto sono diversi gli ambienti in cui si trovano Torino e Napoli?",
                    "Che cosa sono i grissini?",
                    "Quale mestiere devi imparare se vuoi produrre la famosa specialità di Napoli?",
                    "Tutte e due le città sono industrializzate ed hanno un prodotto in comune ma di due marche diverse. Quale?",
                    "Come si chiamano le due marche che vediamo tutti i giorni per strada?"
                ],
            }
        ],
        2: [  # Palermo
            {
                "text": "Per molti abitanti, Napoli non è solo una città ma un modo di vivere. Nel centro storico le strade sono strette e spesso piene di persone. Tra balconi colorati i residenti parlano ad alta voce e ad alcuni (soprattutto a turisti del nord) questo mix di voci, rumori di motori e musica sembra caotico, ma per altri fa parte della vita quotidiana del sud ed è segno di energia.Alcuni giovani dicono che la città sia difficile per quanto riguarda per esempio la cerca di una casa o di un lavoro, ma allo stesso tempo non pererebbero mai la speranza nella loro città e la sentono come una parte della propria identità. Per questo Napoli presenta tante facce diverse a seconda di chi la guarda: una o un turista che ha l‘imbarazzo della scelta di cosa andare a vedere prima, una studentessa o uno studente in cerca del posto ideale per un appuntamento con degli amici nuovi o chi ci vive ogni giorno.",
                "questions": [
                    "Di quali elementi tipici nel centro storico di Napoli si parla nel testo? ",
                    "Quale impressione hanno alcuni  turisti (soprattutto quelli del nord) del centro storico?",
                    "Quale sarebbe invece una interpretazione più positiva di questo mix di rumori?",
                    "Che cosa dice il testo dei giovani napoletani?",
                    "Da che cosa dipende come parli di questa città?"
                ],
            },
        ],

        3: [  # Roma
            {
                "text": "È sera e Carlo sta ascoltando la sua musica preferita nella sua stanza con Tiziana, una sua amica. Secondo Carlo la musica di Rocco Hunt esprime sempre i sentimenti giusti. Trova le melodie ed i testi indimenticabili anche se non sono sempre facili da capire perché canta in napoletano. Infatti Tiziana non capisce tutto. Alla porta della stanza c’è anche la sorellina di Carlo che sta ascoltando alla porta perché vuole sapere cosa Carlo sta facendo. Giorgia è molto chiacchierona ed ha sempre paura di perdersi qualcosa di interessante. Carlo vuole essere lasciato in pace e si augura che la sorella se ne vada via presto ma non interromperebbe mai l‘ascolto della musica o la conversazione con Tiziana per cacciarla via. Tutto sommato lui e Giorgia vanno abbastanza bene d‘accordo.",
                "questions": [
                    "Che cosa sta facendo Carlo?",
                    "Perché Carlo ama la musica di Rocco Hunt?",
                    "Quale problema ha Tiziana con la musica di Rocco Hunt?",
                    "Che cosa sappiamo di Giorgia e che cosa sta facendo?",
                    "Come reagisce Carlo alla sorella?"
                ],
            }
        ],
        4: [  # Siena
            {
                "text": "Il giorno dopo gli amici stanno parlando: vogliono andare a Napoli insieme! Naturalmente Carlo non potrà organizzare tutto da solo. È necessario che tutti aiutino con l‘organizzazione perché è impossibile che una persona legga tutte le informazioni. Gli amici sperano che trovino un appartamento a prezzo basso nel centro e che non debbano pagare tanto neanche per il treno. Per Tiziana è importante che possano visitare tutte le attrazioni della città a piedi. Fabrizio è dell‘opinione che Napoli sia una città molto viva, ma ha paura che ci siano troppi turisti nel centro. Preferirebbe fare anche una gita a Capri, per esempio. Simone vuole che facciano anche qualche sport come nuotare nel mare ma Paola ha dubbi che piaccia a tutti stressarsi troppo dopo tutti i giri in città. Dario non sa ancora se lui abbbia tempo per partecipare, ma è contento che il gruppo sia motivato. Alla fine tutti credono in un bellissimo viaggio insieme.",
                "questions": [
                    "Perché gli amici devono mettersi d‘accordo il giorno dopo?",
                    "Per che cosa non vogliono pagare troppo?",
                    "Come vuole visitare la città Tiziana?",
                    "Che cosa vuole fare Fabrizio e perché?",
                    "Che cosa propone Simone e perché Paola è contraria?"
                ],
            }
        ],
        5: [  # Venezia
            {
                "text": "Un po‘ più tardi Tiziana e Carlo parlano di nuovo del viaggio a Napoli che vogliono fare con gli amici. Tiziana dice che è un po‘ triste che Simone non capisca quanto per lei sia importante vedere il più possibile delle attrazioni di Napoli. “Sai, ci sono troppe cose da vedere! Tutti pensano solo al disordine che si crea nelle strade di Napoli con le manifestazioni all‘aperto che hanno luogo in centro città e che bloccano sempre tutto. Ma c‘è un teatro spettacolare da vedere, castelli, musei ed i tanti mercati dove vorrei comprare uno dei famosi portafortuna napoletani per cacciare la sfortuna. E Simone pensa solo allo sport e alla spiaggia!“ -„Tiziana, ho capito! Ne parlerò dopo con lui, OK?“ Carlo pensa che sia meglio parlare con calma con l‘amico perché ha l’impressione che altrimenti rimanga male. Desidera che il gruppo resti unito durante il viaggio e quindi è necessario prendere sul serio tutte le idee e trovare un accordo.",
                "questions": [
                    "Secondo Tiziana: a che cosa pensa la gente quando si parla di Napoli?",
                    "Di quale problema stanno parlando Carlo e Tiziana?",
                    "Quali attrazioni e attività si trovano sul programma di Tiziana?",
                    "A quale soluzione del problema pensa Carlo?",
                    "Pensando al viaggio: che cosa è importante a Carlo?"
                ],
            }
        ],
        6: [  # Torino
            {
                "text": "Dopo la lezione di educazione fisico Dario parla con Simone e del fatto che Tiziana ha delle idee diverse su cosa fare a Napoli. Simone comincia ad avere dei dubbi sul viaggio insieme. Simone: “Napoli è una città al mare, certo che si va in spiaggia! Comincia già di maggio che la vita è all‘aperto con tutta la gente nelle piazze di sera e a fare lunghe passeggiate lungo il mare. Nel centro è più rumoroso e fa più caldo e perché dovrò girare per vedere tutti i musei, le chiese e i \nCarlo: È chiaro, no? La spiaggia di una città non è mai tanto pulita. Ogni città ha la propria storia e chi la visita impara a vedere le cose che la rendono unica. A Napoli per esempio c‘è il patrono San Gennaro e ogni anno il suo sangue si scioglie. Porta fortuna! E poi voglio vedere un teatro con Pulcinella, quella maschera con il cappuccio in testa che nasconde il viso. Un personaggio interessantissimo e anche divertente! Tiziana è innamorata di Pulcinella. Simone: O forse tu sei innamorato di lei? Non vedo perché non dovrei farmi un bel bagno nel mare! Alla fine di una lunga conversazione decidono che bisogna essere spontanei perché il programma dipenderà anche dal tempo che fa.",
                "questions": [
                    "Con quali argomenti motiva Simone che vuole andare in spiaggia?",
                    "Con quale argomento reagisce Carlo all‘idea di Simone?",
                    "Quali attrazioni stanno sul programma di Carlo e perché?",
                    "Che cosa Spensa Simone invece quali siano i motivi di Carlo?",
                    "Quale è la soluzione del conflitto tra Carlo, Tiziana e Simone?"
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
