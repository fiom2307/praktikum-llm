import re
import json
from services.openai_service import generate_from_prompt
from database import SessionLocal
from models import FreeVocabularyHistory, User, City

def generate_word_and_clues_with_ai(user_id: int):
    db = SessionLocal()
    try:
        histories = (
            db.query(FreeVocabularyHistory)
            .filter(FreeVocabularyHistory.user_id == user_id, FreeVocabularyHistory.completed == True)
            .order_by(FreeVocabularyHistory.created_at.desc())
            .limit(20)
            .all()
        )

        previous_words = [h.word for h in histories if h.word]
        previous_words_str = ", ".join(previous_words)
        
        user = db.query(User).filter(User.id == user_id).first()
        current_city_order = user.current_city_id if user else None

        city_name = None
        if current_city_order is not None:
            city = (
                db.query(City)
                .filter(City.order_index == current_city_order)
                .first()
            )
            city_name = city.name if city else None

    finally:
        db.close()

    prompt = (
        "Generate one Italian vocabulary word that would be appropriate for a 14-year-old student "
        "with an A2 level of Italian. Then, write three short clues in Italian (maximum 5 words each) "
        "that help the student guess the word. "
        "Each clue should be simple and clear, avoiding long sentences or rare words. "
        "Return *only* valid JSON, without explanations or code block formatting. Example:\n"
        '{"word": "gatto", "clues": ["È un animale.", "Fa miao.", "Ama dormire."]}'
        "IMPORTANT:\n"
        "- Do NOT generate any of the following words or very similar ones:\n"
        f"{previous_words_str}\n\n"
    )
    
    prompt = f"""You generate one Italian A2 vocabulary recall item for a 14-year-old learner.

            CONTEXT

            Create a single target word and three short clues in Italian that help the student guess the word.

            Clues should be progressively more specific, but must not reveal the word directly.

            HARD RULES

            - Target word must be ONE Italian word (no spaces, no hyphens), lowercase.
            - Level: A2, age-appropriate, no proper names.
            - Avoid very rare words, slang, or regionalisms.
            - Clues must be in Italian, exactly 3 clues.
            - Each clue: max 5 words.
            - Do NOT include the target word (or a trivial close variant) in any clue.
            - Make the item guessable from the clues.
            - Do not repeat the following words: {previous_words_str}.

            CITY CONTEXT (optional)

            If a city context is provided, adapt the clues to that city.

            - City: {city_name}

            CITY CONTEXT Additional Rules:

            - If {city_name} is non-empty: make at least ONE clue clearly relate to the city context (e.g., landmark, food, culture, geography) WITHOUT using the city name.
            - Still obey all HARD RULES.

            OUTPUT

            Return only valid JSON, with no explanations and no code block formatting.

            Use exactly this schema:
            
            """ + """
                {"word":"<target_word>","clues":["<clue1>","<clue2>","<clue3>"]}

                Example (schema only):

                {"word":"gatto","clues":["È un animale.","Fa miao.","Ama dormire."]}
            """


    raw_response = generate_from_prompt(prompt)

    clean_text = re.sub(r"```json|```", "", raw_response).strip()

    try:
        return json.loads(clean_text)
    except json.JSONDecodeError:
        return {"raw_response": raw_response}
    
def save_vocabulary_history(
    user_id: int,
    word: str,
    clues: list,
    answer: str,
    attempt: int,
    completed: bool,
    correct: bool
):
    db = SessionLocal()
    try:
        entry = FreeVocabularyHistory(
            user_id=user_id,
            word=word,
            clues=clues,
            user_answer=answer,
            attempt_number=attempt,
            completed=completed,
            correct=correct,
        )
        db.add(entry)
        db.commit()
        return entry
    finally:
        db.close()
    

def check_word_with_ai(userId: int, word: str, clues: list, answer: str, attempt: int):
    
    prompt = f"""
            You are an automatic feedback generator for a vocabulary recall item. 

CONTEXT 

The student saw hints and typed a target word. Do NOT show the correct answer. If the student is wrong, the same word will reappear in a later round. Feedback should help the next attempt without giving away the solution. 

INPUT 

- Hints / task shown to the student: {json.dumps(clues, ensure_ascii=False)}

- Target answer (FOR YOU ONLY, never reveal): {word}

- Student answer: {answer}

HARD RULES 

1) Output ONLY the four lines in the exact format below (same labels, same order, same blank line after "Tu respuesta: ..."). No extra text. 

2) "Tu respuesta" must reproduce the student's answer EXACTLY as given. 

3) "Valutazione" must be EXACTLY one of: corretto | parzialmente corretto | falso 

4) "Già corretto" and "Piccola miglioria" must be in German. 

5) Never reveal the target answer. Never print the correct word. Never spell it. Never give enough information that uniquely identifies the target (do NOT give letter sequences; do NOT combine multiple identifiers such as first letter + length + ending). 

6) Total output must be < 50 words (whitespace tokens). Keep "Già corretto" and "Piccola miglioria" short (preferably 1 sentence each). 

7) Never use technical terms in the output: do NOT output “INVALID” and do NOT output “WORD_COUNT”. 

8) The <Label> must be in German. 

INPUT RATING 

- corretto: matches target (ignore trivial case/whitespace). 

- parzialmente corretto: clearly close (minor spelling/inflection/diacritic) or partially aligned. 

- falso: not close, empty, or irrelevant 

SCORING (NON-NEGOTIABLE) 

- If the user's text is empty/in a different language /inappropriate ->Pizze guadagnate = 0. 
- For falso / parzialmente -> Pizze guadagnate = 0. 

- For corretto -> Pizze guadagnate = 1. 

CONTENT RULES FOR "Già corretto" (German) 

- Must be based on the student's input (not generic praise). 

- If corretto: confirm fully (e.g., "Tutto corretto."). 

- If parzialmente corretto: name ONE specific aspect that is already right without revealing the answer, such as: 

* correct direction/meaning implied by the hints 

* plausible word form or category (noun/verb/adjective) for the task 

* a part of the spelling seems consistent (beginning / stem / ending is close) WITHOUT quoting letters 

- If falso and nothing is defensible: be supportive but minimal (e.g., "Guter Versuch."). 

CONTENT RULES FOR "Piccola miglioria" (German) 

- Exactly ONE small, actionable cue for the next round, tailored to the student's input. 

- The cue should point to the biggest error type you infer, but must NOT disclose the solution. 

- Allowed cue types (choose ONE): 

* spelling focus: ending / vowels / double consonants / accent (general, no letters) 

* grammar focus: article/genus or inflection (only if relevant to the task) 

* strategy focus: re-check the hints and commit to one spelling 

- Do NOT combine multiple cues. Do NOT give the correct word, letters, or the full ending. 

OUTPUT FORMAT (MANDATORY)

{{"status":"<correct|almost|incorrect>","hint":"<Italian hint or empty>"}}

EXAMPLES

Example 1:
{{"status":"almost", "hint":"Attenzione all’ortografia: controlla le doppie consonanti."}}

Example 2 (incorrect guess):
{{"status":"incorrect","hint":""}}

Example 3 (almost guess):
{{"status":"almost", "hint":"Manca l’accento finale sulla parola."}}

Example 4 (correct guess):
Word: {word}
Student answer: {word}

Output: 
{{"status":"correct", "hint":""}}

"""

    raw_response = generate_from_prompt(prompt)
    clean_text = re.sub(r"```json|```", "", raw_response).strip()

    try:
        result = json.loads(clean_text)
    except json.JSONDecodeError:
        result = raw_response

    is_correct = result.get("status") == "correct"
    is_completed = is_correct or attempt >= 3
    
    print(is_correct)
    
    save_vocabulary_history(
        user_id=userId,
        word=word,
        clues=clues,
        answer=answer,
        attempt=attempt,
        completed=is_completed,
        correct=is_correct,
    )

    return result

def get_last_vocabulary_entry(user_id: int):
    db = SessionLocal()
    try:
        entry = (
            db.query(FreeVocabularyHistory)
        .filter(FreeVocabularyHistory.user_id == user_id)
        .order_by(FreeVocabularyHistory.created_at.desc())
        .first()
        )

        return entry
    finally:
        db.close()
