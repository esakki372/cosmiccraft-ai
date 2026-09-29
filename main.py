from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.routes import router

app = FastAPI(
    title="ComicCraft AI",
    version="1.0"
)

# Template configuration
templates = Jinja2Templates(directory="templates")

# Include API routes
app.include_router(router)


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )