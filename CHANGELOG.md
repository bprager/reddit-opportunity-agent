<!-- markdownlint-disable MD024 -->
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

No unreleased changes yet.

## [0.2.0] - 2026-05-13

### Changed

- Clustered the backlog into phased work with story point estimates and progress reporting.
- Accepted Phase 1 architecture defaults and updated the decision records.
- Reframed Phase 6 around source-agnostic acquisition so Reddit API approval is no longer a blocking assumption.
- Updated the README and architecture docs to describe swappable acquisition adapters.
- Accepted ADR 0007 for source-agnostic acquisition adapters.

### Added

- Added regression example fixtures and a lightweight `make test` command.
- Recorded the workflow preference to recommend the next best step after each completed task.
- Added rules-first classifier tests and initial classifier behavior for the regression examples.
- Added explainable score-breakdown tests and initial scorer behavior for the regression examples.
- Added SQLite persistence tests and storage for assessed opportunities, score details, risk flags, and human decisions.
- Added query helpers for open review queues and decision history.
- Connected the daily briefing to stored assessments.
- Replaced the dashboard placeholder with data-backed review queues and decision controls.
- Added missed-opportunity, source-candidate, and learning-event storage.
- Added weekly learning report generation.
- Added dry-run Reddit collection, the assessment pipeline, and a local `make dry-run` command.
- Added a PRAW-backed Reddit collector boundary with safe missing-credential reporting.
- Added a bounded live read-only smoke-test command for approved subreddits.
- Added source acquisition research notes and ADR 0007 for source-agnostic adapters.
- Added a source registry, canonical source item model, generic RSS adapter, RSS CLI path, and RSS fixture tests.
- Added a pre-commit quality gate for Python linting, Markdown linting, and minimum 96% Python test coverage.

### Fixed

- Prevented repeated collection of the same Reddit item from creating duplicate review records.
- Made settings ignore unrelated `.env` entries so local secret variables do not break app startup.
- Closed SQLite connections reliably after store operations.

## [0.1.0] - 2026-05-11

### Added

- Initialized project changelog.
- Added `.codex/` project memory documents for goals, constraints, policies, decisions, questions, status, design, and lessons learned.
- Added expanded architecture documentation and architecture decision records.
- Added `TODO.md` and updated the Codex handoff target to include the new project memory documents.
- Ignored generated review reports while keeping source documentation visible to Git.

### Changed

- Reworked `README.md` into a compact GitHub project overview and status page.

### Fixed

- Updated the briefing timestamp to avoid deprecated UTC datetime usage.
