from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router
import os

app = FastAPI(
    title="ComicCraft AI",
    version="1.0",
    description="AI Comic Story Creator powered by Google Gemini and Stable Diffusion"
)

# Add CORS middleware for cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure static directory exists
os.makedirs("static", exist_ok=True)
os.makedirs("static/panels", exist_ok=True)
os.makedirs("static/exports", exist_ok=True)
os.makedirs("templates", exist_ok=True)

# Mount static files directory
try:
    app.mount("/static", StaticFiles(directory="static"), name="static")
except Exception as e:
    print(f"Warning: Could not mount static files: {e}")

# Template configuration
try:
    templates = Jinja2Templates(directory="templates")
except Exception as e:
    print(f"Warning: Could not load templates: {e}")
    templates = None

# Include API routes
app.include_router(router)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Serve the main UI"""
    try:
        if templates:
            return templates.TemplateResponse(
                "index.html",
                {"request": request}
            )
        else:
            return "<h1>ComicCraft AI - Welcome!</h1><p>Templates not found. Check templates/ directory.</p>"
    except Exception as e:
        return f"<h1>ComicCraft AI</h1><p>Error loading template: {str(e)}</p>"

@app.get("/health")
async def health_check():
    """Health check endpoint for Render monitoring"""
    return {
        "status": "healthy",
        "service": "ComicCraft AI",
        "version": "1.0"
    }

@app.get("/api/status")
async def api_status():
    """API status endpoint"""
    return {
        "service": "ComicCraft AI API",
        "status": "running",
        "endpoints": {
            "generate-comic": "/api/generate-comic (POST)"
        }
    }
