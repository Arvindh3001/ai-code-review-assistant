from pydantic import BaseModel
from typing import Literal


class ReviewIssue(BaseModel):
    file: str
    line: int
    severity: Literal["critical", "high", "medium", "low", "info"]
    category: Literal["security", "logic", "performance", "style", "architecture"]
    description: str
    suggestion: str


class ReviewResult(BaseModel):
    pr_number: int
    summary: str
    issues: list[ReviewIssue]
