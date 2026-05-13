# TODO

Backlog estimates use story points for relative size, not exact hours. Current planning assumes the early project velocity is roughly 8-12 story points per focused working day because the repository is still in early MVP build-out.

## Phase 0: Foundation and Project Memory - 13 SP

Status: complete.

- Initialize README, changelog, `.codex/` memory, architecture docs, and ADRs.
- Add package skeleton, example environment file, Makefile, and placeholder briefing/dashboard modules.
- Keep generated reports ignored and project docs visible to Git.

## Phase 1: Architecture Decisions and Test Harness - 5 SP

Status: complete.

- Confirmed pending architecture questions in `.codex/QUESTIONS.md`.
- Updated ADR statuses after Bernd accepted proposed defaults.
- Added the first regression examples for classification, scoring, and rejection.
- Added a minimal test command for the examples.

## Phase 2: Rules-First Opportunity Engine - 21 SP

Status: complete.

- Implemented initial rules-first classification for local leads, remote opportunities, missed opportunities, ignored items, and rejects.
- Implemented initial risk detection for no-budget, equity-only, suspicious urgency, low-rate, free-work, crypto-heavy, Telegram-only, and WhatsApp-only posts.
- Implemented score breakdowns for local leads, remote opportunities, missed opportunities, ignored items, and rejects.
- Added tests for obvious wins, hard rejects, false positives, and false negatives.

## Phase 3: Persistence and Human Decisions - 13 SP

Status: complete.

- Added database initialization.
- Persisted collected items, assessments, score breakdowns, risk flags, and human decisions.
- Added decision labels for ignored, saved, replied, applied, follow-up, converted, rejected, false positive, and false negative.
- Added query helpers for open review queues and decision history.

## Phase 4: Briefing and Dashboard MVP - 13 SP

Status: complete.

- Connected the daily briefing to stored data.
- Replaced placeholder dashboard logic with local and remote opportunity queues.
- Added source link, score, risks, recommendation, and decision controls.
- Added rejected-item and follow-up views.
- Visual Streamlit verification is still pending.

## Phase 5: Learning Loop and Source Quality - 13 SP

Status: complete.

- Added missed-opportunity intake.
- Added source candidate tracking.
- Added learning event recording.
- Added weekly learning reports.
- Preserved the rule that scoring, source, and prompt changes need human approval.

## Phase 6: Source-Agnostic Acquisition and Operational Hardening - 34 SP

Status: complete for the local MVP. Live Reddit API verification remains queued until credentials
are configured.

- Add a dry-run collection path that can process fixture Reddit items.
- Add source definitions that separate what to monitor from how to acquire it.
- Add a canonical `SourceItem` shape independent of Reddit.
- Refactor collectors behind acquisition adapters.
- Add generic RSS ingestion for interim Reddit RSS and non-Reddit feeds.
- Add Hacker News and Lobsters as first non-Reddit proof points.
- Keep Reddit API collection through PRAW with credential validation.
- Add deduplication for repeated collected items.
- Add configuration validation and safer runtime errors.
- Add operational command for running a local dry-run review.
- Add a bounded live read-only command for approved subreddit smoke tests.
- Verify live Reddit collection after `REDDIT_CLIENT_ID` and `REDDIT_CLIENT_SECRET` are configured.
- Add source-level health reporting, rate-limit backoff, and disabled-source status.
- Add a shadow-run path for switching Reddit RSS sources to Reddit API sources.
- Prepare future FastAPI and OpenClaw integration boundaries.
- Keep the pre-commit lint and 96% coverage gate green as adapters are added.

## Post-MVP Follow-Up

- Visually verify the Streamlit dashboard with a dry-run database.
- Run the approved Reddit API smoke test after credentials are configured.
- Consider renaming the compatibility storage table from Reddit item to source item.
- Add GitHub Discussions if the current source mix does not produce enough quality leads.
