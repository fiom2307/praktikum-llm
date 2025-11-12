from flask import Blueprint, request, jsonify
import google.generativeai as genai
import os

reading_routes = Blueprint("reading_routes", __name__)

api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
else:
    print("GEMINI_API_KEY not found")

@reading_routes.route("/correct_answers", methods=["POST"])
def correct_answer():
    data = request.get_json()
    user_text = data.get("text", "")
    generated_text = data.get("generated_text", " ")

    if not api_key:
        return jsonify({"corrected_answers": "GEMINI_API_KEY not found"}), 200

    model = genai.GenerativeModel("gemini-2.5-flash")
    prompt = f"Vergleiche diese Antworten mit den zuvor erstellten Fragen zum Text und markiere, welche richtig sind. Erkläre anschließend, warum sie richtig oder falsch sind. Diese ist der text von vorher \n\n{generated_text}. \n\n Diese ist der antwort der schuler: {user_text},"

    response = model.generate_content(prompt)
    corrected_answers = response.text.strip()

    return jsonify({"corrected_answers": corrected_answers})

@reading_routes.route("/create_reading_text", methods=["POST"])
def create_reading_text():
    
    if not api_key:
        return jsonify({"reading_text": "GEMINI_API_KEY not found"}), 200
    
    model = genai.GenerativeModel("gemini-2.5-flash")
    prompt = (
        "Schreibe einen kurzen Text im Italienisch von etwa 200 Wörtern über eines der folgenden Themen: "
        "Ferien, Schule und Freizeit, Identität und Zukunftspläne, kulturelle Unterschiede zwischen "
        "Nord- und Süditalien, Liebe und Freundschaft, italienische Feste und Jugendkultur, Lesen und "
        "Literatur oder italienische Feiertage und Traditionen. "
        "Erstelle danach fünf Fragen zu deinem Text. Schreibe einfach den Text auf Italienisch, ohne zu sagen, über welche Themen er handelt, und ohne jegliche zusätzliche Interaktion."
    )

    response = model.generate_content(prompt)
    reading_text = (response.text or "").strip()

    return jsonify({"reading_text": reading_text})