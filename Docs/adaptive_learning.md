# Adaptive Learning Design

## Goal

The Reddit Opportunity Radar should learn quickly from outcomes, misses, and changing market signals.

The system should become better at:

- Finding relevant opportunities.
- Discovering new sources.
- Rejecting low-value or risky posts.
- Improving scoring.
- Improving prompts.
- Producing better reply drafts.
- Helping Bernd decide where to spend limited time.

## Learning Inputs

### 1. Human Decisions

Every item should eventually have a decision:

- ignored
- saved
- replied
- applied
- follow-up scheduled
- converted
- rejected
- false positive
- false negative

### 2. Missed Opportunities

Bernd should be able to paste a missed opportunity and mark why it was missed:

- source not monitored
- search phrase missing
- classifier failed
- score too low
- risk detector too aggressive
- opportunity category not yet recognized
- locality signal missed
- budget signal missed

### 3. Source Candidates

The system should keep a backlog of possible new sources:

- subreddits
- Reddit search queries
- flairs
- RSS feeds
- job boards
- Discords
- newsletters
- local directories
- event calendars
- LinkedIn searches

Each candidate source should have:

- reason for adding
- expected signal type
- expected noise level
- test status
- owner decision
- observed value after trial

### 4. Scoring Drift

The system should compare predicted value with actual outcomes.

Examples:

- High score but ignored repeatedly means the scoring is too generous.
- Low score but later converted means the classifier or scoring missed a key signal.
- Many scam flags in one subreddit may justify deprioritizing that source.
- One subreddit producing high-conversion leads should get more attention.

## Learning Events

Store every meaningful adjustment as a learning event:

```json
{
  "type": "scoring_weight_change",
  "reason": "No-budget posts from r/forhire rarely convert.",
  "before": "budget weight 25",
  "after": "budget weight 35",
  "expected_effect": "Fewer vague remote opportunities in top 20"
}
```

## Regression Examples

Good and bad examples should be saved.

The classifier should be tested against these examples so old mistakes do not return.

Example regression classes:

- strong local lead
- strong remote opportunity
- false positive
- scam risk
- low-budget distraction
- missed AI automation opportunity
- missed LA locality signal

## Weekly Learning Report

The system should generate a weekly report with:

- best sources
- worst sources
- highest-scoring misses
- false positives
- false negatives
- scoring changes to consider
- source changes to consider
- prompt changes to consider
- dashboard workflow issues

## Principle

Do not let the agent silently rewrite its own rules.

The agent may recommend changes. Bernd approves them.
