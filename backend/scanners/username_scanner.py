from backend.scanners.github import check_github
from backend.scanners.reddit import check_reddit

def scan_username(username: str):
    github_data = check_github(username)
    reddit_data = check_reddit(username)

    platforms_found = []

    if github_data["exists"]:
        platforms_found.append("GitHub")

    if reddit_data["exists"]:
        platforms_found.append("Reddit")

    return {
        "username": username,
        "platforms_found": platforms_found,
        "details": {
            "github": github_data,
            "reddit": reddit_data
        }
    }
  
