from fastapi import APIRouter, HTTPException
from app.gemini_flash import generate_outline

router = APIRouter()

@router.post("/generate-comic")
def create_comic_outline(prompt: str):
    try:
        outline = generate_outline(prompt)
        return {"status": "success", "outline": outline}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))