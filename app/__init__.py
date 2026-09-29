import os
from dotenv import load_dotenv

load_dotenv()

# Get API key - required for app to run
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("WARNING: GEMINI_API_KEY not set. Set it in .env (local) or Render environment variables.")
    print("App will start but API calls will fail.")
