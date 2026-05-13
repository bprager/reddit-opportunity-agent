import tempfile
import unittest
from pathlib import Path

from reddit_radar.storage import OpportunityStore


class LearningLoopStorageTests(unittest.TestCase):
    def test_store_records_missed_opportunity(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            store = OpportunityStore(Path(temp_dir) / "radar.db")
            store.init_schema()
            missed_id = store.add_missed_opportunity(
                source_url="https://reddit.com/r/SaaS/example",
                title="Need help reducing manual onboarding",
                notes="Good advisory signal that rules should catch.",
                missed_reason="classifier_failed",
            )
            missed = store.list_missed_opportunities()

        self.assertGreater(missed_id, 0)
        self.assertEqual(1, len(missed))
        self.assertEqual("classifier_failed", missed[0]["missed_reason"])
        self.assertEqual("Need help reducing manual onboarding", missed[0]["title"])

    def test_store_records_source_candidate(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            store = OpportunityStore(Path(temp_dir) / "radar.db")
            store.init_schema()
            candidate_id = store.add_source_candidate(
                source_name="r/SaaS",
                source_type="subreddit",
                reason="Contains founder workflow pain and advisory opportunities.",
                expected_signal="B2B SaaS workflow and automation problems.",
                expected_noise="medium",
            )
            candidates = store.list_source_candidates()

        self.assertGreater(candidate_id, 0)
        self.assertEqual(1, len(candidates))
        self.assertEqual("r/SaaS", candidates[0]["source_name"])
        self.assertEqual("candidate", candidates[0]["status"])

    def test_store_records_learning_event(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            store = OpportunityStore(Path(temp_dir) / "radar.db")
            store.init_schema()
            event_id = store.add_learning_event(
                event_type="scoring_rule_change",
                reason="No-budget posts rarely convert.",
                before="budget weight 25",
                after="budget hard reject unless strong buying signal exists",
                expected_effect="Fewer weak startup ideas in the queue.",
            )
            events = store.list_learning_events()

        self.assertGreater(event_id, 0)
        self.assertEqual(1, len(events))
        self.assertEqual("scoring_rule_change", events[0]["event_type"])
        self.assertIn("No-budget", events[0]["reason"])


if __name__ == "__main__":
    unittest.main()
