# Questions

The main Phase 1 architecture questions are resolved. Remaining questions are product workflow details for later phases.

## Resolved Architecture Decisions

1. The MVP stays local-first until the daily queue proves useful.
2. The first dashboard remains Streamlit.
3. Classification starts with explicit rules and saved examples before LLM classification.
4. Remote opportunity discovery comes before local Los Angeles lead discovery.
5. The initial expected value threshold for remote opportunities is about 200 USD per pursuit hour.
6. Reddit author metadata stays minimal until a clear scoring need exists.
7. OpenAI and Ollama may both be supported later, but only one provider should be active at a time.
8. OpenClaw tools come after the daily queue and dashboard prove useful.
9. Treat Reddit as one source family behind source-agnostic acquisition adapters.
10. Normalize all acquired items into canonical source items before classification and scoring.
11. Use generic RSS and non-Reddit public sources while Reddit API approval is pending.
12. Keep the official Reddit API adapter ready and switch to it through source configuration when
    credentials arrive.

## Open Product Decisions

1. What kinds of opportunities are worth interrupting Bernd immediately instead of waiting for the daily briefing?
2. Which opportunity categories should be hard rejects even when the score is high?
3. How should the dashboard represent uncertainty in budget, scope, or close probability?
4. What decision labels should be mandatory before an item leaves the queue?
5. What does a successful weekly learning report need to answer?

## Open Phase 6 Operational Decisions

1. Decide whether Reddit RSS should be enabled immediately as a low-volume interim source or held
   until after a policy review.
2. Decide whether Reddit JSON endpoints should stay disabled unless Reddit explicitly approves them.
3. Reddit API credentials still need to be configured for live collection:
   `REDDIT_CLIENT_ID` and `REDDIT_CLIENT_SECRET`.
4. The first approved live read-only smoke test is `r/forhire` and `r/hireaprogrammer`, 5 newest
   posts each.
5. Should the first live run store all collected items or only items that score above a minimum threshold?
6. Should the next non-Reddit adapter be Hacker News, Lobsters, or both in one slice?
