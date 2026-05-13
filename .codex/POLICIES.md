# Policies

## Outreach Policy

- The system may draft public replies or application notes.
- The system must not send replies, direct messages, applications, or follow-ups.
- Bernd must approve any external communication.

## Reddit Policy

- Respect subreddit rules and Reddit platform limits.
- Avoid aggressive scraping.
- Prefer official API access through configured credentials when approval is available.
- Treat Reddit RSS as a low-volume interim source, not as an unrestricted scraping channel.
- Keep Reddit JSON endpoints disabled or `needs_review` unless a later policy decision approves
  them.
- Keep source attribution and URLs with collected items.

## Source Acquisition Policy

- Use source-specific adapters with explicit limits and failure states.
- Disable sources after repeated permission, policy, or rate-limit failures.
- Store the acquisition method for auditability.
- Do not bypass access controls, paywalls, private communities, or platform rules.

## Data Policy

- Store only data needed for review, scoring, learning, and auditability.
- Avoid unnecessary personal data.
- Treat Reddit usernames and post history as potentially sensitive.
- Do not store secrets in the repository.

## Learning Policy

- The system may recommend changes to sources, scoring, risk rules, or prompts.
- Meaningful rule changes require human approval.
- Keep examples of misses and bad calls for regression testing.
- Record important learning changes as learning events.

## Documentation Policy

- Architecture changes update `Docs/architecture.md`.
- Important architecture decisions get an ADR under `Docs/adr/`.
- Workflow and context changes update `.codex/`.
- Notable changes update `CHANGELOG.md`.
