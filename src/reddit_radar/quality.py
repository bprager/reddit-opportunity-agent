from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

SKIPPED_DIRS = {
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "__pycache__",
    "htmlcov",
}


@dataclass(frozen=True, order=True)
class MarkdownIssue:
    path: Path
    line: int
    message: str

    def format(self, root: Path | None = None) -> str:
        display_path = self.path
        if root is not None:
            try:
                display_path = self.path.relative_to(root)
            except ValueError:
                display_path = self.path
        return f"{display_path}:{self.line}: {self.message}"


def discover_markdown_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*.md"):
        if any(part in SKIPPED_DIRS for part in path.relative_to(root).parts):
            continue
        files.append(path)
    return sorted(files)


def check_markdown_files(paths: Iterable[Path]) -> list[MarkdownIssue]:
    issues: list[MarkdownIssue] = []
    for path in sorted(paths):
        data = path.read_bytes()
        if data and not data.endswith(b"\n"):
            line_number = data.count(b"\n") + 1
            issues.append(MarkdownIssue(path, line_number, "missing final newline"))

        text = data.decode("utf-8")
        for line_number, line in enumerate(text.splitlines(), start=1):
            if "\t" in line:
                issues.append(MarkdownIssue(path, line_number, "tabs are not allowed"))
            if line.rstrip(" \t") != line:
                issues.append(MarkdownIssue(path, line_number, "trailing whitespace"))

    return sorted(issues)
