import unittest
from unittest.mock import patch
from types import SimpleNamespace

from pydantic_settings import SettingsConfigDict

from reddit_radar.collector import DryRunCollector, RedditCollector
from reddit_radar.config import Settings

from test_regression_examples import load_examples


class CollectorTests(unittest.TestCase):
    def test_dry_run_collector_filters_subreddit_and_respects_limit(self) -> None:
        collector = DryRunCollector(load_examples())

        items = collector.collect_subreddit("forhire", limit=1)

        self.assertEqual(1, len(items))
        self.assertEqual("r/forhire", items[0]["source"])

    def test_dry_run_collector_returns_all_items_without_limit(self) -> None:
        examples = load_examples()
        collector = DryRunCollector(examples)

        self.assertEqual(examples, collector.collect_all())

    def test_live_collector_reports_missing_credential_names_only(self) -> None:
        class EmptySettings(Settings):
            model_config = SettingsConfigDict(env_file=None, extra="ignore")

        collector = RedditCollector(EmptySettings())

        self.assertEqual(
            ["REDDIT_CLIENT_ID", "REDDIT_CLIENT_SECRET"],
            collector.validate_credentials(),
        )

    def test_live_collector_requires_credentials_before_network_collection(self) -> None:
        class EmptySettings(Settings):
            model_config = SettingsConfigDict(env_file=None, extra="ignore")

        collector = RedditCollector(EmptySettings())

        with self.assertRaisesRegex(RuntimeError, "Missing Reddit credentials"):
            collector.collect_subreddit("forhire")

    def test_submission_conversion_normalizes_optional_fields(self) -> None:
        collector = RedditCollector(Settings(_env_file=None))
        submission = SimpleNamespace(
            id=123,
            title="Need Python help",
            permalink="/r/forhire/comments/123",
            author=None,
            created_utc=1_700_000_000,
        )

        item = collector._submission_to_item("forhire", submission)

        self.assertEqual(
            {
                "id": "123",
                "source": "r/forhire",
                "title": "Need Python help",
                "body": "",
                "author": None,
                "url": "https://reddit.com/r/forhire/comments/123",
                "created_utc": "2023-11-14T22:13:20+00:00",
            },
            item,
        )

    def test_live_collector_uses_praw_when_credentials_are_available(self) -> None:
        class FakeSubreddit:
            def new(self, limit: int) -> list[SimpleNamespace]:
                return [
                    SimpleNamespace(
                        id=f"id-{limit}",
                        title="Need automation",
                        selftext="Remote budget 5000 USD",
                        author="client",
                        permalink="/r/forhire/comments/id",
                        created_utc=1_700_000_000,
                    )
                ]

        class FakeReddit:
            def __init__(self, **kwargs: str) -> None:
                self.kwargs = kwargs

            def subreddit(self, name: str) -> FakeSubreddit:
                self.name = name
                return FakeSubreddit()

        fake_praw = SimpleNamespace(Reddit=FakeReddit)
        settings = Settings(
            _env_file=None,
            reddit_client_id="client",
            reddit_client_secret="secret",
            reddit_user_agent="agent",
        )
        collector = RedditCollector(settings)

        with patch.dict("sys.modules", {"praw": fake_praw}):
            items = collector.collect_subreddit("r/forhire", limit=3)

        self.assertEqual("id-3", items[0]["id"])
        self.assertEqual("client", items[0]["author"])

    def test_author_name_and_missing_timestamp_have_fallbacks(self) -> None:
        collector = RedditCollector(Settings(_env_file=None))

        self.assertEqual("bernd", collector._author_name("bernd"))
        self.assertIn("+00:00", collector._created_at(None))


if __name__ == "__main__":
    unittest.main()
