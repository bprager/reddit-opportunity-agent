import tempfile
import unittest
from pathlib import Path

from reddit_radar.pipeline import RadarPipeline
from reddit_radar.runner import run_dry_run_collection, run_live_collection
from reddit_radar.storage import OpportunityStore

from test_regression_examples import load_examples


class RadarPipelineTests(unittest.TestCase):
    def test_pipeline_assesses_and_persists_dry_run_items(self) -> None:
        examples = load_examples()[:2]

        with tempfile.TemporaryDirectory() as temp_dir:
            store = OpportunityStore(Path(temp_dir) / "radar.db")
            store.init_schema()
            pipeline = RadarPipeline(store)
            saved_ids = pipeline.process_items(examples)
            assessments = store.list_assessments()

        self.assertEqual(2, len(saved_ids))
        self.assertEqual(2, len(assessments))
        self.assertCountEqual(
            ["remote_opportunity", "local_client_lead"],
            [item["category"] for item in assessments],
        )

    def test_pipeline_deduplicates_repeated_items(self) -> None:
        example = load_examples()[0]

        with tempfile.TemporaryDirectory() as temp_dir:
            store = OpportunityStore(Path(temp_dir) / "radar.db")
            store.init_schema()
            pipeline = RadarPipeline(store)
            first_ids = pipeline.process_items([example])
            second_ids = pipeline.process_items([example])
            assessments = store.list_assessments()

        self.assertEqual(first_ids, second_ids)
        self.assertEqual(1, len(assessments))

    def test_dry_run_runner_processes_fixture_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            result = run_dry_run_collection(
                fixture_path="tests/fixtures/opportunity_examples.json",
                database_path=Path(temp_dir) / "radar.db",
                limit=3,
            )

        self.assertEqual(
            {"collected": 3, "saved": 3, "open": 3},
            result,
        )

    def test_live_runner_processes_bounded_subreddits_with_injected_collector(self) -> None:
        class FakeCollector:
            def collect_subreddit(self, subreddit: str, limit: int = 25) -> list[dict]:
                return [
                    {
                        **load_examples()[0],
                        "id": f"{subreddit}_{index}",
                        "source": f"r/{subreddit}",
                    }
                    for index in range(limit)
                ]

        with tempfile.TemporaryDirectory() as temp_dir:
            result = run_live_collection(
                subreddits=["forhire", "hireaprogrammer"],
                database_path=Path(temp_dir) / "radar.db",
                limit=2,
                collector=FakeCollector(),
            )

        self.assertEqual(
            {"subreddits": 2, "collected": 4, "saved": 4, "open": 4},
            result,
        )


if __name__ == "__main__":
    unittest.main()
