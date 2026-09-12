# Article Visual Enhancement & Easy-Copy Commands Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Upgrade all 53 Linux command reference articles in `article/` to feature Section 1 metadata badges, Section 4 quick-reference cheatsheet tables, friction-free 1-click copy `bash` command blocks separated from sample outputs, and GitHub Flavored Markdown callouts (`> [!WARNING]`, `> [!IMPORTANT]`, `> [!TIP]`, `> [!NOTE]`).

**Architecture:** Systematic manual batch-by-batch enhancement organized across 9 upstream suites, preserving the strict 9-heading contract and YAML front matter while transforming terminal workflows into clean, copyable blocks with separate output representations. Every batch is validated against `scripts/validate_articles.py` before individual file commits.

**Tech Stack:** Markdown (GitHub Flavored Markdown), Python 3, Git, IEEE Std 1003.1-2024 (POSIX.1-2024).

**Spec:** [`docs/superpowers/specs/2026-09-12-article-design-enhancement.md`](file:///c:/Users/mazen/OneDrive/Documents/linux-command-tutorials/docs/superpowers/specs/2026-09-12-article-design-enhancement.md)

## Global Constraints

- Every article must retain its exact 9 top-level numbered headings and front matter schema without deviation.
- Code blocks containing commands intended for execution must use clean `bash` fences without `$ ` or `# ` prompts.
- Terminal outputs and interactive displays must use separate `text` or `console` fences, preceded by an explanatory sentence or subhead.
- Callouts in Sections 8 & 9 must use standard GitHub alert syntax (`> [!WARNING]`, `> [!IMPORTANT]`, `> [!TIP]`, `> [!NOTE]`).
- Every single modified file must be committed individually with descriptive conventional commit messages.

---

### Task 1: OpenSSH Suite Enhancement (7 Articles)

**Files:**
- Modify: `article/linux-sftp-tutorial.md`
- Modify: `article/linux-ssh-tutorial.md`
- Modify: `article/linux-scp-tutorial.md`
- Modify: `article/linux-ssh-keygen-tutorial.md`
- Modify: `article/linux-ssh-agent-tutorial.md`
- Modify: `article/linux-ssh-add-tutorial.md`
- Modify: `article/linux-ssh-keyscan-tutorial.md`

**Requirements:**
- Add Section 1 Metadata Badge bar to each file.
- Add Section 4.1 Quick-Reference Cheatsheet table to each file.
- Split all combined `$ command` prompts in Sections 4, 5, 6 into isolated ```` ```bash ```` command blocks and separate ```` ```text ```` / ```` ```console ```` output blocks.
- Convert security warnings and best practices in Sections 8 and 9 into GitHub callout alerts (`> [!WARNING]`, `> [!IMPORTANT]`, `> [!TIP]`).

- [ ] **Step 1: Enhance `article/linux-sftp-tutorial.md`**
- [ ] **Step 2: Enhance `article/linux-ssh-tutorial.md`**
- [ ] **Step 3: Enhance `article/linux-scp-tutorial.md`**
- [ ] **Step 4: Enhance `article/linux-ssh-keygen-tutorial.md`**
- [ ] **Step 5: Enhance `article/linux-ssh-agent-tutorial.md`**
- [ ] **Step 6: Enhance `article/linux-ssh-add-tutorial.md`**
- [ ] **Step 7: Enhance `article/linux-ssh-keyscan-tutorial.md`**
- [ ] **Step 8: Run suite validation**
  Run: `python scripts/validate_articles.py --suite openssh`
  Expected: PASS on all 7 articles with 0 errors.
- [ ] **Step 9: Commit each file individually**

---

### Task 2: GNU Coreutils File Operations Enhancement (8 Articles)

**Files:**
- Modify: `article/linux-ls-tutorial.md`
- Modify: `article/linux-cp-tutorial.md`
- Modify: `article/linux-mv-tutorial.md`
- Modify: `article/linux-rm-tutorial.md`
- Modify: `article/linux-mkdir-tutorial.md`
- Modify: `article/linux-rmdir-tutorial.md`
- Modify: `article/linux-touch-tutorial.md`
- Modify: `article/linux-ln-tutorial.md`

- [ ] **Step 1: Enhance `article/linux-ls-tutorial.md`**
- [ ] **Step 2: Enhance `article/linux-cp-tutorial.md`**
- [ ] **Step 3: Enhance `article/linux-mv-tutorial.md`**
- [ ] **Step 4: Enhance `article/linux-rm-tutorial.md`**
- [ ] **Step 5: Enhance `article/linux-mkdir-tutorial.md`**
- [ ] **Step 6: Enhance `article/linux-rmdir-tutorial.md`**
- [ ] **Step 7: Enhance `article/linux-touch-tutorial.md`**
- [ ] **Step 8: Enhance `article/linux-ln-tutorial.md`**
- [ ] **Step 9: Run suite validation**
  Run: `python scripts/validate_articles.py --suite gnu-coreutils`
  Expected: PASS on all 8 articles with 0 errors.
- [ ] **Step 10: Commit each file individually**

---

### Task 3: Text Processing & Filtering Enhancement (10 Articles)

**Files:**
- Modify: `article/linux-cat-tutorial.md`
- Modify: `article/linux-head-tutorial.md`
- Modify: `article/linux-tail-tutorial.md`
- Modify: `article/linux-grep-tutorial.md`
- Modify: `article/linux-sed-tutorial.md`
- Modify: `article/linux-awk-tutorial.md`
- Modify: `article/linux-sort-tutorial.md`
- Modify: `article/linux-uniq-tutorial.md`
- Modify: `article/linux-cut-tutorial.md`
- Modify: `article/linux-tr-tutorial.md`

- [ ] **Step 1: Enhance `article/linux-cat-tutorial.md`**
- [ ] **Step 2: Enhance `article/linux-head-tutorial.md`**
- [ ] **Step 3: Enhance `article/linux-tail-tutorial.md`**
- [ ] **Step 4: Enhance `article/linux-grep-tutorial.md`**
- [ ] **Step 5: Enhance `article/linux-sed-tutorial.md`**
- [ ] **Step 6: Enhance `article/linux-awk-tutorial.md`**
- [ ] **Step 7: Enhance `article/linux-sort-tutorial.md`**
- [ ] **Step 8: Enhance `article/linux-uniq-tutorial.md`**
- [ ] **Step 9: Enhance `article/linux-cut-tutorial.md`**
- [ ] **Step 10: Enhance `article/linux-tr-tutorial.md`**
- [ ] **Step 11: Run validation on text processing suites**
  Run: `python scripts/validate_articles.py --suite gnu-grep && python scripts/validate_articles.py --suite gnu-sed && python scripts/validate_articles.py --suite gnu-gawk`
  Expected: PASS with 0 errors.
- [ ] **Step 12: Commit each file individually**

---

### Task 4: GNU Findutils Enhancement (3 Articles)

**Files:**
- Modify: `article/linux-find-tutorial.md`
- Modify: `article/linux-xargs-tutorial.md`
- Modify: `article/linux-locate-tutorial.md`

- [ ] **Step 1: Enhance `article/linux-find-tutorial.md`**
- [ ] **Step 2: Enhance `article/linux-xargs-tutorial.md`**
- [ ] **Step 3: Enhance `article/linux-locate-tutorial.md`**
- [ ] **Step 4: Run suite validation**
  Run: `python scripts/validate_articles.py --suite gnu-findutils`
  Expected: PASS on all 3 articles with 0 errors.
- [ ] **Step 5: Commit each file individually**

---

### Task 5: procps-ng Process & System Inspection Enhancement (8 Articles)

**Files:**
- Modify: `article/linux-ps-tutorial.md`
- Modify: `article/linux-top-tutorial.md`
- Modify: `article/linux-free-tutorial.md`
- Modify: `article/linux-vmstat-tutorial.md`
- Modify: `article/linux-pgrep-tutorial.md`
- Modify: `article/linux-pkill-tutorial.md`
- Modify: `article/linux-w-tutorial.md`
- Modify: `article/linux-uptime-tutorial.md`

- [ ] **Step 1: Enhance `article/linux-ps-tutorial.md`**
- [ ] **Step 2: Enhance `article/linux-top-tutorial.md`**
- [ ] **Step 3: Enhance `article/linux-free-tutorial.md`**
- [ ] **Step 4: Enhance `article/linux-vmstat-tutorial.md`**
- [ ] **Step 5: Enhance `article/linux-pgrep-tutorial.md`**
- [ ] **Step 6: Enhance `article/linux-pkill-tutorial.md`**
- [ ] **Step 7: Enhance `article/linux-w-tutorial.md`**
- [ ] **Step 8: Enhance `article/linux-uptime-tutorial.md`**
- [ ] **Step 9: Run suite validation**
  Run: `python scripts/validate_articles.py --suite procps-ng`
  Expected: PASS on all 8 articles with 0 errors.
- [ ] **Step 10: Commit each file individually**

---

### Task 6: util-linux Storage & Administration Enhancement (6 Articles)

**Files:**
- Modify: `article/linux-mount-tutorial.md`
- Modify: `article/linux-umount-tutorial.md`
- Modify: `article/linux-findmnt-tutorial.md`
- Modify: `article/linux-lsblk-tutorial.md`
- Modify: `article/linux-fdisk-tutorial.md`
- Modify: `article/linux-blkid-tutorial.md`

- [ ] **Step 1: Enhance `article/linux-mount-tutorial.md`**
- [ ] **Step 2: Enhance `article/linux-umount-tutorial.md`**
- [ ] **Step 3: Enhance `article/linux-findmnt-tutorial.md`**
- [ ] **Step 4: Enhance `article/linux-lsblk-tutorial.md`**
- [ ] **Step 5: Enhance `article/linux-fdisk-tutorial.md`**
- [ ] **Step 6: Enhance `article/linux-blkid-tutorial.md`**
- [ ] **Step 7: Run suite validation**
  Run: `python scripts/validate_articles.py --suite util-linux`
  Expected: PASS on all 6 articles with 0 errors.
- [ ] **Step 8: Commit each file individually**

---

### Task 7: iproute2 Linux Networking Enhancement (4 Articles)

**Files:**
- Modify: `article/linux-ip-tutorial.md`
- Modify: `article/linux-ss-tutorial.md`
- Modify: `article/linux-tc-tutorial.md`
- Modify: `article/linux-bridge-tutorial.md`

- [ ] **Step 1: Enhance `article/linux-ip-tutorial.md`**
- [ ] **Step 2: Enhance `article/linux-ss-tutorial.md`**
- [ ] **Step 3: Enhance `article/linux-tc-tutorial.md`**
- [ ] **Step 4: Enhance `article/linux-bridge-tutorial.md`**
- [ ] **Step 5: Run suite validation**
  Run: `python scripts/validate_articles.py --suite iproute2`
  Expected: PASS on all 4 articles with 0 errors.
- [ ] **Step 6: Commit each file individually**

---

### Task 8: systemd Services & Logging Enhancement (2 Articles)

**Files:**
- Modify: `article/linux-systemctl-tutorial.md`
- Modify: `article/linux-journalctl-tutorial.md`

- [ ] **Step 1: Enhance `article/linux-systemctl-tutorial.md`**
- [ ] **Step 2: Enhance `article/linux-journalctl-tutorial.md`**
- [ ] **Step 3: Run suite validation**
  Run: `python scripts/validate_articles.py --suite systemd`
  Expected: PASS on both articles with 0 errors.
- [ ] **Step 4: Commit each file individually**

---

### Task 9: Transfer & Compression Enhancement (5 Articles)

**Files:**
- Modify: `article/linux-curl-tutorial.md`
- Modify: `article/linux-rsync-tutorial.md`
- Modify: `article/linux-tar-tutorial.md`
- Modify: `article/linux-gzip-tutorial.md`
- Modify: `article/linux-xz-tutorial.md`

- [ ] **Step 1: Enhance `article/linux-curl-tutorial.md`**
- [ ] **Step 2: Enhance `article/linux-rsync-tutorial.md`**
- [ ] **Step 3: Enhance `article/linux-tar-tutorial.md`**
- [ ] **Step 4: Enhance `article/linux-gzip-tutorial.md`**
- [ ] **Step 5: Enhance `article/linux-xz-tutorial.md`**
- [ ] **Step 6: Run suite validation**
  Run: `python scripts/validate_articles.py --suite curl && python scripts/validate_articles.py --suite rsync && python scripts/validate_articles.py --suite gnu-tar && python scripts/validate_articles.py --suite gnu-gzip && python scripts/validate_articles.py --suite xz-utils`
  Expected: PASS on all 5 articles with 0 errors.
- [ ] **Step 7: Commit each file individually**

---

### Task 10: Full Library Audit & Verification

- [ ] **Step 1: Run comprehensive article validation**
  Run: `python scripts/validate_articles.py --all`
  Expected: All 53 articles PASS with 0 errors.
- [ ] **Step 2: Run inventory validation**
  Run: `python scripts/validate_inventory.py`
  Expected: All 10 inventory files PASS with 0 errors.
- [ ] **Step 3: Re-verify README links**
  Run: link verification script asserting 0 broken links.
- [ ] **Step 4: Update walkthrough artifact and conclude branch**
