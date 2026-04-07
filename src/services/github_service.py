import httpx
from src.config import GITHUB_APP_TOKEN

GITHUB_API = "https://api.github.com"

HEADERS = {
    "Authorization": f"Bearer {GITHUB_APP_TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}


async def fetch_pr_files(owner: str, repo: str, pr_number: int) -> list[dict]:
    """
    Returns a list of changed files in the PR.
    Each entry has: filename, status, patch (the diff), and raw_url.
    """
    url = f"{GITHUB_API}/repos/{owner}/{repo}/pulls/{pr_number}/files"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=HEADERS)
        response.raise_for_status()
        files = response.json()

    return [
        {
            "filename": f["filename"],
            "status": f["status"],        # added, modified, removed
            "patch": f.get("patch", ""),  # the actual diff — may be absent for binary files
        }
        for f in files
        if f.get("patch")  # skip binary/deleted files with no diff
    ]
