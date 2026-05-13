PYTHON ?= $(shell if [ -x .venv/bin/python ]; then printf .venv/bin/python; else printf python; fi)
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
	Docs/source_acquisition.md \
	Docs/adaptive_learning.md \
	Docs/chatgpt_codex_review.md \
	reports/daily_briefing.md \
	reports/weekly_learning_report.md

.PHONY: check test lint lint-python lint-markdown coverage briefing learning-report dry-run codex-context

check: lint coverage

lint: lint-python lint-markdown

lint-python:
	$(PYTHON) -m ruff check .

lint-markdown:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) scripts/check_markdown.py

coverage:
	$(PYTHON) -m compileall src
	PYTHONPATH=$(PYTHONPATH):tests $(PYTHON) -m coverage run -m unittest discover -s tests -v
	$(PYTHON) -m coverage report --fail-under=96

test:
	PYTHONPATH=$(PYTHONPATH):tests $(PYTHON) -m unittest discover -s tests -v

briefing:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m reddit_radar.briefing

learning-report:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -c "from reddit_radar.learning import generate_weekly_learning_report; from reddit_radar.storage import OpportunityStore; store = OpportunityStore('reddit_radar.db'); store.init_schema(); print(generate_weekly_learning_report(store))"

dry-run:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m reddit_radar.runner --dry-run-fixtures tests/fixtures/opportunity_examples.json

codex-context: briefing learning-report
	@mkdir -p reports
	@cat $(CODEX_CONTEXT_FILES) > reports/codex_handoff.md
	@echo "Wrote reports/codex_handoff.md"
