from collections.abc import Iterable

from .classifier import Classifier
from .scorer import OpportunityScorer
from .storage import OpportunityStore


RECOMMENDED_ACTIONS = {
    "remote_opportunity": (
        "Review and prepare a focused application note with one workflow-mapping question."
    ),
    "local_client_lead": (
        "Save for review and draft a public reply with one diagnostic scheduling question."
    ),
    "missed_opportunity": (
        "Add as a missed-opportunity regression example and tune rules to catch advisory "
        "buying signals."
    ),
    "reject": "Reject without drafting outreach.",
    "ignore": "Ignore as an opportunity, but optionally save as a market signal.",
}


class RadarPipeline:
    """Assess collected Reddit items and persist reviewable opportunity records."""

    def __init__(
        self,
        store: OpportunityStore,
        classifier: Classifier | None = None,
        scorer: OpportunityScorer | None = None,
    ) -> None:
        self.store = store
        self.classifier = classifier or Classifier()
        self.scorer = scorer or OpportunityScorer()

    def process_items(self, items: Iterable[dict]) -> list[int]:
        saved_ids = []
        for item in items:
            classification = self.classifier.classify(item["title"], item.get("body", ""))
            score = self.scorer.score(
                {
                    "title": item["title"],
                    "body": item.get("body", ""),
                    "source": item["source"],
                    "classification": classification,
                }
            )
            saved_ids.append(
                self.store.save_assessed_item(
                    item=self._storage_item(item),
                    classification=classification,
                    score=score,
                    recommended_action=self._recommended_action(classification["category"]),
                )
            )

        return saved_ids

    def _storage_item(self, item: dict) -> dict:
        return {
            "id": item["id"],
            "source": item["source"],
            "title": item["title"],
            "body": item.get("body", ""),
            "author": item.get("author"),
            "url": item.get("url", f"https://reddit.com/{item['id']}"),
        }

    def _recommended_action(self, category: str) -> str:
        return RECOMMENDED_ACTIONS.get(category, RECOMMENDED_ACTIONS["ignore"])
