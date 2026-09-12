---
title: "Linux Command Tutorial: pgrep"
date: 2026-09-12T00:00:00+00:00
categories: ['Technology']
tags:
  - 'Linux'
  - 'procps-ng'
  - 'pgrep'
  - 'Linux Command Tutorial'
draft: false
slug: "linux-pgrep-tutorial"
description: "Authoritative reference tutorial for pgrep (procps-ng), detailing process searching by pattern, user filtering (-u), exact name matching (-x), and full command matching (-f)."
upstream_suite: "procps-ng"
upstream_version: "procps-ng 4.0.4"
posix_standard: "None"
research_date: "2026-09-12"
---

The **Linux Command Tutorial** series provides rigorous, upstream-verified references for essential system commands across Linux distributions and UNIX-like environments. Each article focuses on a single executable, combining exhaustive option documentation, verified real-world examples, security boundaries, and best practices directly derived from official source documentation and POSIX standards.

---

## 1. Introduction

`pgrep` searches the currently running processes and outputs the process IDs (PIDs) matching specified selection criteria to standard output. It eliminates the need for fragile pipelines like `ps aux | grep name | awk '{print $2}'`.

- **Upstream Project & Provenance**: Maintained within **procps-ng** (`procps-ng`).
- **Portability & Standards Baseline**: `pgrep` is an industry-standard UNIX utility originating from Solaris; not defined in POSIX.1-2024.
- **Target Research Implementation**: Audited against **procps-ng 4.0.4** (`pgrep(1)`).
- **Applicability & Lifecycle**: The preferred tool for finding process IDs based on executable names, arguments, usernames, or session groups.

---

## 2. Syntax and Command Model

### 2.1 Canonical Synopsis

```bash
pgrep [options] pattern
```

### 2.2 Execution Model & Extended Regular Expressions

- `pattern` is evaluated as an **Extended Regular Expression (ERE)**.
- By default, `pgrep` matches against the **basename** of the executable (from `/proc/[pid]/stat`).
- If `-f` (full) is passed, `pgrep` matches against the complete command line and arguments (from `/proc/[pid]/cmdline`).
- Output consists of matching PIDs separated by newlines (or custom delimiter via `-d`).

---

## 3. Options

### 3.1 Primary Flags

| Flag | Description | Default | Upstream Note |
|:---|:---|:---|:---|
| `-l` | List the process name as well as the process ID. | PID only | Convenient for verification |
| `-a` | List the full command line arguments as well as the PID. | PID only | Avoids ambiguity |
| `-f` | Match pattern against full command line arguments, not just basename. | Basename | Crucial for scripts |
| `-x` | Exact match: require pattern to match the entire name or command line. | Substring | Prevents false positives |
| `-u user` | Match only processes owned by effective user ID or username. | All users | User filtering |
| `-U user` | Match only processes owned by real user ID or username. | All users | User filtering |
| `-o` | Select only the oldest (least recently started) matching process. | All matches | Singleton selection |
| `-n` | Select only the newest (most recently started) matching process. | All matches | Singleton selection |
| `-c` | Suppress normal output; print a count of matching processes. | Print PIDs | Counting instances |
| `-d delim`| Set string used to separate PIDs in output (e.g. `,`). | Newline `\n` | Pipeline friendly |

---

## 4. Basic Usage

### 4.1 Finding PIDs by Name

```bash
pgrep nginx
```
```text
4512
4513
4514
```

### 4.2 Listing PIDs Alongside Binary Names

```bash
pgrep -l sshd
```
```text
1105 sshd
4912 sshd
```

---

## 5. Practical Operations

### 5.1 Exact Matching to Avoid False Positives (`-x`)

When searching for a service named `sh`, standard `pgrep sh` matches `sshd`, `bash`, `ssh-agent`, etc.:

```bash
pgrep -x sh
```
- **Technical Analysis**: `-x` requires the pattern to match the entire process name from start to finish (`^pattern$`), matching strictly `/bin/sh` processes.

### 5.2 Searching Python and Java Scripts by Full Arguments (`-f`)

Because Python processes appear in `/proc` as `python3`, searching for `worker.py` with standard `pgrep` matches nothing:

```bash
pgrep -fa "worker.py"
```
```text
12402 python3 /opt/app/worker.py --concurrency=4
```
- `-f` inspects the full argument vector, while `-a` prints the arguments for visual confirmation.

### 5.3 Counting Active Worker Instances

Checking how many worker processes are currently alive:

```bash
pgrep -c -u www-data php-fpm
```
```text
16
```

### 5.4 Formatting Comma-Delimited PIDs for Other Utilities

Passing PIDs directly into tools like `top` or `strace`:

```bash
top -p $(pgrep -d, nginx)
```

---

## 6. Advanced Usage

### 6.1 Avoiding the Self-Matching Trap of `ps | grep`

When running `ps aux | grep nginx`, the `grep` command itself often appears in the output because `grep` contains the word `nginx`. `pgrep` never matches its own process.

---

## 7. Exit Status, Environment, and Configuration

### 7.1 Exit Status Codes

| Exit Code | Meaning |
|:---:|:---|
| `0` | One or more matching processes were found. |
| `1` | No matching processes were found. |
| `2` | Syntax error in the command-line options. |
| `3` | Fatal error (e.g. out of memory). |

This makes `pgrep` ideal for shell conditional tests:
```bash
if pgrep -x nginx > /dev/null; then
    echo "Nginx is running"
fi
```

---

## 8. Safety, Security, and Portability

### 8.1 Truncated Comm Names

On Linux, `/proc/[pid]/comm` is limited to 15 characters. If an executable name exceeds 15 characters, standard `pgrep` without `-f` only matches against the first 15 characters. Use `-f` for long process names.

---

## 9. Best Practices

1. **Always Use `-x` When Matching Standard Utilities**:
   - *Guidance*: Write `pgrep -x <name>` when matching well-known binaries.
   - *Authoritative Justification*: Prevents substring collisions with unrelated daemons.
2. **Use `-f` for Interpreted Scripts (Python, Node, Java)**:
   - *Guidance*: Pass `-f` when searching for script paths.
   - *Authoritative Justification*: The binary name of interpreted scripts is the interpreter (`python3`), not the script name.
3. **Use `-c` for Instance Monitoring**:
   - *Guidance*: Check pool concurrency using `pgrep -c`.
   - *Authoritative Justification*: Avoids piping into `wc -l`.

---

## References

1. **procps-ng pgrep(1) Manual**: [https://man7.org/linux/man-pages/man1/pgrep.1.html](https://man7.org/linux/man-pages/man1/pgrep.1.html)
2. **Linux /proc/[pid]/status Documentation**: [https://docs.kernel.org/filesystems/proc.html](https://docs.kernel.org/filesystems/proc.html)
