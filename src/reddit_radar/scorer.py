class OpportunityScorer:
    """Scores local client leads and remote opportunities."""

    def score_local_client(self, item: dict) -> int:
        raise NotImplementedError

    def score_remote_opportunity(self, item: dict) -> int:
        raise NotImplementedError
