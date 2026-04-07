import httpx
from src.config import GITHUB_APP_TOKEN
from src.models.review import ReviewResult

GITHUB_API = "https://api.github.com"

HEADERS = {
    "Authorization": f"Bearer {GITHUB_APP_TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}

SEVERITY_EMOJI = {
    "critical": "🔴",
    "high": "🟠",
    "medium": "🟡",
    "low": "🔵",
    "info": "⚪",
}


def _format_comment(issue) -> str:
    emoji = SEVERITY_EMOJI.get(issue.severity, "⚪")
    return (
        f"{emoji} **[{issue.severity.upper()}] {issue.category.capitalize()} Issue**\n\n"
        f"{issue.description}\n\n"
        f"**Suggestion:** {issue.suggestion}"
    )


async def post_review_comments(
    owner: str, repo: str, pr_number: int, result: ReviewResult
) -> None:
    """
    Posts the AI review as a GitHub Pull Request Review with inline comments.
    If no issues are found, posts a simple approval comment.
    """
    url = f"{GITHUB_API}/repos/{owner}/{repo}/pulls/{pr_number}/reviews"

    inline_comments = [
        {
            "path": issue.file,
            "line": issue.line,
            "body": _format_comment(issue),
        }
        for issue in result.issues
    ]

    summary_body = (
        f"## AI Code Review\n\n"
        f"**Summary:** {result.summary}\n\n"
        f"**Issues found:** {len(result.issues)}"
    )

    payload = {
        "body": summary_body,
        "event": "COMMENT",
        "comments": inline_comments,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=HEADERS, json=payload)
        response.raise_for_status()
