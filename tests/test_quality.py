import tempfile
import unittest
from pathlib import Path

from reddit_radar.quality import MarkdownIssue, check_markdown_files, discover_markdown_files


class MarkdownQualityTests(unittest.TestCase):
    def test_discover_markdown_files_skips_hidden_and_cache_directories(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            visible = root / "README.md"
            hidden = root / ".venv" / "ignored.md"
            cache = root / "__pycache__" / "ignored.md"
            nested = root / "Docs" / "adr" / "0001-test.md"
            for path in (visible, hidden, cache, nested):
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("# Title\n", encoding="utf-8")

            discovered = discover_markdown_files(root)

        self.assertEqual([nested, visible], discovered)

    def test_check_markdown_files_reports_common_formatting_issues(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bad = root / "bad.md"
            bad.write_text("# Title\n\nLine with tab\t\nTrailing space \nNo newline", encoding="utf-8")

            issues = check_markdown_files([bad])

        self.assertEqual(
            [
                MarkdownIssue(bad, 3, "tabs are not allowed"),
                MarkdownIssue(bad, 3, "trailing whitespace"),
                MarkdownIssue(bad, 4, "trailing whitespace"),
                MarkdownIssue(bad, 5, "missing final newline"),
            ],
            issues,
        )

    def test_check_markdown_files_accepts_clean_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            good = root / "good.md"
            good.write_text("# Title\n\nClean body.\n", encoding="utf-8")

            issues = check_markdown_files([good])

        self.assertEqual([], issues)

    def test_issue_format_uses_relative_path_when_possible(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "Docs" / "example.md"
            path.parent.mkdir(parents=True)
            issue = MarkdownIssue(path, 4, "trailing whitespace")

            self.assertEqual("Docs/example.md:4: trailing whitespace", issue.format(root))


if __name__ == "__main__":
    unittest.main()
