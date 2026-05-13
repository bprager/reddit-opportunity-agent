# Source Acquisition Design

Last updated: 2026-05-13

Status: ADR 0007 accepted. The first implementation slice now includes a source registry, canonical
source item model, generic RSS adapter, and RSS command-line collection path.

## Research Summary

Reddit is still an important first source family, but it should no longer be treated as the
application's only acquisition path. Reddit's Responsible Builder Policy says API access requires
explicit approval, transparency, and respect for access limits:
https://support.reddithelp.com/hc/en-us/articles/42728983564564-Responsible-Builder-Policy

Reddit's Data API Terms also make API usage conditional on ongoing compliance, allow Reddit to set
and enforce limits, restrict attempts to bypass limits, and prohibit spam or harassment:
https://redditinc.com/policies/data-api-terms

Reddit's Public Content Policy confirms Reddit public content is broadly visible, but also warns
against misuse of public content, bulk unauthorized collection, sensitive profiling, spam,
harassment, and commercial misuse:
https://support.reddithelp.com/hc/en-us/articles/26410290525844-Public-Content-Policy

The practical architecture conclusion is:

- Reddit API access is useful but uncertain.
- Reddit public feeds may be useful for low-volume interim monitoring, but they can be rate-limited
  and should not be treated as a guaranteed or unrestricted acquisition channel.
- The opportunity engine should process normalized source items, not Reddit-specific objects.
- Acquisition adapters should be replaceable without changing classification, scoring, storage,
  dashboard, briefing, or learning behavior.

Other viable source families have cleaner independent interfaces:

- Hacker News has an official public API with item IDs, stories, jobs, Ask HN, Show HN, and update
  feeds: https://github.com/HackerNews/API
- GitHub Discussions can be queried through GitHub's GraphQL API:
  https://docs.github.com/en/graphql/guides/using-the-graphql-api-for-discussions
- Lobsters documents public RSS feeds by tag and tag combinations:
  https://lobste.rs/about
- Generic RSS and manual curated feeds can use the same adapter shape.

## Recommended Architecture

Introduce a source-agnostic acquisition layer in front of the existing assessment pipeline.

```text
Source Registry
  -> Acquisition Adapter
  -> Source Normalizer
  -> Canonical Source Item
  -> Dedupe
  -> Classifier
  -> Scorer
  -> Store
  -> Dashboard / Briefing / Learning
```

The assessment engine should not know whether an item came from Reddit RSS, Reddit API, Hacker
News, Lobsters, GitHub Discussions, Google Alerts, or a manual import. It should only receive a
canonical source item with stable fields.

## Canonical Source Item

Every adapter should normalize input into this common shape:

```text
id                 stable internal ID
source_id          configured source definition ID
platform           reddit, hacker_news, lobsters, github, rss, manual
acquisition_method rss, official_api, json_endpoint, manual_import
external_id        platform-native item ID when available
canonical_url      source URL for manual review
title              item title
body               item body or summary
author_display     optional public display name
published_at       source timestamp when available
collected_at       local collection timestamp
content_hash       fallback dedupe key
raw_metadata_json  minimal adapter metadata needed for audit and debugging
policy_status      allowed, gated, disabled, needs_review
```

The existing `RedditItem` model can remain temporarily as a compatibility layer, but the next
implementation step should introduce `SourceItem` or equivalent naming so the pipeline stops
implying Reddit-only operation.

## Source Definition

Sources should be configured as data, not hardcoded collector calls:

```text
source_id
display_name
platform
acquisition_method
endpoint_or_query
enabled
priority
poll_interval_minutes
item_limit
cursor
policy_status
notes
```

This lets `r/forhire` move from `reddit_rss` to `reddit_api` later by changing the source
definition, not the scoring pipeline.

## Adapter Portfolio

Adapter implementation status:

- `manual_import`: available indirectly through fixtures and missed-opportunity intake; dedicated
  adapter pending.
- `rss_feed`: implemented for generic RSS ingestion with normalized source items.
- `hacker_news_api`: pending.
- `github_discussions_api`: pending.
- `reddit_api_praw`: adapter boundary exists; live verification waits for credentials and approval.
- `reddit_json_endpoint`: keep disabled or `needs_review` unless a later policy decision approves
   it. It may be technically convenient, but it should not become a quiet workaround for missing
   API approval.

## Reddit API Switch Plan

When Reddit credentials arrive:

1. Keep existing Reddit source IDs stable.
2. Add `reddit_api_praw` source definitions beside existing `reddit_rss` definitions.
3. Run both in shadow mode for a small read-only sample.
4. Compare normalized items, dedupe behavior, timestamps, and source URLs.
5. If the API path is cleaner, disable the RSS source definition and keep the same downstream
   classifier, scorer, dashboard, and learning loop.

No classifier or scorer changes should be required for the switch.

## Compliance Guardrails

- Keep all collection read-only.
- Do not automate replies, DMs, applications, voting, saving, or reporting.
- Use explicit user agents and credentials where required.
- Respect rate limits and stop on repeated 429, 403, or policy-related failures.
- Store only minimal public author display names.
- Do not infer sensitive personal traits.
- Do not train models on collected platform data.
- Keep source links visible for manual review.
- Disable any source when its access policy becomes unclear.

## Proposed Implementation Slices

1. Add Hacker News and Lobsters adapters as non-Reddit proof points.
2. Persist source definitions and source health state if manual configuration becomes cumbersome.
3. Add source-level health reporting and failure backoff.
4. Add a shadow-run path for switching Reddit RSS to Reddit API later.
