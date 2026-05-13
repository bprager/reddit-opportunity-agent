# ADR 0006: Use Phase 1 MVP Defaults

Date: 2026-05-11

Status: Accepted

## Context

The project needed a small set of defaults before implementation could move beyond placeholders. Bernd approved the recommended direction after the architecture interview.

## Decision

Use these MVP defaults:

- Build local-first until the daily queue proves useful.
- Use Streamlit for the first dashboard.
- Use rules and regression examples before adding LLM classification.
- Implement remote opportunities before local Los Angeles lead discovery.
- Start with an expected value threshold around 200 USD per pursuit hour.
- Store only minimal Reddit author metadata until a stronger scoring need exists.
- Support OpenAI and Ollama later, with one configured active provider at a time.
- Design OpenClaw tools after the daily review workflow works.

## Consequences

- Phase 1 architecture questions are resolved.
- Phase 2 can focus on rules-first classification, scoring, and risk detection.
- The first implementation favors testability and local feedback over deployment complexity.
- Product-level details such as interrupt-worthy opportunities and dashboard uncertainty display still need tuning during later phases.
