---
title: "Linux Command Tutorial: find"
date: 2026-09-12T00:00:00+00:00
categories: ['Technology']
tags:
  - 'Linux'
  - 'GNU Findutils'
  - 'find'
  - 'Linux Command Tutorial'
draft: false
slug: "linux-find-tutorial"
description: "Authoritative reference tutorial for find (GNU Findutils), detailing expression predicates, null-delimited output (-print0), execdir safety, and POSIX portability."
upstream_suite: "gnu-findutils"
upstream_version: "GNU Findutils 4.10"
posix_standard: "POSIX.1-2024"
research_date: "2026-09-12"
---

The **Linux Command Tutorial** series provides rigorous, upstream-verified references for essential system commands across Linux distributions and UNIX-like environments. Each article focuses on a single executable, combining exhaustive option documentation, verified real-world examples, security boundaries, and best practices directly derived from official source documentation and POSIX standards.

---

## 1. Introduction

> **Upstream**: GNU Findutils 4.10 | **POSIX**: POSIX.1-2024 (with GNU extensions) | **Safety Tier**: safe-read-only | **Scope**: filesystem-search

`find` searches directory trees recursively, evaluating boolean expressions composed of tests, actions, and global options against each visited file and directory.

- **Upstream Project & Provenance**: Developed and maintained under **GNU Findutils** (`findutils`).
- **Portability & Standards Baseline**: Standardized in **IEEE Std 1003.1-2024 (POSIX.1-2024)**. GNU `find` introduces crucial security and efficiency features, including `-print0`, `-execdir`, `-delete`, `-regextype`, and `-daystart`.
- **Target Research Implementation**: Audited against **GNU Findutils 4.10** (`find(1)`).
- **Applicability & Lifecycle**: The foundational tool for filesystem searching, selective cleanup, and pipeline generation.

---

## 2. Syntax and Command Model

### 2.1 Canonical Synopsis

```bash
find [-H] [-L] [-P] [-D debugopts] [-Olevel] [starting-point...] [expression]
```

### 2.2 Expression Evaluation & Boolean Logic

- `find` evaluates an expression composed of:
  - **Operators**: `-and` (default between adjacent tests), `-or` (`-o`), `not` (`!`).
  - **Tests**: Criteria that return true or false (`-name`, `-type`, `-mtime`, `-size`, `-perm`).
  - **Actions**: Side-effect operations (`-print`, `-print0`, `-delete`, `-exec`, `-execdir`).
- **Short-Circuit Evaluation**: Like C boolean operators, if the left side of an `-and` expression evaluates to false, the right side is never evaluated. Therefore, actions like `-delete` or `-exec` should always appear **after** filtering tests.

---

## 3. Options and Predicates

### 3.1 Common Tests

| Predicate | Description | POSIX Defined |
|:---|:---|:---:|
| `-name pattern` | Base of file name matches shell pattern. | Yes |
| `-iname pattern` | Like `-name`, but the match is case-insensitive. | No |
| `-type c` | File is of type `c`: `f` (regular), `d` (directory), `l` (symlink), `s` (socket). | Yes |
| `-mtime n` | File data was modified `n*24` hours ago (`+n` greater than, `-n` less than). | Yes |
| `-size n[cwbkMG]`| File uses `n` units of space (e.g. `+100M`). | Yes |
| `-perm mode` | File's permission bits are set exactly to `mode` (or matched with `/` or `-`). | Yes |
| `-empty` | File is empty and is either a regular file or a directory. | No |

### 3.2 Primary Actions

| Action | Description | Upstream Note |
|:---|:---|:---|
| `-print` | Print the full file name, followed by a newline. | Default action if no other action given |
| `-print0` | Print the full file name, followed by a null character (`\0`). | Crucial for safe piping to `xargs -0` |
| `-exec cmd {} ;` | Execute `cmd` on each file individually (spawns 1 process per file). | Inefficient for large sets |
| `-exec cmd {} +` | Execute `cmd` on multiple files simultaneously (batches arguments). | High performance |
| `-execdir cmd {} +`| Execute `cmd` from the subdirectory containing the matched file. | Protects against race attacks |
| `-delete` | Delete files; turns on `-depth` automatically. | Direct unlink |

---

## 4. Basic Usage

### 4.1 Quick-Reference Cheatsheet Card

| Operation | Command | Notes |
|:---|:---|:---|
| Find files by name | `find /path -name "*.log"` | Case-sensitive pattern match |
| Find files ignoring case | `find /path -iname "*.conf"` | Case-insensitive pattern match |
| Find regular files only | `find /path -type f` | Excludes directories, symlinks, sockets |
| Find directories only | `find /path -type d` | Recursively finds subdirectories |
| Find files modified in last 7 days | `find /path -type f -mtime -7` | Relative time in 24-hour periods |
| Find files larger than 100MB | `find /path -type f -size +100M` | Searches by exact byte or unit threshold |
| Batch execute safely | `find /path -type f -name "*.tmp" -print0 \| xargs -0 rm -f` | Null-delimited pipeline safe against special characters |

### 4.2 Finding Files by Name

```bash
find /etc -name "*.conf"
```

### 4.3 Finding Directories Only

```bash
find /var/log -type d
```

---

## 5. Practical Operations

### 5.1 Safe File Deletion via `-print0` and `xargs -0`

Purging temporary files safely, even if filenames contain spaces or newlines:

```bash
find /tmp/app_cache -type f -name "*.tmp" -print0 | xargs -0 rm -f
```
- **Technical Analysis**: `-print0` uses the null byte (`\0`) as the delimiter. Because UNIX filenames cannot legally contain `\0`, this guarantees immunity to argument splitting.

### 5.2 Finding Large Files Exceeding 500 MB

```bash
find /var -type f -size +500M -exec ls -lh {} +
```
- **Technical Analysis**: `-size +500M` tests for sizes strictly greater than 500 megabytes; `-exec ... +` batches multiple files into a single `ls` invocation, minimizing process spawning.

### 5.3 Finding Files Modified in the Last 24 Hours

```bash
find /home/admin/project -type f -mtime -1
```

### 5.4 Finding Insecure World-Writable Files

Locating files that any local user can modify:

```bash
find /var/www -type f -perm -0002 -ls
```
- `-perm -0002` checks if the "other" write bit (`w`) is asserted.

---

## 6. Advanced Usage

### 6.1 Avoiding Symlink Traversal Race Conditions via `-execdir`

When running commands on files located in world-writable or shared directories:

```bash
find /tmp/uploads -type f -name "*.sh" -execdir chmod 644 {} +
```
- **Technical Analysis**: `-execdir` changes the working directory to the parent directory of the file before invoking the command, and passes `./filename`. This completely eliminates TOCTOU (Time-Of-Check to Time-Of-Use) race conditions where an attacker substitutes a path component with a symlink while `find` is executing.

### 6.2 Pruning Specific Directory Branches (`-prune`)

Skipping entire directory trees (like `.git` or `node_modules`) to accelerate traversal:

```bash
find . \( -name ".git" -o -name "node_modules" \) -prune -o -type f -name "*.js" -print
```
- When `.git` is encountered, `-prune` tells `find` not to descend into it, drastically reducing disk I/O.

---

## 7. Exit Status, Environment, and Configuration

### 7.1 Exit Status Codes

| Exit Code | Meaning |
|:---:|:---|
| `0` | All files were traversed and all actions succeeded. |
| `>0` | An error occurred (permission denied on directory, `-exec` command failed, invalid syntax). |

---

## 8. Safety, Security, and Portability

### 8.1 The Catastrophic `-delete` Precedence Bug

> [!CAUTION]
> **Catastrophic `-delete` Order Hazard**: `find` processes predicates sequentially from left to right using short-circuit evaluation. Putting `-delete` before filter criteria (e.g., `find /var/tmp -delete -name "*.log"`) evaluates `-delete` on **every file first**, wiping out the entire directory!
> Always place `-delete` as the final action:
> ```bash
> find /var/tmp -type f -name "*.log" -delete
> ```

---

## 9. Best Practices

1. **Always Use `-print0` When Piping into Downstream Commands**:
   - *Guidance*: Pair `find -print0` with `xargs -0` or `while IFS= read -r -d '' file`.
   - *Authoritative Justification*: GNU documentation notes that newline-delimited streams break on filenames containing spaces, tabs, or newlines.
2. **Use `-exec ... +` Instead of `-exec ... \;`**:
   - *Guidance*: Terminate `-exec` with `+` rather than `\;` whenever possible.
   - *Authoritative Justification*: Passes hundreds of files per process invocation, reducing CPU overhead by up to 98%.
3. **Use `-execdir` in Shared and Untrusted Directories**:
   - *Guidance*: Replace `-exec` with `-execdir` on `/tmp` or user-writable uploads.
   - *Authoritative Justification*: Upstream Findutils security advisories warn that standard `-exec` is vulnerable to symlink substitution attacks during path traversal.

---

## References

1. **GNU Findutils find Manual**: [https://www.gnu.org/software/findutils/manual/html_node/find_html/index.html](https://www.gnu.org/software/findutils/manual/html_node/find_html/index.html)
2. **POSIX.1-2024 find Specification**: The Open Group Base Specifications Issue 8. [https://pubs.opengroup.org/onlinepubs/9799919799/utilities/find.html](https://pubs.opengroup.org/onlinepubs/9799919799/utilities/find.html)
