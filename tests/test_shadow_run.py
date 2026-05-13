import tempfile
import unittest
from pathlib import Path

from reddit_radar.runner import run_reddit_shadow_collection

from test_regression_examples import load_examples


class RedditShadowRunTests(unittest.TestCase):
    def test_shadow_collection_compares_rss_and_api_items_without_persisting(self) -> None:
        class FakeAdapter:
            def __init__(self, ids: list[str]) -> None:
                self.ids = ids

            def collect(self, source: object) -> list[object]:
                class Item:
                    def __init__(self, item_id: str) -> None:
                        self.item_id = item_id

                    def to_pipeline_item(self) -> dict:
                        return {
                            **load_examples()[0],
                            "id": self.item_id,
                            "source": "reddit-shadow",
                        }

                return [Item(item_id) for item_id in self.ids]

        with tempfile.TemporaryDirectory() as temp_dir:
            database_path = Path(temp_dir) / "radar.db"
            result = run_reddit_shadow_collection(
                rss_adapter=FakeAdapter(["shared", "rss-only"]),
                api_adapter=FakeAdapter(["shared", "api-only"]),
                database_path=database_path,
            )

        self.assertEqual(
            {
                "rss_collected": 2,
                "api_collected": 2,
                "overlap": 1,
                "rss_only": 1,
                "api_only": 1,
                "persisted": 0,
            },
            result,
        )
        self.assertFalse(database_path.exists())


if __name__ == "__main__":
    unittest.main()
