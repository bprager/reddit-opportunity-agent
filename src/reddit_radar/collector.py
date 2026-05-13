from collections.abc import Iterable
from datetime import datetime, timezone

from .config import Settings


class DryRunCollector:
    """Collect fixture-like items without network access."""

    def __init__(self, items: Iterable[dict]) -> None:
        self.items = list(items)

    def collect_subreddit(self, subreddit: str, limit: int = 25) -> list[dict]:
        source_name = self._source_name(subreddit)
        matches = [item for item in self.items if item["source"].lower() == source_name.lower()]
        return matches[:limit]

    def collect_all(self, limit: int | None = None) -> list[dict]:
        if limit is None:
            return list(self.items)
        return self.items[:limit]

    def _source_name(self, subreddit: str) -> str:
        clean_name = subreddit.removeprefix("r/")
        return f"r/{clean_name}"


class RedditCollector:
    """Collect Reddit posts through PRAW when credentials are configured."""

    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or Settings()

    def validate_credentials(self) -> list[str]:
        return self.settings.missing_reddit_credentials()

    def collect_subreddit(self, subreddit: str, limit: int = 25) -> list[dict]:
        missing = self.validate_credentials()
        if missing:
            names = ", ".join(missing)
            raise RuntimeError(f"Missing Reddit credentials: {names}.")

        try:
            import praw
        except ImportError as error:
            raise RuntimeError("PRAW is required for live Reddit collection.") from error

        reddit = praw.Reddit(
            client_id=self.settings.reddit_client_id,
            client_secret=self.settings.reddit_client_secret,
            user_agent=self.settings.reddit_user_agent,
        )
        clean_name = subreddit.removeprefix("r/")
        posts = reddit.subreddit(clean_name).new(limit=limit)
        return [self._submission_to_item(clean_name, submission) for submission in posts]

    def _submission_to_item(self, subreddit: str, submission: object) -> dict:
        return {
            "id": str(submission.id),
            "source": f"r/{subreddit}",
            "title": str(submission.title),
            "body": str(getattr(submission, "selftext", "") or ""),
            "author": self._author_name(getattr(submission, "author", None)),
            "url": f"https://reddit.com{submission.permalink}",
            "created_utc": self._created_at(getattr(submission, "created_utc", None)),
        }

    def _author_name(self, author: object | None) -> str | None:
        if author is None:
            return None
        return str(author)

    def _created_at(self, created_utc: float | None) -> str:
        if created_utc is None:
            return datetime.now(timezone.utc).isoformat()
        return datetime.fromtimestamp(created_utc, tz=timezone.utc).isoformat()
