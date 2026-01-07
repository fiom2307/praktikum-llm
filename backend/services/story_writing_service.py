from services.openai_service import generate_from_prompt
from database import SessionLocal
from models import StoryWritingHistory, StoryWritingExercise
from services.writing_service import extract_pizzas
from models import User
from models.city_model import City

def save_writing_history(user_id, user_answer, llm_feedback):
    db = SessionLocal()
    try:
        entry = StoryWritingHistory(
            user_id=user_id,
            user_answer=user_answer,
            llm_feedback=llm_feedback
        )
        db.add(entry)
        db.commit()
        db.refresh(entry)
        return entry
    finally:
        db.close()
        
def fetch_writing_text_service(user_id: int, city_key: str | None):
    db = SessionLocal()
    try:
        # 1️⃣ Resolver ciudad
        if city_key:
            city = (
                db.query(City)
                .filter(City.name.ilike(city_key))
                .first()
            )
            if not city:
                return {"error": "Città non valida"}
            city_id = city.id
        else:
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                return {"error": "User not found"}
            city_id = user.current_city_id

        # 2️⃣ Traer ejercicio de WRITING (solo 1 por ciudad)
        exercise = (
            db.query(StoryWritingExercise)
            .filter(StoryWritingExercise.city_id == city_id)
            .first()
        )

        if not exercise:
            return {"error": "No writing exercise found for this city"}

        # 3️⃣ Respuesta al frontend
        return {
            "exerciseId": exercise.id,
            "cityKey": city_key,
            "text": exercise.text,
        }

    finally:
        db.close()


def correct_story_text_with_ai(user_id: int, user_text: str, exercise_id):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return {"corrected_text": "", "pizzas": 0}
        
        histories = (
            db.query(StoryWritingHistory)
            .filter(StoryWritingHistory.user_id == user_id)
            .order_by(StoryWritingHistory.created_at.desc())
            .limit(5)
            .all()
        )

        previous_feedbacks = [
            h.llm_feedback for h in histories if h.llm_feedback
        ]
        
        histories = (
            db.query(StoryWritingHistory)
            .filter(StoryWritingHistory.user_id == user_id)
            .order_by(StoryWritingHistory.created_at.desc())
            .limit(5)
            .all()
        )

        previous_user_answers = [
            h.user_answer for h in histories if h.user_answer
        ]

        previous_feedbacks_str = "\n\n---\n\n".join(previous_feedbacks)
        previous_user_answers_str = "\n\n---\n\n".join(previous_user_answers)

        prompt_1 = (
            f"Analysiere den folgenden Text auf Italienisch und erkläre die vorhandenen Fehler "
            f"zu Grammatik und Stil AUF DEUTSCH: {user_text}\n"
            "Gib NUR eine Erklärung der Fehler zurück.\n"
            "Wiederhole oder korrigiere den Text NICHT.\n"
            "Füge KEINE zusätzlichen Kommentare oder Motivation hinzu.\n"
            "Am Ende gib eine Punktzahl zwischen 0 und 10 als „Pizzas X” an (nur ganze Zahlen).\n"
            "Falls der Text nicht auf Italienisch ist oder nicht zwischen 50 und 150 Wörtern liegt, gib „Pizzas 0” aus."
            f"Jetzt gebe ich dir vorherige antwroten von die Schülern: {previous_user_answers_str}"
            "Wenn sich unter den eingereichten Texten ein Text befindet, der dem des Nutzers sehr ähnlich ist, werden Punkte nur für die Teile vergeben, die sich vom Text unterscheiden und korrekt sind. Ein Text, der einem anderen sehr ähnlich ist, kann nicht mehr als 4 Pizzen erhalten."
        )

        prompt_2 = (
            f"Analysiere den folgenden Text auf Italienisch und erkläre die vorhandenen Fehler."
            f"zu Grammatik und Stil AUF DEUTSCH: {user_text}\n"
            "Gib NUR eine Erklärung der Fehler zurück.\n"
            "Wiederhole oder korrigiere den Text NICHT.\n"
            "Füge KEINE zusätzlichen Kommentare oder Motivation hinzu.\n"
            "Am Ende gib eine Punktzahl zwischen 0 und 10 als „Pizzas X” an (nur ganze Zahlen). Das erwartete Niveau des user ist A2.\n"
            "Falls der Text nicht auf Italienisch ist oder nicht zwischen 50 und 150 Wörtern liegt, gib „Pizzas 0” aus."
            "ZUSÄTZLICH:\n"
            "Analysiere die folgenden früheren Rückmeldungen des Schülers. "
            "Suche nach Fehlern, die sich mehrfach wiederholen (z.B. gleiche Grammatikprobleme, "
            "falsche Verbformen, Präpositionen, Artikel oder Satzstellung).\n\n"
            "Wenn es wiederkehrende Fehler gibt, füge GANZ AM ENDE einen kurzen Abschnitt hinzu mit:\n"
            "- einer Liste der häufigsten wiederholten Fehler\n"
            "- einem kurzen, konkreten Rat, wie der Schüler diese Fehler verbessern oder vermeiden kann\n\n"
            "Frühere Rückmeldungen (nur zur Analyse, NICHT zitieren oder wiederholen):\n"
            f"{previous_feedbacks_str}"
            f"\n\nJetzt gebe ich dir vorherige antwroten von die Schülern: {previous_user_answers_str}"
            "Wenn sich unter den eingereichten Texten ein Text befindet, der dem des Nutzers sehr ähnlich ist, werden Punkte nur für die Teile vergeben, die sich vom Text unterscheiden und korrekt sind. Ein Text, der einem anderen sehr ähnlich ist, kann nicht mehr als 4 Pizzen erhalten."
        )

        if user.user_group == "control":
            prompt = prompt_1
        else: 
            prompt = prompt_2

    finally:
        db.close()

    corrected = generate_from_prompt(prompt)
    pizzas = extract_pizzas(corrected)

    save_writing_history(
        user_id=user_id,
        exercise_id=exercise_id,
        user_answer=user_text,
        llm_feedback=corrected
    )

    return {"corrected_text": corrected, "pizzas": pizzas}

