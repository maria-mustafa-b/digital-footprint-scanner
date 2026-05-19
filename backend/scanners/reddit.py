import httpx

def check_reddit(username: str):
    url = f"https://www.reddit.com/user/{username}/about.json"

    headers = {
        "User-Agent": "Mozilla/5.0 (DFS Project)"
    }

    response = httpx.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()["data"]

        return {
            "exists": True,
            "id": data.get("id"),
            "comment_karma": data.get("comment_karma"),
            "link_karma": data.get("link_karma"),
            "profile_url": f"https://www.reddit.com/user/{username}"
        }

    return {
        "exists": False
    }
