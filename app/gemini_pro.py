import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

# Get API key from environment
api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    client = genai.Client(api_key=api_key)
else:
    client = None
    print("WARNING: GEMINI_API_KEY not configured")

def generate_story(outline: str, character: str, tone: str):
    """Expands panel outlines into rich narration and dialogue using Gemini Pro.
    
    Args:
        outline: Panel outlines
        character: Main character name/description
        tone: Tone of the story (e.g., "funny", "dark", "dramatic")
        
    Returns:
        Rich narrative text for the comic
    """
    if not client:
        return f"Demo story: A {tone} tale of {character}.\nScene: {outline}\nThis is a placeholder story."
    
    try:
        prompt = (
            f"Write engaging comic book narration for a {tone} story featuring {character}. "
            f"Outline: {outline}. Keep it brief and captivating."
        )
        
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        return response.text
    except Exception as e:
        print(f"Error: {str(e)}")
        return f"Demo story: A {tone} tale of {character}.\nScene: {outline}\nThis is a placeholder story."
