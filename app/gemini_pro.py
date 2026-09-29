import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

# Get API key from environment
api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY or GOOGLE_API_KEY environment variable not found. "
        "Please set it in your .env file or Render environment variables."
    )

client = genai.Client(api_key=api_key)

def generate_story(outline: list, character: str, tone: str):
    """Expands panel outlines into rich narration and dialogue using Gemini Pro.
    
    Args:
        outline: List of panel outlines
        character: Main character name/description
        tone: Tone of the story (e.g., "funny", "dark", "dramatic")
        
    Returns:
        Rich narrative text for the comic
    """
    try:
        prompt = (
            f"Write engaging comic book narration, captions, and dialogues for a {tone} story featuring {character}. "
            f"Here is the structural panel outline: {outline}. "
            "Provide unified, captivating narrative descriptions corresponding to the comic panels."
        )
        
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
        )
        return response.text
    except Exception as e:
        raise Exception(f"Error generating story: {str(e)}")
