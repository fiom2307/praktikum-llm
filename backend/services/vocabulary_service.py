import re
import json
from services.gemini_service import generate_from_prompt
from services.user_service import get_user, update_user
from services.user_service import add_history_entry

def generate_word_and_clues_with_ai():
    prompt = (
        "Generate one Italian vocabulary word that would be appropriate for a 14-year-old student "
        "with an A2 level of Italian. Then, write three short clues in Italian (maximum 5 words each) "
        "that help the student guess the word. "
        "Each clue should be simple and clear, avoiding long sentences or rare words. "
        "Return *only* valid JSON, without explanations or code block formatting. Example:\n"
        '{"word": "gatto", "clues": ["È un animale.", "Fa miao.", "Ama dormire."]}'
    )

    raw_response = generate_from_prompt(prompt)

    clean_text = re.sub(r"```json|```", "", raw_response).strip()

    try:
        return json.loads(clean_text)
    except json.JSONDecodeError:
        return {"raw_response": raw_response}
    

def check_word_with_ai(username: str, word: str, clues: list, answer: str):

    prompt = (
        f"Word: {word}\n"
        f"User answer: {answer}\n"
        f"Clues: {json.dumps(clues, ensure_ascii=False)}\n\n"
        "Compare the user's answer with the correct word in Italian.\n"
        "If it matches exactly, return:\n"
        '{"status": "correct", "hint": ""}\n'
        "If it's close (e.g. small spelling mistake or a synonym), return:\n"
        '{"status": "almost", "hint": "brief explanation in Italian"}\n'
        "If it's wrong, return:\n"
        '{"status": "incorrect", "hint": ""}\n'
        "Return only valid JSON, no extra text."
    )

    raw_response = generate_from_prompt(prompt)
    clean_text = re.sub(r"```json|```", "", raw_response).strip()

    try:
        #
        result = json.loads(clean_text)
        
        #
        if result.get("status") in ["correct", "almost"]:
             add_history_entry(
                username=username, 
                module="vocabulary", 
                details={
                    "word": word,
                    "final_answer": answer,
                    "status": result.get("status"),
                    "attempts_made": "N/A" 
                }
            )
        
        #
        return result
    
    except json.JSONDecodeError:
        #
        return {"raw_response": raw_response}
    

def get_current_vocabulary(username):
    user = get_user(username)
    if not user:
        return None
    return user["currentVocabulary"]

def save_current_vocabulary(username, word, clues, attempts, completed):
    user = get_user(username)
    if not user:
        return None

    user["currentVocabulary"] = {
        "word": word,
        "clues": clues,
        "attempts": attempts,
        "completed": completed
    }

    update_user(user)
    return user["currentVocabulary"]
