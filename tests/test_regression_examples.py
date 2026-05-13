import json
import unittest
from pathlib import Path


EXAMPLES_PATH = Path("tests/fixtures/opportunity_examples.json")
REQUIRED_IDS = {
    "strong_remote_ai_automation",
    "strong_local_la_business",
    "scam_risk_reject",
    "weak_no_budget_lead",
    "false_positive_learning",
    "missed_opportunity_learning",
}
REQUIRED_CATEGORIES = {
    "remote_opportunity",
    "local_client_lead",
    "reject",
    "ignore",
    "missed_opportunity",
}
REQUIRED_RISKS = {
    "no_budget",
    "equity_only",
    "suspicious_urgency",
    "low_rate",
    "free_work",
    "crypto_heavy",
    "telegram_only",
    "whatsapp_only",
}


def load_examples() -> list[dict]:
    return json.loads(EXAMPLES_PATH.read_text(encoding="utf-8"))


class RegressionExampleTests(unittest.TestCase):
    def test_regression_examples_cover_core_phase_one_cases(self) -> None:
        examples = load_examples()
        ids = {example["id"] for example in examples}
        categories = {example["expected"]["category"] for example in examples}
        risks = {
            risk
            for example in examples
            for risk in example["expected"].get("risk_flags", [])
        }

        self.assertLessEqual(REQUIRED_IDS, ids)
        self.assertLessEqual(REQUIRED_CATEGORIES, categories)
        self.assertLessEqual(REQUIRED_RISKS, risks)

    def test_regression_examples_have_reviewable_expected_outcomes(self) -> None:
        examples = load_examples()

        for example in examples:
            with self.subTest(example=example["id"]):
                self.assertTrue(example["title"].strip())
                self.assertTrue(example["body"].strip())
                self.assertTrue(example["source"].startswith("r/"))
                self.assertIn(example["expected"]["category"], REQUIRED_CATEGORIES)
                self.assertGreaterEqual(example["expected"]["score_band"]["min"], 0)
                self.assertLessEqual(example["expected"]["score_band"]["min"], 100)
                self.assertGreaterEqual(example["expected"]["score_band"]["max"], 0)
                self.assertLessEqual(example["expected"]["score_band"]["max"], 100)
                self.assertLessEqual(
                    example["expected"]["score_band"]["min"],
                    example["expected"]["score_band"]["max"],
                )
                self.assertTrue(example["expected"]["recommended_action"].strip())
                self.assertTrue(example["expected"]["why"].strip())


if __name__ == "__main__":
    unittest.main()
