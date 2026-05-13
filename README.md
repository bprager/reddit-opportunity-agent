# Reddit Opportunity Radar

Research assistant for finding high-signal Reddit opportunities without automating outreach.

The project monitors selected Reddit communities, classifies posts, scores fit and risk, and produces a daily review queue for Bernd to decide what is worth pursuing.

## Status

Early MVP scaffold.

- Product direction and architecture are documented.
- Python package skeleton exists under `src/reddit_radar/`.
- Data models exist for Reddit items, assessments, missed opportunities, source candidates, and learning events.
- Collector, classifier, scorer, briefing, and dashboard are still mostly placeholders.
- No outreach automation exists, by design.

## What It Does

- Tracks local client signals and remote software/AI opportunities.
- Scores items for fit, seriousness, budget signal, risk, and expected value.
- Generates review notes and draft replies for human approval.
- Records decisions, misses, source ideas, and learning events.
- Produces Markdown handoffs for ChatGPT, Codex, and future OpenClaw tools.

## What It Will Not Do

- No automated DMs.
- No mass posting.
- No automatic applications.
- No scraping that ignores Reddit rules or limits.
- No misleading claims or fake human behavior.

Human approval is required before any external reply, application, or follow-up.

## Current Architecture

The recommended MVP is a local-first Python modular monolith:

- Python 3.12+
- Reddit API access through PRAW or direct OAuth API calls
- SQLite for the first local database
- SQLModel and Pydantic for structured data
- Rules-first classification and scoring, with optional LLM support later
- Streamlit for the first dashboard
- Markdown reports for review and Codex handoff

See [Docs/architecture.md](Docs/architecture.md) for the full architecture and PlantUML diagrams.

## Quick Start

```sh
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
make check
```

Commits run the same quality gate through `.githooks/pre-commit`. Run `uv sync --extra dev` once
to install the development tools; each commit must pass Python linting, Markdown linting, and at
least 96% Python test coverage.

Generate a placeholder daily briefing and Codex handoff:

```sh
make codex-context
```

Generated reports are written under `reports/`.

## Repository Map

```text
.
|-- src/reddit_radar/        # Python package skeleton
|-- Docs/                    # Product, architecture, and review docs
|-- Docs/adr/                # Architecture decision records
|-- .codex/                  # Codex project memory and working context
|-- CHANGELOG.md             # Project change history
|-- TODO.md                  # Current work queue
|-- Makefile                 # Local checks and handoff generation
`-- pyproject.toml           # Python package metadata
```

## First Milestone

The first useful version should answer:

> What are the 20 best Reddit opportunities today, why are they worth looking at, and what should Bernd do next?

## Key Docs

- [Architecture](Docs/architecture.md)
- [Adaptive learning design](Docs/adaptive_learning.md)
- [ChatGPT and Codex review workflow](Docs/chatgpt_codex_review.md)
- [Architecture decisions](Docs/adr/README.md)
- [Codex project memory](.codex/README.md)
- [Changelog](CHANGELOG.md)
