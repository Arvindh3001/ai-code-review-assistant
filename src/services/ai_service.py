import json
from groq import AsyncGroq
from src.config import GROQ_API_KEY, GROQ_MODEL
from src.models.review import ReviewIssue, ReviewResult

client = AsyncGroq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = """You are an expert code reviewer with deep knowledge of security vulnerabilities,
software architecture, and best practices. Your job is to analyze Pull Request diffs and provide
precise, actionable feedback.

You must respond ONLY with a valid JSON object in this exact format:
{
  "summary": "A concise 2-3 sentence overall assessment of the PR.",
  "issues": [
    {
      "file": "path/to/file.py",
      "line": <line number from the diff where the issue occurs>,
      "severity": "<critical|high|medium|low|info>",
      "category": "<security|logic|performance|style|architecture>",
      "description": "Clear explanation of the problem.",
      "suggestion": "Concrete fix or improvement."
    }
  ]
}

Severity guide:
- critical: Security vulnerabilities, data loss risks, crashes
- high: Logic errors, significant bugs, broken functionality
- medium: Performance issues, poor practices that will cause future problems
- low: Minor style or readability issues
- info: Suggestions and best practices

If there are no issues, return an empty issues array. Do not include markdown, only raw JSON."""


def _build_user_prompt(pr_title: str, files: list[dict]) -> str:
    file_sections = []
    for f in files:
        file_sections.append(
            f"### File: {f['filename']} ({f['status']})\n```diff\n{f['patch']}\n```"
        )
    diff_text = "\n\n".join(file_sections)
    return f"Review this Pull Request titled: \"{pr_title}\"\n\n{diff_text}"


async def review_code(pr_title: str, pr_number: int, files: list[dict]) -> ReviewResult:
    user_prompt = _build_user_prompt(pr_title, files)

    response = await client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.2,  # low temperature for consistent, precise output
        max_tokens=4096,
    )

    raw = response.choices[0].message.content.strip()

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        # If the model wrapped JSON in markdown code fences, strip them
        if "```" in raw:
            raw = raw.split("```")[1].lstrip("json").strip()
        data = json.loads(raw)

    issues = [ReviewIssue(**issue) for issue in data.get("issues", [])]
    return ReviewResult(
        pr_number=pr_number,
        summary=data.get("summary", ""),
        issues=issues,
    )
