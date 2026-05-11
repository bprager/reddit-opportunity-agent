# Decisions

This file is the short decision ledger. Full records live in `Docs/adr/`.

## Accepted

| Decision | Reason | Source |
| --- | --- | --- |
| Human approval is required before outreach | Prevents spam, misleading contact, and reputational risk | `README.md`, `Docs/architecture.md` |
| The system should produce a ranked review queue, not run outreach autonomously | Keeps Bernd in control | `README.md` |
| Collection, classification, scoring, risk detection, and drafting should be separate concerns | Each part can improve independently | `Docs/architecture.md` |
| Learning changes must be reviewable | Prevents silent rule drift | `Docs/adaptive_learning.md` |
| ChatGPT, Codex, and future OpenClaw review artifacts are part of the workflow | Supports iterative improvement | `Docs/chatgpt_codex_review.md` |

## Recommended Pending Decisions

| Decision | Recommendation | Why It Needs Confirmation |
| --- | --- | --- |
| MVP architecture shape | Start as a Python modular monolith with CLI jobs, SQLite, and Streamlit | It affects how much backend/API work happens now |
| First classifier strategy | Start with deterministic rules and regression examples before LLM calls | It affects cost, speed, and testability |
| Database migration point | Use SQLite first, move to Postgres when scheduling, multi-user, or deployment needs require it | It affects setup friction |
| Source expansion policy | Keep new sources as candidates until trialed and reviewed | It affects noise and maintenance |
| Outreach artifact scope | Generate drafts only, never send | It should be explicitly confirmed as permanent policy |

## Decision Process

1. Add an ADR for important architecture decisions.
2. Mark status as `Proposed`, `Accepted`, `Superseded`, or `Rejected`.
3. Link affected files.
4. Update this ledger.

