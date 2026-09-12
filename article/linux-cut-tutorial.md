---
title: "Linux Command Tutorial: cut"
date: 2026-09-12T00:00:00+00:00
categories: ['Technology']
tags:
  - 'Linux'
  - 'GNU Coreutils'
  - 'cut'
  - 'Linux Command Tutorial'
draft: false
slug: "linux-cut-tutorial"
description: "Authoritative reference tutorial for cut (GNU Coreutils), detailing column slicing by bytes (-b), characters (-c), and fields (-f), delimiter handling, and POSIX portability."
upstream_suite: "gnu-coreutils"
upstream_version: "GNU Coreutils 9.11"
posix_standard: "POSIX.1-2024"
research_date: "2026-09-12"
---

The **Linux Command Tutorial** series provides rigorous, upstream-verified references for essential system commands across Linux distributions and UNIX-like environments. Each article focuses on a single executable, combining exhaustive option documentation, verified real-world examples, security boundaries, and best practices directly derived from official source documentation and POSIX standards.

---

## 1. Introduction

`cut` removes sections from each line of files or standard input. It extracts column fields based on delimiters (e.g. commas, tabs, colons) or slices exact byte/character offsets.

- **Upstream Project & Provenance**: Distributed in **GNU Coreutils** (`coreutils`).
- **Portability & Standards Baseline**: Standardized in **IEEE Std 1003.1-2024 (POSIX.1-2024)**. GNU `cut` introduces custom output delimiters (`--output-delimiter`), complement ranges (`--complement`), and zero-terminated records (`-z`).
- **Target Research Implementation**: Audited against **GNU Coreutils 9.11** (`cut(1)`).
- **Applicability & Lifecycle**: The lightweight choice for slicing delimited files (CSV, TSV, `/etc/passwd`) without spawning heavy language runtimes.

---

## 2. Syntax and Command Model

### 2.1 Canonical Synopsis

```bash
cut OPTION... [FILE]...
```

### 2.2 Execution Model & Modes

`cut` requires specifying **exactly one** extraction mode:
1. **Bytes (`-b LIST`)**: Selects byte offsets (1-indexed).
2. **Characters (`-c LIST`)**: Selects character offsets (multi-byte safe in UTF-8).
3. **Fields (`-f LIST`)**: Selects delimited fields separated by `-d`.

---

## 3. Options

### 3.1 Primary Operational Flags

| Short Flag | Long Flag | Description | POSIX Defined |
|:---|:---|:---|:---:|
| `-b LIST` | `--bytes=LIST` | Select only these bytes. | Yes |
| `-c LIST` | `--characters=LIST` | Select only these characters. | Yes |
| `-d CHAR` | `--delimiter=CHAR` | Use CHAR instead of TAB for field delimiter. | Yes |
| `-f LIST` | `--fields=LIST` | Select only these fields. | Yes |
| `-s` | `--only-delimited` | Do not print lines not containing delimiters. | Yes |
| N/A | `--complement` | Complement the set of selected bytes, characters or fields. | No |
| N/A | `--output-delimiter=STRING` | Use STRING as the output delimiter (default is input delimiter). | No |
| `-z` | `--zero-terminated` | Line delimiter is NUL (`\0`), not newline. | No |

---

## 4. Basic Usage

### 4.1 Extracting Usernames from `/etc/passwd`

```bash
cut -d: -f1 /etc/passwd | head -n 4
```
```text
root
daemon
bin
sys
```

### 4.2 Slicing Multiple Non-Contiguous Fields

```bash
cut -d: -f1,6,7 /etc/passwd | head -n 2
```
```text
root:/root:/bin/bash
daemon:/usr/sbin:/usr/sbin/nologin
```

---

## 5. Practical Operations

### 5.1 Changing Delimiters on the Fly via `--output-delimiter`

Transforming a colon-delimited `/etc/passwd` line into a space-separated format:

```bash
cut -d: -f1,3,6 --output-delimiter=" | " /etc/passwd | head -n 3
```
```text
root | 0 | /root
daemon | 1 | /usr/sbin
bin | 2 | /bin
```

### 5.2 Dropping Specific Columns with `--complement`

Removing the middle column (Field 2) from a 3-column CSV:

```bash
echo "Alice,SecretData,Engineer" | cut -d, --complement -f2
```
```text
Alice,Engineer
```

### 5.3 Slicing Fixed-Width Character Columns

Extracting fixed-width columns (characters 1–10 and 20–30):

```bash
cut -c 1-10,20-30 fixed_records.txt
```

---

## 6. Advanced Usage

### 6.1 Suppressing Non-Delimited Lines with `-s`

By default, lines that do not contain the delimiter are printed unmodified. In scripts processing CSV headers or mixed logs, this causes dirty lines. Passing `-s` suppresses non-matching lines:

```bash
cut -d, -f2 -s data_with_comments.csv
```
- Lines lacking a comma are discarded.

---

## 7. Exit Status, Environment, and Configuration

### 7.1 Exit Status Codes

| Exit Code | Meaning |
|:---:|:---|
| `0` | Success: fields extracted cleanly. |
| `>0` | An error occurred (multiple selection modes specified, invalid field range, file unreadable). |

---

## 8. Safety, Security, and Portability

### 8.1 Single-Character Delimiter Limitation

- `cut` strictly accepts a **single character** as `-d`. It cannot split on multi-character delimiters (e.g. `::` or `\s+`).
- For multi-character splitting, use `awk -F"::"` or `sed`.

---

## 9. Best Practices

1. **Use `cut` for Simple Delimited Slicing Over `awk`**:
   - *Guidance*: For single-character delimited field extraction (`cut -d: -f1`), prefer `cut`.
   - *Authoritative Justification*: GNU documentation notes `cut` is a lightweight C binary with minimal memory footprint and faster throughput than AWK interpreters.
2. **Always Use `-s` on Delimited Log Files**:
   - *Guidance*: Supply `-s` when processing CSV files that might contain comments or blank lines.
   - *Authoritative Justification*: Prevents non-delimited lines from passing through into column pipelines.
3. **Use `--complement` for Inverted Slices**:
   - *Guidance*: Strip unwanted fields using `--complement` rather than listing all remaining fields.
   - *Authoritative Justification*: Reduces brittle hardcoded column indexes in scripts.

---

## References

1. **GNU Coreutils cut Manual**: [https://www.gnu.org/software/coreutils/manual/html_node/cut-invocation.html](https://www.gnu.org/software/coreutils/manual/html_node/cut-invocation.html)
2. **POSIX.1-2024 cut Specification**: The Open Group Base Specifications Issue 8. [https://pubs.opengroup.org/onlinepubs/9799919799/utilities/cut.html](https://pubs.opengroup.org/onlinepubs/9799919799/utilities/cut.html)
