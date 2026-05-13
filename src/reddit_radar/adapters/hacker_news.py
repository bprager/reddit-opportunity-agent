from __future__ import annotations

import json
import re
from collections.abc import Callable
from html import unescape
from urllib.request import Request, urlopen

from reddit_radar.sources import (
    SourceDefinition,
    SourceItem,
    build_source_item_id,
    content_hash,
)

HN_BASE_URL = "https://hacker-news.firebaseio.com/v0"


class HackerNewsAdapter:
    def __init__(self, fetch_json: Callable[[str], object] | None = None) -> None:
        self.fetch_json = fetch_json or self._fetch_json

    def collect(self, source: SourceDefinition) -> list[SourceItem]:
        story_ids = self.fetch_json(f"{HN_BASE_URL}/{source.endpoint_or_query}.json")
        if not isinstance(story_ids, list):
            raise RuntimeError("Hacker News story list did not return a list.")

        items = []
        for story_id in story_ids[: source.item_limit]:
            raw_item = self.fetch_json(f"{HN_BASE_URL}/item/{story_id}.json")
            if isinstance(raw_item, dict) and raw_item.get("type") in {"job", "story"}:
                items.append(self._source_item_from_hn(source, raw_item))
        return items

    def _source_item_from_hn(self, source: SourceDefinition, item: dict) -> SourceItem:
        external_id = str(item["id"])
        title = self._clean_text(str(item.get("title", "")))
        body = self._clean_text(str(item.get("text", "")))
        canonical_url = str(
            item.get("url") or f"https://news.ycombinator.com/item?id={external_id}"
        )

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
            author_display=item.get("by"),
            published_at=str(item.get("time", "")),
            content_hash=content_hash(title, body, canonical_url),
            raw_metadata={
                "display_name": source.display_name,
                "hn_type": item.get("type", ""),
            },
            policy_status=source.policy_status,
        )

    def _clean_text(self, value: str) -> str:
        without_tags = re.sub(r"<[^>]+>", "", value)
        return unescape(without_tags).strip()

    def _fetch_json(self, url: str) -> object:
        request = Request(
            url,
            headers={"User-Agent": "reddit-opportunity-radar/0.2 read-only HN"},
        )
        with urlopen(request, timeout=20) as response:
            return json.loads(response.read().decode("utf-8"))
