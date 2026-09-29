from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize the client (it will automatically look for GEMINI_API_KEY environment variable)
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY environment variable not found. "
        "Please set it in your .env file or Render environment variables."
    )

client = genai.Client(api_key=api_key)

def generate_outline(prompt: str):
    """Generate comic panel outline using Gemini Flash 2.5
    
    Args:
        prompt: The user's comic story concept
        
    Returns:
        Text outline of comic panels
    """
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        return response.text
    except Exception as e:
        raise Exception(f"Error generating outline: {str(e)}")
