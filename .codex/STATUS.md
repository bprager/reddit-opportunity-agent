# Status

Last updated: 2026-05-11

## Current State

- Repository contains an early Python package under `src/reddit_radar/`.
- Product direction is described in `README.md`.
- Existing docs cover architecture notes, adaptive learning, and ChatGPT/Codex review workflow.
- Collector, classifier, scorer, and dashboard are placeholders.
- SQLModel entities exist for Reddit items, assessments, missed opportunities, source candidates, and learning events.
- `Makefile` has `check`, `briefing`, and `codex-context` targets.

## Current Documentation Work

- `.codex/` project memory has been initialized.
- `CHANGELOG.md` has been initialized.
- `Docs/architecture.md` has been expanded into the architecture reference.
- `Docs/adr/` has been initialized for decision records.
- `TODO.md` has been initialized with the next architecture and implementation work.
- `make codex-context` now includes the `.codex/` memory, architecture docs, and changelog.

## Known Gaps

- The current collector is not connected to Reddit yet.
- Classification and scoring are not implemented yet.
- The briefing generator writes a placeholder report.
- The dashboard is a placeholder.
- No tests exist yet.
- Important architecture choices still need Bernd's confirmation.

## Next Useful Work

1. Resolve the pending architecture questions.
2. Add regression examples for opportunity classification and rejection.
3. Implement a rules-first classifier and scorer.
4. Persist assessments and decisions in SQLite.
5. Connect the daily briefing to real stored data.
