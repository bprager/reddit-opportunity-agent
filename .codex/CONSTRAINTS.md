# Constraints

## Product Constraints

- Do not automate direct messages.
- Do not mass-post replies.
- Do not bypass Reddit rules or rate limits.
- Do not pretend to be a human.
- Do not generate misleading claims about Bernd, his experience, or availability.
- Do not store unnecessary personal data.
- Keep human approval required before any outreach.

## Technical Constraints

- Start with Python 3.12.
- Keep the MVP small and understandable.
- Use SQLite for early local development unless a later ADR changes this.
- Keep Pydantic and SQLModel as the first structured data layer.
- Keep Streamlit as the first dashboard unless a later ADR changes this.
- Support future FastAPI and OpenClaw integration without requiring them for the MVP.

## Workflow Constraints

- Changes that affect architecture require `Docs/architecture.md` updates.
- Important decisions require an ADR in `Docs/adr/`.
- Scoring and prompt changes should be versioned or recorded as learning events.
- Prefer representative tests for classification, scoring, and risk rules.

