# Reddit Opportunity Radar

Research assistant for finding high-signal public-source opportunities without automating outreach.

The project monitors selected communities and feeds, classifies posts, scores fit and risk, and produces a daily review queue for Bernd to decide what is worth pursuing. Reddit remains the first source family, but ingestion is being redesigned so RSS, Hacker News, Lobsters, GitHub Discussions, manual feeds, and the official Reddit API can plug into the same pipeline.

## Status

Version 0.2.0 release candidate. Early local MVP.

- Product direction and architecture are documented.
- Python package exists under `src/reddit_radar/`.
- Rules-first classification, scoring, persistence, briefings, dashboard sections, and learning reports have initial tests.
- Dry-run collection and a bounded Reddit API smoke-test command exist.
- Source-agnostic acquisition has started: a source registry, canonical source item model, generic RSS adapter, and RSS command path exist.
- Commits are protected by Python linting, Markdown linting, and 96% minimum Python test coverage.
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
- Source registry plus swappable acquisition adapters
- Generic RSS and public-source adapters while Reddit API approval is pending
- Reddit API access through PRAW when credentials are issued
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

Generate a daily briefing and Codex handoff:

```sh
make codex-context
```

Generated reports are written under `reports/`.

Run a bounded RSS source collection:

```sh
PYTHONPATH=src python -m reddit_radar.runner \
  --rss-source example=https://example.com/feed.xml \
  --limit 10
```

## Repository Map

```text
.
|-- src/reddit_radar/        # Python package skeleton
|-- Docs/                    # Product, architecture, and review docs
|-- Docs/adr/                # Architecture decision records
|-- Docs/source_acquisition.md # Source acquisition design
|-- .codex/                  # Codex project memory and working context
|-- CHANGELOG.md             # Project change history
|-- TODO.md                  # Current work queue
|-- Makefile                 # Local checks and handoff generation
`-- pyproject.toml           # Python package metadata
```

## First Milestone

The first useful version should answer:

> What are the 20 best public-source opportunities today, why are they worth looking at, and what should Bernd do next?

## Key Docs

- [Architecture](Docs/architecture.md)
- [Source acquisition design](Docs/source_acquisition.md)
- [Adaptive learning design](Docs/adaptive_learning.md)
- [ChatGPT and Codex review workflow](Docs/chatgpt_codex_review.md)
- [Architecture decisions](Docs/adr/README.md)
- [Codex project memory](.codex/README.md)
- [Changelog](CHANGELOG.md)
