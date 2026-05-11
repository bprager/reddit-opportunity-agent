from datetime import datetime
from enum import StrEnum

from sqlmodel import Field, SQLModel


class RadarType(StrEnum):
    LOCAL_CLIENT = "local_client"
    REMOTE_OPPORTUNITY = "remote_opportunity"


class RedditItem(SQLModel, table=True):
    id: str = Field(primary_key=True)
    subreddit: str
    title: str
    body: str = ""
    author: str | None = None
    url: str
    created_utc: datetime
    collected_at: datetime = Field(default_factory=datetime.utcnow)


class OpportunityAssessment(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    reddit_item_id: str = Field(foreign_key="reddititem.id")
    radar_type: RadarType
    category: str
    score: int
    estimated_value: str | None = None
    risks: str = ""
    recommended_action: str
    draft_reply: str = ""
    created_at: datetime = Field(default_factory=datetime.utcnow)


class MissedReason(StrEnum):
    SOURCE_NOT_MONITORED = "source_not_monitored"
    SEARCH_PHRASE_MISSING = "search_phrase_missing"
    CLASSIFIER_FAILED = "classifier_failed"
    SCORE_TOO_LOW = "score_too_low"
    RISK_TOO_AGGRESSIVE = "risk_too_aggressive"
    CATEGORY_MISSING = "category_missing"
    LOCALITY_SIGNAL_MISSED = "locality_signal_missed"
    BUDGET_SIGNAL_MISSED = "budget_signal_missed"


class MissedOpportunity(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    source_url: str
    title: str
    notes: str = ""
    missed_reason: MissedReason
    created_at: datetime = Field(default_factory=datetime.utcnow)


class SourceCandidate(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    source_name: str
    source_type: str
    reason: str
    expected_signal: str = ""
    status: str = "candidate"
    created_at: datetime = Field(default_factory=datetime.utcnow)


class LearningEvent(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    event_type: str
    reason: str
    before: str = ""
    after: str = ""
    expected_effect: str = ""
    created_at: datetime = Field(default_factory=datetime.utcnow)
