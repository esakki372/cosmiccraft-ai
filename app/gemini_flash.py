import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def generate_outline(prompt: str, character: str, setting: str, tone: str, art_style: str):
    """Generates a structured 5-panel comic outline using Gemini Flash."""
    system_instruction = (
        f"Create a 5-panel comic outline based on the user's prompt. "
        f"Main Character: {character}, Setting: {setting}, Tone: {tone}, Art Style: {art_style}. "
        "Return ONLY valid JSON as a list of dictionaries with keys: 'panel_number', 'title', 'scene_description', 'image_prompt'."
    )
    
    full_prompt = f"{system_instruction}\n\nUser Prompt: {prompt}"
    
    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=full_prompt,
        )
        cleaned_text = response.text.strip().replace("```json", "").replace("```", "")
        return json.loads(cleaned_text)
    except Exception:
        # Fallback outline if model output parsing fails
        return [
            {
                "panel_number": i+1,
                "title": f"Panel {i+1}: Chapter {i+1}",
                "scene_description": f"{character} navigates through {setting}.",
                "image_prompt": f"{art_style} style illustration of {character} in {setting}, {tone} atmosphere"
            } for i in range(5)
        ]