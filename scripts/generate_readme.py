#!/usr/bin/env python3
"""
scripts/generate_readme.py

Deterministically generates README.md based on inventory/*.json files
and current article availability in article/*.md.
"""

import argparse
import json
import sys
from pathlib import Path

SUITE_DISPLAY_NAMES = {
    "openssh": "OpenSSH Utilities",
    "gnu-coreutils": "GNU Coreutils",
    "gnu-findutils": "GNU Findutils",
    "gnu-grep": "GNU Grep",
    "gnu-sed": "GNU Sed",
    "gnu-gawk": "GNU GAWK",
    "procps-ng": "procps-ng (Process & System Inspection)",
    "util-linux": "util-linux (Storage & Core System Administration)",
    "iproute2": "iproute2 (Linux Networking Suite)",
    "systemd": "systemd (Services & System Journal)",
    "curl": "curl (Network Transfer)",
    "rsync": "rsync (Remote Sync)",
    "gnu-tar": "GNU tar (Archiving)",
    "gnu-gzip": "GNU gzip (Compression)",
    "xz-utils": "XZ Utils (Compression)",
}


def build_readme(output_path: Path) -> None:
    inventory_dir = Path("inventory")
    article_dir = Path("article")

    if not inventory_dir.exists():
        print("ERROR: 'inventory' directory does not exist.", file=sys.stderr)
        sys.exit(1)

    all_entries = []
    for jf in sorted(inventory_dir.glob("*.json")):
        try:
            with open(jf, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    all_entries.extend(data)
        except Exception as e:
            print(f"ERROR reading {jf.name}: {e}", file=sys.stderr)
            sys.exit(1)

    # Group by upstream suite
    grouped = {}
    for entry in all_entries:
        suite = entry.get("upstream_suite", "other")
        grouped.setdefault(suite, []).append(entry)

    # Count statistics
    total_commands = len(all_entries)
    available_articles = 0

    lines = []
    lines.append("# Linux Command Reference Series\n")
    lines.append(
        "An authoritative, upstream-driven, and research-verifiable Linux command reference library.\n"
    )
    lines.append("## Overview\n")
    lines.append(
        "Every article in this series adheres to a strict architectural standard: exactly one executable per article, exhaustive option tables, verified real-world operations, exit status references, security boundaries, and source-backed best practices derived directly from official upstream manuals and IEEE Std 1003.1-2024 (POSIX.1-2024).\n"
    )
    lines.append("## Command Catalog\n")

    for suite_key, display_name in SUITE_DISPLAY_NAMES.items():
        entries = grouped.get(suite_key, [])
        if not entries:
            continue

        lines.append(f"### {display_name}\n")
        lines.append(
            "| Command | Article | Upstream Version | POSIX.1-2024 | Status |"
        )
        lines.append("|:---|:---|:---|:---:|:---:|")

        for item in sorted(entries, key=lambda x: x["command"]):
            cmd = item["command"]
            article_rel = f"article/linux-{cmd}-tutorial.md"
            article_path = Path(article_rel)
            version = item.get("current_researched_version", "N/A")
            is_posix = (
                "Yes"
                if item.get("standard_status", {}).get("is_posix_standardized")
                else "No"
            )

            if article_path.exists():
                available_articles += 1
                link = f"[{cmd}](./{article_rel})"
                status = "Available"
            else:
                link = f"`{cmd}`"
                status = "Planned"

            lines.append(
                f"| `{cmd}` | {link} | {version} | {is_posix} | {status} |"
            )

        lines.append("")

    lines.append("## Project Standards\n")
    lines.append(
        "- [Article Specification Contract](./docs/article-contract.md)\n"
    )
    lines.append(
        "- [Upstream Inventory Schema](./schemas/upstream-inventory.schema.json)\n"
    )
    lines.append(
        f"\n**Catalog Summary:** {available_articles}/{total_commands} articles available.\n"
    )

    output_path.write_text("\n".join(lines), encoding="utf-8")
    print(
        f"SUCCESS: Generated {output_path} with {total_commands} catalog entries ({available_articles} available)."
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate README.md from upstream inventory."
    )
    parser.add_argument(
        "--output", default="README.md", help="Output path for README file."
    )
    args = parser.parse_args()
    build_readme(Path(args.output))
    return 0


if __name__ == "__main__":
    sys.exit(main())
