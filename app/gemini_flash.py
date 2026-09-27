from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize the client (it will automatically look for GEMINI_API_KEY environment variable)
client = genai.Client()

def generate_outline(prompt: str):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )
    return response.text