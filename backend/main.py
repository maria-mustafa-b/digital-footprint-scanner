from fastapi import FastAPI
from backend.scanners.username_scanner import scan_username

app = FastAPI(title="Digital Footprint Scanner")

@app.get("/")
def home():
    return {"message": "DFS API running"}

@app.get("/scan/{username}")
def scan(username: str):
    result = scan_username(username)
    return result
