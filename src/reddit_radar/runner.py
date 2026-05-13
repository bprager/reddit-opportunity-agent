import argparse
import json
from pathlib import Path

from .adapters.rss import RssFeedAdapter
from .collector import DryRunCollector, RedditCollector
from .pipeline import RadarPipeline
from .sources import SourceDefinition, SourceRegistry
from .storage import OpportunityStore


def run_dry_run_collection(
    fixture_path: str | Path,
    database_path: str | Path,
    limit: int | None = None,
) -> dict:
    items = json.loads(Path(fixture_path).read_text(encoding="utf-8"))
    collector = DryRunCollector(items)
    collected_items = collector.collect_all(limit=limit)

    store = OpportunityStore(database_path)
    store.init_schema()
    pipeline = RadarPipeline(store)
    saved_ids = pipeline.process_items(collected_items)

    return {
        "collected": len(collected_items),
        "saved": len(saved_ids),
        "open": len(store.list_open_assessments(limit=1000)),
    }


def run_live_collection(
    subreddits: list[str],
    database_path: str | Path,
    limit: int = 5,
    collector: RedditCollector | None = None,
) -> dict:
    live_collector = collector or RedditCollector()
    collected_items = []
    for subreddit in subreddits:
        collected_items.extend(live_collector.collect_subreddit(subreddit, limit=limit))

    store = OpportunityStore(database_path)
    store.init_schema()
    pipeline = RadarPipeline(store)
    saved_ids = pipeline.process_items(collected_items)

    return {
        "subreddits": len(subreddits),
        "collected": len(collected_items),
        "saved": len(saved_ids),
        "open": len(store.list_open_assessments(limit=1000)),
    }


def run_source_collection(
    registry: SourceRegistry,
    adapters: dict[str, object],
    database_path: str | Path,
) -> dict:
    collected_items = []
    sources = registry.enabled_sources()
    for source in sources:
        adapter = adapters[source.acquisition_method]
        source_items = adapter.collect(source)
        collected_items.extend(item.to_pipeline_item() for item in source_items)

    store = OpportunityStore(database_path)
    store.init_schema()
    pipeline = RadarPipeline(store)
    saved_ids = pipeline.process_items(collected_items)

    return {
        "sources": len(sources),
        "collected": len(collected_items),
        "saved": len(saved_ids),
        "open": len(store.list_open_assessments(limit=1000)),
    }


def rss_source_from_arg(value: str, limit: int) -> SourceDefinition:
    if "=" not in value:
        raise ValueError("RSS sources must use SOURCE_ID=URL format.")

    source_id, url = value.split("=", 1)
    source_id = source_id.strip()
    url = url.strip()
    if not source_id or not url:
        raise ValueError("RSS sources must include both SOURCE_ID and URL.")

    return SourceDefinition(
        source_id=source_id,
        display_name=source_id,
        platform="rss",
        acquisition_method="rss_feed",
        endpoint_or_query=url,
        item_limit=limit,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the local Reddit radar pipeline.")
    parser.add_argument(
        "--dry-run-fixtures",
        default="tests/fixtures/opportunity_examples.json",
        help="Path to fixture Reddit items for local dry runs.",
    )
    parser.add_argument(
        "--database",
        default="reddit_radar.db",
        help="SQLite database path.",
    )
    parser.add_argument("--limit", type=int, default=None, help="Optional maximum item count.")
    parser.add_argument(
        "--live-subreddit",
        action="append",
        default=[],
        help="Subreddit to collect from Reddit. Repeat for multiple subreddits.",
    )
    parser.add_argument(
        "--rss-source",
        action="append",
        default=[],
        help="RSS source in SOURCE_ID=URL format. Repeat for multiple feeds.",
    )
    args = parser.parse_args()

    if args.rss_source:
        try:
            sources = [
                rss_source_from_arg(value, limit=args.limit or 10)
                for value in args.rss_source
            ]
            result = run_source_collection(
                registry=SourceRegistry(sources),
                adapters={"rss_feed": RssFeedAdapter()},
                database_path=args.database,
            )
        except (RuntimeError, ValueError) as error:
            raise SystemExit(f"RSS collection stopped: {error}") from None
        print(
            "RSS collection complete: "
            f"{result['sources']} sources, "
            f"{result['collected']} collected, "
            f"{result['saved']} assessed, "
            f"{result['open']} open for review."
        )
    elif args.live_subreddit:
        try:
            result = run_live_collection(
                subreddits=args.live_subreddit,
                database_path=args.database,
                limit=args.limit or 5,
            )
        except RuntimeError as error:
            raise SystemExit(f"Live collection stopped: {error}") from None
        print(
            "Live read-only smoke test complete: "
            f"{result['subreddits']} subreddits, "
            f"{result['collected']} collected, "
            f"{result['saved']} assessed, "
            f"{result['open']} open for review."
        )
    else:
        result = run_dry_run_collection(
            fixture_path=args.dry_run_fixtures,
            database_path=args.database,
            limit=args.limit,
        )
        print(
            "Dry run complete: "
            f"{result['collected']} collected, "
            f"{result['saved']} assessed, "
            f"{result['open']} open for review."
        )


if __name__ == "__main__":
    main()
