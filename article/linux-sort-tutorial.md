---
title: "Linux Command Tutorial: sort"
date: 2026-09-12T00:00:00+00:00
categories: ['Technology']
tags:
  - 'Linux'
  - 'GNU Coreutils'
  - 'sort'
  - 'Linux Command Tutorial'
draft: false
slug: "linux-sort-tutorial"
description: "Authoritative reference tutorial for sort (GNU Coreutils), detailing collation orders, numeric/human sorting (-n, -h), key specifications (-k), and POSIX portability."
upstream_suite: "gnu-coreutils"
upstream_version: "GNU Coreutils 9.11"
posix_standard: "POSIX.1-2024"
research_date: "2026-09-12"
---

The **Linux Command Tutorial** series provides rigorous, upstream-verified references for essential system commands across Linux distributions and UNIX-like environments. Each article focuses on a single executable, combining exhaustive option documentation, verified real-world examples, security boundaries, and best practices directly derived from official source documentation and POSIX standards.

---

## 1. Introduction

`sort` sorts, merges, or checks the ordering of lines in text files. It implements external merge sort algorithms capable of sorting datasets that exceed the host machine's physical RAM by utilizing temporary disk storage buffers.

- **Upstream Project & Provenance**: Distributed in **GNU Coreutils** (`coreutils`).
- **Portability & Standards Baseline**: Standardized in **IEEE Std 1003.1-2024 (POSIX.1-2024)**. GNU `sort` introduces human-numeric sorting (`-h`), version sorting (`-V`), multi-threading (`--parallel`), and zero-terminated records (`-z`).
- **Target Research Implementation**: Audited against **GNU Coreutils 9.11** (`sort(1)`).
- **Applicability & Lifecycle**: The standard utility for ordering lists, preparing inputs for `uniq` or `comm`, and sorting massive log datasets.

---

## 2. Syntax and Command Model

### 2.1 Canonical Synopsis

```bash
sort [OPTION]... [FILE]...
sort [OPTION]... --files0-from=F
```

### 2.2 Execution Model & Key Definitions

- By default, `sort` compares entire lines according to the collation sequence defined by `LC_COLLATE`.
- **Key Specifications (`-k`)**: Restricts sorting to specific fields or character ranges within fields using `POS1[,POS2]` notation.
- **External Merge Sort**: If the dataset exceeds available memory, `sort` creates temporary intermediate files in `/tmp` (or specified via `-T`) and merges them in passes.

---

## 3. Options

### 3.1 Ordering and Sorting Types

| Short Flag | Long Flag | Description | POSIX Defined |
|:---|:---|:---|:---:|
| `-b` | `--ignore-leading-blanks` | Ignore leading blanks when determining start/end of keys. | Yes |
| `-d` | `--dictionary-order` | Consider only blanks and alphanumeric characters. | Yes |
| `-f` | `--ignore-case` | Fold lower case characters into upper case. | Yes |
| `-g` | `--general-numeric-sort` | Compare according to general numerical value (supports scientific notation). | No |
| `-h` | `--human-numeric-sort` | Compare human readable numbers (e.g., 2K, 1G). | No |
| `-n` | `--numeric-sort` | Compare according to string numerical value. | Yes |
| `-r` | `--reverse` | Reverse the result of comparisons. | Yes |
| `-V` | `--version-sort` | Natural sort of (version) numbers within text. | No |
| `-u` | `--unique` | With `-c`, check for strict ordering; without `-c`, output only the first of an equal run. | Yes |

### 3.2 Key and Buffer Controls

| Short Flag | Long Flag | Description | Default |
|:---|:---|:---|:---|
| `-k KEYDEF` | `--key=KEYDEF` | Define field position and comparison options for a key. | Entire line |
| `-t CHAR` | `--field-separator=CHAR` | Use CHAR instead of whitespace as field separator. | Whitespace |
| `-o FILE` | `--output=FILE` | Write result to FILE instead of standard output. | `stdout` |
| `-T DIR` | `--temporary-directory=DIR` | Use DIR for temporary files, not `$TMPDIR` or `/tmp`. | `/tmp` |
| N/A | `--parallel=N` | Change the number of concurrent sorting threads. | Available cores |
| `-z` | `--zero-terminated` | Line delimiter is NUL (`\0`), not newline. | Newline |

---

## 4. Basic Usage

### 4.1 Alphabetical Sorting

```bash
sort names.txt
```

### 4.2 Numeric Sorting in Reverse

```bash
sort -n -r scores.txt
```

---

## 5. Practical Operations

### 5.1 Sorting Delimited Tables by Specific Columns

Sorting `/etc/passwd` numerically by User ID (Field 3), using `:` as the separator:

```bash
sort -t: -k3,3n /etc/passwd | head -n 4
```
```text
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
```
- **Technical Analysis**: `-k3,3n` defines a key starting at field 3 and ending at field 3, sorted with numeric (`n`) comparison. Omitting the ending field (`-k3`) would sort from field 3 through the end of the line.

### 5.2 Sorting Disk Usage in Human-Readable Units

Sorting output from `du -h` by disk consumption:

```bash
du -h --max-depth=1 /var | sort -h -r | head -n 5
```
```console
12G     /var
8.4G    /var/lib
2.1G    /var/log
1.2G    /var/cache
140M    /var/backups
```
- **Technical Analysis**: `-h` understands that `8.4G` is larger than `140M`.

### 5.3 Safely Overwriting the Input File in Place

In standard shell syntax, `sort file > file` truncates the input file to 0 bytes before reading it. Using `-o` guarantees safe in-place sorting:

```bash
sort -o accounts.txt accounts.txt
```
- GNU `sort` opens the output file only after all input streams have been fully read.

---

## 6. Advanced Usage

### 6.1 Multi-Key Hierarchical Sorting

Sorting a dataset first by department (alphabetical) and then by salary (numeric descending):

```bash
sort -t, -k1,1 -k2,2nr employees.csv
```
- Field 1 is sorted forward alphabetically; within identical departments, Field 2 is sorted in reverse numerical order.

---

## 7. Exit Status, Environment, and Configuration

### 7.1 Exit Status Codes

| Exit Code | Meaning |
|:---:|:---|
| `0` | Success: lines sorted or `-c` check succeeded. |
| `1` | Disorder found when checking with `-c` or `-C`. |
| `2` | An error occurred (file unreadable, invalid key definition). |

### 7.2 Collation Order and `LC_ALL`

In UTF-8 locales, `sort` defaults to case-insensitive dictionary order, where `"a"` and `"A"` group together. To force deterministic, traditional byte-order sorting:
```bash
LC_ALL=C sort data.txt
```

---

## 8. Safety, Security, and Portability

### 8.1 Temp Directory Space Exhaustion

Sorting huge datasets (e.g. 50 GB) can fill the `/tmp` filesystem (often mounted as an in-memory `tmpfs`), crashing the command. Always specify a physical disk location using `-T`:
```bash
sort -T /data/scratch massive_log.csv
```

---

## 9. Best Practices

1. **Explicitly Bound Key Specifications (`-kPOS,POS`)**:
   - *Guidance*: Always specify both start and end field positions (e.g. `-k2,2n` instead of `-k2`).
   - *Authoritative Justification*: GNU documentation notes that an unbounded `-k2` compares from field 2 to the end of the line as a single string.
2. **Use `-o` for In-Place Sorting**:
   - *Guidance*: Never use shell redirection `sort f > f`. Use `sort -o f f`.
   - *Authoritative Justification*: Shell redirection truncates files before the program executes; `-o` guarantees complete reading before write.
3. **Use `LC_ALL=C` for Pipeline Predictability and Speed**:
   - *Guidance*: Prepend `LC_ALL=C` when sorting before `uniq` or `join`.
   - *Authoritative Justification*: Standardizes ASCII byte ordering across all systems and accelerates performance.

---

## References

1. **GNU Coreutils sort Manual**: [https://www.gnu.org/software/coreutils/manual/html_node/sort-invocation.html](https://www.gnu.org/software/coreutils/manual/html_node/sort-invocation.html)
2. **POSIX.1-2024 sort Specification**: The Open Group Base Specifications Issue 8. [https://pubs.opengroup.org/onlinepubs/9799919799/utilities/sort.html](https://pubs.opengroup.org/onlinepubs/9799919799/utilities/sort.html)
