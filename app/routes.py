from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.gemini_flash import generate_outline
from app.gemini_pro import generate_story
from app.image_generator import generate_image
from app.layout_builder import build_comic_layout
from app.exporters import save_pdf

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.post("/generate", response_class=HTMLResponse)
async def generate_comic(
    request: Request,
    prompt: str = Form(...),
    character: str = Form(...),
    setting: str = Form(...),
    tone: str = Form(...),
    art_style: str = Form(...)
):
    try:
        # 1. Generate Outline via Gemini Flash
        outline = generate_outline(prompt, character, setting, tone, art_style)
        
        # 2. Generate Story Content via Gemini Pro
        story = generate_story(outline, character, tone)
        
        # 3. Generate Panel Images
        image_paths = [
            generate_image(p.get("image_prompt", prompt), p.get("panel_number", 1)) 
            for p in outline
        ]
        
        # 4. Compile Layout & Export PDF
        layout = build_comic_layout(outline, image_paths, story)
        pdf_path = save_pdf(layout)
        
        return templates.TemplateResponse("comic_preview.html", {
            "request": request,
            "layout": layout,
            "pdf_path": pdf_path
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/export-success", response_class=HTMLResponse)
async def export_success(request: Request):
    return templates.TemplateResponse("export_success.html", {"request": request})