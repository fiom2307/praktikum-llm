from services.gemini_service import generate_from_prompt

def correct_text_with_ai(user_text: str):

    prompt = (
        "Korrigiere diesen italienischen Text in Bezug auf Grammatik und Stil:\n\n"
        f"{user_text}"
    )

    corrected = generate_from_prompt(prompt)
    return {"corrected_text": corrected}
