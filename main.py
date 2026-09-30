from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router
import os

app = FastAPI(title="ComicCraft AI", version="1.0", description="AI Comic Story Creator")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("static/panels", exist_ok=True)
os.makedirs("static/exports", exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
app.include_router(router)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/health")
async def health():
    return {"status": "ok", "service": "ComicCraft AI"}

@app.get("/api/info")
async def api_info():
    return {
        "name": "ComicCraft AI",
        "version": "1.0",
        "endpoints": [
            "/api/generate-comic",
            "/api/generate-outline",
            "/api/generate-story",
            "/api/status",
        ],
    }
