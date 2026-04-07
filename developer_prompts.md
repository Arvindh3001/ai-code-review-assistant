# Developer Prompts: AI-Powered Code Review Assistant

This document provides a set of highly-engineered prompts to guide the development process. Use these prompts sequentially to build the project from MVP to a production-ready system.

---

## 🛠️ Phase 1: MVP & Core Infrastructure

### Prompt 1: Project Initialization
> "Initialize a FastAPI project for an 'AI-Powered Code Review Assistant'. Set up a clean directory structure with a `src/` folder, a `.env` for API keys, and a `docker-compose.yml` for local development. Include a `main.py` with a health-check endpoint."

### Prompt 2: GitHub Webhook Listener
> "Implement a POST endpoint `/webhook/github` in FastAPI that validates GitHub HMAC signatures. It should parse `pull_request` events and extract the repository URL, PR number, and commit SHA. Log the received events using a structured logger."

### Prompt 3: Code Fetching Service
> "Create a service using `httpx` or `PyGithub` to fetch the diff of a specific GitHub Pull Request. Ensure it handles authentication via a GitHub App token or Personal Access Token (PAT). Store the diff as a string for now."

---

## 🧠 Phase 2: AI Review Core & Context Awareness

### Prompt 4: AI Analysis Orchestrator
> "Implement an `AIReviewService` that takes a code diff and sends it to an LLM (e.g., GPT-4o or Gemini). Craft a system prompt that instructs the AI to identify: Logical errors, Security vulnerabilities (SQLi, XSS), Performance bottlenecks, and Code smells. Ensure the output is valid JSON."

### Prompt 5: Inline PR Commenter
> "Build a service to post comments back to GitHub. It should take the JSON output from the AI service and map each suggestion to a specific line and file in the Pull Request using the GitHub Reviews API (`POST /repos/{owner}/{repo}/pulls/{pull_number}/reviews`)."

---

## 📊 Phase 3: Dashboard & Analytics

### Prompt 6: Database & Persistence
> "Set up a PostgreSQL database using SQLAlchemy (async). Design schemas for `Repositories`, `PullRequests`, and `Issues`. Implement logic to save every AI-generated review into the database for future analytics."

### Prompt 7: Frontend Visualization (React + Tailwind)
> "Create a React dashboard to visualize code quality trends. Use Tailwind CSS for a premium, dark-mode aesthetic. Display a list of recent PRs with a 'Risk Score' (0-100) and bar charts showing the most common issue categories (e.g., Security vs. Style)."

---

## 🚀 Phase 4: Advanced Intelligence (RAG)

### Prompt 8: Vector Indexing with RAG
> "Implement a background task using Celery and ChromaDB/FAISS. When a new repository is added, it should traverse the entire codebase, chunk the files, and store embeddings. Use these embeddings to provide the LLM with full repository context during its next PR review."

---

## 🌍 Phase 5: Multi-Platform Scaling

### Prompt 9: Provider Abstraction Layer
> "Refactor the Git interaction logic into a Provider Interface (Abstract Base Class). Implement concrete classes for `GitHubProvider` and `GitLabProvider`, allowing the system to easily switch between platforms without changing the core analysis logic."
