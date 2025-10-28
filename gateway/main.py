# gateway/main.py
from fastapi import FastAPI, Request
import httpx
import uvicorn

app = FastAPI(title="Gateway Service")

# URLs of the other services
APP_SERVER_URL = "http://localhost:8000"      # your application server
DISPLAY_SERVER_URL = "http://localhost:8001"  # your display server

@app.get("/")
def root():
    return {"gateway": "up and running"}

# Route POST requests to the application server
@app.post("/api/app/{path:path}")
async def forward_to_app(request: Request, path: str):
    data = await request.json()
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{APP_SERVER_URL}/{path}", json=data)
    return response.json()

# Route GET requests to the ui server
@app.get("/api/display/{path:path}")
async def forward_to_display(path: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{DISPLAY_SERVER_URL}/{path}")
    return response.json()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080)
