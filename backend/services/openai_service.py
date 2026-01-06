import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_from_prompt(prompt: str, model_name: str = "gpt-4o-mini") -> str:
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return "OPENAI_API_KEY not found"

    try:
        completion = client.chat.completions.create(
            model=model_name,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a helpful Italian language tutor. Correct grammar and style clearly."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
        )

        return completion.choices[0].message.content.strip()

    except Exception as e:
        return f"LLM error: {str(e)}"