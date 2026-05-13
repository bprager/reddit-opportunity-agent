import unittest

from reddit_radar.classifier import Classifier
from reddit_radar.scorer import OpportunityScorer

from test_regression_examples import load_examples


class OpportunityScorerTests(unittest.TestCase):
    def test_scorer_places_examples_inside_expected_score_bands(self) -> None:
        classifier = Classifier()
        scorer = OpportunityScorer()

        for example in load_examples():
            with self.subTest(example=example["id"]):
                classification = classifier.classify(example["title"], example["body"])
                result = scorer.score(
                    {
                        "title": example["title"],
                        "body": example["body"],
                        "source": example["source"],
                        "classification": classification,
                    }
                )
                score_band = example["expected"]["score_band"]

                self.assertGreaterEqual(result["score"], score_band["min"])
                self.assertLessEqual(result["score"], score_band["max"])

    def test_scorer_returns_reviewable_breakdown(self) -> None:
        classifier = Classifier()
        scorer = OpportunityScorer()

        for example in load_examples():
            with self.subTest(example=example["id"]):
                classification = classifier.classify(example["title"], example["body"])
                result = scorer.score(
                    {
                        "title": example["title"],
                        "body": example["body"],
                        "source": example["source"],
                        "classification": classification,
                    }
                )

                self.assertIn("score", result)
                self.assertIn("breakdown", result)
                self.assertIn("reasons", result)
                self.assertTrue(result["breakdown"])
                self.assertTrue(result["reasons"])
                self.assertTrue(all("factor" in item for item in result["breakdown"]))
                self.assertTrue(all("points" in item for item in result["breakdown"]))

    def test_legacy_score_helpers_return_numeric_scores(self) -> None:
        scorer = OpportunityScorer()
        item = {
            "title": "Need help with automation",
            "body": "Remote project with 5000 USD budget",
            "classification": {"category": "remote_opportunity", "risk_flags": []},
        }

        self.assertEqual(85, scorer.score_remote_opportunity(item))
        self.assertEqual(85, scorer.score_local_client(item))


if __name__ == "__main__":
    unittest.main()
