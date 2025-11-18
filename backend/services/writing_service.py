from services.gemini_service import generate_from_prompt
from services.user_service import add_history_entry

def correct_text_with_ai(username: str, user_text: str):

    prompt = (
        "Korrigiere diesen italienischen Text in Bezug auf Grammatik und Stil:\n\n"
        f"{user_text}"
    )

    corrected = generate_from_prompt(prompt)

    add_history_entry(
        username=username, 
        module="writing", 
        details={
            "submitted_text": user_text,
            "ai_correction": corrected
        }
    )

    return {"corrected_text": corrected}
