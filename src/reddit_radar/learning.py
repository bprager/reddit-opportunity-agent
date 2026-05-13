from datetime import UTC, datetime
from pathlib import Path

from .storage import OpportunityStore


def generate_weekly_learning_report(
    store: OpportunityStore,
    output_path: str | Path = "reports/weekly_learning_report.md",
) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    false_positives = store.list_by_decision("false_positive", limit=50)
    false_negatives = store.list_by_decision("false_negative", limit=50)
    missed = store.list_missed_opportunities(limit=50)
    candidates = store.list_source_candidates(limit=50)
    events = store.list_learning_events(limit=50)

    content = "\n".join(
        [
            "# Reddit Opportunity Radar Weekly Learning Report",
            "",
            f"Generated: {datetime.now(UTC).isoformat()}",
            "",
            "## False Positives",
            "",
            _render_assessments(false_positives),
            "",
            "## False Negatives",
            "",
            _render_assessments(false_negatives),
            "",
            "## Missed Opportunities",
            "",
            _render_missed(missed),
            "",
            "## Source Candidates",
            "",
            _render_sources(candidates),
            "",
            "## Learning Events",
            "",
            _render_events(events),
            "",
            "## Suggested Review",
            "",
            _suggested_review(false_positives, false_negatives, missed, candidates),
            "",
            "## Guardrail",
            "",
            "Do not silently change rules. Bernd approves source, scoring, and prompt changes.",
            "",
        ]
    )
    path.write_text(content, encoding="utf-8")
    return path


def _render_assessments(items: list[dict]) -> str:
    if not items:
        return "No items."
    return "\n".join(
        f"- **{item['title']}** ({item['source']}, score {item['score']})"
        for item in items
    )


def _render_missed(items: list[dict]) -> str:
    if not items:
        return "No missed opportunities recorded."
    return "\n".join(
        f"- **{item['title']}** ({item['missed_reason']}): {item['notes']}"
        for item in items
    )


def _render_sources(items: list[dict]) -> str:
    if not items:
        return "No source candidates recorded."
    return "\n".join(
        (
            f"- **{item['source_name']}** ({item['source_type']}, {item['status']}): "
            f"{item['reason']} Expected signal: {item['expected_signal']}"
        )
        for item in items
    )


def _render_events(items: list[dict]) -> str:
    if not items:
        return "No learning events recorded."
    return "\n".join(
        f"- **{item['event_type']}**: {item['reason']} Expected effect: {item['expected_effect']}"
        for item in items
    )


def _suggested_review(
    false_positives: list[dict],
    false_negatives: list[dict],
    missed: list[dict],
    candidates: list[dict],
) -> str:
    suggestions = []
    if false_positives:
        suggestions.append("- Review whether scoring is too generous for weak buying intent.")
    if false_negatives or missed:
        suggestions.append("- Review missed buying-signal language and add regression examples.")
    if candidates:
        suggestions.append("- Trial candidate sources before adding them to routine collection.")
    if not suggestions:
        suggestions.append("- Collect more decisions before changing scoring or sources.")
    return "\n".join(suggestions)
