import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from reddit_radar.adapters.rss import RssFeedAdapter
from reddit_radar.runner import rss_source_from_arg, run_source_collection
from reddit_radar.sources import SourceDefinition, SourceRegistry, build_source_item_id


RSS_FIXTURE = Path("tests/fixtures/rss_opportunity.xml").read_text(encoding="utf-8")


class SourceRegistryTests(unittest.TestCase):
    def test_registry_returns_enabled_sources_in_priority_order(self) -> None:
        registry = SourceRegistry(
            [
                SourceDefinition(
                    source_id="hn-jobs",
                    display_name="HN Jobs",
                    platform="hacker_news",
                    acquisition_method="hacker_news_api",
                    endpoint_or_query="jobstories",
                    priority=20,
                ),
                SourceDefinition(
                    source_id="reddit-forhire-rss",
                    display_name="r/forhire RSS",
                    platform="reddit",
                    acquisition_method="rss_feed",
                    endpoint_or_query="https://www.reddit.com/r/forhire/.rss",
                    priority=10,
                ),
                SourceDefinition(
                    source_id="disabled",
                    display_name="Disabled source",
                    platform="rss",
                    acquisition_method="rss_feed",
                    endpoint_or_query="https://example.com/feed.xml",
                    enabled=False,
                ),
            ]
        )

        self.assertEqual(
            ["reddit-forhire-rss", "hn-jobs"],
            [source.source_id for source in registry.enabled_sources()],
        )

    def test_source_item_id_falls_back_to_url_or_title(self) -> None:
        from_url = build_source_item_id(
            source_id="rss",
            external_id="",
            canonical_url="https://example.com/post",
            title="Ignored",
        )
        from_title = build_source_item_id(
            source_id="rss",
            external_id="",
            canonical_url="",
            title="Only title",
        )

        self.assertTrue(from_url.startswith("rss:"))
        self.assertTrue(from_title.startswith("rss:"))
        self.assertNotEqual(from_url, from_title)


class RssFeedAdapterTests(unittest.TestCase):
    def test_rss_source_argument_creates_conservative_source_definition(self) -> None:
        source = rss_source_from_arg("example=https://example.com/feed.xml", limit=5)

        self.assertEqual("example", source.source_id)
        self.assertEqual("example", source.display_name)
        self.assertEqual("rss", source.platform)
        self.assertEqual("rss_feed", source.acquisition_method)
        self.assertEqual("https://example.com/feed.xml", source.endpoint_or_query)
        self.assertEqual(5, source.item_limit)
        self.assertEqual("allowed", source.policy_status)

    def test_rss_adapter_normalizes_feed_items_to_source_items(self) -> None:
        source = SourceDefinition(
            source_id="example-rss",
            display_name="Example RSS",
            platform="rss",
            acquisition_method="rss_feed",
            endpoint_or_query="https://example.com/feed.xml",
            item_limit=5,
        )
        adapter = RssFeedAdapter(fetcher=lambda _: RSS_FIXTURE)

        items = adapter.collect(source)

        self.assertEqual(1, len(items))
        self.assertEqual("example-rss:rss-remote-ai", items[0].id)
        self.assertEqual("example-rss", items[0].source_id)
        self.assertEqual("rss", items[0].platform)
        self.assertEqual("rss_feed", items[0].acquisition_method)
        self.assertEqual("[Hiring] Build an internal AI workflow", items[0].title)
        self.assertIn("Budget is 5000 USD", items[0].body)
        self.assertEqual("https://example.com/items/rss-remote-ai", items[0].canonical_url)
        self.assertEqual("example_author", items[0].author_display)

    def test_rss_adapter_handles_missing_optional_text(self) -> None:
        source = SourceDefinition(
            source_id="example-rss",
            display_name="Example RSS",
            platform="rss",
            acquisition_method="rss_feed",
            endpoint_or_query="https://example.com/feed.xml",
        )
        adapter = RssFeedAdapter(fetcher=lambda _: "<rss><channel><item /></channel></rss>")

        item = adapter.collect(source)[0]

        self.assertEqual("", item.title)
        self.assertIsNone(item.author_display)

    def test_rss_adapter_fetches_url_with_project_user_agent(self) -> None:
        class Response:
            def __enter__(self) -> "Response":
                return self

            def __exit__(self, *_args: object) -> None:
                return None

            def read(self) -> bytes:
                return b"<rss />"

        captured = {}

        def fake_urlopen(request: object, timeout: int) -> Response:
            captured["request"] = request
            captured["timeout"] = timeout
            return Response()

        with patch("reddit_radar.adapters.rss.urlopen", fake_urlopen):
            content = RssFeedAdapter()._fetch_url("https://example.com/feed.xml")

        self.assertEqual("<rss />", content)
        self.assertEqual(20, captured["timeout"])

    def test_source_runner_processes_rss_items_through_existing_pipeline(self) -> None:
        source = SourceDefinition(
            source_id="example-rss",
            display_name="Example RSS",
            platform="rss",
            acquisition_method="rss_feed",
            endpoint_or_query="https://example.com/feed.xml",
        )
        registry = SourceRegistry([source])
        adapters = {"rss_feed": RssFeedAdapter(fetcher=lambda _: RSS_FIXTURE)}

        with tempfile.TemporaryDirectory() as temp_dir:
            result = run_source_collection(
                registry=registry,
                adapters=adapters,
                database_path=Path(temp_dir) / "radar.db",
            )

        self.assertEqual(
            {"sources": 1, "collected": 1, "saved": 1, "open": 1, "failed": 0, "skipped": 0},
            result,
        )


if __name__ == "__main__":
    unittest.main()
