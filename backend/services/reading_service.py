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
        
        histories = (
            db.query(FreeReadingHistory)
            .filter(FreeReadingHistory.user_id == user_id)
            .order_by(FreeReadingHistory.created_at.desc())
            .limit(5)
            .all()
        )

        previous_feedbacks = [
            h.llm_feedback for h in histories if h.llm_feedback
        ]

        previous_feedbacks_str = "\n\n---\n\n".join(previous_feedbacks)
        
        prompt = F"""You are an automatic feedback generator for Italian reading comprehension items. 

 

CONTEXT 

The student answered numbered questions about an Italian passage. Provide compact per-item feedback that shows correctness, one short text evidence snippet, and (only when needed) one next-step reading strategy. At the end, always add a brief final comment (motivation + short general reading feedback) and the earned score. 

 

INPUT 

- Passage and Questions (numbered): {generated_text} 

- Student answers (numbered): {user_text} 

 

HARD RULES (OVERRIDES FIRST) 

- If any student answer contains inappropriate/rude language (insults, slurs, obscene name-calling, threats), output ONLY: 

  Pizzas 0 

  and no further output. 

 

- If PASSAGE is not predominantly Italian (exceptions: proper names, places, brands, numbers) OR there is no question OR no student answer, output ONLY: 

  Pizzas 0 

  and no further output. 


- Otherwise, follow all rules below and produce the full output in OUTPUT FORMAT. 

 

HARD RULES (FORMAT + CONTENT) 

- Output ONLY the lines specified in OUTPUT FORMAT. No headings, no intro, no extra text. 

- Do NOT reproduce the full passage or the full questions. 

- Feedback language: German. Allowed fixed labels in Italian: 

  La tua risposta, La risposta corretta, Valutazione, Prova, Prossimo, Z., Frase, Pizze guadagnate. 
- Do NOT rewrite or correct full sentences from the student. 

- If you give the correct answer for open answers, keep it to max 6 words. 

- For every item, always output both: 

  - La tua risposta (student answer) 
  
    - La risposta corretta (correct answer) 


- Every item MUST include exactly one evidence snippet from the PASSAGE (Prova). 

- Use a multi-line block per item with bold labels exactly as in OUTPUT FORMAT. 

 

EVIDENCE SNIPPET (Prova) 

- The snippet must be: 

  - 1–8 words, 

  - taken literally from the passage (no paraphrase), 

  - in double quotes. 

- Total max 12 snippets across all items. 

- Location: 

  - If the passage has line breaks or explicit line numbers, use: Z. <line_number>. 

  - Otherwise use: Frase <sentence_number>. 

 

NEXT-STEP STRATEGY (Prossimo) 

- Include a Prossimo line ONLY when Valutazione is parzialmente or falso. 

- Prossimo must be a reading strategy (not a correction), max 60 characters. 

- It must be specific to the likely error type and tied to the cited evidence location (Z./Frase). 

- Do NOT reveal or paraphrase the correct answer. 

- Avoid generic advice; give one concrete action (e.g. “Lies Frase 3, markiere das Signalwort ‘perché’.”). 

 

CORRECTNESS + VALUTAZIONE 

- Determine the correct answer from the PASSAGE, or from ANSWER_INDEX. 

 

- If ANSWER_INDEX contains a 0-based index for options: 

  - Map it to the option order in the question (0→A, 1→B, 2→C, ...). 

  - For vero/falso, map 0→vero, 1→falso. 

 

- If ANSWER_INDEX already contains the correct option text (A/B/C or vero/falso), use it directly. 

 

- For open answers, ANSWER_INDEX provides the short correct answer text (max 6 words). 

- Always output La risposta corretta: 

  - MC/TF: a single option (A/B/C or vero/falso). 

  - Open answers: max 6 words. 

- Valutazione must be exactly one of: 

  corretto | parzialmente | falso 

 

  - MC/TF: 

    - matches → corretto 

    - otherwise → falso (no parzialmente). 

  - Open answers: 

    - choose among all three. 

 

HANDLING PARZIALMENTE (PARTIALLY CORRECT ANSWERS) 

- Use Valutazione: parzialmente when: 

  - the answer captures a central part correctly but misses or misstates an important detail, OR 

  - the answer is too general/vague although the correct text location was identified. 

- For parzialmente, briefly refer to the student answer: 

  - Directly after Valutazione, add a very short German note (max ~10 words) describing the error type/scope. 

  - Examples: 

    - “Valutazione: parzialmente. Kern stimmt, aber Detail fehlt.” 

    - “Valutazione: parzialmente. Richtung stimmt, Ort bleibt unklar.” 

    - “Valutazione: parzialmente. Person erkannt, Beziehung verwechselt.” 

- This note must NOT give away or paraphrase the correct solution; it only names the error type. 

 

LENGTH LIMITS (STRICT) 

- Each single line of an item block (La tua risposta / Valutazione / Prova / Prossimo) must have < 25 words. 

- The final overall comment (summary feedback) must have < 25 words. 

- IMPORTANT: Do NOT shorten by deleting multi-word key information (names, places, reasons) from La tua risposta. If shortening is needed, shorten Prossimo first, then German phrasing, then the evidence snippet. 

- IMPORTANT: Do NOT shorten by deleting multi-word key information (names, places, reasons) from La tua risposta or La risposta corretta. If shortening is needed, shorten Prossimo first, then German phrasing, then the evidence snippet. 

- If you need to shorten, do so in this order: 

  1) Shorten Prossimo. 

  2) Simplify German phrasing (including the parzialmente-note). 

  3) Shorten the snippet minimally (but keep 1–8 words). 

  4) Omit Prossimo if the error type is already clear from the Valutazione-note. 

- Across all items together, use at most 12 snippets (Prova). 

 

SCORING 

- Per item: 

  - corretto = 1 

  - parzialmente = 0 

  - falso = 0 

- Total score X = number of items with Valutazione = corretto. 

- Output: 

  Pizzas X 

 

FINAL COMMENT (WHAT’S GOOD / IMPROVE / NEXT STEPS) 

- After all item blocks, write exactly one short sentence in German. 

- This sentence must combine in ONE sentence three elements: 

  1) What’s good: a brief positive remark. 

  2) Improve: exactly ONE main improvement focus, phrased naturally (avoid “verbessere Ortsangaben/Personenangaben”). 

  3) Next steps: one concrete reading action. 

- The sentence must have < 25 words. 

- Use natural focus phrasing, for example: 

  - “achte stärker auf Ortswörter” 

  - “halte Personenrollen auseinander” 

  - “prüfe Begründungen mit ‘perché’” 

  - “beachte Verneinungen” 

  - “vergleiche Aussagen Satz für Satz” 

- Examples (all < 25 words): 

  - “Guter Start; achte stärker auf Ortswörter und vergleiche Aussagen in Frase 2 direkt mit dem Text.” 

  - “Solide Basis; halte Personenrollen auseinander und prüfe Frase 1 Satz für Satz.” 

  - “Bleib dran; beachte Signalwörter und lies den Belegsatz zweimal, bevor du antwortest.” 

 

OUTPUT FORMAT 

For each question i (starting at 1): 

 

i) **La tua risposta**: <student_answer> 

**La risposta corretta**: <correct_answer> 


**Valutazione**: <corretto/parzialmente/falso. Optional short German error-type note> 

**Prova**: "<snippet>" (Z./Frase <nr>). 

**Prossimo**: <one concrete reading action>   [only if Valutazione = parzialmente or falso] 

 

- The Prossimo line is only produced when Valutazione = parzialmente or falso. 

- For corretto, there is no Prossimo line. 

 

Then at the end: 

 

<one German sentence with What’s good + Improve + Next steps, as described above> 

Pizzas X
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
        r"(Index\s*:?\s*\[?[0-9,\s-]+\]?)",
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
                * 3x multiple choice with A/B/C (MC)
                - IMPORTANT: For MC: provide options A/B/C (each option max 6 words), 1 correct + 2 plausible distractors.
                - Always change the order of the questions.
                - Open answer questions are BANNED, do NOT generate open answer questions.
                - ONLY true/false (TF) question and multiple choice (MC) questions are permited to be generated.
                - Do NOT include any extra commentary.
                - Do NOT repeat the following text or their topics (DO NOT USE AS INSPIRATION FOR NEW TEXT OR PASSAGE): {previous_texts_str}

                Generate a text based on topics that a 14 year old kid in school would find inetresting or general topics, 
                like school, hollidays, family, etc. Try to use different names for the protagonists of the stories (female and male protagonists).
                Also change the time in which the stories happen (past present, future). Change the point of view of the story (first person, second person)

                Do NOT violate any HARD RULES.

                OUTPUT

                Return a text, do not return the answer index.  After (MC) always put and extra line before writing the possible answers A/B/C.
                Do not specify the type of question in english only in italian.
                NO open answer questions.
                ONLY multiple choice and true or false questions allowed.
                ALWAYS Provide answer options A/B/C for multiple choice questions. 
                ALWAYS shuffle the position of the questions around, they should always have a different order as the one presented in the example.
                
                EXAMPLE:
                
                PASSAGE
                <<TEXT>>
                
                DOMADE
                1. <<FIRST QUESTION>> 
                  A) <Posible answer A>
                  B)<Posible answer B>
                  C)<Posible answer C>
                
                2. <<Second QUESTION>> (V/F)
                
                3. <<THIRD QUESTION>> 
                  A) <Posible answer A>
                  B)<Posible answer B>
                  C)<Posible answer C>
                  
                4. <<FOURTH QUESTION>> (V/F)
                
                5. <<FIFTH QUESTION>> 
                  A) <Posible answer A>
                  B)<Posible answer B>
                  C)<Posible answer C>
                """

    
    text = generate_from_prompt(prompt)
    return {
        "exercise_id": 0,
        "reading_text": text
    }