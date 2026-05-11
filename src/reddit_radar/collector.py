from collections.abc import Iterable

from .models import RedditItem


class RedditCollector:
    """Collects Reddit posts.

    MVP note:
    Wire this to PRAW or the Reddit API after credentials are configured.
    """

    def collect_subreddit(self, subreddit: str, limit: int = 25) -> Iterable[RedditItem]:
        raise NotImplementedError("Connect this to PRAW in Phase 1.")
