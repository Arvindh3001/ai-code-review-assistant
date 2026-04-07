# AI-Powered Code Review Assistant — Complete Guidebook

> Think of this as the owner's manual for the system. Everything from "why does this exist" to "how do I run it" is covered here. Read it top to bottom once, then use it as a reference.

---

## Table of Contents

1. [Problem Statement](#1-problem-statement)
2. [What This System Does](#2-what-this-system-does)
3. [How It Works — The Big Picture](#3-how-it-works--the-big-picture)
4. [Technology Stack](#4-technology-stack)
5. [Project Structure](#5-project-structure)
6. [Configuration & Environment Variables](#6-configuration--environment-variables)
7. [How to Run the Project](#7-how-to-run-the-project)
8. [API Endpoints](#8-api-endpoints)
9. [Phased Roadmap](#9-phased-roadmap)
10. [Key Concepts Explained](#10-key-concepts-explained)
11. [Glossary](#11-glossary)

---

## 1. Problem Statement

### The Pain of Modern Code Review

In any software team, code review is a critical quality gate — it is the last human checkpoint before code reaches production. However, the current state of code review is deeply flawed:

- **Reviewers are overloaded.** A senior engineer may receive 10–20 PRs per week to review on top of their own work. Reviews become rushed, superficial, or delayed.
- **Standard tools are shallow.** Linters (ESLint, Pylint, Flake8) only catch syntax and style violations. They cannot reason about *logic*, *intent*, or *architecture*.
- **Context is lost.** A reviewer looking at a diff of 200 lines has no visibility into how that change affects other files, classes, or services they cannot see.
- **Bugs slip through.** Security vulnerabilities (SQL injection, exposed secrets, broken authentication logic), performance regressions, and architectural violations are regularly missed because a tired human didn't catch them.
- **The feedback loop is slow.** A developer may wait 24–48 hours for a review, only to be told to fix something that an automated system could have flagged in seconds.

### The Opportunity

Large Language Models (LLMs) have demonstrated a remarkable ability to understand code — not just its syntax, but its meaning, its intent, and its risks. This project harnesses that capability to create an AI reviewer that:

- Works 24/7 with zero review fatigue
- Understands the *purpose* of a code change, not just its form
- Can be given full context (multiple files, not just the diff)
- Provides structured, actionable feedback with line-level precision
- Learns from developer feedback over time

---

## 2. What This System Does

The AI Code Review Assistant is a backend service that integrates directly with GitHub. When a developer opens or updates a Pull Request, the system automatically:

1. **Receives a notification** from GitHub (via a webhook event)
2. **Fetches the code changes** (the diff) and relevant surrounding files
3. **Sends the code to an LLM** (Groq-hosted models, e.g., LLaMA 3) with a carefully crafted review prompt
4. **Parses the AI's response** into structured feedback (issue category, severity, line number, suggested fix)
5. **Posts the feedback directly** as inline comments on the GitHub Pull Request

The developer sees the AI's review inside their normal GitHub workflow — no new tools, no context switching.

---

## 3. How It Works — The Big Picture

```
Developer opens a PR on GitHub
          |
          v
  GitHub sends a POST request (webhook) to our server
          |
          v
  [Webhook Listener] — validates the request is genuine (HMAC signature)
          |
          v
  [Code Fetcher] — calls GitHub API to get the PR diff + related files
          |
          v
  [AI Core Service] — builds a prompt and calls Groq API (LLaMA 3 / Mixtral)
          |
          v
  [Response Parser] — extracts structured issues from the AI response
          |
          v
  [PR Commenter] — posts inline comments back to the GitHub PR via GitHub API
          |
          v
  Developer sees AI review comments on their PR
```

Every component above is a discrete Python module, making the system easy to test and extend.

---

## 4. Technology Stack

| Layer | Technology | Why |
|---|---|---|
| **Web Framework** | FastAPI (Python) | Async-native, fast, auto-generates API docs, type-safe |
| **Server** | Uvicorn | ASGI server for FastAPI, production-grade |
| **LLM Provider** | Groq API | Ultra-fast inference on open models (LLaMA 3, Mixtral) — no GPU needed |
| **HTTP Client** | httpx | Async HTTP client for calling GitHub API |
| **GitHub Integration** | GitHub REST API v3 | Fetch PR diffs, post comments |
| **Environment Config** | python-dotenv | Load secrets from `.env` file safely |
| **Containerization** | Docker + Docker Compose | Reproducible local environment, easy deployment |
| **Testing** | pytest (planned) | Unit and integration tests |
| **Future DB** | PostgreSQL (Phase 3) | Store PR history, issue trends, feedback |
| **Future Queue** | Celery + Redis (Phase 5) | Async processing for large PRs |

---

## 5. Project Structure

```
AI Code Review Assistant/
│
├── src/                          # All core application code lives here
│   ├── __init__.py
│   ├── main.py                   # FastAPI app entry point, /health endpoint
│   ├── routers/                  # (Phase 1) API route handlers
│   │   └── webhook.py            # Receives GitHub pull_request events
│   ├── services/                 # Business logic layer
│   │   ├── github_service.py     # Fetches PR diffs from GitHub API
│   │   ├── ai_service.py         # Calls Groq API, builds prompts
│   │   └── commenter.py          # Posts review comments to GitHub
│   └── models/                   # Pydantic data models
│       └── review.py             # Structures for AI review output
│
├── tests/                        # All tests live here
│   ├── __init__.py
│   └── test_webhook.py           # (Phase 1) Tests for webhook validation
│
├── .env                          # Secret keys — NEVER commit this file
├── .gitignore                    # Prevents secrets and cache from being committed
├── requirements.txt              # Python package dependencies
├── Dockerfile                    # Defines how to build the app container
├── docker-compose.yml            # Orchestrates the container for local dev
├── implementation_plan.md        # Phased development roadmap
└── GUIDEBOOK.md                  # This file
```

> **Rule of thumb:** `src/routers/` handles *what comes in*, `src/services/` handles *what we do with it*.

---

## 6. Configuration & Environment Variables

All secrets and configuration live in the `.env` file at the project root. This file is **gitignored** and must never be committed to version control.

| Variable | Description | Where to Get It |
|---|---|---|
| `GROQ_API_KEY` | API key for Groq inference (LLaMA 3 / Mixtral) | console.groq.com → API Keys |
| `GITHUB_APP_TOKEN` | Personal Access Token to read PRs and post comments | GitHub → Settings → Developer Settings → Personal Access Tokens (Classic). Needs `repo` scope. |
| `GITHUB_WEBHOOK_SECRET` | A secret string used to verify that webhook events truly come from GitHub | You create this yourself (any random string). You will paste the same value into GitHub's webhook settings. |

### How to generate a strong webhook secret

Run this in your terminal:
```bash
openssl rand -hex 32
```
Copy the output into your `.env` and into GitHub's webhook configuration.

---

## 7. How to Run the Project

### Prerequisites

- Python 3.11+
- Docker Desktop (optional, but recommended)
- A GitHub account with a repository you control

### Option A — Run directly with Python

```bash
# Step 1: Create and activate a virtual environment
python -m venv .venv

# On Windows:
.venv\Scripts\activate
# On Mac/Linux:
source .venv/bin/activate

# Step 2: Install dependencies
pip install -r requirements.txt

# Step 3: Start the server
uvicorn src.main:app --reload --port 8000
```

The server will be live at `http://localhost:8000`.

### Option B — Run with Docker (recommended)

```bash
# Build the image and start the container
docker-compose up --build
```

The server will be live at `http://localhost:8000`. The `--reload` flag is active inside the container, so code changes are picked up automatically.

### Verify it's working

Open your browser or run:
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{"status": "active", "version": "0.1.0"}
```

You can also browse the **auto-generated API documentation** at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Exposing your local server to GitHub (for webhook testing)

GitHub needs a publicly accessible URL to send webhook events to. During development, use **ngrok** to create a tunnel:

```bash
# Install ngrok from ngrok.com, then:
ngrok http 8000
```

ngrok will give you a URL like `https://abc123.ngrok.io`. Use this as your webhook URL in GitHub settings.

---

## 8. API Endpoints

### Currently implemented

| Method | Path | Description |
|---|---|---|
| `GET` | `/health` | Health check — confirms the service is running |

### Planned (Phase 1)

| Method | Path | Description |
|---|---|---|
| `POST` | `/webhook/github` | Receives `pull_request` events from GitHub |

### Planned (Phase 3)

| Method | Path | Description |
|---|---|---|
| `GET` | `/reviews` | List all past PR reviews |
| `GET` | `/reviews/{pr_id}` | Get issues found for a specific PR |
| `GET` | `/analytics/trends` | Aggregated issue trends over time |

---

## 9. Phased Roadmap

### Phase 1 — Foundation & MVP (Current)
**Goal:** Get the end-to-end pipeline working for a single PR.

- [x] FastAPI project structure
- [x] Docker containerization
- [x] `/health` endpoint
- [ ] Webhook listener (`POST /webhook/github`) with HMAC validation
- [ ] GitHub service — fetch PR diff via GitHub API
- [ ] AI service — send diff to Groq, receive review
- [ ] Commenter service — post AI feedback as GitHub PR comments

**Outcome:** Open a PR → AI automatically comments on it.

---

### Phase 2 — Context-Aware Review
**Goal:** Give the AI more than just the diff so it can reason about the broader codebase.

- [ ] Context Manager — fetch imported files, related classes
- [ ] Multi-file analysis — send multiple files to the AI in one prompt
- [ ] Structured JSON output — issue category, severity, line number, suggested fix
- [ ] Improved prompt engineering for precision

**Outcome:** The AI understands not just *what changed* but *what it affects*.

---

### Phase 3 — Dashboard & Analytics
**Goal:** Make team code quality visible over time.

- [ ] PostgreSQL database — store PR reviews, issues, developer feedback
- [ ] Analytics API — trending issues, most vulnerable files, team health score
- [ ] React + Tailwind dashboard — charts, PR history, risk scores

**Outcome:** Engineering managers can see code quality trends at a glance.

---

### Phase 4 — Advanced Intelligence
**Goal:** Enterprise-level accuracy using the full codebase as context.

- [ ] RAG pipeline — index the entire repo into a Vector DB (ChromaDB/FAISS/Pinecone)
- [ ] At review time, retrieve the most relevant code chunks for the AI
- [ ] Static analysis integration — Bandit (Python security), ESLint (JS)
- [ ] Adaptive learning — use developer "Accept/Reject" feedback to tune prompts

**Outcome:** The AI has full codebase awareness, not just the diff.

---

### Phase 5 — Scale & Multi-Platform
**Goal:** Handle high volume and support more Git platforms.

- [ ] Celery + Redis task queue — async processing, no request timeouts on large PRs
- [ ] GitLab and Bitbucket support via provider abstraction layer
- [ ] Production deployment (cloud hosting, one-click Docker deployment)

**Outcome:** A production-grade SaaS-ready system.

---

## 10. Key Concepts Explained

### What is a Webhook?
A webhook is GitHub's way of notifying your server about events. When a developer opens a PR, GitHub sends an HTTP POST request to a URL you configure. Your server receives this, reads the event data, and acts on it. It's like subscribing to GitHub push notifications but for your server.

### What is HMAC Signature Validation?
When GitHub sends a webhook, it signs the request body using your `GITHUB_WEBHOOK_SECRET` and includes the signature in the request headers. Your server must verify this signature before processing the request. This prevents anyone else from sending fake webhook events to your server.

### What is a PR Diff?
A diff is a machine-readable description of exactly what changed in a file — which lines were added, which were removed, and the context around those changes. It is the primary input to the AI reviewer.

### What is Groq?
Groq is an AI inference company that provides extremely fast API access to open-source models like Meta's LLaMA 3 and Mistral's Mixtral. "Fast" here means tokens-per-second speeds 10–100x faster than typical cloud AI providers, making it ideal for near-real-time code review.

### What is RAG (Phase 4)?
Retrieval-Augmented Generation. Instead of sending the entire codebase to the AI (which is too large), you first index it into a vector database. At review time, you retrieve only the most relevant chunks and include them in the prompt. The AI gets precise, targeted context rather than noise.

---

## 11. Glossary

| Term | Meaning |
|---|---|
| **PR** | Pull Request — a proposed set of code changes on GitHub |
| **Diff** | The textual representation of what changed in a PR |
| **Webhook** | An HTTP callback — GitHub posts to your server when events happen |
| **HMAC** | Hash-based Message Authentication Code — used to verify webhook authenticity |
| **LLM** | Large Language Model — the AI that reads and reviews the code |
| **Groq** | AI inference provider used to run LLaMA 3 / Mixtral models |
| **FastAPI** | Python web framework used to build the backend API |
| **Uvicorn** | The ASGI web server that runs the FastAPI application |
| **ngrok** | Tool that creates a public URL tunnel to your localhost for testing |
| **RAG** | Retrieval-Augmented Generation — giving the AI targeted context from a large corpus |
| **Vector DB** | A database that stores embeddings for semantic similarity search (used in RAG) |
| **SDLC** | Software Development Lifecycle — the full process from design to deployment |
