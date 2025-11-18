from services.gemini_service import generate_from_prompt
from services.user_service import add_history_entry

def correct_answers_ai(username: str, generated_text: str, user_text: str):
    
    prompt = (
        "Vergleiche diese Antworten mit den zuvor erstellten Fragen zum Text und markiere, welche richtig sind. Gib die richtige antwort und "
        f"erkläre sie kurz. Diese ist der text von vorher \n\n{generated_text}." 
        f"\n\n Diese ist der antwort der schuler: {user_text},"
    )
    
    corrected = generate_from_prompt(prompt)

    add_history_entry(
        username=username, 
        module="reading", 
        details={
            "submitted_answers": user_text,
            "ai_correction": corrected
        }
    )

    return {"corrected_answers": corrected}
    
def generate_reading_text_from_ai():

    prompt = (
        "Schreibe einen kurzen Text im Italienisch von etwa 150 Wörtern über eines der folgenden Themen: "
        "Ferien, Schule und Freizeit, Identität und Zukunftspläne, kulturelle Unterschiede zwischen "
        "Nord- und Süditalien, Liebe und Freundschaft, italienische Feste und Jugendkultur, Lesen und "
        "Literatur oder italienische Feiertage und Traditionen. "
        "Erstelle danach fünf Fragen zu deinem Text. Schreibe einfach den Text auf Italienisch, aber die Fragen auf deutsch, ohne zu "
        "sagen, über welche Themen er handelt, und ohne jegliche zusätzliche Interaktion. Beachte, dass das Italienisch-Niveau A2 sein muss."
    )
    
    text = generate_from_prompt(prompt)
    return {"reading_text": text}