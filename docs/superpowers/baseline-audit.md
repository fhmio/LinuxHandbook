# Repository Baseline Audit Report

**Date:** 2026-09-12  
**Target Repository:** `forrestchang-linux-command-tutorials`

## 1. Initial State Inventory

- `README.md`: 5 lines. Contains title and 2 links:
  - `./article/linux-sftp-tutorial.md` (Exists)
  - `./article/linux-ssh-tutorial.md` (Missing / Broken link)
- `article/linux-sftp-tutorial.md`: 232 lines. Written in 2018.

## 2. Identified Baseline Defects

1. **Date & Language Staleness**:
   - `article/linux-sftp-tutorial.md` has front matter date `2018-12-06T14:56:46+08:00`.
   - Body contains untranslated Chinese text: 「Linux Detailed Command Explanation」.
2. **Markdown Syntax Anomalies**:
   - Code fences in legacy document have malformed language tags or inconsistent escaping.
3. **Outdated & Incomplete OpenSSH Feature Coverage**:
   - Missing modern OpenSSH URI syntax: `sftp://[user@]host[:port][/path]`.
   - Missing high-level transfer options (`-X`, `-J` ProxyJump, `-b` batch mode analysis).
   - Missing recent OpenSSH 10.5 security notes and options.
4. **Broken Link in Index**:
   - `README.md` references `./article/linux-ssh-tutorial.md` which does not yet exist on disk.
5. **Lack of Automated Validation**:
   - No schema validation for catalog entries.
   - No markdown or link consistency linter.

## 3. Immediate Baseline Remediation
- Clean dead link from `README.md`.
- Establish foundation schemas and validation scripts in Phase 1 before rebuilding the SFTP reference tutorial.
