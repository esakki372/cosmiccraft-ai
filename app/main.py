from fastapi import FastAPI
from app.routes import router

app = FastAPI(title="ComicCraft AI", version="1.0")

app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "Welcome to ComicCraft AI API!"}