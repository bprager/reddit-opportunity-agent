class Classifier:
    """Classifies Reddit items into local leads, remote opportunities, or ignore."""

    def classify(self, title: str, body: str) -> dict:
        raise NotImplementedError("Add rules first, then LLM classification.")
