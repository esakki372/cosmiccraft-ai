import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = None
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    client = genai.Client(api_key=api_key)

def generate_outline(prompt: str) -> str:
    fallback = (
        f"Demo outline for: {prompt}\n\n"
        "Panel 1: Opening scene\n"
        "Panel 2: Conflict\n"
        "Panel 3: Climax\n"
        "Panel 4: Resolution"
    )
    if not client:
        return fallback
    try:
        response = client.models.generate_content(
            model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
            contents=prompt,
        )
        return response.text or fallback
    except Exception as e:
        print(f"Gemini outline error: {e}")
        return fallback
