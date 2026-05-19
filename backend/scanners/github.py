import httpx

def check_github(username: str):
    url = f"https://api.github.com/users/{username}"

    response = httpx.get(url)

    if response.status_code == 200:
        data = response.json()

        return {
            "exists": True,
            "name": data.get("name"),
            "public_repos": data.get("public_repos"),
            "followers": data.get("followers"),
            "profile_url": data.get("html_url")
        }

    return {
        "exists": False
    }
