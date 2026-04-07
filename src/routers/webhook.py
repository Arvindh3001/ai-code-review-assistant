import hmac
import hashlib
import json
import logging

from fastapi import APIRouter, Request, HTTPException, BackgroundTasks

from src.config import GITHUB_WEBHOOK_SECRET
from src.services.github_service import fetch_pr_files
from src.services.ai_service import review_code
from src.services.commenter import post_review_comments

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/webhook", tags=["Webhook"])

# Only process these actions — ignore closed, labeled, etc.
HANDLED_ACTIONS = {"opened", "synchronize", "reopened"}


def _verify_signature(payload: bytes, signature_header: str) -> bool:
    """Validates the X-Hub-Signature-256 header sent by GitHub."""
    if not signature_header.startswith("sha256="):
        return False
    expected = "sha256=" + hmac.new(
        GITHUB_WEBHOOK_SECRET.encode(),
        payload,
        hashlib.sha256,
    ).hexdigest()
    return hmac.compare_digest(expected, signature_header)


async def _process_pull_request(
    owner: str, repo: str, pr_number: int, pr_title: str
) -> None:
    """Background task: fetch diff → AI review → post comments."""
    logger.info("Processing PR #%d in %s/%s", pr_number, owner, repo)
    try:
        files = await fetch_pr_files(owner, repo, pr_number)
        if not files:
            logger.info("PR #%d has no reviewable file changes.", pr_number)
            return

        result = await review_code(pr_title, pr_number, files)
        await post_review_comments(owner, repo, pr_number, result)
        logger.info(
            "Review posted for PR #%d — %d issue(s) found.", pr_number, len(result.issues)
        )
    except Exception:
        logger.exception("Failed to process PR #%d in %s/%s", pr_number, owner, repo)


@router.post("/github", status_code=202)
async def github_webhook(request: Request, background_tasks: BackgroundTasks):
    """
    Receives pull_request events from GitHub.
    Validates the HMAC signature, then triggers a background review.
    """
    payload = await request.body()
    signature = request.headers.get("X-Hub-Signature-256", "")

    if not _verify_signature(payload, signature):
        raise HTTPException(status_code=401, detail="Invalid webhook signature.")

    event_type = request.headers.get("X-GitHub-Event", "")
    if event_type != "pull_request":
        return {"status": "ignored", "reason": f"event '{event_type}' not handled"}

    data = json.loads(payload)
    action = data.get("action", "")

    if action not in HANDLED_ACTIONS:
        return {"status": "ignored", "reason": f"action '{action}' not handled"}

    pr = data["pull_request"]
    repo = data["repository"]

    background_tasks.add_task(
        _process_pull_request,
        owner=repo["owner"]["login"],
        repo=repo["name"],
        pr_number=pr["number"],
        pr_title=pr["title"],
    )

    return {"status": "accepted", "pr": pr["number"]}
