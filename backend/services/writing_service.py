from services.openai_service import generate_from_prompt
from database import SessionLocal
from models import FreeWritingHistory
import re
from models import User
from services.reading_service import clean_llm_output, extract_pizzas

def save_free_writing_history(user_id, user_answer, llm_feedback, llm_question):
    db = SessionLocal()
    try:
        entry = FreeWritingHistory(
            user_id=user_id,
            user_answer=user_answer,
            llm_feedback=llm_feedback,
            llm_question=llm_question
        )
        db.add(entry)
        db.commit()
        db.refresh(entry)
        return entry
    finally:
        db.close()

def correct_text_with_ai(user_id: int, user_text: str, current_topic: str):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return {"corrected_text": "", "pizzas": 0}
        
        histories = (
            db.query(FreeWritingHistory)
            .filter(FreeWritingHistory.user_id == user_id)
            .order_by(FreeWritingHistory.created_at.desc())
            .limit(5)
            .all()
        )

        previous_feedbacks = [
            h.llm_feedback for h in histories if h.llm_feedback
        ]

        previous_feedbacks_str = "\n\n---\n\n".join(previous_feedbacks)
        
        histories = (
            db.query(FreeWritingHistory)
            .filter(FreeWritingHistory.user_id == user_id)
            .order_by(FreeWritingHistory.created_at.desc())
            .limit(5)
            .all()
        )

        previous_answers = [
            h.user_answer for h in histories if h.user_answer
        ]

        previous_answers_str = "\n\n---\n\n".join(previous_answers)

        
        prompt = f"""You are an automatic feedback generator for a short Italian writing submission. 

 

CONTEXT 

The student wrote a short text intended to be Italian. You must validate (language/length/bad language), run a similarity check, and then give concise feedback in German using a strict 3-part structure. Total output must be short (< 101 words). 

 

INPUT 

- Student text (ONLY this text is evaluated): {user_text} 

- Previous student texts (ONLY for similarity check; do NOT mention in output): {previous_answers_str} 

 

NON-NEGOTIABLE TARGET LENGTH (use ONLY this, even if the task text elsewhere says something different) 

- Minimum length: at least 45 words (no upper limit) 

 

HARD RULES 

1) Output ONLY the block in the exact format below (same headings, same order). No extra text before/after. 

2) Do NOT reproduce the full student text. Do NOT provide rewritten/corrected full sentences. 

3) Headings must be exactly: Obiettivo / Errori principali / Prossimi passi 

4) All bullet content must be in German (except headings and snippets copied from STUDENT_TEXT). 

5) Evidence snippets (“Il tuo testo”) must be in double quotes and count toward max 4 snippets TOTAL: 

   - Normal case: 1–6 words copied from STUDENT_TEXT, in quotes. 

   - Length penalty case: use "Wörter: N" (N = your computed WORD_COUNT), in quotes. 

   - Bad language case: use the fixed token unangemessene Sprache (NO quotes) as the snippet; do NOT show the word(s). 

6) Total output must be < 101 words (whitespace-separated), including headings and "Pizzas X". 

7) Never use technical terms in the output (do NOT output: INVALID, token, prompt, rules). 

8) Keep bullets on one line each; each bullet MUST start with "- ". 

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

    save_free_writing_history(
        user_id=user_id,
        user_answer=user_text,
        llm_feedback=corrected,
        llm_question=current_topic
    )

    return {"corrected_text": corrected, "pizzas": pizzas}


def generate_exercise_with_ai(user_id: int):
    db = SessionLocal()
    try:
        histories = (
            db.query(FreeWritingHistory)
            .filter(FreeWritingHistory.user_id == user_id)
            .order_by(FreeWritingHistory.created_at.desc())
            .limit(5)
            .all()
        )

        previous_texts = [h.llm_question for h in histories if h.llm_question]

        previous_texts_str = "\n\n---\n\n".join(previous_texts)


    finally:
        db.close()

    
    prompt = f"""You generate one short Italian A2 writing task for a 14-year-old learner. 
        CONTEXT 

        The learner will write a short text in Italian. The target length is 50–150 words. 

        HARD RULES 

        - Output language for the student task: Italian. 

        - Level: A2, age-appropriate. 

        - Base the text on one of these topics: Holidays; School; free time; Identity;future plans; Love; friendship; Italian festivals; youth culture. 

        - Do NOT name the topic explicitly (no “Topic: …”). 

        - Task must be clear and simple, no long sentences. 

        - Include exactly 2 simple requirements (A2-friendly). 

        - Do NOT include an example text. 
        
        - Do NOT repeat the same texts from the last 5 excercises: {previous_texts_str} (DO NOT INCLUDE OR REPEAT)
        
        EXAMPLES:
        
        EXAMPLE 1:
        Scrivi un breve testo sulla: Vacanze. Usa tra 50 e 150 parole.
        
        EXAMPLE 2:
        Scrivi un breve testo sulla: Scuola e tempo libero. Usa tra 50 e 150 parole.
        
        EXAMPLE 3:
        Scrivi un breve testo sulla: Identità e progetti per il futuro. Usa tra 50 e 150 parole.
            
        EXAMPLE :
        Scrivi un breve testo sulla: Amore e amicizia. Usa tra 50 e 150 parole.
                        """

    
    text = generate_from_prompt(prompt)
    return {
        "exerciseId": 0,
        "cityKey": "",
        "text": text,
    }
