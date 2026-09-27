from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes import router

app = FastAPI(
    title="ComicCraft AI", 
    description="Automated AI Comic Story Creator using Gemini & Stable Diffusion", 
    version="1.0"
)

# Mount static files folder to serve generated images and PDFs
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routing endpoints
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)