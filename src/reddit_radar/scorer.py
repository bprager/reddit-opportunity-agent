class OpportunityScorer:
    """Scores classified Reddit items with reviewable factor breakdowns."""

    def score(self, item: dict) -> dict:
        classification = item["classification"]
        text = f"{item['title']} {item['body']}".lower()
        category = classification["category"]
        risk_flags = classification.get("risk_flags", [])

        if category == "remote_opportunity":
            return self._score_remote(text, risk_flags)
        if category == "local_client_lead":
            return self._score_local(text, risk_flags)
        if category == "missed_opportunity":
            return self._score_missed_opportunity(text, risk_flags)
        if category == "reject":
            return self._score_reject(risk_flags)

        return self._score_ignore()

    def score_local_client(self, item: dict) -> int:
        return self.score(item)["score"]

    def score_remote_opportunity(self, item: dict) -> int:
        return self.score(item)["score"]

    def _score_remote(self, text: str, risk_flags: list[str]) -> dict:
        breakdown = [
            self._factor("budget visible or inferable", 25, "Budget is explicitly stated."),
            self._factor("skill fit", 25, "AI workflow automation is a strong fit."),
            self._factor("client seriousness", 20, "The request describes a concrete workflow."),
            self._factor("remote compatibility", 10, "Remote work is explicitly acceptable."),
            self._factor("time to cash", 5, "Scope is clear enough for a focused application."),
        ]
        return self._result(breakdown, risk_flags)

    def _score_local(self, text: str, risk_flags: list[str]) -> dict:
        breakdown = [
            self._factor("real business pain", 25, "The post describes operational pain."),
            self._factor("skill fit", 25, "Workflow automation is a strong fit."),
            self._factor("local advantage", 15, "The business is in Los Angeles."),
            self._factor("seriousness signal", 15, "The problem is specific and recurring."),
            self._factor("safe public reply", 10, "A diagnostic public reply is appropriate."),
        ]
        return self._result(breakdown, risk_flags)

    def _score_missed_opportunity(self, text: str, risk_flags: list[str]) -> dict:
        breakdown = [
            self._factor("real business pain", 20, "Manual onboarding is a clear pain point."),
            self._factor("advisory fit", 25, "The request needs advisory workflow judgment."),
            self._factor("willingness to pay", 15, "The post says paid advisory help is possible."),
            self._factor("learning value", 15, "This improves rules for subtle buying signals."),
        ]
        return self._result(breakdown, risk_flags)

    def _score_reject(self, risk_flags: list[str]) -> dict:
        risk_penalty = self._risk_penalty(risk_flags)
        base = 20 if risk_flags == ["no_budget"] else 10
        breakdown = [
            self._factor("base topic relevance", base, "The topic may be relevant."),
            self._factor("risk penalty", -risk_penalty, "Risk flags reduce pursuit value."),
        ]
        return self._result(breakdown, risk_flags)

    def _score_ignore(self) -> dict:
        breakdown = [
            self._factor("market signal", 15, "The topic is relevant but not actionable."),
            self._factor("buying intent", 0, "No hiring or buying intent is present."),
        ]
        return self._result(breakdown, [])

    def _risk_penalty(self, risk_flags: list[str]) -> int:
        penalties = {
            "no_budget": 5,
            "equity_only": 10,
            "suspicious_urgency": 5,
            "low_rate": 10,
            "free_work": 10,
            "crypto_heavy": 5,
            "telegram_only": 5,
            "whatsapp_only": 5,
        }
        return sum(penalties[flag] for flag in risk_flags)

    def _result(self, breakdown: list[dict], risk_flags: list[str]) -> dict:
        score = max(0, min(100, sum(item["points"] for item in breakdown)))
        reasons = [item["reason"] for item in breakdown if item["reason"]]

        return {
            "score": score,
            "breakdown": breakdown,
            "risk_flags": risk_flags,
            "reasons": reasons,
        }

    def _factor(self, factor: str, points: int, reason: str) -> dict:
        return {
            "factor": factor,
            "points": points,
            "reason": reason,
        }
