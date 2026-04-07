# AI-Powered Code Review Assistant

> An automated code review system that integrates with GitHub to analyze Pull Requests using LLMs — catching security vulnerabilities, logic errors, and architectural issues before they reach production.

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111.0-009688?logo=fastapi&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-LLaMA%203.3%2070B-orange)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

---

## What It Does

When a developer opens a Pull Request on GitHub, this system automatically:

1. Receives a GitHub webhook event
2. Fetches the PR diff via the GitHub REST API
3. Sends the code to **Groq (LLaMA 3.3 70B)** with a code-review prompt
4. Parses the AI response into structured issues (severity, category, line number, fix)
5. Posts inline review comments directly on the GitHub PR

No new tools for the developer — the review appears inside their normal GitHub workflow.

---

## Demo

```
PR Opened by Developer
        ↓
GitHub → POST /webhook/github
        ↓
HMAC Signature Verified
        ↓
Diff Fetched from GitHub API
        ↓
Groq AI (LLaMA 3.3 70B) Reviews Code
        ↓
Inline Comments Posted on PR
```

**Example AI comment on a PR:**

> 🔴 **[CRITICAL] Security Issue**
>
> Hardcoded password detected in the authentication function.
>
> **Suggestion:** Use environment variables or a secrets manager instead of inline credentials.

---

## Features

- **HMAC-SHA256 Webhook Verification** — only processes genuine GitHub events
- **Background Processing** — returns 202 immediately, reviews asynchronously (no timeouts)
- **Structured AI Output** — each issue has a file, line number, severity, category, description, and suggestion
- **Severity Levels** — Critical / High / Medium / Low / Info with emoji indicators
- **Issue Categories** — Security / Logic / Performance / Style / Architecture
- **Ping Handler** — responds correctly to GitHub's initial webhook test ping
- **Docker Ready** — single command to spin up the entire stack

---

## Tech Stack

| | Technology |
|---|---|
| **Framework** | FastAPI + Uvicorn |
| **AI Model** | LLaMA 3.3 70B via Groq API |
| **GitHub Integration** | GitHub REST API v3 |
| **HTTP Client** | httpx (async) |
| **Config** | python-dotenv |
| **Container** | Docker + Docker Compose |

---

## Project Structure

```
├── src/
│   ├── main.py                  # App entry point, logging, router registration
│   ├── config.py                # Environment variable loader
│   ├── routers/
│   │   └── webhook.py           # POST /webhook/github — HMAC validation + event dispatch
│   ├── services/
│   │   ├── github_service.py    # Fetches PR diffs from GitHub API
│   │   ├── ai_service.py        # Groq API integration + prompt engineering
│   │   └── commenter.py         # Posts inline review comments to GitHub
│   └── models/
│       └── review.py            # Pydantic models: ReviewIssue, ReviewResult
├── tests/
├── .env                         # Secrets (gitignored)
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```

---

## Getting Started

### Prerequisites

- Python 3.11+
- A [Groq API key](https://console.groq.com) (free tier available)
- A GitHub Personal Access Token with `repo` scope
- [ngrok](https://ngrok.com) for local webhook testing

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO
```

### 2. Set up environment variables

```bash
cp .env.example .env   # or create .env manually
```

Fill in your `.env`:
```env
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxx
GITHUB_APP_TOKEN=github_pat_xxxxxxxxxxxxxxxxxxxx
GITHUB_WEBHOOK_SECRET=your_secret_string
```

### 3. Run with Python

```bash
python -m venv .venv
# Windows:
.venv\Scripts\Activate.ps1
# Mac/Linux:
source .venv/bin/activate

pip install -r requirements.txt
uvicorn src.main:app --reload --port 8000
```

### 4. Run with Docker

```bash
docker-compose up --build
```

### 5. Verify

```bash
curl http://localhost:8000/health
# {"status": "active", "version": "0.1.0"}
```

---

## Connecting to GitHub

### Expose your local server

```bash
ngrok http 8000
# Copy the https://xxxx.ngrok-free.app URL
```

### Add the webhook on GitHub

1. Go to your repo → **Settings → Webhooks → Add webhook**
2. Set:
   - **Payload URL:** `https://xxxx.ngrok-free.app/webhook/github`
   - **Content type:** `application/json`
   - **Secret:** value of `GITHUB_WEBHOOK_SECRET` from your `.env`
   - **Events:** Pull requests only
3. Click **Add webhook** — GitHub will send a ping and you should see a green checkmark

Now open a PR in the repo and watch the AI review appear.

---

## API Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Health check |
| `POST` | `/webhook/github` | GitHub webhook receiver |

### Webhook responses

| Scenario | Status |
|---|---|
| PR opened / pushed to / reopened | `202 Accepted` |
| GitHub ping event | `200 OK` |
| Unhandled event or action | `200 OK` (ignored) |
| Invalid signature | `401 Unauthorized` |

---

## Roadmap

- [x] **Phase 1** — Webhook listener, GitHub diff fetcher, Groq AI review, PR commenter
- [ ] **Phase 2** — Context-aware review (multi-file analysis, related file fetching)
- [ ] **Phase 3** — Dashboard & analytics (PostgreSQL, React UI, trend charts)
- [ ] **Phase 4** — RAG pipeline (full codebase indexing, static analysis integration)
- [ ] **Phase 5** — Multi-platform support (GitLab, Bitbucket) + production scaling

---

## Environment Variables

| Variable | Description |
|---|---|
| `GROQ_API_KEY` | Groq API key for LLM inference |
| `GITHUB_APP_TOKEN` | GitHub PAT with `repo` scope |
| `GITHUB_WEBHOOK_SECRET` | Secret for validating GitHub webhook signatures |

---

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add your feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

---

## License

This project is licensed under the MIT License.
