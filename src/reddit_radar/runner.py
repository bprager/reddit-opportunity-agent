import argparse
import json
from pathlib import Path

from .adapters.hacker_news import HackerNewsAdapter
from .adapters.lobsters import LobstersRssAdapter, lobsters_source
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
    failed = 0
    skipped = 0
    store = OpportunityStore(database_path)
    store.init_schema()

    for source in sources:
        if store.source_is_backed_off(source.source_id):
            skipped += 1
            continue

        adapter = adapters[source.acquisition_method]
        try:
            source_items = adapter.collect(source)
        except RuntimeError as error:
            failed += 1
            store.record_source_failure(source.source_id, str(error))
            continue

        store.record_source_success(source.source_id)
        collected_items.extend(item.to_pipeline_item() for item in source_items)

    pipeline = RadarPipeline(store)
    saved_ids = pipeline.process_items(collected_items)

    return {
        "sources": len(sources),
        "collected": len(collected_items),
        "saved": len(saved_ids),
        "open": len(store.list_open_assessments(limit=1000)),
        "failed": failed,
        "skipped": skipped,
    }


def run_reddit_shadow_collection(
    rss_adapter: object,
    api_adapter: object,
    database_path: str | Path,
) -> dict:
    rss_source = SourceDefinition(
        source_id="reddit-shadow-rss",
        display_name="Reddit RSS shadow",
        platform="reddit",
        acquisition_method="rss_feed",
        endpoint_or_query="https://www.reddit.com/r/forhire/.rss",
    )
    api_source = SourceDefinition(
        source_id="reddit-shadow-api",
        display_name="Reddit API shadow",
        platform="reddit",
        acquisition_method="reddit_api_praw",
        endpoint_or_query="forhire",
    )
    rss_items = [item.to_pipeline_item() for item in rss_adapter.collect(rss_source)]
    api_items = [item.to_pipeline_item() for item in api_adapter.collect(api_source)]
    rss_ids = {item["id"] for item in rss_items}
    api_ids = {item["id"] for item in api_items}

    return {
        "rss_collected": len(rss_items),
        "api_collected": len(api_items),
        "overlap": len(rss_ids & api_ids),
        "rss_only": len(rss_ids - api_ids),
        "api_only": len(api_ids - rss_ids),
        "persisted": 0,
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


def hn_source_from_arg(value: str, limit: int) -> SourceDefinition:
    source_id, endpoint = _source_pair(value, "HN sources")
    return SourceDefinition(
        source_id=source_id,
        display_name=source_id,
        platform="hacker_news",
        acquisition_method="hacker_news_api",
        endpoint_or_query=endpoint,
        item_limit=limit,
    )


def lobsters_source_from_arg(value: str, limit: int) -> SourceDefinition:
    source_id, tag_query = _source_pair(value, "Lobsters sources")
    return lobsters_source(source_id=source_id, tag_query=tag_query, limit=limit)


def _source_pair(value: str, label: str) -> tuple[str, str]:
    if "=" not in value:
        raise ValueError(f"{label} must use SOURCE_ID=QUERY format.")

    source_id, query = value.split("=", 1)
    source_id = source_id.strip()
    query = query.strip()
    if not source_id or not query:
        raise ValueError(f"{label} must include both SOURCE_ID and QUERY.")
    return source_id, query


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
    parser.add_argument(
        "--hn-source",
        action="append",
        default=[],
        help="Hacker News source in SOURCE_ID=ENDPOINT format, such as hn-jobs=jobstories.",
    )
    parser.add_argument(
        "--lobsters-source",
        action="append",
        default=[],
        help="Lobsters source in SOURCE_ID=TAGS format, such as lobsters-jobs=job,python.",
    )
    args = parser.parse_args()

    if args.rss_source or args.hn_source or args.lobsters_source:
        try:
            sources = [
                rss_source_from_arg(value, limit=args.limit or 10)
                for value in args.rss_source
            ]
            sources.extend(
                hn_source_from_arg(value, limit=args.limit or 10)
                for value in args.hn_source
            )
            sources.extend(
                lobsters_source_from_arg(value, limit=args.limit or 10)
                for value in args.lobsters_source
            )
            result = run_source_collection(
                registry=SourceRegistry(sources),
                adapters={
                    "rss_feed": RssFeedAdapter(),
                    "hacker_news_api": HackerNewsAdapter(),
                    "lobsters_rss": LobstersRssAdapter(),
                },
                database_path=args.database,
            )
        except (RuntimeError, ValueError) as error:
            raise SystemExit(f"Source collection stopped: {error}") from None
        print(
            "Source collection complete: "
            f"{result['sources']} sources, "
            f"{result['collected']} collected, "
            f"{result['saved']} assessed, "
            f"{result['open']} open for review, "
            f"{result['failed']} failed, "
            f"{result['skipped']} skipped."
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
