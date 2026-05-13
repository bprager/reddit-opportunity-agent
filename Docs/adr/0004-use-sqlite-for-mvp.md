# ADR 0004: Use SQLite For the MVP

Date: 2026-05-11

Status: Accepted

## Context

The project is currently local and single-user. The initial job is to collect, classify, score, review, and learn from Reddit opportunities. The repository already has `DATABASE_URL=sqlite:///./reddit_radar.db` in `.env.example`.

## Decision

Use SQLite for the MVP, accessed through SQLModel. Move to Postgres when hosted deployment, concurrent workers, multi-user access, or stronger operational tooling becomes necessary.

## Consequences

- Local setup stays lightweight.
- Early schema work can happen without infrastructure overhead.
- Migration discipline is still needed if the data model changes.
- Postgres remains a later migration when hosted deployment, concurrent workers, or multi-user access requires it.
