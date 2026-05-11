# ADR 0005: Keep Learning Changes Human-Approved

Date: 2026-05-11

Status: Accepted

## Context

The adaptive learning design says the system should learn from outcomes, missed opportunities, source quality, false positives, and false negatives. It also says the agent should not silently rewrite its own rules.

## Decision

The system may recommend changes to sources, prompts, scoring weights, risk rules, and workflow. Meaningful changes require Bernd's approval and should be recorded as learning events.

## Consequences

- Learning remains auditable.
- Bad automatic adjustments are less likely to degrade the queue.
- The dashboard and reports should make recommended changes easy to approve, reject, and review later.
- Regression examples should be used to prevent old mistakes from returning.

