from reddit_radar.classifier import Classifier
from reddit_radar.scorer import OpportunityScorer
from reddit_radar.storage import OpportunityStore


def save_example(store: OpportunityStore, example: dict) -> int:
    classifier = Classifier()
    scorer = OpportunityScorer()
    classification = classifier.classify(example["title"], example["body"])
    score = scorer.score(
        {
            "title": example["title"],
            "body": example["body"],
            "source": example["source"],
            "classification": classification,
        }
    )

    return store.save_assessed_item(
        item={
            "id": example["id"],
            "source": example["source"],
            "title": example["title"],
            "body": example["body"],
            "url": f"https://reddit.com/{example['id']}",
        },
        classification=classification,
        score=score,
        recommended_action=example["expected"]["recommended_action"],
    )
