PYTHON ?= python
PYTHONPATH ?= src
CODEX_CONTEXT_FILES = \
	README.md \
	TODO.md \
	CHANGELOG.md \
	.codex/README.md \
	.codex/DEFAULT_INSTRUCTIONS.md \
	.codex/GOALS.md \
	.codex/CONSTRAINTS.md \
	.codex/POLICIES.md \
	.codex/DECISIONS.md \
	.codex/QUESTIONS.md \
	.codex/STATUS.md \
	.codex/LESSONS_LEARNED.md \
	.codex/Design.md \
	Docs/architecture.md \
	Docs/adaptive_learning.md \
	Docs/chatgpt_codex_review.md \
	reports/daily_briefing.md

.PHONY: check briefing codex-context

check:
	$(PYTHON) -m compileall src

briefing:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m reddit_radar.briefing

codex-context: briefing
	@mkdir -p reports
	@cat $(CODEX_CONTEXT_FILES) > reports/codex_handoff.md
	@echo "Wrote reports/codex_handoff.md"
