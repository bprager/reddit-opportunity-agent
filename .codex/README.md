# Codex Project Memory

This directory is the working memory for Codex sessions on Reddit Opportunity Radar.
It summarizes the product intent, guardrails, decisions, and current status so future
work can start from a shared project picture.

## Read Order

1. `DEFAULT_INSTRUCTIONS.md`
2. `GOALS.md`
3. `CONSTRAINTS.md`
4. `POLICIES.md`
5. `Design.md`
6. `DECISIONS.md`
7. `QUESTIONS.md`
8. `STATUS.md`
9. `LESSONS_LEARNED.md`

## Canonical Project Documents

- `README.md` is the product overview and high-level behavior contract.
- `Docs/architecture.md` is the current architecture reference.
- `Docs/adaptive_learning.md` explains outcome learning, missed opportunities, source discovery, and prompt evolution.
- `Docs/chatgpt_codex_review.md` explains the review and handoff loop.
- `Docs/adr/` contains architecture decision records.
- `CHANGELOG.md` records notable project changes.

## Maintenance Rule

When a Codex session changes project direction, architecture, workflow, or policy:

- Update the relevant `.codex/` document.
- Update `Docs/architecture.md` if the system shape changes.
- Add or update an ADR in `Docs/adr/` for important architecture decisions.
- Add a `CHANGELOG.md` entry when the change is notable.

