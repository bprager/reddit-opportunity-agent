#!/usr/bin/env python
from __future__ import annotations

from pathlib import Path

from reddit_radar.quality import check_markdown_files, discover_markdown_files


def main() -> int:
    root = Path.cwd()
    issues = check_markdown_files(discover_markdown_files(root))
    if issues:
        for issue in issues:
            print(issue.format(root))
        return 1

    print("Markdown lint passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
