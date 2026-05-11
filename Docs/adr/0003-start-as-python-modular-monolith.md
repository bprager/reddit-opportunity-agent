# ADR 0003: Start As a Python Modular Monolith

Date: 2026-05-11

Status: Proposed

## Context

The repository already uses a Python package layout with modules for configuration, models, collection, classification, scoring, briefing, and dashboard. The product needs fast iteration before API and deployment complexity are useful.

## Decision

Start the MVP as a Python modular monolith with clear internal module boundaries:

- Collection.
- Persistence.
- Classification.
- Scoring.
- Risk detection.
- Draft generation.
- Dashboard and reports.
- Learning loop.

FastAPI and OpenClaw tools should be added after the daily review queue and learning loop prove useful.

## Consequences

- The first version stays simple to run locally.
- Module boundaries remain ready for later API extraction.
- The project avoids premature service splitting.
- Bernd should confirm whether local-first is acceptable before implementation proceeds.

