from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sherlock_runner import run_sherlock

app = FastAPI(title="Digital Footprint Scanner")

# Allow the React frontend (localhost:5173) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ScanRequest(BaseModel):
    username: str

class ScanResult(BaseModel):
    platform: str
    url: str
    status: str

@app.get("/")
def health_check():
    return {"status": "ok"}

@app.post("/api/scan", response_model=list[ScanResult])
async def scan_username(request: ScanRequest):
    username = request.username.strip()

    if not username or len(username) < 2:
        raise HTTPException(status_code=400, detail="Username too short")
    if len(username) > 50:
        raise HTTPException(status_code=400, detail="Username too long")

    results = await run_sherlock(username)
    return results
