from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize the client
api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    client = genai.Client(api_key=api_key)
else:
    client = None
    print("WARNING: GEMINI_API_KEY not configured")

def generate_outline(prompt: str):
    """Generate comic panel outline using Gemini Flash 2.5
    
    Args:
        prompt: The user's comic story concept
        
    Returns:
        Text outline of comic panels
    """
    if not client:
        return f"Demo outline for: {prompt}\n\nPanel 1: Opening scene\nPanel 2: Conflict\nPanel 3: Climax\nPanel 4: Resolution"
    
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        return response.text
    except Exception as e:
        print(f"Error: {str(e)}")
        return f"Demo outline for: {prompt}\n\nPanel 1: Opening scene\nPanel 2: Conflict\nPanel 3: Climax\nPanel 4: Resolution"
