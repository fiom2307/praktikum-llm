from services.openai_service import generate_from_prompt
from database import SessionLocal
from models import FreeReadingHistory
import re
from models import User, City
from typing import List

def save_reading_history(user_id, llm_question, user_answer, llm_feedback):
    db = SessionLocal()
    try:
        entry = FreeReadingHistory(
            user_id=user_id,
            llm_question=llm_question,
            user_answer=user_answer,
            llm_feedback=llm_feedback
        )
        db.add(entry)
        db.commit()
        db.refresh(entry)
        return entry
    finally:
        db.close()

def correct_answers_ai(user_id: int, generated_text: str, user_text: str):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return {"corrected_answers": "", "pizzas": 0}
        
        prompt = F"""You are an automatic feedback generator for Italian reading comprehension items.

            CONTEXT

            The student answered numbered questions about an Italian passage. Provide compact per-item feedback that shows correctness, one short text evidence snippet, and (only when needed) one next-step reading strategy. At the end, always add a brief final comment (motivation + short general reading feedback), the earned score.
            If the user does not answer a question it is marked as incorrect.

            INPUT

            - Passage with questions (numbered): {generated_text}
            - Student answers (not necessarily numbered, text to evaluate): {user_text}

            HARD RULES (OVERRIDES FIRST)

            - If any student answer contains inappropriate/rude language (insults, slurs, obscene name-calling, threats), output ONLY: Pizze guadagnate: 0 and no further output.
            - If PASSAGE is not predominantly Italian (exceptions: proper names, places, brands, numbers) OR there is no question OR no student answer, output ONLY: Pizze guadagnate: 0 and no further output.
            - Otherwise, follow all rules below and produce the full output in OUTPUT FORMAT.

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

            Pizzas X
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
    corrected = clean_llm_output(corrected)

    save_reading_history(
        user_id=user_id,
        llm_question=generated_text,
        user_answer=user_text,
        llm_feedback=corrected
    )

    return {"corrected_answers": corrected,"pizzas": pizzas}

def extract_pizzas(text: str) -> int:
    match = re.search(r"Pizzas\s+(-?\d+)", text)
    if match:
        return int(match.group(1))
    return 0

def extract_indexes(text: str) -> List[int]:
    match = re.search(r"Index\s*:\s*\[?([0-9,\s-]+)\]?", text)
    if not match:
        return []

    raw_indexes = match.group(1)
    return [int(i.strip()) for i in raw_indexes.split(",") if i.strip()]

def clean_llm_output(text: str) -> str:
    return re.sub(
        r"(Pizzas\s+-?\d+|Index\s*:?\s*\[?[0-9,\s-]+\]?)",
        "",
        text,
        flags=re.IGNORECASE
    ).strip()


def generate_reading_text_from_ai(user_id: int):
    db = SessionLocal()
    try:
        histories = (
            db.query(FreeReadingHistory)
            .filter(FreeReadingHistory.user_id == user_id)
            .order_by(FreeReadingHistory.created_at.desc())
            .limit(5)
            .all()
        )

        previous_texts = [h.llm_question for h in histories if h.llm_question]

        previous_texts_str = "\n\n---\n\n".join(previous_texts)


    finally:
        db.close()

    
    prompt = f"""You generate one Italian A2 reading set: a passage + 5 questions + an answer index for automatic feedback.

                CONTEXT

                A learner reads the passage and answers the questions. The system will later generate feedback using:

                - PASSAGE
                - QUESTIONS
                - STUDENT_ANSWERS

                HARD RULES

                - Passage language: Italian, A2, age-appropriate.
                - Passage length: 120–170 words.
                - Passage must be 6–9 short sentences, separated by periods (so sentence numbers are unambiguous).
                - Create exactly 5 questions in Italian, numbered 1–5.
                - Mix question types:
                * 2x vero/falso (TF)
                * 2x multiple choice with A/B/C (MC)
                * 1x open short answer (OPEN)
                - For MC: provide options A/B/C (each option max 6 words), 1 correct + 2 plausible distractors.
                - For OPEN: the correct answer must be max 6 words and directly supported by the passage.
                - Do NOT include any extra commentary.
                - Do NOT repeat the following text or their topics (DONT DO SOMETHING SIMILAR): {previous_texts_str}

                Generate a text based on topics that a 14 year old kid in school would find inetresting or general topics, 
                like school, hollidays, family, etc. Try to use different names for the protagonists of the stories (female and male protagonists).
                Also change the time in which the stories happen (past present, future). Change the point of view of the story (first person, second person)

                Do NOT violate any HARD RULES.

                OUTPUT

                Return a text, do not return the answer index. After (MC) always put and extra line before writing anything else.
                Do not specify the type of question in english only in italian.
                - Do NOT repeat the following text or their topics: {previous_texts_str}
                """

    
    text = generate_from_prompt(prompt)
    return {
        "exercise_id": 0,
        "reading_text": text
    }