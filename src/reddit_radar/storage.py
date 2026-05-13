import json
import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
from pathlib import Path


ALLOWED_DECISIONS = {
    "ignored",
    "saved",
    "replied",
    "applied",
    "follow_up",
    "converted",
    "rejected",
    "false_positive",
    "false_negative",
}


class OpportunityStore:
    """Small SQLite persistence layer for assessed opportunities and decisions."""

    def __init__(self, database_path: str | Path) -> None:
        self.database_path = Path(database_path)

    def init_schema(self) -> None:
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS reddit_items (
                    id TEXT PRIMARY KEY,
                    source TEXT NOT NULL,
                    title TEXT NOT NULL,
                    body TEXT NOT NULL,
                    author TEXT,
                    url TEXT NOT NULL,
                    collected_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS opportunity_assessments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    reddit_item_id TEXT NOT NULL,
                    category TEXT NOT NULL,
                    score INTEGER NOT NULL,
                    risk_flags_json TEXT NOT NULL,
                    score_breakdown_json TEXT NOT NULL,
                    reasons_json TEXT NOT NULL,
                    recommended_action TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY (reddit_item_id) REFERENCES reddit_items (id)
                );

                CREATE TABLE IF NOT EXISTS human_decisions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    assessment_id INTEGER NOT NULL,
                    decision TEXT NOT NULL,
                    notes TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY (assessment_id) REFERENCES opportunity_assessments (id)
                );

                CREATE TABLE IF NOT EXISTS missed_opportunities (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source_url TEXT NOT NULL,
                    title TEXT NOT NULL,
                    notes TEXT NOT NULL,
                    missed_reason TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS source_candidates (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source_name TEXT NOT NULL,
                    source_type TEXT NOT NULL,
                    reason TEXT NOT NULL,
                    expected_signal TEXT NOT NULL,
                    expected_noise TEXT NOT NULL,
                    status TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS learning_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_type TEXT NOT NULL,
                    reason TEXT NOT NULL,
                    before TEXT NOT NULL,
                    after TEXT NOT NULL,
                    expected_effect TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS source_health (
                    source_id TEXT PRIMARY KEY,
                    status TEXT NOT NULL,
                    failure_count INTEGER NOT NULL,
                    last_success_at TEXT NOT NULL,
                    last_failure_at TEXT NOT NULL,
                    disabled_until TEXT NOT NULL,
                    last_error TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                );
                """
            )

    def save_assessed_item(
        self,
        item: dict,
        classification: dict,
        score: dict,
        recommended_action: str,
    ) -> int:
        now = self._now()
        with self._connect() as connection:
            connection.execute(
                """
                INSERT OR REPLACE INTO reddit_items
                    (id, source, title, body, author, url, collected_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    item["id"],
                    item["source"],
                    item["title"],
                    item.get("body", ""),
                    item.get("author"),
                    item["url"],
                    now,
                ),
            )
            existing_assessment_id = self._existing_assessment_id(connection, item["id"])
            if existing_assessment_id is not None:
                connection.execute(
                    """
                    UPDATE opportunity_assessments
                    SET
                        category = ?,
                        score = ?,
                        risk_flags_json = ?,
                        score_breakdown_json = ?,
                        reasons_json = ?,
                        recommended_action = ?
                    WHERE id = ?
                    """,
                    (
                        classification["category"],
                        score["score"],
                        json.dumps(score.get("risk_flags", [])),
                        json.dumps(score.get("breakdown", [])),
                        json.dumps(score.get("reasons", [])),
                        recommended_action,
                        existing_assessment_id,
                    ),
                )
                return existing_assessment_id

            cursor = connection.execute(
                """
                INSERT INTO opportunity_assessments
                    (
                        reddit_item_id,
                        category,
                        score,
                        risk_flags_json,
                        score_breakdown_json,
                        reasons_json,
                        recommended_action,
                        created_at
                    )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    item["id"],
                    classification["category"],
                    score["score"],
                    json.dumps(score.get("risk_flags", [])),
                    json.dumps(score.get("breakdown", [])),
                    json.dumps(score.get("reasons", [])),
                    recommended_action,
                    now,
                ),
            )
            return int(cursor.lastrowid)

    def record_decision(self, assessment_id: int, decision: str, notes: str = "") -> int:
        if decision not in ALLOWED_DECISIONS:
            allowed = ", ".join(sorted(ALLOWED_DECISIONS))
            raise ValueError(f"Unsupported decision '{decision}'. Use one of: {allowed}.")

        with self._connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO human_decisions
                    (assessment_id, decision, notes, created_at)
                VALUES (?, ?, ?, ?)
                """,
                (assessment_id, decision, notes, self._now()),
            )
            return int(cursor.lastrowid)

    def list_assessments(self, limit: int = 20) -> list[dict]:
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT
                    opportunity_assessments.id AS assessment_id,
                    reddit_items.id AS item_id,
                    reddit_items.source,
                    reddit_items.title,
                    reddit_items.body,
                    reddit_items.url,
                    opportunity_assessments.category,
                    opportunity_assessments.score,
                    opportunity_assessments.risk_flags_json,
                    opportunity_assessments.score_breakdown_json,
                    opportunity_assessments.reasons_json,
                    opportunity_assessments.recommended_action,
                    latest_decisions.decision,
                    latest_decisions.notes AS decision_notes
                FROM opportunity_assessments
                JOIN reddit_items
                    ON reddit_items.id = opportunity_assessments.reddit_item_id
                LEFT JOIN (
                    SELECT human_decisions.*
                    FROM human_decisions
                    JOIN (
                        SELECT assessment_id, MAX(id) AS latest_id
                        FROM human_decisions
                        GROUP BY assessment_id
                    ) AS latest
                        ON latest.latest_id = human_decisions.id
                ) AS latest_decisions
                    ON latest_decisions.assessment_id = opportunity_assessments.id
                ORDER BY opportunity_assessments.score DESC,
                    opportunity_assessments.id ASC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()

        return [self._assessment_from_row(row) for row in rows]

    def list_open_assessments(self, limit: int = 20) -> list[dict]:
        return [
            item
            for item in self.list_assessments(limit=limit)
            if item["decision"] is None
        ]

    def list_by_decision(self, decision: str, limit: int = 20) -> list[dict]:
        if decision not in ALLOWED_DECISIONS:
            allowed = ", ".join(sorted(ALLOWED_DECISIONS))
            raise ValueError(f"Unsupported decision '{decision}'. Use one of: {allowed}.")

        return [
            item
            for item in self.list_assessments(limit=limit)
            if item["decision"] == decision
        ]

    def add_missed_opportunity(
        self,
        source_url: str,
        title: str,
        notes: str,
        missed_reason: str,
    ) -> int:
        with self._connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO missed_opportunities
                    (source_url, title, notes, missed_reason, created_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (source_url, title, notes, missed_reason, self._now()),
            )
            return int(cursor.lastrowid)

    def list_missed_opportunities(self, limit: int = 20) -> list[dict]:
        return self._list_table("missed_opportunities", limit)

    def add_source_candidate(
        self,
        source_name: str,
        source_type: str,
        reason: str,
        expected_signal: str = "",
        expected_noise: str = "",
        status: str = "candidate",
    ) -> int:
        with self._connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO source_candidates
                    (
                        source_name,
                        source_type,
                        reason,
                        expected_signal,
                        expected_noise,
                        status,
                        created_at
                    )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    source_name,
                    source_type,
                    reason,
                    expected_signal,
                    expected_noise,
                    status,
                    self._now(),
                ),
            )
            return int(cursor.lastrowid)

    def list_source_candidates(self, limit: int = 20) -> list[dict]:
        return self._list_table("source_candidates", limit)

    def add_learning_event(
        self,
        event_type: str,
        reason: str,
        before: str = "",
        after: str = "",
        expected_effect: str = "",
    ) -> int:
        with self._connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO learning_events
                    (event_type, reason, before, after, expected_effect, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (event_type, reason, before, after, expected_effect, self._now()),
            )
            return int(cursor.lastrowid)

    def list_learning_events(self, limit: int = 20) -> list[dict]:
        return self._list_table("learning_events", limit)

    def record_source_success(self, source_id: str) -> None:
        now = self._now()
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO source_health (
                    source_id,
                    status,
                    failure_count,
                    last_success_at,
                    last_failure_at,
                    disabled_until,
                    last_error,
                    updated_at
                )
                VALUES (?, 'healthy', 0, ?, '', '', '', ?)
                ON CONFLICT(source_id) DO UPDATE SET
                    status = 'healthy',
                    failure_count = 0,
                    last_success_at = excluded.last_success_at,
                    disabled_until = '',
                    last_error = '',
                    updated_at = excluded.updated_at
                """,
                (source_id, now, now),
            )

    def record_source_failure(
        self,
        source_id: str,
        error: str,
        backoff_minutes: int = 15,
    ) -> None:
        now = datetime.now(timezone.utc)
        disabled_until = (now + timedelta(minutes=backoff_minutes)).isoformat()
        now_text = now.isoformat()
        with self._connect() as connection:
            existing = connection.execute(
                "SELECT failure_count FROM source_health WHERE source_id = ?",
                (source_id,),
            ).fetchone()
            failure_count = 1 if existing is None else int(existing["failure_count"]) + 1
            connection.execute(
                """
                INSERT INTO source_health (
                    source_id,
                    status,
                    failure_count,
                    last_success_at,
                    last_failure_at,
                    disabled_until,
                    last_error,
                    updated_at
                )
                VALUES (?, 'degraded', ?, '', ?, ?, ?, ?)
                ON CONFLICT(source_id) DO UPDATE SET
                    status = 'degraded',
                    failure_count = excluded.failure_count,
                    last_failure_at = excluded.last_failure_at,
                    disabled_until = excluded.disabled_until,
                    last_error = excluded.last_error,
                    updated_at = excluded.updated_at
                """,
                (
                    source_id,
                    failure_count,
                    now_text,
                    disabled_until,
                    error,
                    now_text,
                ),
            )

    def list_source_health(self) -> dict[str, dict]:
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT * FROM source_health ORDER BY source_id ASC"
            ).fetchall()
        return {row["source_id"]: dict(row) for row in rows}

    def source_is_backed_off(self, source_id: str) -> bool:
        health = self.list_source_health().get(source_id)
        if not health or not health["disabled_until"]:
            return False
        disabled_until = datetime.fromisoformat(health["disabled_until"])
        return disabled_until > datetime.now(timezone.utc)

    def _assessment_from_row(self, row: sqlite3.Row) -> dict:
        return {
            "assessment_id": row["assessment_id"],
            "item_id": row["item_id"],
            "source": row["source"],
            "title": row["title"],
            "body": row["body"],
            "url": row["url"],
            "category": row["category"],
            "score": row["score"],
            "risk_flags": json.loads(row["risk_flags_json"]),
            "score_breakdown": json.loads(row["score_breakdown_json"]),
            "reasons": json.loads(row["reasons_json"]),
            "recommended_action": row["recommended_action"],
            "decision": row["decision"],
            "decision_notes": row["decision_notes"],
        }

    @contextmanager
    def _connect(self) -> Iterator[sqlite3.Connection]:
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        try:
            yield connection
            connection.commit()
        finally:
            connection.close()

    def _existing_assessment_id(
        self,
        connection: sqlite3.Connection,
        reddit_item_id: str,
    ) -> int | None:
        row = connection.execute(
            """
            SELECT id
            FROM opportunity_assessments
            WHERE reddit_item_id = ?
            ORDER BY id ASC
            LIMIT 1
            """,
            (reddit_item_id,),
        ).fetchone()
        if row is None:
            return None
        return int(row["id"])

    def _now(self) -> str:
        return datetime.now(timezone.utc).isoformat()

    def _list_table(self, table_name: str, limit: int) -> list[dict]:
        with self._connect() as connection:
            rows = connection.execute(
                f"SELECT * FROM {table_name} ORDER BY id DESC LIMIT ?",
                (limit,),
            ).fetchall()
        return [dict(row) for row in rows]
