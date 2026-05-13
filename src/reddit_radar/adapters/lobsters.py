from collections.abc import Callable

from reddit_radar.adapters.rss import RssFeedAdapter
from reddit_radar.sources import SourceDefinition, SourceItem


class LobstersRssAdapter:
    def __init__(self, fetcher: Callable[[str], str] | None = None) -> None:
        self.rss_adapter = RssFeedAdapter(fetcher=fetcher)

    def collect(self, source: SourceDefinition) -> list[SourceItem]:
        return self.rss_adapter.collect(source)


def lobsters_source(source_id: str, tag_query: str, limit: int) -> SourceDefinition:
    clean_tags = tag_query.strip().removeprefix("/t/").removesuffix(".rss")
    return SourceDefinition(
        source_id=source_id,
        display_name=f"Lobsters {clean_tags}",
        platform="lobsters",
        acquisition_method="lobsters_rss",
        endpoint_or_query=f"https://lobste.rs/t/{clean_tags}.rss",
        item_limit=limit,
    )
