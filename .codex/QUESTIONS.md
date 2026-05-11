# Questions

These questions are ready for the next architecture interview.

## Architecture Decisions

1. Should the MVP stay a local-first tool, or should it be designed for a hosted deployment from the start?
   - Recommended default: local-first until the daily queue proves useful.

2. Should the first dashboard remain Streamlit, or should the project move directly to FastAPI plus a separate web UI?
   - Recommended default: Streamlit first for speed, FastAPI later for tools and integrations.

3. Should classification start with explicit rules and saved examples, or should it use an LLM immediately?
   - Recommended default: rules first, then LLM classification behind a reviewable interface.

4. Which source should be implemented first: local Los Angeles lead discovery or remote opportunity discovery?
   - Recommended default: remote opportunities first, because budget and work intent are easier to score.

5. What is the minimum expected value per pursuit hour for a remote opportunity?
   - Recommended default: set an initial threshold, then tune from outcomes.

6. Should the system store Reddit author metadata beyond username and observed item history?
   - Recommended default: keep it minimal until a clear scoring need exists.

7. Which model provider should be the first default for draft generation: OpenAI, Ollama, or both?
   - Recommended default: support both, but make one configured provider active at a time.

8. Should OpenClaw tools be designed now or after the dashboard proves useful?
   - Recommended default: keep interfaces clean now, expose tools later.

## Product Decisions

1. What kinds of opportunities are worth interrupting Bernd immediately instead of waiting for the daily briefing?
2. Which opportunity categories should be hard rejects even when the score is high?
3. How should the dashboard represent uncertainty in budget, scope, or close probability?
4. What decision labels should be mandatory before an item leaves the queue?
5. What does a successful weekly learning report need to answer?

