import unittest
from pathlib import Path

from reddit_radar.adapters.hacker_news import HackerNewsAdapter
from reddit_radar.adapters.lobsters import LobstersRssAdapter, lobsters_source
from reddit_radar.sources import SourceDefinition


class HackerNewsAdapterTests(unittest.TestCase):
    def test_hacker_news_adapter_normalizes_job_items(self) -> None:
        responses = {
            "https://hacker-news.firebaseio.com/v0/jobstories.json": [101, 102],
            "https://hacker-news.firebaseio.com/v0/item/101.json": {
                "id": 101,
                "type": "job",
                "by": "yc_company",
                "time": 1_780_000_000,
                "title": "Remote AI workflow engineer",
                "text": "Build support automation &amp; internal tools.",
                "url": "https://example.com/jobs/101",
            },
            "https://hacker-news.firebaseio.com/v0/item/102.json": {
                "id": 102,
                "type": "comment",
                "title": "Ignored comment",
            },
        }
        adapter = HackerNewsAdapter(fetch_json=responses.__getitem__)
        source = SourceDefinition(
            source_id="hn-jobs",
            display_name="HN Jobs",
            platform="hacker_news",
            acquisition_method="hacker_news_api",
            endpoint_or_query="jobstories",
            item_limit=2,
        )

        items = adapter.collect(source)

        self.assertEqual(1, len(items))
        self.assertEqual("hn-jobs:101", items[0].id)
        self.assertEqual("hacker_news", items[0].platform)
        self.assertEqual("hacker_news_api", items[0].acquisition_method)
        self.assertEqual("Remote AI workflow engineer", items[0].title)
        self.assertEqual("Build support automation & internal tools.", items[0].body)
        self.assertEqual("yc_company", items[0].author_display)
        self.assertEqual("https://example.com/jobs/101", items[0].canonical_url)

    def test_hacker_news_adapter_falls_back_to_hn_item_url(self) -> None:
        responses = {
            "https://hacker-news.firebaseio.com/v0/askstories.json": [201],
            "https://hacker-news.firebaseio.com/v0/item/201.json": {
                "id": 201,
                "type": "story",
                "title": "Ask HN: Need help with workflow automation",
                "text": "<p>Remote budget available.</p>",
            },
        }
        adapter = HackerNewsAdapter(fetch_json=responses.__getitem__)
        source = SourceDefinition(
            source_id="hn-ask",
            display_name="Ask HN",
            platform="hacker_news",
            acquisition_method="hacker_news_api",
            endpoint_or_query="askstories",
        )

        item = adapter.collect(source)[0]

        self.assertEqual("https://news.ycombinator.com/item?id=201", item.canonical_url)
        self.assertEqual("Remote budget available.", item.body)


class LobstersAdapterTests(unittest.TestCase):
    def test_lobsters_source_builds_tag_feed_definition(self) -> None:
        source = lobsters_source("jobs", tag_query="job,python", limit=3)

        self.assertEqual("jobs", source.source_id)
        self.assertEqual("lobsters", source.platform)
        self.assertEqual("lobsters_rss", source.acquisition_method)
        self.assertEqual("https://lobste.rs/t/job,python.rss", source.endpoint_or_query)
        self.assertEqual(3, source.item_limit)

    def test_lobsters_adapter_normalizes_rss_items(self) -> None:
        fixture = Path("tests/fixtures/lobsters_jobs.xml").read_text(encoding="utf-8")
        source = lobsters_source("lobsters-jobs", tag_query="job", limit=5)
        adapter = LobstersRssAdapter(fetcher=lambda _url: fixture)

        items = adapter.collect(source)

        self.assertEqual(1, len(items))
        self.assertEqual("lobsters-jobs:lobsters-job-1", items[0].id)
        self.assertEqual("lobsters", items[0].platform)
        self.assertEqual("lobsters_rss", items[0].acquisition_method)
        self.assertEqual("Freelance Python automation role", items[0].title)


if __name__ == "__main__":
    unittest.main()
