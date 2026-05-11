# ADR 0002: Require Human Approval Before Outreach

Date: 2026-05-11

Status: Accepted

## Context

The project exists to help Bernd find and evaluate opportunities. Existing project documents explicitly reject automated DMs, mass posting, and misleading outreach.

## Decision

The system may generate internal recommendations, public reply drafts, and application notes, but it must not send messages, submit applications, post replies, or follow up externally without Bernd's explicit approval.

## Consequences

- Outreach remains under human control.
- The system can optimize for quality and judgment rather than volume.
- UI and tool design must keep drafts clearly separated from external actions.
- Any future integration that can send messages must require a separate approval step.

