# app/main.py
from fastapi import FastAPI
from app.routes import router

app = FastAPI(
    title="News Processing API",
    description="Fetches news from The Guardian, classifies with HuggingFace, and saves to SOMEE DB",
    version="1.0.0"
)

# חיבור ה־routes
app.include_router(router)


# Route ל-root
@app.get("/")
def read_root():
    return {"message": "API is running"}