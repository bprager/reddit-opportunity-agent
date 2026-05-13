from datetime import datetime
import unittest

from reddit_radar.models import (
    LearningEvent,
    MissedOpportunity,
    MissedReason,
    OpportunityAssessment,
    RadarType,
    RedditItem,
    SourceCandidate,
)


class ModelTests(unittest.TestCase):
    def test_models_can_be_created_with_expected_defaults(self) -> None:
        item = RedditItem(
            id="abc",
            subreddit="forhire",
            title="Need help",
            author=None,
            url="https://reddit.com/abc",
            created_utc=datetime(2026, 1, 1),
        )
        assessment = OpportunityAssessment(
            reddit_item_id=item.id,
            radar_type=RadarType.REMOTE_OPPORTUNITY,
            category="remote_opportunity",
            score=91,
            recommended_action="review",
        )
        missed = MissedOpportunity(
            source_url=item.url,
            title=item.title,
            missed_reason=MissedReason.SEARCH_PHRASE_MISSING,
        )
        candidate = SourceCandidate(
            source_name="Python jobs",
            source_type="rss",
            reason="More remote posts",
        )
        event = LearningEvent(event_type="rule", reason="Tuned phrase")

        self.assertEqual("", item.body)
        self.assertEqual("", assessment.risks)
        self.assertEqual("candidate", candidate.status)
        self.assertEqual("", event.before)
        self.assertEqual(MissedReason.SEARCH_PHRASE_MISSING, missed.missed_reason)


if __name__ == "__main__":
    unittest.main()
