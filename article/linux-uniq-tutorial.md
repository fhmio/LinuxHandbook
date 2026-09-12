---
title: "Linux Command Tutorial: uniq"
date: 2026-09-12T00:00:00+00:00
categories: ['Technology']
tags:
  - 'Linux'
  - 'GNU Coreutils'
  - 'uniq'
  - 'Linux Command Tutorial'
draft: false
slug: "linux-uniq-tutorial"
description: "Authoritative reference tutorial for uniq (GNU Coreutils), detailing duplicate line filtering, occurrence counting (-c), field skipping, and POSIX portability."
upstream_suite: "gnu-coreutils"
upstream_version: "GNU Coreutils 9.11"
posix_standard: "POSIX.1-2024"
research_date: "2026-09-12"
---

The **Linux Command Tutorial** series provides rigorous, upstream-verified references for essential system commands across Linux distributions and UNIX-like environments. Each article focuses on a single executable, combining exhaustive option documentation, verified real-world examples, security boundaries, and best practices directly derived from official source documentation and POSIX standards.

---

## 1. Introduction

`uniq` filters out or reports repeated adjacent lines in an input stream. Because `uniq` only compares contiguous lines, input streams are typically pre-sorted with `sort` before processing.

- **Upstream Project & Provenance**: Distributed in **GNU Coreutils** (`coreutils`).
- **Portability & Standards Baseline**: Standardized in **IEEE Std 1003.1-2024 (POSIX.1-2024)**. GNU `uniq` adds all-repeated controls (`-D`), grouping flags (`--group`), and zero-terminated records (`-z`).
- **Target Research Implementation**: Audited against **GNU Coreutils 9.11** (`uniq(1)`).
- **Applicability & Lifecycle**: The standard command for deduplication, counting frequencies, and finding unique vs duplicate entries.

---

## 2. Syntax and Command Model

### 2.1 Canonical Synopsis

```bash
uniq [OPTION]... [INPUT [OUTPUT]]
```

### 2.2 Execution Model & Adjacency Requirement

- `uniq` reads lines sequentially, comparing each line strictly to its **immediate predecessor**.
- Non-adjacent duplicates are **not** filtered:
  ```text
  Input:  A, B, A
  Output: A, B, A  (A is not removed because it is not adjacent)
  ```
- To deduplicate entire files, input must be pre-sorted: `sort file | uniq`.

---

## 3. Options

### 3.1 Primary Flags

| Short Flag | Long Flag | Description | POSIX Defined |
|:---|:---|:---|:---:|
| `-c` | `--count` | Prefix lines by the number of occurrences. | Yes |
| `-d` | `--repeated` | Only print duplicate lines (one per group). | Yes |
| `-D` | N/A | Print all duplicate lines. | No |
| `-u` | `--unique` | Only print unique lines (lines that appear exactly once). | Yes |
| `-i` | `--ignore-case` | Ignore differences in case when comparing. | No |
| `-f N` | `--skip-fields=N` | Avoid comparing the first N fields on each line. | Yes |
| `-s N` | `--skip-chars=N` | Avoid comparing the first N characters on each line. | Yes |
| `-w N` | `--check-chars=N` | Compare no more than N characters in lines. | No |
| `-z` | `--zero-terminated` | Line delimiter is NUL (`\0`), not newline. | No |

---

## 4. Basic Usage

### 4.1 Basic Deduplication

```bash
cat <<'EOF' | uniq
alpha
beta
beta
gamma
EOF
```
```text
alpha
beta
gamma
```

### 4.2 Counting Frequencies with `-c`

```bash
cat <<'EOF' | uniq -c
alpha
beta
beta
gamma
EOF
```
```text
      1 alpha
      2 beta
      1 gamma
```

---

## 5. Practical Operations

### 5.1 Top 5 Most Frequent Client IP Addresses

Analyzing an Nginx access log to identify top hitting clients:

```bash
awk '{print $1}' access.log | sort | uniq -c | sort -nr | head -n 5
```
```text
   4512 192.168.1.105
   2198 10.0.0.14
    892 172.16.0.45
    421 192.168.1.200
    115 10.0.0.88
```
- **Technical Analysis**: Extracts IP, sorts alphabetically so identical IPs are adjacent, uses `uniq -c` to count occurrences, and sorts numerically descending (`sort -nr`).

### 5.2 Isolating Only Duplicate Records

Displaying only usernames that appear more than once in an export:

```bash
sort usernames.txt | uniq -d
```

### 5.3 Isolating Only Unique Records (Excluding All Duplicates)

Finding values that appear strictly once (omitting any entry that had duplicates):

```bash
sort ids.txt | uniq -u
```

---

## 6. Advanced Usage

### 6.1 Skipping Leading Fields via `-f`

Comparing lines while ignoring a leading timestamp column:

```bash
cat <<'EOF' | uniq -f 1
[10:00:01] Service started
[10:00:02] Service started
[10:00:03] Connection established
EOF
```
```text
[10:00:01] Service started
[10:00:03] Connection established
```
- Skips field 1 (`[timestamp]`) and evaluates adjacency based on the remainder of the line.

---

## 7. Exit Status, Environment, and Configuration

### 7.1 Exit Status Codes

| Exit Code | Meaning |
|:---:|:---|
| `0` | Success: deduplication completed cleanly. |
| `>0` | An error occurred (input file unreadable, output target write error). |

---

## 8. Safety, Security, and Portability

### 8.1 Sorting Prerequisite

Failing to sort input before piping into `uniq` is a common administrative bug:
```bash
# INCORRECT: leaves duplicates scattered across the file
uniq raw_log.txt

# CORRECT: guarantees full deduplication
sort raw_log.txt | uniq
```
Alternatively, `sort -u` can perform sorting and deduplication in a single process.

---

## 9. Best Practices

1. **Always Sort Before Calling `uniq`**:
   - *Guidance*: Formulate pipelines as `sort | uniq`.
   - *Authoritative Justification*: GNU documentation explicitly states that `uniq` operates strictly on adjacent lines.
2. **Use `sort -u` When Counts Are Not Needed**:
   - *Guidance*: If `-c`, `-d`, or `-u` is not required, use `sort -u` instead of `sort | uniq`.
   - *Authoritative Justification*: Eliminates an extra process and pipe overhead.
3. **Use `-i` for Case-Insensitive Email or Domain Deduplication**:
   - *Guidance*: Pass `uniq -i` when processing case-insensitive network identifiers.
   - *Authoritative Justification*: Prevents duplicates due to mixed capitalization.

---

## References

1. **GNU Coreutils uniq Manual**: [https://www.gnu.org/software/coreutils/manual/html_node/uniq-invocation.html](https://www.gnu.org/software/coreutils/manual/html_node/uniq-invocation.html)
2. **POSIX.1-2024 uniq Specification**: The Open Group Base Specifications Issue 8. [https://pubs.opengroup.org/onlinepubs/9799919799/utilities/uniq.html](https://pubs.opengroup.org/onlinepubs/9799919799/utilities/uniq.html)
