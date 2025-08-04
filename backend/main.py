from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import string
import random

app = FastAPI()

# ✅ CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

url_db = {}

class URLRequest(BaseModel):
    original_url: str

def generate_short_code():
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(6))

@app.get("/")
def home():
    return {"status": "Ready to shorten URLs!"}

@app.post("/shorten")
def create_short_url(url: URLRequest):
    short_code = generate_short_code()
    url_db[short_code] = url.original_url
    return {"short_url": f"http://localhost:8001/{short_code}"}

@app.get("/{short_code}")
def redirect_url(short_code: str):
    if short_code not in url_db:
        raise HTTPException(status_code=404)
    return RedirectResponse(url_db[short_code])
