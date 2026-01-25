from services.openai_service import generate_from_prompt
from database import SessionLocal
from models import StoryWritingHistory, StoryWritingExercise
from services.writing_service import extract_pizzas
from models import User, UserCityProgress
from models.city_model import City
from services.reading_service import clean_llm_output

def save_story_writing_history(user_id, user_answer, llm_feedback, exercise_id):
    db = SessionLocal()
    try:
        entry = StoryWritingHistory(
            user_id=user_id,
            exercise_id=exercise_id,
            user_answer=user_answer,
            llm_feedback=llm_feedback
        )
        db.add(entry)
        db.commit()
        db.refresh(entry)
        return entry
    finally:
        db.close()
        
def fetch_writing_text_service(user_id: int, city_key: str):
    db = SessionLocal()
    try:
        # Resolve city
        city = (
            db.query(City)
            .filter(City.name.ilike(city_key))
            .first()
        )
        if not city:
            return {"error": "Città non valida"}
        
        # Fetch user progress for this city
        progress = (
            db.query(UserCityProgress)
            .filter(
                UserCityProgress.user_id == user_id,
                UserCityProgress.city_id == city.id
            )
            .first()
        )

        if (
            progress.writing_pizzas_earned >= city.writing_pizza_goal
            and progress.writing_tasks_done >= city.writing_task_count
        ):
            return {"status": "done"}

        # Fetch the ONLY writing exercise for this city
        exercise = (
            db.query(StoryWritingExercise)
            .filter(StoryWritingExercise.city_id == city.id)
            .first()
        )

        if not exercise:
            return {"error": "No writing exercise found for this city"}

        # Response
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

        previous_feedbacks_str = "\n\n---\n\n".join(previous_feedbacks)
        
        histories = (
            db.query(StoryWritingHistory)
            .filter(StoryWritingHistory.user_id == user_id)
            .order_by(StoryWritingHistory.created_at.desc())
            .limit(5)
            .all()
        )

        previous_answers = [
            h.user_answer for h in histories if h.user_answer
        ]

        previous_answers_str = "\n\n---\n\n".join(previous_answers)

        prompt = f"""You are an automatic feedback generator for a short Italian writing submission. 

            CONTEXT 

            The student wrote a short text intended to be Italian (target length: 50–150 words). You must validate (language/length/bad language), run a similarity check, and then give concise feedback in German using a strict 3-part structure. The total feedback must be short (< 101 words), so prioritize only the most important points. 

            INPUT 

            - Student text: {user_text} 

            - Previous student texts (for similarity check; do NOT mention in output): {previous_answers_str}

            HARD RULES 

            1) Output ONLY the block in the exact format below (same headings, same order). No extra text. 

            2) Do NOT reproduce the full student text. Do NOT provide rewritten/corrected full sentences. 

            3) Headings must be exactly the Italian headings shown in OUTPUT. 

            4) All bullet content must be in German (except for the predefined Italian headings and snippets directly retrieved from the input text). 

            5) Evidence snippets (“Il tuo testo”) must be in double quotes and count toward the max 4 snippets TOTAL: 

            - Normal case: 1–6 words copied from the student text. 

            - Special case B (length penalty applies): use "Wörter: N" (N = WORD_COUNT), not a text excerpt. 

            - Special case C (bad language): show only "***" (masked), not the original word(s). 

            6) Total output must be < 101 words (whitespace tokens), including headings and "Pizzas X". 

            7) Never use technical terms in the output: do NOT output “INVALID” and do NOT output “WORD_COUNT”. 

            8) Keep bullets on one line each. 

            9) The <Label> must be in German and must be one of: Inhalt, Struktur, Wortschatz, Grammatik, Textfluss, Rechtschreibung, Länge, Sprache 

            10) Do NOT mention similarity checks, scoring rules, penalties, or previous texts in the output. 

            11) SNIPPET DISCIPLINE: 

            - If a bullet label is NOT Sprache and NOT Länge, its snippet MUST be Italian words from the Italian part of STUDENT_TEXT (avoid quoting German/English there). 

            - German/English snippets may be used ONLY in a Sprache bullet (or Länge/bad language as specified). 
            
            12) FORMATTING REQUIREMENT: 

             - The exact string **Il tuo testo:** must appear in every bullet that has a snippet, and it must be bold exactly like this: **Il tuo testo:** (including the colon). 

            STEP 1 — WORD COUNT (STRICT) 

            Compute WORD_COUNT from STUDENT_TEXT ONLY: 

            - Split by whitespace. 

            - Each whitespace-separated chunk counts as 1 word (punctuation attached still counts as the same word). 

            Then set LENGTH_OK = (WORD_COUNT >= 45). 
            
            CRITICAL CONSISTENCY FOR LENGTH 

            - If LENGTH_OK is TRUE: you MUST NOT mention length anywhere (no label "Länge", no advice to write longer/shorter). 

            - If LENGTH_OK is FALSE: you MUST include exactly one length bullet in “Errori principali”: 

            Label: Länge | Message: “Unter 45 Wörter” | Snippet: "Wörter: WORD_COUNT" 

            And at least one “Prossimi passi” bullet must instruct to expand to 45+ words. 

            STEP 2 — BAD LANGUAGE (EARLY EXIT, STRICT) 

            Bad language includes insults, slurs, obscene name-calling, degrading labels, or threats (in ANY language: Italian, German, English, etc.). This applies even if the student reports or quotes it. 

            Examples (non-exhaustive): idiota, stronzo, coglione; idiot, bitch, asshole; du Idiot, Schlampe; threats like “I will hurt you”. 

            If any bad language is present: 

            - final score MUST be exactly 0. 

            - In “Errori principali” include a bullet: 

            Sprache: “Unangemessene Sprache”. **Il tuo testo:** unangemessene Sprache 

            - STOP: skip all other checks and scoring (including language/length/similarity). Output only the required structure. 

            
            STEP 3 — LANGUAGE PENALTY (ONLY WHEN CLEARLY NOT ITALIAN) 

            Trigger language penalty ONLY if you can identify at least 3 non-Italian tokens (German/English) in STUDENT_TEXT. 

            - Do NOT treat Italian insults as “Nicht überwiegend Italienisch” (they are handled by bad language). 

            If triggered, include one bullet in “Errori principali”: 

            - Sprache: “Nicht überwiegend Italienisch” (or “Deutsch-Italienisch gemischt”). **Il tuo testo:** "<non-Italian excerpt 1–6 words>" 

            IMPORTANT: Do NOT label code-switching as Grammatik. Mixing languages belongs ONLY under Sprache. 

            If you add a second bullet in “Errori principali” while language penalty is triggered, it must address Italian quality (e.g., Grammatik/Wortschatz/Textfluss) and must quote ONLY Italian words. 

            STEP 4 — SIMILARITY CAP (INTERNAL ONLY) 

            Compare STUDENT_TEXT against PREVIOUS_USER_ANSWERS_STR: 

            - If very similar (same storyline/structure with minor edits), cap SCORE at 4. 

            - Do NOT mention similarity or previous texts in the output. 

            SCORING (INTERNAL ONLY) 

1) Choose BASE_SCORE as an integer 0–10 (overall Italian quality). 

2) SCORE = BASE_SCORE 

3) If language penalty triggered: SCORE = floor(SCORE * 0.7) 

4) If LENGTH_OK is FALSE: SCORE = floor(SCORE * 0.7) 

5) Apply similarity cap if needed. 

6) If bad language is present: SCORE = 0 (already handled by early exit). 

7) Pizze guadagnate = SCORE. 

 

FEEDBACK PRIORITIES (to stay < 101 words) 

- Obiettivo: max 1 bullet. 

- Errori principali: max 2 bullets (one may be required by rules). 

- Prossimi passi: max 2 bullets. 

- If needed, shorten in this order: 

  1) Motivating comment to one word (e.g., “Gut.”) 

  2) Remove Prossimi passi bullet 2 

  3) Remove Errori principali bullet 2 (unless it is a required bullet) 


OUTPUT (EXACT FORMAT) 

Obiettivo: 

- <Label>: <Zielkriterium kurz auf Deutsch>. **Il tuo testo:** "<snippet>" 


Errori principali: 

- <Label>: <kurze Erklärung auf Deutsch>. **Il tuo testo:** "<snippet>" 

- <Label>: <kurze Erklärung auf Deutsch>. **Il tuo testo:** "<snippet>" 


Prossimi passi: 

- <konkreter nächster Schritt auf Deutsch> 

- <konkreter nächster Schritt auf Deutsch> 


<Brief motivating German comment.> 

Pizzas <Pizzas earned> 
            """
            
        history_prompt = f"""HISTORY (TREATMENT; prior feedback patterns)

            - Prior feedbacks (for pattern detection only; do NOT quote in output): {previous_feedbacks_str}

            USE OF PRIOR FEEDBACKS

            - Scan {previous_feedbacks_str} for recurring error patterns (e.g., verb forms, articles, prepositions, word order, agreement).
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
    corrected = clean_llm_output(corrected)

    save_story_writing_history(
        user_id=user_id,
        exercise_id=exercise_id,
        user_answer=user_text,
        llm_feedback=corrected
    )

    return {"corrected_text": corrected, "pizzas": pizzas}

