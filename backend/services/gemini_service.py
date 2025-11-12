import os
import google.generativeai as genai

api_key = os.getenv("GEMINI_API_KEY")

def generate_from_prompt(prompt: str, model_name: str = "gemini-2.5-flash"):
    model = genai.GenerativeModel(model_name)
    response = model.generate_content(prompt)
    return response.text.strip()