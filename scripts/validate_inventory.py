#!/usr/bin/env python3
"""
scripts/validate_inventory.py

Validates all command entries in inventory/*.json against the upstream schema rules.
"""

import json
import re
import sys
from pathlib import Path

ALLOWED_SUITES = {
    "gnu-coreutils",
    "gnu-findutils",
    "gnu-grep",
    "gnu-sed",
    "gnu-gawk",
    "procps-ng",
    "util-linux",
    "iproute2",
    "openssh",
    "systemd",
    "curl",
    "rsync",
    "gnu-tar",
    "gnu-gzip",
    "xz-utils",
    "apt",
    "yum",
    "dnf",
    "sudo",
    "shadow-utils",
    "psmisc",
    "bash",
}

ALLOWED_DOC_TYPES = {"man-page", "texinfo", "html-manual", "rfc", "kernel-doc"}

ALLOWED_COMPLIANCE = {
    "posix-standard-strict",
    "posix-standard-with-gnu-extensions",
    "linux-specific-upstream-extension",
    "de-facto-standard",
}

ALLOWED_LIFECYCLE = {
    "active",
    "deprecated-upstream",
    "obsolete-upstream",
    "maintenance-only",
}

ALLOWED_ARTICLE_STATUS = {
    "planned",
    "drafting",
    "in-review",
    "validated",
    "published",
}

ALLOWED_SAFETY_TIERS = {
    "safe-read-only",
    "unprivileged-filesystem-write",
    "privileged-system-destructive",
    "privileged-network-state-altering",
}

COMMAND_PATTERN = re.compile(r"^[a-z0-9_+-]+$")
DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def validate_entry(entry: dict, source_file: Path) -> list[str]:
    errors = []
    cmd = entry.get("command", "<unknown>")

    # Required fields check
    required_fields = [
        "command",
        "article_filename",
        "upstream_suite",
        "upstream_package",
        "upstream_homepage",
        "official_documentation",
        "standard_status",
        "current_researched_version",
        "research_date",
        "lifecycle_status",
        "article_status",
        "execution_safety_tier",
    ]
    for rf in required_fields:
        if rf not in entry:
            errors.append(f"[{cmd}] Missing required field: '{rf}'")

    # Command format
    if "command" in entry and not COMMAND_PATTERN.match(entry["command"]):
        errors.append(f"[{cmd}] Invalid command name: '{entry['command']}'")

    # Article filename format
    expected_filename = f"article/linux-{entry.get('command')}-tutorial.md"
    if entry.get("article_filename") != expected_filename:
        errors.append(
            f"[{cmd}] article_filename must be '{expected_filename}', got '{entry.get('article_filename')}'"
        )

    # Upstream suite enum
    if entry.get("upstream_suite") not in ALLOWED_SUITES:
        errors.append(
            f"[{cmd}] Invalid upstream_suite: '{entry.get('upstream_suite')}'"
        )

    # Documentation object
    doc = entry.get("official_documentation")
    if not isinstance(doc, dict):
        errors.append(f"[{cmd}] 'official_documentation' must be an object")
    else:
        if doc.get("doc_type") not in ALLOWED_DOC_TYPES:
            errors.append(f"[{cmd}] Invalid doc_type: '{doc.get('doc_type')}'")
        if not str(doc.get("primary_url", "")).startswith(("http://", "https://")):
            errors.append(f"[{cmd}] 'primary_url' must be valid HTTP/HTTPS URL")

    # Standard status object
    std = entry.get("standard_status")
    if not isinstance(std, dict):
        errors.append(f"[{cmd}] 'standard_status' must be an object")
    else:
        if not isinstance(std.get("is_posix_standardized"), bool):
            errors.append(f"[{cmd}] 'is_posix_standardized' must be boolean")
        if std.get("compliance_level") not in ALLOWED_COMPLIANCE:
            errors.append(
                f"[{cmd}] Invalid compliance_level: '{std.get('compliance_level')}'"
            )

    # Research date format
    if not DATE_PATTERN.match(str(entry.get("research_date", ""))):
        errors.append(
            f"[{cmd}] 'research_date' must be YYYY-MM-DD, got '{entry.get('research_date')}'"
        )

    # Enums
    if entry.get("lifecycle_status") not in ALLOWED_LIFECYCLE:
        errors.append(
            f"[{cmd}] Invalid lifecycle_status: '{entry.get('lifecycle_status')}'"
        )
    if entry.get("article_status") not in ALLOWED_ARTICLE_STATUS:
        errors.append(
            f"[{cmd}] Invalid article_status: '{entry.get('article_status')}'"
        )
    if entry.get("execution_safety_tier") not in ALLOWED_SAFETY_TIERS:
        errors.append(
            f"[{cmd}] Invalid execution_safety_tier: '{entry.get('execution_safety_tier')}'"
        )

    return errors


def main() -> int:
    inventory_dir = Path("inventory")
    if not inventory_dir.exists():
        print("ERROR: 'inventory' directory does not exist.", file=sys.stderr)
        return 1

    json_files = list(inventory_dir.glob("*.json"))
    if not json_files:
        print("No inventory JSON files found to validate.")
        return 0

    total_commands = 0
    seen_commands = {}
    all_errors = []

    for jf in json_files:
        try:
            with open(jf, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            all_errors.append(f"[{jf.name}] JSON parse error: {e}")
            continue

        if not isinstance(data, list):
            all_errors.append(
                f"[{jf.name}] Root element must be an array of command entries."
            )
            continue

        for entry in data:
            total_commands += 1
            cmd = entry.get("command")
            if cmd in seen_commands:
                all_errors.append(
                    f"Duplicate command '{cmd}' in {jf.name} (previously defined in {seen_commands[cmd]})"
                )
            else:
                seen_commands[cmd] = jf.name

            errs = validate_entry(entry, jf)
            all_errors.extend(errs)

    if all_errors:
        print(
            f"FAILED: Found {len(all_errors)} validation errors across {len(json_files)} files:",
            file=sys.stderr,
        )
        for err in all_errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    print(
        f"SUCCESS: Validated {total_commands} commands across {len(json_files)} inventory files with 0 errors."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
