# Lessons Learned

## 2026-05-11 Documentation Ingestion

- The project intent is clear: find opportunities, rank them, and keep Bernd in control.
- The strongest existing design constraint is ethical outreach control: no automated DMs, no mass posting, and no misleading claims.
- The current codebase is intentionally skeletal, so architecture documents should guide the first implementation rather than describe a finished system.
- Adaptive learning is a first-class product requirement, not a later analytics add-on.
- The ChatGPT/Codex review loop needs compact generated reports, not large raw data dumps.
- `Docs/` is the current directory name in the repository. The Codex handoff target now points to `Docs/`, but some descriptive text still references `docs/` and can be standardized later.
