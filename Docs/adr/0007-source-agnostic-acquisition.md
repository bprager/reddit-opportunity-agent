# ADR 0007: Use Source-Agnostic Acquisition Adapters

Date: 2026-05-13

Status: Accepted

## Context

Reddit API credentials have been requested, but approval may take weeks or may not arrive. The
current project should keep moving without binding the opportunity engine to one Reddit acquisition
method.

Research on 2026-05-13 confirmed that Reddit API access is approval-based and policy-sensitive.
Reddit requires transparent use, respect for limits, and prohibits workarounds, spam, harassment,
sensitive profiling, and unapproved commercial misuse. A direct attempt to inspect a Reddit RSS feed
also returned an HTTP 429 in this environment, which reinforces that RSS is useful but not
guaranteed.

At the same time, adjacent sources such as Hacker News, GitHub Discussions, Lobsters, generic RSS,
and manual curated feeds can provide useful opportunity signals without waiting for Reddit API
approval.

## Decision

Treat Reddit as one source family, not as the application's core ingestion model.

Introduce a source-agnostic acquisition layer:

- Source definitions describe what to monitor.
- Acquisition adapters describe how to fetch items.
- Normalizers convert adapter output into canonical source items.
- The classifier, scorer, store, dashboard, briefing, and learning loop consume canonical source
  items rather than Reddit-specific objects.

The recommended first adapters are:

1. Manual import.
2. Generic RSS.
3. Hacker News official API.
4. Lobsters RSS.
5. GitHub Discussions API.
6. Reddit official API through PRAW when credentials are available.

Reddit public JSON endpoints should remain disabled or marked `needs_review` unless a later policy
decision explicitly approves them.

## Consequences

- Work can continue while Reddit API approval is pending.
- Switching to the official Reddit API becomes a source configuration and adapter change, not a
  rewrite of classification or scoring.
- The project can measure source quality across platforms.
- The data model should evolve from `RedditItem` toward `SourceItem`.
- Source-specific policy, rate limits, and health states become first-class operational concerns.

## Follow-Up Questions

- Hacker News and Lobsters are still pending as follow-up adapters.
- Should the first cross-source run store every normalized item or only items above a score
  threshold?
- Should Reddit JSON endpoints be permanently excluded unless Reddit explicitly approves them?
