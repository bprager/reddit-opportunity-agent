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
| MVP architecture is local-first Python modular monolith | Keeps the first version small and testable | `Docs/adr/0003-start-as-python-modular-monolith.md` |
| SQLite is the MVP database | Keeps setup lightweight until deployment needs grow | `Docs/adr/0004-use-sqlite-for-mvp.md` |
| Streamlit is the first dashboard | Speeds up the first review workflow | `Docs/adr/0006-phase-one-mvp-defaults.md` |
| Rules and regression examples come before LLM classification | Keeps scoring explainable and testable | `Docs/adr/0006-phase-one-mvp-defaults.md` |
| Remote opportunities come before local LA leads | Budget and work intent are easier to score first | `Docs/adr/0006-phase-one-mvp-defaults.md` |
| Initial remote expected-value threshold is about 200 USD per pursuit hour | Gives the scorer an explicit first cutoff | `Docs/adr/0006-phase-one-mvp-defaults.md` |
| Store minimal Reddit author metadata | Reduces privacy risk and unnecessary retention | `Docs/adr/0006-phase-one-mvp-defaults.md` |
| OpenClaw tools come after the daily queue works | Avoids premature integration work | `Docs/adr/0006-phase-one-mvp-defaults.md` |
| Use source-agnostic acquisition adapters | Keeps the project moving while Reddit API approval is pending and makes the later API switch a source configuration change | `Docs/adr/0007-source-agnostic-acquisition.md`, `Docs/source_acquisition.md` |
| Keep Reddit JSON endpoints disabled or `needs_review` by default | Avoids treating a convenient endpoint as a policy workaround | `Docs/adr/0007-source-agnostic-acquisition.md` |

## Remaining Product Decisions

| Decision | Current Direction | Why It Remains Open |
| --- | --- | --- |
| Source expansion policy | Keep new sources as candidates until trialed and reviewed | It affects noise and maintenance |
| Interrupt-worthy opportunities | Daily review by default; urgent alerts later if needed | It affects notification design |
| Hard-reject categories | Start with documented risk flags | It affects rejection behavior |
| Dashboard uncertainty display | Show uncertainty plainly near score and budget estimates | It affects review ergonomics |
| Required decision labels | Start with ignored, saved, replied, applied, follow-up, converted, rejected, false positive, false negative | It affects workflow completeness |

## Decision Process

1. Add an ADR for important architecture decisions.
2. Mark status as `Proposed`, `Accepted`, `Superseded`, or `Rejected`.
3. Link affected files.
4. Update this ledger.
