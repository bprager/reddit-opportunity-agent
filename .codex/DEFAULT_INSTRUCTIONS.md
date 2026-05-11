# Default Instructions

## Operating Mode

- Keep the project human-in-the-loop.
- Preserve the no-spam and no-auto-outreach rules.
- Prefer small, testable changes.
- Use the existing Python package layout unless a documented decision changes it.
- Update documentation when behavior, architecture, or policy changes.
- Run available checks before reporting work as complete.

## Required Context Before Changes

Read these files before meaningful project work:

- `README.md`
- `Docs/architecture.md`
- `Docs/adaptive_learning.md`
- `Docs/chatgpt_codex_review.md`
- `.codex/STATUS.md`
- `.codex/QUESTIONS.md`

## Verification

Use the strongest practical check for the change:

- Documentation-only changes: inspect generated files and run a Markdown sanity check when available.
- Python changes: run `make check`.
- Behavior changes: add or update tests before changing the implementation.
- Dashboard changes: run and view the dashboard when practical.

## Communication

Final reports to Bernd should be plain, clear English. Avoid unnecessary implementation detail and avoid assuming he has the code open.

## Preference Memory

At the start of substantial work, retrieve global and project preferences through the persist-preferences skill. If Bernd states a durable project preference, save it and sync the local preference mirror before finishing.

