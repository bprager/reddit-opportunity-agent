from contextlib import redirect_stdout
from io import StringIO
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from reddit_radar import runner
from reddit_radar.adapters.rss import RssFeedAdapter


class RunnerCliTests(unittest.TestCase):
    def test_main_prints_dry_run_summary(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output = StringIO()
            argv = [
                "runner",
                "--dry-run-fixtures",
                "tests/fixtures/opportunity_examples.json",
                "--database",
                str(Path(temp_dir) / "radar.db"),
                "--limit",
                "1",
            ]

            with patch.object(sys, "argv", argv), redirect_stdout(output):
                runner.main()

        self.assertIn("Dry run complete: 1 collected, 1 assessed, 1 open", output.getvalue())

    def test_main_reports_live_collection_errors(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            argv = [
                "runner",
                "--live-subreddit",
                "forhire",
                "--database",
                str(Path(temp_dir) / "radar.db"),
            ]

            with patch.object(sys, "argv", argv):
                with self.assertRaisesRegex(SystemExit, "Live collection stopped"):
                    runner.main()

    def test_main_reports_bad_rss_source_errors(self) -> None:
        argv = ["runner", "--rss-source", "missing-url"]

        with patch.object(sys, "argv", argv):
            with self.assertRaisesRegex(SystemExit, "Source collection stopped"):
                runner.main()

    def test_main_prints_rss_collection_summary(self) -> None:
        feed = Path("tests/fixtures/rss_opportunity.xml").read_text(encoding="utf-8")

        class FakeAdapter:
            def collect(self, source: object) -> list[object]:
                return RssFeedAdapter(lambda _url: feed).collect(source)

        with tempfile.TemporaryDirectory() as temp_dir:
            output = StringIO()
            argv = [
                "runner",
                "--rss-source",
                "jobs=https://example.com/feed.xml",
                "--database",
                str(Path(temp_dir) / "radar.db"),
            ]

            with (
                patch.object(sys, "argv", argv),
                patch.object(runner, "RssFeedAdapter", FakeAdapter),
                redirect_stdout(output),
            ):
                runner.main()

        self.assertIn("Source collection complete: 1 sources", output.getvalue())


if __name__ == "__main__":
    unittest.main()
