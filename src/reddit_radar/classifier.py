class Classifier:
    """Classifies Reddit items into local leads, remote opportunities, or ignore."""

    def classify(self, title: str, body: str) -> dict:
        text = f"{title} {body}".lower()
        risk_flags = self._risk_flags(text)

        if risk_flags:
            return {
                "category": "reject",
                "risk_flags": risk_flags,
                "method": "rules",
            }

        if self._is_missed_advisory_opportunity(text):
            return {
                "category": "missed_opportunity",
                "risk_flags": risk_flags,
                "method": "rules",
            }

        if self._is_ignore(text):
            return {
                "category": "ignore",
                "risk_flags": risk_flags,
                "method": "rules",
            }

        if self._is_local_client_lead(text):
            return {
                "category": "local_client_lead",
                "risk_flags": risk_flags,
                "method": "rules",
            }

        if self._is_remote_opportunity(text):
            return {
                "category": "remote_opportunity",
                "risk_flags": risk_flags,
                "method": "rules",
            }

        return {
            "category": "ignore",
            "risk_flags": risk_flags,
            "method": "rules",
        }

    def _risk_flags(self, text: str) -> list[str]:
        flags = []

        if "no budget" in text or "do not have a budget" in text:
            flags.append("no_budget")
        if "equity" in text and ("no cash" in text or "only" in text):
            flags.append("equity_only")
        if "urgent" in text or "immediately" in text or "today" in text:
            flags.append("suspicious_urgency")
        if "10 usd per hour" in text or "10 dollars per hour" in text:
            flags.append("low_rate")
        if "free architecture" in text or "trial tasks before payment" in text:
            flags.append("free_work")
        if "crypto" in text:
            flags.append("crypto_heavy")
        if "telegram" in text:
            flags.append("telegram_only")
        if "whatsapp" in text:
            flags.append("whatsapp_only")

        return flags

    def _is_missed_advisory_opportunity(self, text: str) -> bool:
        return (
            "advice" in text
            and "manual" in text
            and "onboarding" in text
            and "pay" in text
        )

    def _is_ignore(self, text: str) -> bool:
        return "not hiring" in text or "just want recommendations" in text

    def _is_local_client_lead(self, text: str) -> bool:
        return (
            "los angeles" in text
            and ("small service business" in text or "local shop" in text)
            and ("scheduling" in text or "spreadsheet" in text)
        )

    def _is_remote_opportunity(self, text: str) -> bool:
        has_hiring_signal = (
            "[hiring]" in text
            or "need help" in text
            or "looking for someone" in text
        )
        has_budget_signal = "budget" in text or "usd" in text
        has_remote_signal = "remote" in text
        has_fit_signal = "ai" in text or "workflow" in text or "automation" in text

        return has_hiring_signal and has_budget_signal and has_remote_signal and has_fit_signal
