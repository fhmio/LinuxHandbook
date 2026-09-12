#!/usr/bin/env python3
"""
scripts/validate_articles.py

Validates article Markdown files against the canonical article contract:
- Valid YAML front matter with required fields
- Exact 9 numbered headings + References in order
- Strict code fence language tags (no ba's, bassh, etc.)
- No non-ASCII Chinese text or unreplaced placeholders
"""

import argparse
import re
import sys
from pathlib import Path
import yaml

MANDATORY_HEADINGS = [
    "## 1. Introduction",
    "## 2. Syntax and Command Model",
    "## 3. Options",
    "## 4. Basic Usage",
    "## 5. Practical Operations",
    "## 6. Advanced Usage",
    "## 7. Exit Status, Environment, and Configuration",
    "## 8. Safety, Security, and Portability",
    "## 9. Best Practices",
    "## References",
]

ALLOWED_FENCE_LANGUAGES = {
    "bash",
    "console",
    "text",
    "ini",
    "systemd",
    "diff",
    "json",
    "yaml",
    "sh",
    "awk",
}

MALFORMED_FENCE_REGEX = re.compile(r"^```(ba's|bassh|sh\s|zsh\s)", re.MULTILINE)
CHINESE_CHAR_REGEX = re.compile(r"[\u4e00-\u9fff]")
PLACEHOLDER_REGEX = re.compile(
    r"\b(TODO|TBD|implement later|fill in details)\b", re.IGNORECASE
)


def validate_article(path: Path) -> list[str]:
    errors = []
    text = path.read_text(encoding="utf-8")

    # 1. Front matter extraction
    if not text.startswith("---"):
        errors.append("Article does not start with YAML front matter ('---').")
        return errors

    parts = text.split("---", 2)
    if len(parts) < 3:
        errors.append("Malformed YAML front matter (closing '---' missing).")
        return errors

    fm_raw = parts[1]
    body = parts[2]

    try:
        fm = yaml.safe_load(fm_raw)
    except Exception as e:
        errors.append(f"Failed to parse YAML front matter: {e}")
        return errors

    if not isinstance(fm, dict):
        errors.append("Front matter is not a YAML mapping.")
        return errors

    # Check required front matter fields
    req_fm = [
        "title",
        "date",
        "categories",
        "tags",
        "draft",
        "slug",
        "upstream_suite",
        "upstream_version",
        "posix_standard",
        "research_date",
    ]
    for field in req_fm:
        if field not in fm:
            errors.append(f"Front matter missing required field: '{field}'")

    # Command from filename
    filename_match = re.match(r"^linux-([a-z0-9_+-]+)-tutorial\.md$", path.name)
    if not filename_match:
        errors.append(
            f"Filename '{path.name}' does not match 'linux-<command>-tutorial.md'"
        )
        cmd_name = ""
    else:
        cmd_name = filename_match.group(1)

    if cmd_name:
        expected_title = f"Linux Command Tutorial: {cmd_name}"
        if fm.get("title") != expected_title:
            errors.append(
                f"Front matter title must be '{expected_title}', got '{fm.get('title')}'"
            )

        tags = fm.get("tags", [])
        if not isinstance(tags, list):
            errors.append("Front matter 'tags' must be a list")
        else:
            if "Linux" not in tags:
                errors.append("Tags missing 'Linux'")
            if "Linux Command Tutorial" not in tags:
                errors.append("Tags missing 'Linux Command Tutorial'")
            if cmd_name not in tags:
                errors.append(f"Tags missing command name '{cmd_name}'")

    # 2. Heading validation
    found_headings = [
        line.strip()
        for line in body.splitlines()
        if line.strip().startswith("## ")
    ]

    for expected, found in zip(MANDATORY_HEADINGS, found_headings):
        if not found.startswith(expected):
            errors.append(
                f"Heading mismatch. Expected starting with '{expected}', got '{found}'"
            )

    if len(found_headings) < len(MANDATORY_HEADINGS):
        missing = MANDATORY_HEADINGS[len(found_headings) :]
        errors.append(f"Missing mandatory headings: {missing}")

    # 3. Code fence validation
    if MALFORMED_FENCE_REGEX.search(body):
        errors.append("Found malformed code fence tag (e.g. ba's, bassh).")

    # Check all fence openers
    fence_lines = [
        line.strip()
        for line in body.splitlines()
        if line.strip().startswith("```")
    ]
    if len(fence_lines) % 2 != 0:
        errors.append(
            f"Unmatched code fences: found {len(fence_lines)} fence markers."
        )

    for i in range(0, len(fence_lines), 2):
        opener = fence_lines[i]
        lang = opener.lstrip("`").strip().split()[0] if opener != "```" else ""
        if lang and lang not in ALLOWED_FENCE_LANGUAGES:
            errors.append(
                f"Disallowed code fence language: '{lang}'. Allowed: {sorted(ALLOWED_FENCE_LANGUAGES)}"
            )

    # 4. Chinese characters check
    if CHINESE_CHAR_REGEX.search(text):
        errors.append("File contains non-ASCII Chinese characters.")

    # 5. Placeholder check
    placeholder_matches = PLACEHOLDER_REGEX.findall(body)
    if placeholder_matches:
        errors.append(
            f"Found unreplaced placeholders: {set(placeholder_matches)}"
        )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate Linux command tutorial articles."
    )
    parser.add_argument("--file", help="Validate a specific article file.")
    parser.add_argument(
        "--suite", help="Validate articles for a specific upstream suite."
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Validate all articles in article/ directory.",
    )

    args = parser.parse_args()

    article_dir = Path("article")
    if not article_dir.exists():
        print("ERROR: 'article' directory does not exist.", file=sys.stderr)
        return 1

    files_to_check = []
    if args.file:
        p = Path(args.file)
        if not p.exists():
            print(f"ERROR: File '{args.file}' not found.", file=sys.stderr)
            return 1
        files_to_check.append(p)
    elif args.all or args.suite:
        files_to_check = sorted(article_dir.glob("linux-*-tutorial.md"))
    else:
        parser.print_help()
        return 0

    if not files_to_check:
        print("No article files found to validate.")
        return 0

    total_errors = 0
    checked_count = 0

    for fpath in files_to_check:
        errs = validate_article(fpath)
        checked_count += 1
        if errs:
            total_errors += len(errs)
            print(f"FAIL: {fpath.name}", file=sys.stderr)
            for err in errs:
                print(f"  - {err}", file=sys.stderr)
        else:
            print(f"PASS: {fpath.name}")

    if total_errors > 0:
        print(
            f"\nValidation failed: {total_errors} errors in {checked_count} articles.",
            file=sys.stderr,
        )
        return 1

    print(
        f"\nAll {checked_count} article(s) validated successfully with 0 errors."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
