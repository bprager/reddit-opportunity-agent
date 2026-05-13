import tempfile
import unittest
from pathlib import Path

from reddit_radar.learning import (
    _render_events,
    _render_missed,
    _render_sources,
    _suggested_review,
    generate_weekly_learning_report,
)
from reddit_radar.storage import OpportunityStore

from helpers import save_example
from test_regression_examples import load_examples


class WeeklyLearningReportTests(unittest.TestCase):
    def test_weekly_learning_report_summarizes_learning_inputs(self) -> None:
        examples = load_examples()

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            store = OpportunityStore(temp_path / "radar.db")
            store.init_schema()
            false_positive_id = save_example(store, examples[4])
            store.record_decision(false_positive_id, "false_positive")
            store.add_missed_opportunity(
                source_url="https://reddit.com/r/SaaS/example",
                title="Manual onboarding advisory signal",
                notes="Classifier should catch advisory buying language.",
                missed_reason="classifier_failed",
            )
            store.add_source_candidate(
                source_name="r/SaaS",
                source_type="subreddit",
                reason="Founder workflow pain appears often.",
                expected_signal="SaaS automation and advisory needs.",
                expected_noise="medium",
            )
            store.add_learning_event(
                event_type="rule_review",
                reason="Tune advisory signal rules.",
                expected_effect="Fewer missed onboarding opportunities.",
            )
            report_path = generate_weekly_learning_report(
                store=store,
                output_path=temp_path / "weekly_learning_report.md",
            )
            content = report_path.read_text(encoding="utf-8")

        self.assertIn("## False Positives", content)
        self.assertIn("What AI tools do you use for invoices?", content)
        self.assertIn("## Missed Opportunities", content)
        self.assertIn("Manual onboarding advisory signal", content)
        self.assertIn("## Source Candidates", content)
        self.assertIn("r/SaaS", content)
        self.assertIn("## Learning Events", content)
        self.assertIn("Tune advisory signal rules.", content)

    def test_learning_renderers_show_empty_states_and_false_negative_review(self) -> None:
        self.assertEqual("No missed opportunities recorded.", _render_missed([]))
        self.assertEqual("No source candidates recorded.", _render_sources([]))
        self.assertEqual("No learning events recorded.", _render_events([]))
        self.assertIn(
            "missed buying-signal",
            _suggested_review([], [{"title": "missed"}], [], []),
        )
        self.assertIn(
            "Collect more decisions",
            _suggested_review([], [], [], []),
        )


if __name__ == "__main__":
    unittest.main()
