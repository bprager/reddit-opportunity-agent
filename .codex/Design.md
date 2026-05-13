# Design

## Product Shape

Reddit Opportunity Radar is a daily intelligence tool for finding and ranking business opportunities
from public communities and feeds. Reddit is the first source family, but the product should not
depend on one Reddit acquisition method. It is not an outreach bot.

The experience should feel like a practical analyst desk:

- Review a short ranked queue.
- See why each item matters.
- See risk and rejection reasons.
- Decide whether to ignore, save, reply publicly, apply, follow up, or mark an outcome.
- Feed missed opportunities and bad calls back into the learning loop.

## Core Workflow

1. Load configured sources.
2. Acquire items through the source's configured adapter.
3. Normalize each item into a canonical source item.
4. Store and deduplicate source items.
5. Classify each item.
6. Score opportunity fit and economic value.
7. Detect risk and low-quality signals.
8. Generate a recommended action and optional draft.
9. Present a daily dashboard and briefing.
10. Record Bernd's decision.
11. Convert outcomes and misses into learning events.

## Main Screens

- Daily queue: top local and remote opportunities.
- Rejected items: why each item was filtered out.
- Opportunity detail: source, text, score breakdown, risks, suggested action, draft.
- Decision tracker: saved, replied, applied, follow-up, converted, rejected.
- Learning review: false positives, false negatives, source candidates, scoring changes.

## Tone and Output

Generated recommendations should be direct, specific, and cautious. Draft replies should ask useful diagnostic questions and avoid sounding automated.

## Design Guardrails

- No marketing-style dashboard clutter.
- Prioritize scanning and comparison.
- Show rejection reasons clearly.
- Make human approval explicit near any draft reply.
- Keep source links visible for manual review.
- Keep acquisition method visible enough to diagnose source quality and policy failures.
