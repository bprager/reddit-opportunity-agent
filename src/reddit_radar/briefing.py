from datetime import UTC, datetime
from pathlib import Path


def generate_briefing(output_path: str = "reports/daily_briefing.md") -> Path:
    """Generate a Markdown briefing for ChatGPT, Codex, or OpenClaw review.

    MVP placeholder:
    Connect this to the database after Phase 2.
    """

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    content = f"""# Reddit Opportunity Radar Briefing

Generated: {datetime.now(UTC).isoformat()}

## Top Local Client Leads

TODO: query database.

## Top Remote Opportunities

TODO: query database.

## Rejected Items

TODO: query database.

## False Positives

TODO: query database.

## False Negatives / Missed Opportunities

TODO: query database.

## New Source Candidates

TODO: query database.

## Recommended Adjustments

TODO: generate scoring, source, and prompt recommendations.

## Questions for ChatGPT

- What opportunity types are we missing?
- Which sources should be added or removed?
- Are the scoring weights too strict or too generous?
- What should Codex implement next?

## Codex Task Candidates

TODO: generate implementation tasks.
"""

    path.write_text(content, encoding="utf-8")
    return path


if __name__ == "__main__":
    print(generate_briefing())
