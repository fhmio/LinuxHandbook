---
title: "Linux Command Tutorial: cat"
date: 2026-09-12T00:00:00+00:00
categories: ['Technology']
tags:
  - 'Linux'
  - 'GNU Coreutils'
  - 'cat'
  - 'Linux Command Tutorial'
draft: false
slug: "linux-cat-tutorial"
description: "Authoritative reference tutorial for cat (GNU Coreutils), detailing stream concatenation, non-printable character display, buffer semantics, and POSIX portability."
upstream_suite: "gnu-coreutils"
upstream_version: "GNU Coreutils 9.11"
posix_standard: "POSIX.1-2024"
research_date: "2026-09-12"
---

The **Linux Command Tutorial** series provides rigorous, upstream-verified references for essential system commands across Linux distributions and UNIX-like environments. Each article focuses on a single executable, combining exhaustive option documentation, verified real-world examples, security boundaries, and best practices directly derived from official source documentation and POSIX standards.

---

## 1. Introduction

> **Upstream**: `GNU Coreutils 9.11` | **POSIX**: `POSIX.1-2024 (with GNU extensions)` | **Safety Tier**: `safe-read-only` | **Scope**: `Sequential file concatenation, stream output & character visualization`

`cat` (concatenate) sequentially reads files and writes them to standard output. It is one of the most fundamental stream manipulation utilities in UNIX, operating directly on binary or text streams with page-aligned kernel buffers.

- **Upstream Project & Provenance**: Distributed in **GNU Coreutils** (`coreutils`).
- **Portability & Standards Baseline**: Standardized in **IEEE Std 1003.1-2024 (POSIX.1-2024)**. GNU `cat` extends POSIX with number squeeze flags (`-s`), display non-printing tabs (`-T`), and end-of-line markers (`-E`).
- **Target Research Implementation**: Audited against **GNU Coreutils 9.11** (`cat(1)`).
- **Applicability & Lifecycle**: Intended for concatenating multiple files, viewing short text configurations, and streaming files into pipelines.

---

## 2. Syntax and Command Model

### 2.1 Canonical Synopsis

```bash
cat [OPTION]... [FILE]...
```

### 2.2 Execution Model & Stream Behavior

- With no `FILE`, or when `FILE` is `-`, `cat` reads from standard input (`stdin`).
- `cat` transfers blocks using the `copy_file_range(2)` or `splice(2)` Linux system calls where supported, allowing zero-copy kernel transfers directly between file descriptors without copying data back and forth to user space.

---

## 3. Options

### 3.1 Primary Flags

| Short Flag | Long Flag | Description | POSIX Defined |
|:---|:---|:---|:---:|
| `-A` | `--show-all` | Equivalent to `-vET` (shows all non-printing, end-of-line, tabs). | No |
| `-b` | `--number-nonblank` | Number nonempty output lines, overrides `-n`. | No |
| `-e` | N/A | Equivalent to `-vE`. | No |
| `-E` | `--show-ends` | Display `$` at end of each line. | No |
| `-n` | `--number` | Number all output lines. | No |
| `-s` | `--squeeze-blank` | Suppress repeated empty output lines. | No |
| `-t` | N/A | Equivalent to `-vT`. | No |
| `-T` | `--show-tabs` | Display TAB characters as `^I`. | No |
| `-u` | N/A | Ignored by GNU `cat` (provided for POSIX compatibility). | Yes |
| `-v` | `--show-nonprinting` | Use `^` and `M-` notation, except for LFD and TAB. | No |

---

## 4. Basic Usage

### 4.1 Quick Reference & Common Invocations

| Task / Scenario | Command | Key Flags / Behavior |
|:---|:---|:---|
| Display file contents | `cat /etc/os-release` | Outputs full file to stdout |
| Concatenate multiple files | `cat part1.txt part2.txt > full.txt` | Merges files sequentially into single stream |
| View non-printing characters & CRLF | `cat -A script.sh` | `-A` shows tabs (`^I`), non-printables, and line ends (`$`) |
| Squeeze multiple blank lines | `cat -s log.txt` | `-s` collapses consecutive empty lines into one |
| Number non-empty lines | `cat -b code.py` | `-b` numbers only lines containing text |
| Number all lines | `cat -n file.txt` | `-n` prefixes line numbers to every line |
| Write file via heredoc | `cat <<'EOF' > config.conf` | Heredoc stream capture to destination file |

### 4.2 Displaying File Contents

```bash
cat /etc/os-release
```

### 4.3 Concatenating Multiple Files

```bash
cat header.html body.html footer.html > index.html
```

---

## 5. Practical Operations

### 5.1 Debugging Windows CRLF vs Linux LF Line Endings

Hidden carriage return characters (`\r` or `^M`) cause elusive syntax errors in shell scripts. Visualizing line endings:

```bash
cat -A script.sh
```

*Sample terminal output:*

```text
#!/bin/bash^M$
echo "Starting deploy..."^M$
exit 0^M$
```

- **Technical Analysis**: `^M$` reveals DOS/Windows carriage return (`\r\n`) sequences. A pure UNIX file displays only `$` at line ends.

### 5.2 Squeezing Multi-Line Spacing in Logs

Collapsing multiple consecutive blank lines into a single blank line:

```bash
cat -s application.log > cleaned_application.log
```

### 5.3 Numbering Non-Empty Code Lines

```bash
cat -b main.py | head -n 5
```

*Sample terminal output:*

```text
     1  import sys
     2  import os

     3  def main():
     4      print("Started")
```

---

## 6. Advanced Usage

### 6.1 Creating Files via Standard Input (Heredoc)

Writing structured configuration files directly in bash scripts:

```bash
cat <<'EOF' > /etc/systemd/resolved.conf.d/dns.conf
[Resolve]
DNS=1.1.1.1 8.8.8.8
Domains=~.
EOF
```

- Quoting `'EOF'` prevents shell parameter expansion, ensuring content is written verbatim.

---

## 7. Exit Status, Environment, and Configuration

### 7.1 Exit Status Codes

| Exit Code | Meaning |
|:---:|:---|
| `0` | All input files were read and output successfully. |
| `>0` | An error occurred (input file does not exist, permission denied, output device full). |

---

## 8. Safety, Security, and Portability

### 8.1 The "Useless Use of Cat" (UUOC) Anti-Pattern

> [!TIP]
> **I/O Overhead Optimization**: Piping `cat file | grep pattern` spawns an unnecessary child process, extra pipeline buffer, and IPC context-switching overhead.
>
> Passing arguments directly (`grep pattern file`) or using shell input redirection (`grep pattern < file`) allows utilities to optimize I/O via `mmap(2)` and direct kernel buffering.

### 8.2 Binary Stream Clobbering

> [!WARNING]
> Running `cat` on binary executable files or raw device files without redirection dumps non-printable escape codes directly into your terminal session, frequently corrupting terminal fonts, line disciplines, and cursor states. Use `tset` or `reset` to restore your shell if this occurs.

---

## 9. Best Practices

1. **Avoid UUOC in Performance-Critical Pipelines**:
   > [!TIP]
   > *Guidance*: Never invoke `cat file | command`. Use `command < file` or `command file`.
   > *Authoritative Justification*: GNU documentation notes that passing filenames directly allows utilities to optimize I/O via memory mapping (`mmap`).

2. **Use `cat -A` When Debugging Whitespace and Syntax Errors**:
   > [!TIP]
   > *Guidance*: Run `cat -A` on failing shell scripts or Makefile tabs.
   > *Authoritative Justification*: Discloses non-printable ASCII, mixed tab/spaces, and `\r` carriage returns.

3. **Use Single-Quoted Heredocs (`<<'EOF'`) for Literal Script Generation**:
   > [!IMPORTANT]
   > *Guidance*: Quote delimiter tags when generating scripts.
   > *Authoritative Justification*: Prevents variable expansion from altering payload code.

---

## References

1. **GNU Coreutils cat Manual**: [https://www.gnu.org/software/coreutils/manual/html_node/cat-invocation.html](https://www.gnu.org/software/coreutils/manual/html_node/cat-invocation.html)
2. **POSIX.1-2024 cat Specification**: The Open Group Base Specifications Issue 8. [https://pubs.opengroup.org/onlinepubs/9799919799/utilities/cat.html](https://pubs.opengroup.org/onlinepubs/9799919799/utilities/cat.html)
