---
title: "Linux Command Tutorial: tr"
date: 2026-09-12T00:00:00+00:00
categories: ['Technology']
tags:
  - 'Linux'
  - 'GNU Coreutils'
  - 'tr'
  - 'Linux Command Tutorial'
draft: false
slug: "linux-tr-tutorial"
description: "Authoritative reference tutorial for tr (GNU Coreutils), detailing character translation, deletion (-d), squeezing (-s), character classes, and POSIX portability."
upstream_suite: "gnu-coreutils"
upstream_version: "GNU Coreutils 9.11"
posix_standard: "POSIX.1-2024"
research_date: "2026-09-12"
---

The **Linux Command Tutorial** series provides rigorous, upstream-verified references for essential system commands across Linux distributions and UNIX-like environments. Each article focuses on a single executable, combining exhaustive option documentation, verified real-world examples, security boundaries, and best practices directly derived from official source documentation and POSIX standards.

---

## 1. Introduction

> **Upstream**: GNU Coreutils 9.11 | **POSIX**: POSIX.1-2024 (with GNU extensions) | **Safety Tier**: safe-read-only | **Scope**: text-processing

`tr` (translate) translates, squeezes, or deletes characters from standard input, writing the results to standard output. It operates strictly on character streams (not file path arguments) as a fast, byte-level transformation filter.

- **Upstream Project & Provenance**: Distributed in **GNU Coreutils** (`coreutils`).
- **Portability & Standards Baseline**: Standardized in **IEEE Std 1003.1-2024 (POSIX.1-2024)**.
- **Target Research Implementation**: Audited against **GNU Coreutils 9.11** (`tr(1)`).
- **Applicability & Lifecycle**: The standard filter for case conversion, stripping carriage returns, and collapsing whitespace.

---

## 2. Syntax and Command Model

### 2.1 Canonical Synopsis

```bash
tr [OPTION]... SET1 [SET2]
```

### 2.2 Execution Model

- `tr` reads **strictly from standard input** (`stdin`). It does not take input file path operands.
- **Translation (`SET1 -> SET2`)**: Maps the *N*-th character in `SET1` to the *N*-th character in `SET2`. If `SET2` is shorter than `SET1`, `SET2` is padded to match the length of `SET1` with its last character.

---

## 3. Options

### 3.1 Primary Operational Flags

| Short Flag | Long Flag | Description | POSIX Defined |
|:---|:---|:---|:---:|
| `-c`, `-C` | `--complement` | Use the complement of SET1. | Yes |
| `-d` | `--delete` | Delete characters in SET1, do not translate. | Yes |
| `-s` | `--squeeze-repeats` | Replace each sequence of a repeated character with a single occurrence. | Yes |
| `-t` | `--truncate-set1` | First truncate SET1 to length of SET2. | Yes |

### 3.2 Character Classes

POSIX character classes are specified enclosed in `[:` and `:]`:
- `[:alnum:]`, `[:alpha:]`, `[:digit:]`, `[:lower:]`, `[:upper:]`, `[:space:]`, `[:punct:]`, `[:cntrl:]`.

---

## 4. Basic Usage

### 4.1 Quick-Reference Cheatsheet Card

| Operation | Command | Notes |
|:---|:---|:---|
| Lowercase to uppercase | `tr '[:lower:]' '[:upper:]' < file.txt` | Standard POSIX case translation |
| Uppercase to lowercase | `tr '[:upper:]' '[:lower:]' < file.txt` | Standard POSIX lowercase fold |
| Delete specific characters | `tr -d '\r' < dos.txt > unix.txt` | Strips DOS carriage return bytes |
| Squeeze repeated spaces | `tr -s ' ' < spaced.txt` | Collapses consecutive spaces into one |
| Replace character with newline | `tr ' ' '\n' < words.txt` | Splits space-separated list into lines |
| Keep only alphanumerics | `tr -cd '[:alnum:]' < input.txt` | Deletes complement of alphanumeric set |
| Translate delimiters | `tr ':' '\t' < /etc/passwd` | Converts colons to tabs |

### 4.2 Lowercase to Uppercase Conversion

```bash
echo "linux command tutorial" | tr '[:lower:]' '[:upper:]'
```
```text
LINUX COMMAND TUTORIAL
```

### 4.3 Deleting Specific Characters

```bash
echo "Phone: (555) 123-4567" | tr -d ' ()-'
```
```text
Phone:5551234567
```

---

## 5. Practical Operations

### 5.1 Stripping Windows Carriage Returns (`\r`)

Cleaning up a DOS text file in a pipeline:

```bash
cat windows_file.txt | tr -d '\r' > unix_file.txt
```
- Deletes every `\r` character without altering line feeds (`\n`).

### 5.2 Squeezing Repeated Whitespace

Normalizing inconsistent multi-space formatting into a single space:

```bash
echo "column1    column2        column3" | tr -s ' '
```
```text
column1 column2 column3
```

### 5.3 Extracting Only Alphanumeric Characters (Complement `-c`)

Purging all non-alphanumeric characters, replacing them with newlines to generate a word frequency list:

```bash
tr -c '[:alnum:]' '\n' < article.txt | tr '[:upper:]' '[:lower:]' | sort | uniq -c | sort -nr | head -n 4
```
- Uses `-c` to target everything that is *not* alphanumeric, mapping it to newlines.

---

## 6. Advanced Usage

### 6.1 Generating Random Cryptographic Passwords

Extracting printable characters from `/dev/urandom`:

```bash
tr -dc 'A-Za-z0-9!@#$%^&*' < /dev/urandom | head -c 24; echo
```
```text
7b@Wq!9mK#1vL8zP$4xN&2aQ
```
- **Technical Analysis**: `-d` (delete) combined with `-c` (complement) strips all bytes *except* those in the specified character set, producing a clean random token stream.

---

## 7. Exit Status, Environment, and Configuration

### 7.1 Exit Status Codes

| Exit Code | Meaning |
|:---:|:---|
| `0` | Success: character translation completed. |
| `>0` | An error occurred (invalid character range, missing SET operand). |

---

## 8. Safety, Security, and Portability

### 8.1 No Direct Filename Operands

> [!IMPORTANT]
> `tr` does not accept file paths as arguments. Running `tr 'a' 'b' file.txt` treats `"file.txt"` as part of `SET2`, causing catastrophic translation errors or infinite hangs waiting on stdin. Always supply input via shell redirection (`< file.txt`) or a pipeline (`cat file.txt | tr ...`).

---

## 9. Best Practices

1. **Always Use POSIX Classes Over Ranges for Case Folding**:
   - *Guidance*: Use `tr '[:lower:]' '[:upper:]'` instead of `tr 'a-z' 'A-Z'`.
   - *Authoritative Justification*: POSIX documentation notes that character classes properly respect locale-specific casing rules.
2. **Use `tr -d '\r'` for Fast DOS to UNIX Conversion**:
   - *Guidance*: Strip `\r` using `tr -d '\r'` rather than installing `dos2unix`.
   - *Authoritative Justification*: Standardized in all UNIX systems and operates directly on standard streams.
3. **Use `-s` Before Line Tokenization**:
   - *Guidance*: Squeeze repeated delimiters (`tr -s ' '`) before piping into `cut -d' '`.
   - *Authoritative Justification*: Prevents empty field proliferation caused by consecutive spaces.

---

## References

1. **GNU Coreutils tr Manual**: [https://www.gnu.org/software/coreutils/manual/html_node/tr-invocation.html](https://www.gnu.org/software/coreutils/manual/html_node/tr-invocation.html)
2. **POSIX.1-2024 tr Specification**: The Open Group Base Specifications Issue 8. [https://pubs.opengroup.org/onlinepubs/9799919799/utilities/tr.html](https://pubs.opengroup.org/onlinepubs/9799919799/utilities/tr.html)
