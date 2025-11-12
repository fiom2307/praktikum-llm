from flask import Blueprint, request, jsonify
import google.generativeai as genai
import os

text_routes = Blueprint("text_routes", __name__)

api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
else:
    print("GEMINI_API_KEY not found")

@text_routes.route("/correct_text", methods=["POST"])
def correct_text():
    data = request.get_json()
    user_text = data.get("text", "")

    if not api_key:
        return jsonify({"corrected_text": "GEMINI_API_KEY not found"}), 200

    model = genai.GenerativeModel("gemini-2.5-flash")
    prompt = f"Korrigiere diesen italienischen Text in Bezug auf Grammatik und Stil:\n\n{user_text}"

    response = model.generate_content(prompt)
    corrected_text = response.text.strip()

    return jsonify({"corrected_text": corrected_text})
