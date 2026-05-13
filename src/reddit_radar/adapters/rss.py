from collections.abc import Callable
from html import unescape
from urllib.request import Request, urlopen
from xml.etree import ElementTree

from reddit_radar.sources import (
    SourceDefinition,
    SourceItem,
    build_source_item_id,
    content_hash,
)


class RssFeedAdapter:
    def __init__(self, fetcher: Callable[[str], str] | None = None) -> None:
        self.fetcher = fetcher or self._fetch_url

    def collect(self, source: SourceDefinition) -> list[SourceItem]:
        rss_text = self.fetcher(source.endpoint_or_query)
        root = ElementTree.fromstring(rss_text)
        items = root.findall("./channel/item")
        return [self._item_from_element(source, item) for item in items[: source.item_limit]]

    def _item_from_element(self, source: SourceDefinition, item: ElementTree.Element) -> SourceItem:
        title = self._text(item, "title")
        body = self._text(item, "description")
        canonical_url = self._text(item, "link")
        external_id = self._text(item, "guid") or canonical_url

        return SourceItem(
            id=build_source_item_id(
                source_id=source.source_id,
                external_id=external_id,
                canonical_url=canonical_url,
                title=title,
            ),
            source_id=source.source_id,
            platform=source.platform,
            acquisition_method=source.acquisition_method,
            external_id=external_id,
            canonical_url=canonical_url,
            title=title,
            body=body,
            author_display=self._text(item, "author") or None,
            published_at=self._text(item, "pubDate"),
            content_hash=content_hash(title, body, canonical_url),
            raw_metadata={
                "feed_url": source.endpoint_or_query,
                "display_name": source.display_name,
            },
            policy_status=source.policy_status,
        )

    def _text(self, item: ElementTree.Element, tag: str) -> str:
        element = item.find(tag)
        if element is None or element.text is None:
            return ""
        return unescape(element.text).strip()

    def _fetch_url(self, url: str) -> str:
        request = Request(
            url,
            headers={"User-Agent": "reddit-opportunity-radar/0.1 read-only RSS"},
        )
        with urlopen(request, timeout=20) as response:
            return response.read().decode("utf-8")
