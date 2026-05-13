import unittest

from reddit_radar.classifier import Classifier

from test_regression_examples import load_examples


class ClassifierRuleTests(unittest.TestCase):
    def test_classifier_assigns_expected_category_for_regression_examples(self) -> None:
        classifier = Classifier()

        for example in load_examples():
            with self.subTest(example=example["id"]):
                result = classifier.classify(example["title"], example["body"])

                self.assertEqual(example["expected"]["category"], result["category"])

    def test_classifier_returns_expected_risk_flags_for_regression_examples(self) -> None:
        classifier = Classifier()

        for example in load_examples():
            with self.subTest(example=example["id"]):
                result = classifier.classify(example["title"], example["body"])

                self.assertCountEqual(example["expected"]["risk_flags"], result["risk_flags"])

    def test_classifier_uses_ignore_fallback_for_unmatched_text(self) -> None:
        classifier = Classifier()

        result = classifier.classify("General discussion", "Interesting ideas.")

        self.assertEqual("ignore", result["category"])
        self.assertEqual([], result["risk_flags"])


if __name__ == "__main__":
    unittest.main()
