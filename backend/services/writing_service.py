from services.openai_service import generate_from_prompt
from database import SessionLocal
from models import FreeWritingHistory
import re
from models import User
from services.reading_service import clean_llm_output

def save_free_writing_history(user_id, user_answer, llm_feedback):
    db = SessionLocal()
    try:
        entry = FreeWritingHistory(
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

def correct_text_with_ai(user_id: int, user_text: str):
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

            The student wrote a short text intended to be Italian (target length: 50–150 words). You must validate (language/length/bad language), run a similarity check, and then give concise feedback in German using a strict 3-part structure. The total feedback must be short (< 101 words), so prioritize only the most important points. 

            INPUT 

            - Student text: {user_text} 

            - Previous student texts (for similarity check; do NOT mention in output): {previous_feedbacks_str}

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

            

            VALIDATION & SCORING (STRICT, INTERNAL ONLY) 

            1) Compute WORD_COUNT = number of whitespace-separated tokens in {user_text}. 

            2) Bad language (early exit) 

            - If {user_text} contains “bad language” (insults, slurs, obscene name-calling, threats): 

            * final score MUST be exactly -5. 

            * In the output, include at least one bullet in “Errori principali” with: 

                - Label: Sprache 

                - Message: “Unangemessene Sprache” 

                - Snippet: "***" 

            * STOP: skip all other checks and scoring. 

            3) Base score 

            - Set BASE_SCORE as a whole number from 0–10 based on overall quality. 

            - Set SCORE = BASE_SCORE. 

            4) Penalty triggers 

            - Define two penalty triggers: 

            * Language penalty: If the text is NOT predominantly Italian, allow exceptions for proper names, numbers, and very short German insertions (1–2 tokens). 

            * Length penalty: If NOT (49 < WORD_COUNT < 151). 

            5) Apply penalties 

            - If Language penalty triggered: SCORE = SCORE * 0.7. 

            - If Length penalty triggered: SCORE = SCORE * 0.7. 

            - After penalties, round SCORE DOWN to the next whole number (floor). 

            6) Similarity cap 

            - Compare {user_text} against {previous_answers_str}. 

            - If there exists a previous text that is very similar (same storyline/structure with only minor edits): 

            * Award points ONLY for parts that are clearly new/different AND correct. 

            * If SCORE > 4, set SCORE = 4. 

            * Do NOT mention similarity or previous texts in the output. 

            7) Final score & pizzas 

            - final score = SCORE. 

            - Set "Pizzas" = final score, except: 

            * If final score < 0, set Pizzas 0. 

            REQUIREMENT WHEN A PENALTY APPLIES (OUTPUT IN PLAIN LANGUAGE) 

            - If any penalty was applied (Language penalty and/or Length penalty), include at least one bullet in “Errori principali” stating the failing criterion in normal German and include an “Il tuo testo” snippet: 

            * Language penalty -> label "Sprache" + “Nicht überwiegend Italienisch” + short non-Italian excerpt (1-6 words). 

            * Length penalty -> label "Länge" + “Nicht im Bereich 50–150 Wörter” + "Wörter: N". 

            FEEDBACK PRIORITIES (to stay < 101 words) 

            - Obiettivo: max 1 bullet. 

            - Errori principali: max 2 bullets. 

            - Prossimi passi: max 2 bullets. 

            - If needed, shorten deterministically in this order: 
            * Shorten the motivating comment to one word (e.g., “Gut.”). 

            * Remove Prossimi passi bullet 2 

            * Remove Errori principali bullet 2 

            OUTPUT (EXACT FORMAT) 

            Obiettivo: 

            - <Label>: <Zielkriterium kurz auf Deutsch>. Il tuo testo: "<snippet>" 

            Errori principali: 

            - <Label>: <kurze Erklärung auf Deutsch>. Il tuo testo: "<snippet>" 

            - <Label>: <kurze Erklärung auf Deutsch>. Il tuo testo: "<snippet>" 

            Prossimi passi: 

            - <konkreter nächster Schritt auf Deutsch> 

            - <konkreter nächster Schritt auf Deutsch> 


            <Brief motivating German comment.> 


            Pizzas <Pizzas earned> 


            EXAMPLES (without indexes) 


            >EXAMPLE 1 

            >Student text: Oggi vado a scuola con mia sorella. Dopo la lezione mangiamo una pizza e poi studiamo in biblioteca perché domani abbiamo un test. Mi piace leggere e scrivere, ma a volte faccio errori di grammatica. Nel pomeriggio gioco a calcio con gli amici e la sera guardo un film. 

            >Expected output: 

            Obiettivo: 

            - Grammatik: Präsensformen konsistent zur Person einsetzen, damit der Text sicher wirkt. Il tuo testo: "vado a scuola" 

            Errori principali: 

            - Grammatik: Artikel vor Nomen prüfen; hier wirkt die Wahl noch unsicher. Il tuo testo: "un test" 

            - Textfluss: „poi“ ist sehr häufig; variiere Konnektoren für klarere Abfolge. Il tuo testo: "e poi studiamo" 

            Prossimi passi: 

            - Markiere alle Artikel und entscheide bewusst: il/la/un/una. 

            - Ersetze 2× „poi“ durch „dopo“ oder „in seguito“. 

            Guter Inhalt und gut verständlich – mit kleinen Anpassungen wirkt es noch natürlicher. 

            Pizza 7 


            >EXAMPLE 2 

            >Student text: Ciao! Io sono Marco. Oggi scuola. Pizza. 

            >Expected output: 

            Obiettivo: 

            - Länge: 50–150 Wörter erreichen, damit man eine kleine Geschichte versteht. Il tuo testo: "Wörter: 8" 

            Errori principali: 

            - Länge: Nicht im Bereich 50-150 Wörter; es fehlen Infos und mehrere Verben. Il tuo testo: "Wörter: 8" 

            Prossimi passi: 

            - Schreibe 6-8 Sätze: Wer? Was? Wann? Wo? Warum? 

            - Nutze pro Satz ein Verb (z.B. andare, mangiare, studiare). 

            Guter Start - bau daraus eine kurze, zusammenhängende Szene. 

            Pizzas 0 
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
        llm_feedback=corrected
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

def extract_pizzas(text: str) -> int:
    match = re.search(r"Pizzas\s+(-?\d+)", text)
    if match:
        return int(match.group(1))
    return 0