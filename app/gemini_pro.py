import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def generate_story(outline: list, character: str, tone: str):
    """Expands panel outlines into rich narration and dialogue using Gemini Pro."""
    prompt = (
        f"Write engaging comic book narration, captions, and dialogues for a {tone} story featuring {character}. "
        f"Here is the structural panel outline: {outline}. "
        "Provide unified, captivating narrative descriptions corresponding to the comic panels."
    )
    
    response = client.models.generate_content(
        model="gemini-3.1-pro-preview",
        contents=prompt,
    )
    return response.text