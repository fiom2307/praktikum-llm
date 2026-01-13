import random
from database import SessionLocal
from models.city_model import City
from models import StoryReadingExercise, StoryReadingHistory
from models import User
from services.openai_service import generate_from_prompt
from services.reading_service import extract_pizzas, extract_indexes, clean_llm_output

def save_reading_story_history(user_id, exercise_id, user_answer, llm_feedback, correct_question_indexes):
    db = SessionLocal()
    try:
        entry = StoryReadingHistory(
            user_id=user_id,
            exercise_id=exercise_id,
            user_answer=user_answer,
            llm_feedback=llm_feedback,
            correct_question_indexes=correct_question_indexes
        )
        db.add(entry)
        db.commit()
        db.refresh(entry)
        return entry
    finally:
        db.close()

def get_city_reading_text_for_user(user_id: int, city_key: str):
    db = SessionLocal()
    try:
        # 1️⃣ Resolve city (city_key = lowercase city name)
        city = (
            db.query(City)
            .filter(City.name.ilike(city_key))
            .first()
        )
        if not city:
            return {"reading_text": "❌ Città non valida."}

        # 2️⃣ Fetch reading exercises for this city
        exercises = (
            db.query(StoryReadingExercise)
            .filter(StoryReadingExercise.city_id == city.id)
            .all()
        )
        if not exercises:
            return {"reading_text": "❌ Nessun esercizio disponibile per questa città."}

        exercise_ids = [e.id for e in exercises]

        # 3️⃣ Fetch user history for these exercises
        histories = (
            db.query(StoryReadingHistory)
            .filter(
                StoryReadingHistory.user_id == user_id,
                StoryReadingHistory.exercise_id.in_(exercise_ids)
            )
            .all()
        )

        # 4️⃣ Merge correctly answered questions per exercise
        correct_by_exercise = {}
        for h in histories:
            correct_by_exercise.setdefault(h.exercise_id, set())
            if h.correct_question_indexes:
                correct_by_exercise[h.exercise_id].update(h.correct_question_indexes)

        # 5️⃣ Determine valid exercises and remaining questions
        ALL_QUESTIONS = {0, 1, 2, 3, 4}
        candidates = []

        for ex in exercises:
            correct = correct_by_exercise.get(ex.id, set())
            remaining = sorted(list(ALL_QUESTIONS - correct))

            if remaining:  # there are still unanswered questions
                candidates.append((ex, remaining))

        # All reading exercises completed
        if not candidates:
            return {
                "status": "done"
            }

        # 6️⃣ Choose a random exercise
        ex, remaining_indexes = random.choice(candidates)

        # 7️⃣ Build FINAL MARKDOWN
        questions_md = "\n".join(
            [f"{i+1}. {ex.questions[i]}" for i in remaining_indexes]
        )

        reading_text_md = f"""

{ex.text}

---

{questions_md}
"""

        return {
            "exercise_id": ex.id,
            "reading_text": reading_text_md
        }

    finally:
        db.close()
        
def correct_story_answers_ai(user_id: int, generated_text: str, user_text: str, exercise_id: int):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return {"corrected_answers": "", "pizzas": 0}

        prompt = F"""You are an automatic feedback generator for Italian reading comprehension items.

            CONTEXT

            The student answered numbered questions about an Italian passage. Provide compact per-item feedback that shows correctness, one short text evidence snippet, and (only when needed) one next-step reading strategy.  At the end, always add a brief final comment (motivation + short general reading feedback), the earned score, and the 0-based indexes of correct items. 
            If the user does not answer a question it is marked as incorrect. 

            INPUT

            - Passage with questions (numbered): {generated_text}
            - Student answers (not necessarily numbered, text to evaluate): {user_text}
            

            HARD RULES (OVERRIDES FIRST)

            - If any student answer contains inappropriate/rude language (insults, slurs, obscene name-calling, threats), output ONLY: Pizze guadagnate: 0 and no further output.
            - If PASSAGE is not predominantly Italian (exceptions: proper names, places, brands, numbers) OR there is no question OR no student answer, output ONLY: Pizze guadagnate: 0 and no further output.
            - Otherwise, follow all rules below and produce the full output in OUTPUT FORMAT.
            
            ANSWER_INDEX RULES

            - Provide ANSWER_INDEX aligned with questions 1–5 (same order, length 5).

            HARD RULES (FORMAT + CONTENT)

            - Output ONLY the lines specified in OUTPUT FORMAT. No headings, no intro, no extra text.
            - Do NOT reproduce the full passage or the full questions.
            - Feedback language: German. Allowed fixed labels in Italian: La tua risposta, La risposta corretta, Valutazione, Prova, Prossimo, Z., Frase, Pizzas.
            - Do NOT rewrite or correct full sentences.
            - If you give the correct answer for open answers, keep it to max 6 words.
            - Always output "La tua risposta" and "La risposta corretta" for every item line.
            - Every item line MUST include exactly one evidence snippet from the PASSAGE ("Prova").
            - Evidence snippet: 1–8 words, in double quotes. Total max 12 snippets across all items.
            - Add a location for the evidence:
            * If the passage has line breaks or explicit line numbers, use "Z. <line_number>".
            * Otherwise use "Frase <sentence_number>".
            - Next-step strategy (Prossimo):
            * Include "Prossimo: ..." ONLY when Valutazione is parzialmente or falso.
            * Prossimo must be a reading strategy (not a correction), max 60 characters.
            * It must be specific to the likely error type and tied to the cited evidence location (Z./Frase).
            * Do NOT reveal or paraphrase the correct answer.
            * Avoid generic advice; make it one concrete action.
            - Do NOT mention any rules in the output.

            CORRECTNESS + VALUTAZIONE

            - Determine the correct answer from the PASSAGE.
            * Map it to the option order in the question (0→A, 1→B, 2→C, ...).
            * For vero/falso, map 0→vero, 1→falso.
            - Always output La risposta corretta:
            * MC/TF: a single option (A/B/C or vero/falso).
            * Open answers: max 6 words.
            - Valutazione must be exactly one of: corretto | parzialmente | falso
            * MC/TF: corretto if matches; otherwise falso (no parzialmente).
            * Open answers: choose among all three.

            LENGTH LIMITS (STRICT)

            - Each item line must be < 21 words (whitespace tokens).
            * If needed, shorten in this order: 1) shorten Prossimo, 2) shorten snippet, 3) shorten German phrasing, 4) keep only essential parts.
            - The final comment must be < 13 words.
            - Score line and indexes line must keep the exact required format.

            SCORING

            - Per item (if there is no answer no point is given for the question.):
            * corretto = 1
            * parzialmente = 0
            * falso = 0
            - Total score X = number of items with Valutazione = corretto.
            - Output as: "Pizzas X"
            
            FINAL COMMENT (MOTIVATION + SHORT FEEDBACK)

            - Add one brief German sentence before the score line.
            - It must include a motivating phrase AND one concrete reading habit.
            - Keep it neutral and encouraging (no personalization).
            - Must be < 13 words.

            OUTPUT FORMAT

            <N>) Deine Antwort: <student_answer> → Die richtige Antwort: <correct_answer>. Bewertung: <richtig/teilweise richtig/falsch>. Test: „<snippet>” (Z./Satz <nr>). <optional Weiter: ...>
            ... (one line per question)

            <final comment in German>

            Pizzas X Index: 1, 2, 3
            
            EXAMPLE 

            > 1) Deine Antwort: B → Die richtige Antwort: C. Bewertung: falsch. Beweis: „...“ (Satz 2). Weiter: Lies Satz 2, prüfe Negation. 

            > 2) Deine Antwort: wahr → Die richtige Antwort: wahr. Bewertung: richtig. Beweis: „...“ (Satz 3). 

            >Guter Fortschritt; lies den Belegsatz noch einmal genau. 

            >Pizzas 1 Index: 1
            """
        
        history_prompt = """HISTORY (TREATMENT; prior feedback patterns)

            - Prior feedbacks (for pattern detection only; do NOT quote in output): {{PREVIOUS_FEEDBACKS_STR}}

            USE OF PRIOR FEEDBACKS

            - Scan {{PREVIOUS_FEEDBACKS_STR}} for recurring error patterns (e.g., verb forms, articles, prepositions, word order, agreement).
            - If a pattern clearly repeats, prioritize that pattern in the limited output:
            * Prefer selecting it as one of the “Errori principali” bullets OR as the first “Prossimi passi”.
            - Do NOT add an extra section beyond the fixed OUTPUT FORMAT.
            - Do NOT mention, quote, or reference prior feedbacks in the output.
            - Do NOT change validation or scoring based on prior feedbacks.
            - Do NOT personalize to hobbies/preferences/personality traits; use only learning-relevant signals.
            """


        prompt = (
            prompt
            if user.user_group == "control"
            else prompt + "\n\n" + history_prompt
        )

    finally:
        db.close()

    corrected = generate_from_prompt(prompt)
    pizzas = extract_pizzas(corrected)
    indexes = extract_indexes(corrected)
    corrected = clean_llm_output(corrected)

    save_reading_story_history(
        user_id=user_id,
        exercise_id=exercise_id,
        user_answer=user_text,
        llm_feedback=corrected,
        correct_question_indexes=indexes
    )

    return {"corrected_answers": corrected,"pizzas": pizzas}
