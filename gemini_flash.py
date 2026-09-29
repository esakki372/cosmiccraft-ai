import os
from dotenv import load_dotenv
from google import genai

# Load variables from .env
load_dotenv()

# Read Gemini API key
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError(
        "GEMINI_API_KEY is not configured. "
        "Add it to your .env file."
    )

# Create Gemini client
client = genai.Client(api_key=api_key)

# Current Gemini model
MODEL_NAME = "gemini-3.8-flash"


def generate_outline(prompt: str) -> str:
    """
    Generate a comic story outline using Gemini.
    """

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    if not response.text:
        raise RuntimeError("Gemini returned an empty response.")

    return response.text