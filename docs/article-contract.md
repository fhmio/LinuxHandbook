# Linux Command Reference Article Contract

This document defines the strict structural, metadata, and quality specification that every tutorial in the `article/` directory must satisfy.

---

## 1. File Naming Contract

- Every tutorial documents exactly **one** binary executable.
- The path must be:
  ```
  article/linux-<command>-tutorial.md
  ```
  Where `<command>` is the lowercase binary executable name (e.g., `linux-sftp-tutorial.md`, `linux-ls-tutorial.md`).
- Multi-subcommand utilities (such as `ip link`, `systemctl start`) belong entirely to the parent executable article (`linux-ip-tutorial.md`, `linux-systemctl-tutorial.md`).

---

## 2. Front Matter Contract (YAML)

Every article must begin with this exact YAML block:

```yaml
---
title: "Linux Command Tutorial: <command>"
date: 2026-09-12T00:00:00+00:00
categories: ['Technology']
tags:
  - 'Linux'
  - '<Upstream Suite Display Name>' # e.g. 'OpenSSH', 'GNU Coreutils', 'procps-ng'
  - '<command>'                    # exact binary name
  - 'Linux Command Tutorial'        # constant series tag
draft: false
slug: "linux-<command>-tutorial"
description: "Authoritative reference tutorial for <command> (<Upstream Suite>), detailing syntax, complete verified options, practical workflows, safety safeguards, and upstream-documented best practices."
upstream_suite: "<upstream-suite-id>"
upstream_version: "<version>"      # e.g. "OpenSSH 10.5", "GNU Coreutils 9.11"
posix_standard: "POSIX.1-2024"     # "POSIX.1-2024" or "None"
research_date: "YYYY-MM-DD"
---
```

---

## 3. Mandatory Heading Structure

The article body must follow these exact 9 top-level numbered headings, concluding with `## References`:

```markdown
An introductory paragraph introducing the Linux Command Tutorial series and the specific utility.

## 1. Introduction
- Functional role, upstream provenance, POSIX/standard status, target researched release version, lifecycle/applicability.

## 2. Syntax and Command Model
- Canonical synopsis, operands, execution/process model, standard streams (stdin, stdout, stderr).

## 3. Options
- Exhaustive option matrix table, default settings, option interactions, conflicts, and version notes.

## 4. Basic Usage
- Minimal valid invocations, read-only and query commands, verified real terminal output.

## 5. Practical Operations
- 3 to 5 task-oriented system administration workflows with scenario, command, and verified output.

## 6. Advanced Usage
- Pipelines, null-delimited processing (-0, -print0, -z), scripting integration, machine-readable formats.

## 7. Exit Status, Environment, and Configuration
- Exit codes table, environment variables table, configuration files hierarchy.

## 8. Safety, Security, and Portability
- Destructive hazards, upstream safeguards (--preserve-root), privilege boundaries, symlinks/TOCTOU, POSIX vs GNU portability.

## 9. Best Practices
- Source-justified operational rules citing specific upstream manual passages or standards. Zero personal conjecture.

## References
- Numbered canonical URLs to primary upstream manuals, POSIX specs, and official advisories.
```

---

## 4. Code Block & Formatting Policy

1. **Strict Language Tags**: Every Markdown fence must use a valid language identifier:
   - `bash`: For executable shell commands.
   - `console`: For terminal sessions displaying prompts and responses.
   - `text`: For pure command output, logs, or plain data.
   - `ini` or `systemd`: For configuration files.
2. **Prohibited Tags**: Tags such as `ba's`, `bassh`, unclosed fences, or blank fences for shell commands are strictly prohibited.
3. **Language Integrity**: The article must be 100% English. No untranslated Chinese characters or legacy series text.

---

## 5. Research & Evidence Hierarchy

1. **Tier 1**: Official upstream manual / man page (e.g. `man.openbsd.org`, `gnu.org/software/coreutils/manual`).
2. **Tier 2**: Upstream release notes, security advisories, and source commit logs.
3. **Tier 3**: IEEE Std 1003.1-2024 (POSIX.1-2024) Base Specifications.
4. **Tier 4**: Linux Kernel Documentation (`kernel.org`).
5. **Tier 5**: Distribution documentation (Debian, ArchWiki) solely for distribution-specific packaging quirks.
6. **Tier 6**: Secondary technical sources permitted only when Tiers 1–5 leave an edge case underspecified.

---

## 6. Definition of Done (20-Point Checklist)

1. English only.
2. Single executable focus.
3. Correct `article/linux-<command>-tutorial.md` filename.
4. Valid YAML front matter with ISO timestamps.
5. Sourced against identified upstream version.
6. Cross-referenced against POSIX.1-2024.
7. Complete syntax and command model documented.
8. Exhaustive option matrix with defaults.
9. Basic read-only operations verified.
10. 3–5 practical workflows documented.
11. Advanced scripting & pipeline features included.
12. Complete exit code reference.
13. Documented environment variables and config files.
14. Destructive behavior and safety flags documented.
15. Privilege and security boundaries documented.
16. Portability and kernel constraints documented.
17. Best practices backed by official upstream citations.
18. Validated Markdown code fences.
19. Canonical references linked.
20. Indexed in README and verified in inventory.
