import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = None
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    client = genai.Client(api_key=api_key)

def generate_story(outline: str, character: str, tone: str) -> str:
    fallback = f"Demo story: A {tone} tale featuring {character}.\n\n{outline}"
    if not client:
        return fallback
    try:
        prompt = (
            f"Write concise comic narration and dialogue for a {tone} story featuring {character}. "
            f"Use this outline:\n{outline}\nKeep it suitable for a 4-panel comic."
        )
        response = client.models.generate_content(
            model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
            contents=prompt,
        )
        return response.text or fallback
    except Exception as e:
        print(f"Gemini story error: {e}")
        return fallback
