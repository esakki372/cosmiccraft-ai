from fastapi import APIRouter
from pydantic import BaseModel
from app.gemini_flash import generate_outline
from app.gemini_pro import generate_story
from app.image_generator import generate_image
from app.layout_builder import build_comic_layout
from app.exporters import save_pdf

router = APIRouter(prefix="/api", tags=["comic"])

class ComicRequest(BaseModel):
    prompt: str
    character: str = "Hero"
    setting: str = ""
    tone: str = "adventure"
    art_style: str = "classic comic book"

@router.post("/generate-comic")
def create_comic(request: ComicRequest):
    try:
        full_prompt = f"""Create a clear 4-panel comic story outline.
Story idea: {request.prompt}
Main character: {request.character}
Setting: {request.setting}
Tone: {request.tone}
Art style: {request.art_style}
For each panel, describe the scene briefly."""

        outline = generate_outline(full_prompt)
        story = generate_story(outline, request.character, request.tone)

        image_paths = [
            generate_image(
                f"{request.art_style} comic panel {i}: {request.prompt}. Character: {request.character}. Setting: {request.setting}.",
                i,
            )
            for i in range(1, 5)
        ]

        layout = build_comic_layout(outline, image_paths, story)
        pdf_path = save_pdf(layout)

        return {
            "status": "success",
            "outline": outline,
            "story": story,
            "layout": layout,
            "pdf_path": "/" + pdf_path if pdf_path else "",
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}

@router.post("/generate-outline")
def create_comic_outline(request: ComicRequest):
    try:
        outline = generate_outline(request.prompt)
        return {"status": "success", "outline": outline}
    except Exception as e:
        return {"status": "error", "error": str(e)}

@router.post("/generate-story")
def create_story(request: ComicRequest):
    try:
        story = generate_story(request.prompt, request.character, request.tone)
        return {"status": "success", "story": story}
    except Exception as e:
        return {"status": "error", "error": str(e)}

@router.get("/status")
def comic_api_status():
    return {"service": "Comic Generation API", "status": "running", "version": "1.0"}
