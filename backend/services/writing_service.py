from services.gemini_service import generate_from_prompt
from services.user_service import add_history_entry

def correct_text_with_ai(username: str, user_text: str):

    prompt = (
        f"Korrigieren sie den text auf grammatik und still: {user_text}"
        "\nDanach gib eine kurze Erklärung AUF DEUTSCH (nur Erklärung, nichts mehr)."
        "Am Ende gib einen kurzen, positiven Kommentar AUF DEUTSCH zur Motivation des Schülers."
        "Wiederhole den user Text NICHT noch einmal."
        "\nGib am Ende einen positiven Kommentar, der den Schüler motiviert, egal ob er gut oder schlecht abschneidet."
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
