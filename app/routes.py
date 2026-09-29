from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.gemini_flash import generate_outline
from app.gemini_pro import generate_story
from app.image_generator import generate_image
from app.layout_builder import build_comic_layout
from app.exporters import save_pdf
import os

router = APIRouter(prefix="/api", tags=["comic"])

class ComicRequest(BaseModel):
    prompt: str
    character: str = "Hero"
    tone: str = "adventure"

class ComicResponse(BaseModel):
    status: str
    outline: str = None
    story: str = None
    pdf_path: str = None
    error: str = None

@router.post("/generate-comic", response_model=ComicResponse)
def create_comic(request: ComicRequest):
    """Generate a complete comic with outline, story, and PDF export
    
    Args:
        request: ComicRequest with prompt, character, and tone
        
    Returns:
        ComicResponse with generated content and PDF path
    """
    try:
        # Step 1: Generate outline
        outline = generate_outline(request.prompt)
        
        # Step 2: Generate story/narration
        story = generate_story(outline, request.character, request.tone)
        
        # Step 3: Generate images for panels (simplified - one image per panel)
        # In production, you'd parse the outline to get individual panels
        num_panels = min(4, outline.count('\n') + 1)  # Use newlines as panel delimiter
        image_paths = []
        for i in range(num_panels):
            img_path = generate_image(f"{request.prompt} - Panel {i+1}", i+1)
            image_paths.append(img_path)
        
        # Step 4: Build layout
        layout = build_comic_layout(
            outline=[{"panel_number": i+1, "title": f"Panel {i+1}", "scene_description": outline} for i in range(num_panels)],
            image_paths=image_paths,
            story_text=story
        )
        
        # Step 5: Export to PDF
        pdf_path = save_pdf(layout)
        
        return ComicResponse(
            status="success",
            outline=outline,
            story=story,
            pdf_path=pdf_path
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-outline")
def create_comic_outline(prompt: str):
    """Generate only the comic outline
    
    Args:
        prompt: The comic story concept
        
    Returns:
        JSON with outline
    """
    try:
        outline = generate_outline(prompt)
        return {"status": "success", "outline": outline}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-story")
def create_story(prompt: str, character: str = "Hero", tone: str = "adventure"):
    """Generate only the story/narration
    
    Args:
        prompt: The outline or story concept
        character: Main character
        tone: Story tone
        
    Returns:
        JSON with story
    """
    try:
        story = generate_story(prompt, character, tone)
        return {"status": "success", "story": story}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status")
def comic_api_status():
    """Check API status"""
    return {
        "service": "Comic Generation API",
        "status": "running",
        "endpoints": {
            "/generate-comic": "POST - Full comic generation",
            "/generate-outline": "POST - Outline only",
            "/generate-story": "POST - Story only"
        }
    }
