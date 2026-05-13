import tempfile
import unittest
from pathlib import Path

from reddit_radar.runner import run_source_collection
from reddit_radar.sources import SourceDefinition, SourceRegistry
from reddit_radar.storage import OpportunityStore

from test_regression_examples import load_examples


class SourceHealthTests(unittest.TestCase):
    def test_store_records_source_success_and_failure(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            store = OpportunityStore(Path(temp_dir) / "radar.db")
            store.init_schema()

            store.record_source_failure("hn-jobs", "HTTP 503", backoff_minutes=15)
            store.record_source_success("lobsters-jobs")
            health = store.list_source_health()

        self.assertEqual("degraded", health["hn-jobs"]["status"])
        self.assertEqual(1, health["hn-jobs"]["failure_count"])
        self.assertEqual("HTTP 503", health["hn-jobs"]["last_error"])
        self.assertTrue(health["hn-jobs"]["disabled_until"])
        self.assertEqual("healthy", health["lobsters-jobs"]["status"])
        self.assertEqual(0, health["lobsters-jobs"]["failure_count"])

    def test_source_runner_records_failures_and_continues(self) -> None:
        class PassingAdapter:
            def collect(self, source: SourceDefinition) -> list[object]:
                class Item:
                    def to_pipeline_item(self) -> dict:
                        return {
                            **load_examples()[0],
                            "id": f"{source.source_id}-item",
                            "source": source.source_id,
                        }

                return [Item()]

        class FailingAdapter:
            def collect(self, source: SourceDefinition) -> list[object]:
                raise RuntimeError("temporary source failure")

        registry = SourceRegistry(
            [
                SourceDefinition(
                    source_id="broken",
                    display_name="Broken",
                    platform="rss",
                    acquisition_method="broken",
                    endpoint_or_query="https://example.com/broken.xml",
                ),
                SourceDefinition(
                    source_id="working",
                    display_name="Working",
                    platform="rss",
                    acquisition_method="working",
                    endpoint_or_query="https://example.com/working.xml",
                ),
            ]
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            database_path = Path(temp_dir) / "radar.db"
            result = run_source_collection(
                registry=registry,
                adapters={"broken": FailingAdapter(), "working": PassingAdapter()},
                database_path=database_path,
            )
            store = OpportunityStore(database_path)
            store.init_schema()
            health = store.list_source_health()

        self.assertEqual(
            {"sources": 2, "collected": 1, "saved": 1, "open": 1, "failed": 1, "skipped": 0},
            result,
        )
        self.assertEqual("degraded", health["broken"]["status"])
        self.assertEqual("healthy", health["working"]["status"])

    def test_source_runner_skips_backed_off_sources(self) -> None:
        source = SourceDefinition(
            source_id="backed-off",
            display_name="Backed Off",
            platform="rss",
            acquisition_method="rss_feed",
            endpoint_or_query="https://example.com/feed.xml",
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            database_path = Path(temp_dir) / "radar.db"
            store = OpportunityStore(database_path)
            store.init_schema()
            store.record_source_failure("backed-off", "HTTP 429", backoff_minutes=30)

            result = run_source_collection(
                registry=SourceRegistry([source]),
                adapters={"rss_feed": object()},
                database_path=database_path,
            )

        self.assertEqual(
            {"sources": 1, "collected": 0, "saved": 0, "open": 0, "failed": 0, "skipped": 1},
            result,
        )


if __name__ == "__main__":
    unittest.main()
