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
    description="AI Comic Story Creator"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create directories
os.makedirs("static", exist_ok=True)
os.makedirs("static/panels", exist_ok=True)
os.makedirs("static/exports", exist_ok=True)
os.makedirs("templates", exist_ok=True)

# Mount static files
try:
    app.mount("/static", StaticFiles(directory="static"), name="static")
except:
    pass

# Templates
try:
    templates = Jinja2Templates(directory="templates")
except:
    templates = None

# Routes
app.include_router(router)

@app.get("/")
async def read_root():
    """Root endpoint"""
    if templates:
        try:
            return templates.TemplateResponse(
                "index.html",
                {"request": {}}
            )
        except:
            pass
    return {"message": "ComicCraft AI API", "docs": "/docs"}

@app.get("/health")
async def health():
    """Health check"""
    return {"status": "ok", "service": "ComicCraft AI"}

@app.get("/api/info")
async def api_info():
    """API info"""
    return {
        "name": "ComicCraft AI",
        "version": "1.0",
        "endpoints": [
            "/api/generate-comic",
            "/api/generate-outline",
            "/api/generate-story",
            "/api/status"
        ]
    }
