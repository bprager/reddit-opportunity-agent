import tempfile
import unittest
from pathlib import Path

from reddit_radar.briefing import _recommended_adjustments, _sqlite_path, generate_briefing
from reddit_radar.storage import OpportunityStore

from helpers import save_example
from test_regression_examples import load_examples


class BriefingTests(unittest.TestCase):
    def test_generate_briefing_uses_stored_assessments(self) -> None:
        examples = load_examples()

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            database_path = temp_path / "radar.db"
            output_path = temp_path / "daily_briefing.md"
            store = OpportunityStore(database_path)
            store.init_schema()
            for example in examples:
                save_example(store, example)

            path = generate_briefing(
                output_path=str(output_path),
                database_path=str(database_path),
            )
            content = path.read_text(encoding="utf-8")

        self.assertIn("## Top Remote Opportunities", content)
        self.assertIn("[Hiring] Build an internal AI workflow", content)
        self.assertIn("## Top Local Client Leads", content)
        self.assertIn("Local shop needs help", content)
        self.assertIn("## Rejected Items", content)
        self.assertIn("Need AI crypto app today", content)
        self.assertNotIn("TODO: query database.", content)

    def test_briefing_helpers_cover_empty_and_plain_database_paths(self) -> None:
        self.assertEqual("radar.db", _sqlite_path("sqlite:///radar.db"))
        self.assertEqual("/tmp/radar.db", _sqlite_path("/tmp/radar.db"))
        self.assertEqual(
            "Run classification and scoring before tuning sources or scoring rules.",
            _recommended_adjustments([]),
        )


if __name__ == "__main__":
    unittest.main()
