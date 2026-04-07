# Implementation Plan: AI-Powered Code Review Assistant

This document outlines the phased implementation of a deep-analysis AI engine for automated code reviews, integrating with GitHub/GitLab to provide context-aware feedback.

## User Review Required

> [!IMPORTANT]
> The initial focus will be on a **Python (FastAPI)** backend and **GitHub** integration.
> 
> [!WARNING]
> Phase 4 (RAG) requires a Vector Database (e.g., Pinecone or Weaviate). Please confirm if you have a preference for the database or if we should use a local FAISS instance for starters.

## Proposed Changes

### Phase 1: MVP (Basic Working System)
**Goal:** Establish the end-to-end pipeline from PR creation to AI feedback.

- **[NEW] Webhook Listener:** Create an endpoint to receive and validate GitHub `pull_request` events.
- **[NEW] Code Fetcher:** Implement logic to fetch PR diffs and content using the GitHub REST API.
- **[NEW] AI Core Service:** Orchestrate calls to an LLM (GPT-4 or Gemini) with a tailored system prompt for code review.
- **[NEW] PR Commenter:** Logic to post AI-generated suggestions as inline comments on the GitHub PR.

---

### Phase 2: Context-Aware Review
**Goal:** Improve review quality by providing the AI with more than just the diff.

- **[NEW] Context Manager:** Logic to fetch related files (e.g., source of imported classes) to provide broader context.
- **[MODIFY] AI Prompts:** Shift to structured JSON outputs (issue category, severity, line number, suggested fix).
- **[NEW] Analysis Engine:** Support for multi-file analysis and dependency graph awareness.

---

### Phase 3: Dashboard & Analytics
**Goal:** Provide visibility into team code quality and tool effectiveness.

- **[NEW] Database Layer:** Set up PostgreSQL to store PR metadata, detected issues, and "Accept/Reject" feedback.
- **[NEW] Analytics API:** Endpoints to aggregate data for trends (e.g., "Most frequent security smells").
- **[NEW] Dashboard UI (React + Tailwind):** A premium interface visualizing:
    - Recent PR reviews and their risk scores.
    - Charts of issue categories over time.
    - Repository health overview.

---

### Phase 4: Advanced Intelligence (Production-Grade)
**Goal:** Reach enterprise-level accuracy and depth.

- **[NEW] RAG Pipeline:** Index the entire repository into a Vector DB to provide the LLM with full codebase context.
- **[NEW] Static Analysis Shield:** Integrate tools like `Bandit` or `ESLint` to cross-verify AI suggestions and reduce false positives.
- **[NEW] Adaptive Learning:** Use stored developer feedback to "tune" future prompts or context retrieval hits.

---

### Phase 5: Multi-Platform & Scaling
**Goal:** Expand the ecosystem and ensure performance.

- **[NEW] Multi-Platform Support:** Add integration for GitLab and Bitbucket via a provider abstraction layer.
- **[MODIFY] Task Queue:** Implement Celery/Redis for asynchronous, parallel processing of large PRs.
- **[NEW] Deployment:** Dockerize the entire stack for easy "One-Click" deployment or SaaS hosting.

## Open Questions

1. **LLM Provider:** Should we start with **OpenAI (GPT-4o)** or **Google (Gemini 1.5 Pro)**? 
2. **Database:** For the Vector DB in Phase 4, do you prefer a managed service (Pinecone) or self-hosted (Chromadb/FAISS)?
3. **Primary Languages:** Which programming languages should we optimize the initial prompts for? (e.g., Python, Javascript, Go).

## Verification Plan

### Automated Tests
- Unit tests for the Webhook and API logic using `pytest`.
- Integration tests simulating a GitHub PR event and verifying the outgoing AI request.

### Manual Verification
- Creating a test PR in a private repo with known vulnerabilities (e.g., hardcoded credentials) and checking if the AI identifies them.
- Visual check of the Dashboard UI for correct data representation.
