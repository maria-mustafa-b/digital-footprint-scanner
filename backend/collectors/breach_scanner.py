# backend/breach_scanner.py
import aiohttp
import os
from dotenv import load_dotenv

load_dotenv()
LEAKCHECK_KEY = os.getenv("LEAKCHECK_API_KEY")

async def check_email_breaches(email: str) -> list[dict]:
    """
    Query LeakCheck free tier for breach data.
    Free tier: 10 requests/day, no credit card.
    """
    url = f"https://leakcheck.io/api/public?check={email}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                if not data.get("success") or not data.get("found"):
                    return []
                return [
                    {
                        "name": source,
                        "domain": "",
                        "breach_date": "Unknown",
                        "pwn_count": 0,
                        "data_classes": ["Emails"],
                        "is_sensitive": False,
                        "is_verified": True,
                    }
                    for source in data.get("sources", [])
                ]
            return []


async def check_paste_exposure(email: str) -> list[dict]:
    # LeakCheck free tier doesn't include pastes
    # Return empty — paste scanning is a Phase 3+ feature
    return []
