from services.gemini_service import generate_from_prompt
from services.user_service import add_history_entry
import re


def correct_answers_ai(username: str, generated_text: str, user_text: str):
    
    prompt = (
        "Vergleiche diese Antworten mit den zuvor erstellten Fragen zum Text und markiere, welche richtig sind. "
        "Gib NUR folgendes Format aus und halte dich strikt daran:\n\n"
        "**Frage 1:** richtige Antwort\n"
        "--------------------\n"
        "**Erklärung:** Korrektur der Schülerantwort\n\n"
        "**Richtige Antwort:** Antwort der Frage"
        "**Frage 2:** richtige Antwort\n"
        "--------------------\n"
        "**Erklärung:** Korrektur der Schülerantwort\n\n"
        "**Richtige Antwort:** Antwort der Frage"
        "(… und so weiter für alle Fragen …)\n\n"
        "Am Ende gib:\n"
        "- Einen kurzen, motivierenden Kommentar für den Schüler, egal ob er gut oder schlecht abgeschnitten hat.\n"
        "- Eine Punktzahl von 0 bis 5 im Format: Pizzas X\n\n"
        "Beantworte nur im oben beschriebenen Format, ohne zusätzliche Erklärungen, ohne Einleitung und ohne zusätzlichen Text.\n\n"
        "Nutze dafür den folgenden Ausgangstext:\n"
        f"{generated_text}\n\n"
        "Dies sind die Antworten des Schülers:\n"
        f"{user_text}\n\n"
        "Se lo studente dice qualcosa di inappropriato o di scortese, assegnagli un punteggio di -5 e non rispondere."
    )

    
    corrected = generate_from_prompt(prompt)
    
    pizzas = extract_pizzas(corrected)
    
    print("Pizzas: ", pizzas)

    add_history_entry(
        username=username, 
        module="reading", 
        details={
            "submitted_answers": user_text,
            "ai_correction": corrected
        }
    )

    return {"corrected_answers": corrected, "pizzas" : pizzas}


def extract_pizzas(text: str) -> int:
    match = re.search(r"Pizzas\s+(-?\d+)", text)
    if match:
        return int(match.group(1))
    return 0

def generate_reading_text_from_ai():
    
    prompt = (
        "Schreibe einen kurzen Text im Italienisch von etwa 150 Wörtern über eines der folgenden Themen, whälen sie den Thema random aus: "
        "Ferien, Schule und Freizeit, Identität und Zukunftspläne, kulturelle Unterschiede zwischen "
        "Nord- und Süditalien, Liebe und Freundschaft, italienische Feste und Jugendkultur, Lesen und "
        "Literatur oder italienische Feiertage und Traditionen. "
        "Erstelle danach fünf Fragen zu deinem Text. Schreibe einfach den Text auf Italienisch die Fragen auch, ohne zu "
        "sagen, über welche Themen er handelt, und ohne jegliche zusätzliche Interaktion. Beachte, dass das Italienisch-Niveau A2 sein muss."
    )
    
    text = generate_from_prompt(prompt)
    return {"reading_text": text}