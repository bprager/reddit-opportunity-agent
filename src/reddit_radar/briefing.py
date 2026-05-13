from datetime import UTC, datetime
from pathlib import Path

from .storage import OpportunityStore

DEFAULT_DATABASE_URL = "sqlite:///./reddit_radar.db"


def generate_briefing(
    output_path: str = "reports/daily_briefing.md",
    database_path: str | None = None,
) -> Path:
    """Generate a Markdown briefing for ChatGPT, Codex, or OpenClaw review."""

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    store = OpportunityStore(_sqlite_path(database_path or DEFAULT_DATABASE_URL))
    store.init_schema()
    assessments = store.list_assessments(limit=50)
    open_items = [item for item in assessments if item["decision"] is None]
    local_leads = [
        item for item in open_items if item["category"] == "local_client_lead"
    ]
    remote_opportunities = [
        item for item in open_items if item["category"] == "remote_opportunity"
    ]
    rejected_items = [
        item for item in assessments if item["category"] == "reject"
    ]
    false_positives = store.list_by_decision("false_positive", limit=20)
    missed_opportunities = [
        item for item in assessments if item["category"] == "missed_opportunity"
    ]

    content = "\n".join(
        [
            "# Reddit Opportunity Radar Briefing",
            "",
            f"Generated: {datetime.now(UTC).isoformat()}",
            "",
            "## Top Local Client Leads",
            "",
            _render_items(local_leads),
            "",
            "## Top Remote Opportunities",
            "",
            _render_items(remote_opportunities),
            "",
            "## Rejected Items",
            "",
            _render_items(rejected_items),
            "",
            "## False Positives",
            "",
            _render_items(false_positives),
            "",
            "## False Negatives / Missed Opportunities",
            "",
            _render_items(missed_opportunities),
            "",
            "## New Source Candidates",
            "",
            "No source candidates recorded yet.",
            "",
            "## Recommended Adjustments",
            "",
            _recommended_adjustments(assessments),
            "",
            "## Questions for ChatGPT",
            "",
            "- What opportunity types are we missing?",
            "- Which sources should be added or removed?",
            "- Are the scoring weights too strict or too generous?",
            "- What should Codex implement next?",
            "",
            "## Codex Task Candidates",
            "",
            "- Connect this briefing to the dashboard review queue.",
            "- Add source candidate tracking to the learning loop.",
            "- Add real Reddit collection once review output is useful.",
            "",
        ]
    )

    path.write_text(content, encoding="utf-8")
    return path


def _sqlite_path(database_url: str) -> str:
    if database_url.startswith("sqlite:///"):
        return database_url.removeprefix("sqlite:///")
    return database_url


def _render_items(items: list[dict]) -> str:
    if not items:
        return "No items."

    lines = []
    for item in items:
        risks = ", ".join(item["risk_flags"]) if item["risk_flags"] else "none"
        reasons = "; ".join(item["reasons"][:2])
        lines.extend(
            [
                f"- **{item['title']}**",
                f"  - Source: {item['source']}",
                f"  - Score: {item['score']}",
                f"  - Risks: {risks}",
                f"  - Recommended action: {item['recommended_action']}",
                f"  - Why: {reasons}",
                f"  - URL: {item['url']}",
            ]
        )
    return "\n".join(lines)


def _recommended_adjustments(assessments: list[dict]) -> str:
    if not assessments:
        return "Run classification and scoring before tuning sources or scoring rules."

    rejected_count = len([item for item in assessments if item["category"] == "reject"])
    missed_count = len(
        [item for item in assessments if item["category"] == "missed_opportunity"]
    )
    return "\n".join(
        [
            f"- Review {rejected_count} rejected items for overly strict rules.",
            f"- Review {missed_count} missed-opportunity examples for new buying signals.",
            "- Keep outreach human-approved; drafts remain internal only.",
        ]
    )


if __name__ == "__main__":
    print(generate_briefing())
