# Linux Command Tutorial Series Expansion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Transform the repository from a single 2018 SFTP tutorial into an authoritative, upstream-driven English reference library covering standardized and core Linux commands derived directly from official suites (GNU Coreutils, Findutils, procps-ng, util-linux, iproute2, OpenSSH, systemd, curl, rsync, tar, gzip, xz-utils) with 100% mechanical verification.

**Architecture:** A flat `article/linux-<command>-tutorial.md` repository contract governed by an upstream inventory schema (`inventory/`), a strict 9-section article metadata contract, an authoritative multi-tier research policy, and automated validation scripts (`scripts/validate_articles.py` and `scripts/validate_inventory.py`) ensuring zero broken links, no malformed markdown fences, and full upstream traceability.

**Tech Stack:** Markdown (GitHub Flavored Markdown), YAML Front Matter, Python 3 (standard library `json`, `pathlib`, `re`, `urllib` for automated validation scripts), Git.

**Spec:** [docs/superpowers/specs/2026-09-12-linux-command-tutorials-architecture.md](file:///c:/Users/mazen/OneDrive/Documents/linux-command-tutorials/docs/superpowers/specs/2026-09-12-linux-command-tutorials-architecture.md)

## Global Constraints

- **Language:** English only. No untranslated legacy text or Chinese characters.
- **Granularity:** Strictly one binary executable = one article. Subcommands (`ip link`, `systemctl start`) belong to the parent executable article (`linux-ip-tutorial.md`, `linux-systemctl-tutorial.md`).
- **File Naming:** Strictly `article/linux-<command>-tutorial.md`.
- **Fences & Syntax:** Strictly valid code fences (`bash`, `console`, `text`). Zero malformed tags (no `ba's`, no `bassh`).
- **Research Hierarchy:** Primary upstream manual > Upstream release notes/security advisories > POSIX.1-2024 > Linux kernel docs > Distribution docs.
- **No Speculation:** Zero unsupported blog advice or invented rules. Every item in Section 9 (Best Practices) must cite an official upstream or POSIX rationale.
- **Index Integrity:** 1:1 bidirectional mapping between `README.md`, `inventory/`, and `article/`. No orphan articles and no broken links.

---

## File Structure

```
linux-command-tutorials/
├── README.md                                          # Master catalog indexed by upstream suite
├── LICENSE                                            # Project license
├── schemas/
│   └── upstream-inventory.schema.json                # JSON Schema for command catalog entries
├── inventory/                                         # Upstream command catalogs (JSON)
│   ├── coreutils.json
│   ├── findutils.json
│   ├── procps-ng.json
│   ├── util-linux.json
│   ├── iproute2.json
│   ├── openssh.json
│   ├── systemd.json
│   ├── transfer.json
│   └── compression.json
├── scripts/
│   ├── validate_inventory.py                          # Validates inventory JSON against schema
│   ├── validate_articles.py                           # Validates article structure, front matter, fences
│   └── generate_readme.py                             # Deterministically builds README.md from inventory
├── docs/
│   └── superpowers/
│       ├── specs/
│       │   └── 2026-09-12-linux-command-tutorials-architecture.md
│       └── plans/
│           └── 2026-09-12-linux-command-tutorials-expansion.md
└── article/
    ├── linux-sftp-tutorial.md                         # Canonical reference article (OpenSSH 10.5)
    ├── linux-ssh-tutorial.md
    ├── linux-ls-tutorial.md
    ├── linux-find-tutorial.md
    └── ...
```

---

## Execution Phases & Tasks

### Task 1: Repository Baseline Audit & Cleanup

**Files:**
- Modify: `README.md`
- Inspect: `article/linux-sftp-tutorial.md`

**Interfaces:**
- Consumes: Existing repository files.
- Produces: Clean baseline audit log and removal of broken initial links.

- [ ] **Step 1: Inspect and document baseline defects**
  Verify the existing tree and record known baseline issues in `docs/superpowers/baseline-audit.md`:
  - `article/linux-sftp-tutorial.md` dated 2018-12-06 with Chinese series text.
  - Malformed code fences (`ba's`, `bassh`) in SFTP article.
  - Incomplete OpenSSH feature coverage (missing `-X`, URI syntax, OpenSSH 10.5 options).
  - Broken link to non-existent `linux-ssh-tutorial.md` in `README.md`.

- [ ] **Step 2: Remove dead link in README.md**
  Update `README.md` to temporarily reference only the existing SFTP tutorial with clean formatting until the automated generator runs in Task 17.

- [ ] **Step 3: Verify audit completion**
  Run: `python -c "assert open('README.md').read().count('linux-ssh-tutorial.md') == 0"`
  Expected: Clean exit (0).

---

### Task 2: Freeze Article Contract & Inventory Schema

**Files:**
- Create: `schemas/upstream-inventory.schema.json`
- Create: `docs/article-contract.md`

**Interfaces:**
- Consumes: Architectural specification approved in design gate.
- Produces: Reusable JSON Schema and developer guide for all future article writers and subagents.

- [ ] **Step 1: Write schemas/upstream-inventory.schema.json**
  Implement the JSON Schema (Draft 2020-12) specifying `command`, `article_filename`, `upstream_suite`, `official_documentation`, `standard_status`, `current_researched_version`, `lifecycle_status`, and `execution_safety_tier`.

- [ ] **Step 2: Write docs/article-contract.md**
  Document the exact front matter YAML requirements, the mandatory 9 top-level headings + References, the code fence language rules, and the 20-point Definition of Done checklist.

- [ ] **Step 3: Verify schema validity**
  Run: `python -c "import json; schema = json.load(open('schemas/upstream-inventory.schema.json')); assert schema['title'] == 'LinuxCommandInventoryEntry'"`
  Expected: PASS.

---

### Task 3: Build Automated Validation Tooling

**Files:**
- Create: `scripts/validate_inventory.py`
- Create: `scripts/validate_articles.py`
- Create: `scripts/generate_readme.py`

**Interfaces:**
- Consumes: `schemas/upstream-inventory.schema.json`, `inventory/*.json`, and `article/*.md`.
- Produces: CLI verification gates used in every subsequent batch task.

- [ ] **Step 1: Write scripts/validate_inventory.py**
  Implement validation of all JSON records in `inventory/` against `schemas/upstream-inventory.schema.json` using Python's standard library. Check that every command defines a unique executable and valid file path.

- [ ] **Step 2: Write scripts/validate_articles.py**
  Implement rigorous linting of all `article/*.md` files:
  - Front matter parsed as YAML, asserting `title`, `date`, `tags`, `categories`, `upstream_suite`, `upstream_version`, `posix_standard`.
  - Exactly 9 required `##` headings + `## References` in correct numeric order.
  - Zero disallowed fence tags (match on ```` ```(ba's|bassh|sh |zsh ) ````).
  - No non-ASCII Chinese series text remaining.

- [ ] **Step 3: Write scripts/generate_readme.py**
  Implement a deterministic README builder that reads all `inventory/*.json` entries, groups them by upstream suite, and produces a structured Markdown table of tutorials with status badges.

- [ ] **Step 4: Run validation suite smoke test**
  Run: `python scripts/validate_articles.py --help`
  Expected: Returns exit code 0 with usage instructions.

---

### Task 4: Authoritative Upstream Inventory Extraction

**Files:**
- Create: `inventory/coreutils.json`
- Create: `inventory/findutils.json`
- Create: `inventory/procps-ng.json`
- Create: `inventory/util-linux.json`
- Create: `inventory/iproute2.json`
- Create: `inventory/openssh.json`
- Create: `inventory/systemd.json`
- Create: `inventory/transfer.json`
- Create: `inventory/compression.json`

**Interfaces:**
- Consumes: Official upstream project manifests and POSIX.1-2024 utilities list.
- Produces: Validated, complete catalog of commands to be written across the project.

- [ ] **Step 1: Compile OpenSSH & Transfer inventories**
  Add entries for `sftp`, `ssh`, `scp`, `ssh-keygen`, `ssh-agent`, `ssh-add`, `ssh-keyscan`, `curl`, and `rsync` with current release versions (e.g., OpenSSH 10.5, rsync 3.5.0).

- [ ] **Step 2: Compile GNU Coreutils & Findutils inventories**
  Add all official binaries from Coreutils 9.11 (`ls`, `cp`, `mv`, `rm`, `cat`, `chmod`, `chown`, `dd`, `df`, `du`, etc.) and Findutils (`find`, `xargs`, `locate`).

- [ ] **Step 3: Compile System, Network & Storage inventories**
  Add binaries from `procps-ng` (`ps`, `top`, `free`, `vmstat`, `pgrep`, `pkill`), `util-linux` (`mount`, `umount`, `findmnt`, `lsblk`, `fdisk`, `blkid`), `iproute2` (`ip`, `ss`, `tc`, `bridge`), and `systemd` (`systemctl`, `journalctl`).

- [ ] **Step 4: Run inventory validation script**
  Run: `python scripts/validate_inventory.py`
  Expected: PASS with 0 validation errors across all inventory files.

---

### Task 5: Rewrite SFTP as the Canonical Reference Article

**Files:**
- Modify: `article/linux-sftp-tutorial.md`

**Interfaces:**
- Consumes: OpenSSH 10.5 official manual (`sftp(1)`), RFC 4251, `inventory/openssh.json`.
- Produces: The benchmark English tutorial against which all subsequent articles are graded.

- [ ] **Step 1: Research current OpenSSH 10.5 SFTP capabilities**
  Audit `sftp(1)` manual for:
  - Destination format: `[user@]host[:path]` and URI format `sftp://[user@]host[:port][/path]`.
  - Batch mode (`-b`), transfer limits (`-l`), transfer parameters (`-X`).
  - Interactive commands (`reget`, `reput`, `df`, `lumask`, `progress`).
  - Security notes: Resumed transfer risks on mismatched source, host key verification.

- [ ] **Step 2: Draft canonical Front Matter and Section 1 & 2**
  Write English front matter, Section 1 (Introduction, OpenSSH 10.5 provenance, non-POSIX de-facto standard), and Section 2 (Syntax, URI synopsis, interactive process model).

- [ ] **Step 3: Draft Section 3 (Options) & Section 4 (Basic Usage)**
  Exhaustive option matrix covering `-4`, `-6`, `-A`, `-a`, `-B`, `-b`, `-C`, `-c`, `-D`, `-F`, `-i`, `-J`, `-l`, `-P`, `-p`, `-q`, `-R`, `-r`, `-S`, `-s`, `-v`, `-X`. Verified terminal outputs for read-only connections and directory queries.

- [ ] **Step 4: Draft Section 5 (Practical Operations) & Section 6 (Advanced Usage)**
  Workflows:
  - Automated batch script transfer via `-b`.
  - ProxyJump connection via `-J`.
  - Transfer rate limiting (`-l`) and custom buffer tuning (`-B`, `-R`).
  - Resuming interrupted downloads with `reget`.

- [ ] **Step 5: Draft Section 7, 8, 9 & References**
  - Section 7: Exit statuses (`0`, `1`, `255`), environment variables (`SSH_AUTH_SOCK`), config file search paths (`~/.ssh/config`).
  - Section 8: Unverified resumed file corruption warning, host key verification, permissions requirements.
  - Section 9: 5 source-backed best practices citing OpenSSH upstream docs.
  - References: OpenBSD `sftp(1)` man page, OpenSSH 10.5 release notes, IETF draft secsh-filexfer.

---

### Task 6: Validate the Reference Article

**Files:**
- Test: `article/linux-sftp-tutorial.md`

**Interfaces:**
- Consumes: `article/linux-sftp-tutorial.md`, `scripts/validate_articles.py`.
- Produces: Verified reference article passing all 20 DoD points.

- [ ] **Step 1: Execute automated article validator**
  Run: `python scripts/validate_articles.py --file article/linux-sftp-tutorial.md`
  Expected: PASS: 0 lint errors, 0 malformed fences, valid front matter, all 9 sections present.

- [ ] **Step 2: Manual technical review against DoD**
  Verify that all 20 checklist criteria from the design contract are satisfied. Ensure no legacy Chinese text remains and all examples represent valid OpenSSH 10.5 syntax.

---

### Task 7: Batch Implementation — OpenSSH Utility Suite

**Files:**
- Create: `article/linux-ssh-tutorial.md`
- Create: `article/linux-scp-tutorial.md`
- Create: `article/linux-ssh-keygen-tutorial.md`
- Create: `article/linux-ssh-agent-tutorial.md`
- Create: `article/linux-ssh-add-tutorial.md`
- Create: `article/linux-ssh-keyscan-tutorial.md`

**Interfaces:**
- Consumes: OpenSSH 10.5 manuals (`ssh(1)`, `scp(1)`, `ssh-keygen(1)`, `ssh-agent(1)`, `ssh-add(1)`, `ssh-keyscan(1)`).
- Produces: 6 production-grade articles adhering to canonical contract.

- [ ] **Step 1: Author OpenSSH batch articles**
  Write each article following the 9-section template, incorporating modern algorithms (Ed25519), certificate-based auth, agent forwarding security implications, and SFTP-subsystem scp behavior (`-s`).

- [ ] **Step 2: Validate OpenSSH batch**
  Run: `python scripts/validate_articles.py --suite openssh`
  Expected: PASS for all 6 articles.

---

### Task 8: Batch Implementation — Core File Operations (GNU Coreutils)

**Files:**
- Create: `article/linux-ls-tutorial.md`
- Create: `article/linux-cp-tutorial.md`
- Create: `article/linux-mv-tutorial.md`
- Create: `article/linux-rm-tutorial.md`
- Create: `article/linux-mkdir-tutorial.md`
- Create: `article/linux-rmdir-tutorial.md`
- Create: `article/linux-touch-tutorial.md`
- Create: `article/linux-ln-tutorial.md`

**Interfaces:**
- Consumes: GNU Coreutils 9.11 manual, POSIX.1-2024 Shell and Utilities.
- Produces: 8 verified file operation tutorials with `--preserve-root`, atomic renames, and symlink dereference rules documented.

- [ ] **Step 1: Author Coreutils file operation articles**
  Implement full 9 sections per article. Document POSIX standard flags vs GNU extensions (`--reflink`, `--backup`, `--preserve-root`).

- [ ] **Step 2: Validate file operations batch**
  Run: `python scripts/validate_articles.py --suite gnu-coreutils-file`
  Expected: PASS for all 8 articles.

---

### Task 9: Batch Implementation — Text Processing & Filtering (Coreutils, Grep, Sed, Awk)

**Files:**
- Create: `article/linux-cat-tutorial.md`
- Create: `article/linux-head-tutorial.md`
- Create: `article/linux-tail-tutorial.md`
- Create: `article/linux-grep-tutorial.md`
- Create: `article/linux-sed-tutorial.md`
- Create: `article/linux-awk-tutorial.md`
- Create: `article/linux-sort-tutorial.md`
- Create: `article/linux-uniq-tutorial.md`
- Create: `article/linux-cut-tutorial.md`
- Create: `article/linux-tr-tutorial.md`

**Interfaces:**
- Consumes: GNU Grep 3.12, GNU Sed 4.9, GAWK 5.3, Coreutils 9.11, POSIX.1-2024.
- Produces: 10 verified text processing tutorials featuring null-delimited processing (`-z`), regex dialects, and safe script piping.

- [ ] **Step 1: Author text processing articles**
  Write articles adhering to standard structure with detailed regex and delimiter analysis.

- [ ] **Step 2: Validate text processing batch**
  Run: `python scripts/validate_articles.py --suite text-processing`
  Expected: PASS for all 10 articles.

---

### Task 10: Batch Implementation — Search & Directory Traversal (GNU Findutils)

**Files:**
- Create: `article/linux-find-tutorial.md`
- Create: `article/linux-xargs-tutorial.md`
- Create: `article/linux-locate-tutorial.md`

**Interfaces:**
- Consumes: GNU Findutils 4.10, POSIX.1-2024 `find`/`xargs`.
- Produces: 3 traversal tutorials documenting `-print0` / `-0` pipeline safety, `-exec ... +` performance, and updatedb mechanics.

- [ ] **Step 1: Author Findutils articles**
  Document expression evaluation order, `-execdir` vs `-exec` security implications against symlink race attacks, and POSIX conformance.

- [ ] **Step 2: Validate Findutils batch**
  Run: `python scripts/validate_articles.py --suite gnu-findutils`
  Expected: PASS for all 3 articles.

---

### Task 11: Batch Implementation — Process & System Inspection (procps-ng)

**Files:**
- Create: `article/linux-ps-tutorial.md`
- Create: `article/linux-top-tutorial.md`
- Create: `article/linux-free-tutorial.md`
- Create: `article/linux-vmstat-tutorial.md`
- Create: `article/linux-pgrep-tutorial.md`
- Create: `article/linux-pkill-tutorial.md`
- Create: `article/linux-w-tutorial.md`
- Create: `article/linux-uptime-tutorial.md`

**Interfaces:**
- Consumes: procps-ng 4.0.4+ manuals, Linux `/proc` filesystem documentation.
- Produces: 8 process inspection articles detailing syntax standards (UNIX vs BSD vs GNU style options for `ps`), memory calculation metrics in `free`, and signal dispatching safety in `pkill`.

- [ ] **Step 1: Author procps-ng articles**
  Write articles with clear explanation of memory buffers/cache metrics, process state codes, and multi-syntax flags.

- [ ] **Step 2: Validate procps-ng batch**
  Run: `python scripts/validate_articles.py --suite procps-ng`
  Expected: PASS for all 8 articles.

---

### Task 12: Batch Implementation — Storage & Filesystem Administration (util-linux)

**Files:**
- Create: `article/linux-mount-tutorial.md`
- Create: `article/linux-umount-tutorial.md`
- Create: `article/linux-findmnt-tutorial.md`
- Create: `article/linux-lsblk-tutorial.md`
- Create: `article/linux-fdisk-tutorial.md`
- Create: `article/linux-blkid-tutorial.md`

**Interfaces:**
- Consumes: util-linux 2.40 manuals, Linux VFS mount documentation.
- Produces: 6 storage administration articles documenting modern `findmnt --verify` workflows, non-blocking unmounts, UUID targeting, and block device topology inspection.

- [ ] **Step 1: Author util-linux articles**
  Detail root privilege boundaries, partition table types (GPT vs MBR), fstab verification, and script-friendly column selection (`--output`).

- [ ] **Step 2: Validate util-linux batch**
  Run: `python scripts/validate_articles.py --suite util-linux`
  Expected: PASS for all 6 articles.

---

### Task 13: Batch Implementation — Linux Networking (iproute2)

**Files:**
- Create: `article/linux-ip-tutorial.md`
- Create: `article/linux-ss-tutorial.md`
- Create: `article/linux-tc-tutorial.md`
- Create: `article/linux-bridge-tutorial.md`

**Interfaces:**
- Consumes: iproute2 6.13 manuals, Linux netlink kernel documentation.
- Produces: 4 networking tutorials detailing replacement of legacy net-tools (`ifconfig`, `netstat`, `route`), subobject syntax (`ip addr`, `ip route`, `ip link`, `ip neigh`), JSON output (`-j`), and socket state filters.

- [ ] **Step 1: Author iproute2 articles**
  Cover kernel netlink communication, persistent network configuration boundaries, socket memory buffer interpretation in `ss`, and traffic control queuing disciplines in `tc`.

- [ ] **Step 2: Validate iproute2 batch**
  Run: `python scripts/validate_articles.py --suite iproute2`
  Expected: PASS for all 4 articles.

---

### Task 14: Batch Implementation — Services & Logging (systemd)

**Files:**
- Create: `article/linux-systemctl-tutorial.md`
- Create: `article/linux-journalctl-tutorial.md`

**Interfaces:**
- Consumes: systemd 255/256 manuals (`systemctl(1)`, `journalctl(1)`).
- Produces: 2 system runtime tutorials covering unit dependency trees, cgroup management, journal cursors, boot query flags (`-b`), and structured journal filtering.

- [ ] **Step 1: Author systemd articles**
  Write articles covering user vs system service scopes, daemon reloads, socket activation, structured export (`-o json`), and log retention verification.

- [ ] **Step 2: Validate systemd batch**
  Run: `python scripts/validate_articles.py --suite systemd`
  Expected: PASS for both articles.

---

### Task 15: Batch Implementation — Data Transfer & Compression (curl, rsync, tar, gzip, xz)

**Files:**
- Create: `article/linux-curl-tutorial.md`
- Create: `article/linux-rsync-tutorial.md`
- Create: `article/linux-tar-tutorial.md`
- Create: `article/linux-gzip-tutorial.md`
- Create: `article/linux-xz-tutorial.md`

**Interfaces:**
- Consumes: curl 8.12, rsync 3.5.0, GNU tar 1.35, GNU gzip 1.13, XZ Utils 5.6 manuals.
- Produces: 5 transfer and archive tutorials covering resilient network sync (`--partial`, `--checksum`), atomic archive extraction, and multi-threaded compression algorithms.

- [ ] **Step 1: Author transfer & compression articles**
  Document curl security options, rsync trailing-slash directory semantics (`dir/` vs `dir`), tar directory traversal protections, and xz multi-threaded flags (`-T`).

- [ ] **Step 2: Validate transfer & compression batch**
  Run: `python scripts/validate_articles.py --suite transfer-compression`
  Expected: PASS for all 5 articles.

---

### Task 16: Cross-Article Technical & Consistency Audit

**Files:**
- Inspect: All `article/*.md` files

**Interfaces:**
- Consumes: Entire `article/` collection.
- Produces: Verification report confirming zero schema divergence or inconsistent terminology across the series.

- [ ] **Step 1: Run comprehensive lint across all articles**
  Run: `python scripts/validate_articles.py --all`
  Expected: PASS with 0 errors across 100% of articles.

- [ ] **Step 2: Automated check for unescaped code fences & placeholders**
  Run: `python -c "import pathlib, re; bad = [p.name for p in pathlib.Path('article').glob('*.md') if re.search(r'```(ba\'s|bassh)|(TBD|TODO|implement later)', p.read_text(encoding='utf-8'))]; assert len(bad) == 0, f'Defects in: {bad}'"`
  Expected: PASS (no output).

---

### Task 17: Authoritative README & Catalog Index Generation

**Files:**
- Modify: `README.md`

**Interfaces:**
- Consumes: `inventory/*.json`, `scripts/generate_readme.py`.
- Produces: Formatted master index linking to every generated tutorial, grouped by authoritative upstream suite with version and standard tags.

- [ ] **Step 1: Execute generate_readme.py**
  Run: `python scripts/generate_readme.py --output README.md`
  Expected: Overwrites `README.md` with complete catalog matrix.

- [ ] **Step 2: Validate link integrity in README.md**
  Run: `python -c "import re, pathlib; links = re.findall(r'\[(.*?)\]\(\./article/(linux-[a-z0-9_+-]+-tutorial\.md)\)', open('README.md').read()); missing = [f for _, f in links if not (pathlib.Path('article') / f).exists()]; assert len(missing) == 0, f'Broken links: {missing}'"`
  Expected: PASS with 0 broken links.

---

### Task 18: Upstream Completeness & Parity Audit

**Files:**
- Test: All `inventory/*.json` against `article/` and `README.md`

**Interfaces:**
- Consumes: `inventory/`, `article/`, `README.md`.
- Produces: Certification of zero orphan articles and zero unfulfilled inventory entries.

- [ ] **Step 1: Execute bidirectional completeness audit**
  Run: `python -c "import json, pathlib; inv_cmds = {item['command'] for f in pathlib.Path('inventory').glob('*.json') for item in json.load(open(f))}; art_cmds = {p.name.replace('linux-', '').replace('-tutorial.md', '') for p in pathlib.Path('article').glob('*.md')}; diff = inv_cmds ^ art_cmds; assert len(diff) == 0, f'Inventory/Article mismatch: {diff}'"`
  Expected: PASS with exact 1:1 match.

---

### Task 19: Final Documentation Verification & Release Sign-Off

**Files:**
- Inspect: Full repository tree

**Interfaces:**
- Consumes: Entire repository.
- Produces: Final verified release state.

- [ ] **Step 1: Verify Git status and cleanliness**
  Ensure all files are formatted, UTF-8 encoded with standard UNIX line endings, and pass repository sanity checks.

- [ ] **Step 2: Generate Walkthrough Document**
  Produce `docs/superpowers/specs/walkthrough.md` documenting the completed migration, verified catalog counts, and audit logs.

---

## Execution Handoff

Plan complete and saved to `docs/superpowers/plans/2026-09-12-linux-command-tutorials-expansion.md`. Two execution options:

1. **Subagent-Driven (recommended)** — I dispatch a fresh subagent per task, review between tasks, with fast and isolated iteration.
2. **Inline Execution** — Execute tasks sequentially in this session using `superpowers:executing-plans`, with checkpoints for review.

Which approach would you like to take?
