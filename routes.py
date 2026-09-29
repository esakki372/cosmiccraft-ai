from fastapi import APIRouter, HTTPException, Form
from app.gemini_flash import generate_outline

router = APIRouter()


@router.post("/generate-comic")
def create_comic_outline(
    prompt: str = Form(...),
    character: str = Form(...),
    setting: str = Form(...),
    tone: str = Form(...),
    art_style: str = Form(...)
):
    try:
        # Combine all form information into one prompt for Gemini
        full_prompt = f"""
Create a comic story based on the following information.

Story Prompt:
{prompt}

Main Character:
{character}

Setting:
{setting}

Story Tone:
{tone}

Art Style:
{art_style}

Create a clear and engaging comic story outline.
"""

        outline = generate_outline(full_prompt)

        return {
            "status": "success",
            "outline": outline,
            "character": character,
            "setting": setting,
            "tone": tone,
            "art_style": art_style
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )