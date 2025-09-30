# app/main.py
# Import FastAPI framework and the router from the app_server module

from fastapi import FastAPI
from app_server.routes import router

# Initialize FastAPI application with metadata
app = FastAPI(
    title="News Processing API",  # The API title shown in documentation
    description="Fetches news from The Guardian, classifies with HuggingFace, and saves to SOMEE DB",  # A short description of the API
    version="1.0.0"  # API version
)

# Include the routes defined in the router
app.include_router(router)


# Define a root endpoint
@app.get("/")  # HTTP GET request at the root path
def read_root():
    return {"message": "API is running"}  # Simple response indicating that the API is up
