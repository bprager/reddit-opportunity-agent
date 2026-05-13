import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass(frozen=True)
class SourceDefinition:
    source_id: str
    display_name: str
    platform: str
    acquisition_method: str
    endpoint_or_query: str
    enabled: bool = True
    priority: int = 100
    poll_interval_minutes: int = 1440
    item_limit: int = 10
    cursor: str = ""
    policy_status: str = "allowed"
    notes: str = ""


@dataclass(frozen=True)
class SourceItem:
    id: str
    source_id: str
    platform: str
    acquisition_method: str
    external_id: str
    canonical_url: str
    title: str
    body: str = ""
    author_display: str | None = None
    published_at: str = ""
    collected_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    content_hash: str = ""
    raw_metadata: dict = field(default_factory=dict)
    policy_status: str = "allowed"

    def to_pipeline_item(self) -> dict:
        return {
            "id": self.id,
            "source": self.source_id,
            "title": self.title,
            "body": self.body,
            "author": self.author_display,
            "url": self.canonical_url,
        }


class SourceRegistry:
    def __init__(self, sources: list[SourceDefinition]) -> None:
        self.sources = list(sources)

    def enabled_sources(self) -> list[SourceDefinition]:
        return sorted(
            [
                source
                for source in self.sources
                if source.enabled and source.policy_status != "disabled"
            ],
            key=lambda source: (source.priority, source.source_id),
        )


def build_source_item_id(source_id: str, external_id: str, canonical_url: str, title: str) -> str:
    if external_id:
        stable_key = external_id
    elif canonical_url:
        stable_key = canonical_url
    else:
        stable_key = title

    digest = hashlib.sha256(stable_key.encode("utf-8")).hexdigest()[:16]
    return f"{source_id}:{external_id or digest}"


def content_hash(title: str, body: str, canonical_url: str) -> str:
    payload = json.dumps(
        {"title": title.strip(), "body": body.strip(), "url": canonical_url.strip()},
        sort_keys=True,
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()
