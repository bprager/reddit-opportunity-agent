# ChatGPT and Codex Review Workflow

## Purpose

This project should be easy to discuss with ChatGPT, Codex, or OpenClaw.

The system should produce compact, useful context so Bernd can ask:

- What is working?
- What is not working?
- What should I change next?
- Which sources should I add or remove?
- Are the scoring rules too strict or too generous?
- What should Codex implement next?

## Generated Files

The system should generate these review artifacts:

```text
reports/
  daily_briefing.md
  weekly_learning_report.md
  codex_handoff.md
  source_performance.md
```

## ChatGPT Review Prompt

```text
I am building Reddit Opportunity Radar.

Review the attached weekly report and recommend concrete changes to improve outcomes.

Focus on:
1. Better source discovery
2. Better scoring
3. Missed opportunities
4. False positives
5. Better daily workflow
6. Better positioning for Bernd's AI/cloud/fractional CTO services

Do not recommend automated DMs or spam.
```

## Codex Handoff Prompt

```text
You are working on the reddit-opportunity-radar repo.

Read:
- README.md
- TODO.md
- docs/adaptive_learning.md
- docs/chatgpt_codex_review.md
- reports/codex_handoff.md

Implement the highest-leverage next task from the handoff.

Constraints:
- Do not add automated DMs.
- Do not add automated posting.
- Keep human approval required.
- Prefer small, tested changes.
- Run `make check` before finishing.
```

## OpenClaw Future Tooling

Future OpenClaw tools should include:

```text
reddit.daily_briefing
reddit.weekly_learning_report
reddit.source_candidates
reddit.add_missed_opportunity
reddit.mark_false_positive
reddit.mark_false_negative
reddit.propose_scoring_change
reddit.generate_codex_handoff
```

## Discussion Loop

1. Agent collects and scores.
2. Bernd reviews and marks outcomes.
3. System generates report.
4. Bernd discusses report with ChatGPT.
5. ChatGPT suggests changes.
6. Codex implements approved changes.
7. System records learning event.
8. Repeat weekly.
