import sqlite3
import tempfile
import unittest
from pathlib import Path

from reddit_radar.storage import OpportunityStore

from helpers import save_example
from test_regression_examples import load_examples


class OpportunityStoreTests(unittest.TestCase):
    def test_connect_context_closes_database_connection(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            store = OpportunityStore(Path(temp_dir) / "radar.db")
            with store._connect() as connection:
                connection.execute("SELECT 1")

            with self.assertRaises(sqlite3.ProgrammingError):
                connection.execute("SELECT 1")

    def test_store_saves_and_lists_assessed_opportunity(self) -> None:
        example = load_examples()[0]

        with tempfile.TemporaryDirectory() as temp_dir:
            store = OpportunityStore(Path(temp_dir) / "radar.db")
            store.init_schema()
            assessment_id = save_example(store, example)
            assessments = store.list_assessments()

        self.assertEqual(1, len(assessments))
        self.assertEqual(assessment_id, assessments[0]["assessment_id"])
        self.assertEqual(example["expected"]["category"], assessments[0]["category"])
        self.assertEqual(example["expected"]["risk_flags"], assessments[0]["risk_flags"])
        self.assertTrue(assessments[0]["score_breakdown"])
        self.assertTrue(assessments[0]["reasons"])

    def test_store_records_human_decision_for_assessment(self) -> None:
        example = load_examples()[0]

        with tempfile.TemporaryDirectory() as temp_dir:
            store = OpportunityStore(Path(temp_dir) / "radar.db")
            store.init_schema()
            assessment_id = save_example(store, example)
            decision_id = store.record_decision(
                assessment_id=assessment_id,
                decision="saved",
                notes="Worth reviewing after first daily run.",
            )
            assessments = store.list_assessments()

        self.assertGreater(decision_id, 0)
        self.assertEqual("saved", assessments[0]["decision"])
        self.assertEqual("Worth reviewing after first daily run.", assessments[0]["decision_notes"])

    def test_store_rejects_unknown_decisions(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            store = OpportunityStore(Path(temp_dir) / "radar.db")
            store.init_schema()

            with self.assertRaisesRegex(ValueError, "Unsupported decision"):
                store.record_decision(assessment_id=1, decision="maybe")

            with self.assertRaisesRegex(ValueError, "Unsupported decision"):
                store.list_by_decision("maybe")

    def test_store_lists_open_assessments_without_human_decisions(self) -> None:
        examples = load_examples()[:2]

        with tempfile.TemporaryDirectory() as temp_dir:
            store = OpportunityStore(Path(temp_dir) / "radar.db")
            store.init_schema()
            first_id = save_example(store, examples[0])
            second_id = save_example(store, examples[1])
            store.record_decision(first_id, "saved")
            open_assessments = store.list_open_assessments()

        self.assertEqual([second_id], [item["assessment_id"] for item in open_assessments])

    def test_store_lists_assessments_by_decision(self) -> None:
        examples = load_examples()[:2]

        with tempfile.TemporaryDirectory() as temp_dir:
            store = OpportunityStore(Path(temp_dir) / "radar.db")
            store.init_schema()
            saved_id = save_example(store, examples[0])
            rejected_id = save_example(store, examples[1])
            store.record_decision(saved_id, "saved")
            store.record_decision(rejected_id, "rejected")
            saved_items = store.list_by_decision("saved")

        self.assertEqual([saved_id], [item["assessment_id"] for item in saved_items])
        self.assertEqual(["saved"], [item["decision"] for item in saved_items])


if __name__ == "__main__":
    unittest.main()
