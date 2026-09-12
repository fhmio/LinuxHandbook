---
title: "Linux Command Tutorial: tail"
date: 2026-09-12T00:00:00+00:00
categories: ['Technology']
tags:
  - 'Linux'
  - 'GNU Coreutils'
  - 'tail'
  - 'Linux Command Tutorial'
draft: false
slug: "linux-tail-tutorial"
description: "Authoritative reference tutorial for tail (GNU Coreutils), detailing file following (-f, -F), positive offset indexing (+K), log monitoring, and POSIX portability."
upstream_suite: "gnu-coreutils"
upstream_version: "GNU Coreutils 9.11"
posix_standard: "POSIX.1-2024"
research_date: "2026-09-12"
---

The **Linux Command Tutorial** series provides rigorous, upstream-verified references for essential system commands across Linux distributions and UNIX-like environments. Each article focuses on a single executable, combining exhaustive option documentation, verified real-world examples, security boundaries, and best practices directly derived from official source documentation and POSIX standards.

---

## 1. Introduction

`tail` outputs the end portion (the last *N* lines or bytes) of specified files or standard input. Beyond static slicing, `tail` provides real-time streaming capability via the follow flags (`-f` and `-F`), monitoring growing files and log streams as new lines are appended.

- **Upstream Project & Provenance**: Distributed in **GNU Coreutils** (`coreutils`).
- **Portability & Standards Baseline**: Standardized in **IEEE Std 1003.1-2024 (POSIX.1-2024)**. GNU `tail` adds inotify-backed monitoring, descriptor vs filename tracking (`-F`), and PID tracking (`--pid`).
- **Target Research Implementation**: Audited against **GNU Coreutils 9.11** (`tail(1)`).
- **Applicability & Lifecycle**: The de facto utility for monitoring system journals, application logs, and streaming real-time metrics.

---

## 2. Syntax and Command Model

### 2.1 Canonical Synopsis

```bash
tail [OPTION]... [FILE]...
```

### 2.2 Execution Model: Inotify vs Polling

- On modern Linux, GNU `tail` automatically utilizes the **inotify(7)** kernel event subsystem to monitor filesystem append events, waking up instantaneously when new data is written without CPU busy-looping.
- If inotify is unavailable or disabled, `tail` falls back to periodic polling (`-s`).

---

## 3. Options

### 3.1 Primary Operational Flags

| Short Flag | Long Flag | Description | POSIX Defined | Default |
|:---|:---|:---|:---:|:---|
| `-n K` | `--lines=[+]K` | Output last K lines; with `+K`, output starting with line K. | Yes | 10 |
| `-c K` | `--bytes=[+]K` | Output last K bytes; with `+K`, output starting with byte K. | Yes | N/A |
| `-f` | `--follow[={name|descriptor}]` | Output appended data as file grows. | Yes | `descriptor` |
| `-F` | N/A | Same as `--follow=name --retry` (tracks log rotations). | No | Off |
| N/A | `--pid=PID` | With `-f`, terminate after process ID PID dies. | No | Off |
| `-s N` | `--sleep-interval=N` | With `-f`, sleep approximately N seconds between iterations. | No | 1.0s |
| `-q` | `--quiet`, `--silent` | Never output headers giving file names. | No | Multi-file auto |
| `-z` | `--zero-terminated` | Line delimiter is NUL (`\0`), not newline. | No | Off |

---

## 4. Basic Usage

### 4.1 Last 10 Lines (Default)

```bash
tail /var/log/nginx/access.log
```

### 4.2 Last 25 Lines Explicitly

```bash
tail -n 25 /var/log/syslog
```

---

## 5. Practical Operations

### 5.1 Real-Time Log Monitoring Across Rotations (`-F`)

Tracking an active application log across logrotate truncation and renaming events:

```bash
tail -F /var/log/nginx/error.log
```
- **Technical Analysis**:
  - Standard `-f` tracks the underlying file descriptor (`inode`). When `logrotate` renames `error.log` to `error.log.1` and opens a new file, `-f` stays locked to the old rotated file.
  - `-F` tracks by **filename** and re-opens the file descriptor when a new file with that name appears, seamlessly continuing stream monitoring across daily rotations.

### 5.2 Slicing "From Line K to the End" via `+K`

Stripping a 1-line CSV header and processing the remaining data:

```bash
tail -n +2 data.csv | awk -F, '{print $1, $3}'
```
- **Technical Analysis**: `+2` specifies starting from line 2 onward to the end of the file, cleanly removing the first row.

### 5.3 Auto-Terminating Tail with Process Tracking (`--pid`)

Monitoring a long-running backup process and terminating log streaming the exact moment the process finishes:

```bash
./run_backup.sh > backup.log 2>&1 &
BACKUP_PID=$!
tail --pid=$BACKUP_PID -f backup.log
```
- When process `$BACKUP_PID` exits, `tail` automatically terminates and yields the shell prompt.

---

## 6. Advanced Usage

### 6.1 Monitoring Multiple Files Simultaneously

```bash
tail -f /var/log/auth.log /var/log/syslog
```
```text
==> /var/log/auth.log <==
Sep 12 11:15:01 web sshd[4912]: Accepted publickey for admin...

==> /var/log/syslog <==
Sep 12 11:15:10 web systemd[1]: Started Session 45 of User admin.
```
- Switches context and outputs file headers automatically as new writes occur across monitored streams.

---

## 7. Exit Status, Environment, and Configuration

### 7.1 Exit Status Codes

| Exit Code | Meaning |
|:---:|:---|
| `0` | Success: requested lines output cleanly. |
| `>0` | An error occurred (file unreadable, invalid line offset). |

---

## 8. Safety, Security, and Portability

### 8.1 Differences Between `-f` and `-F`

- `-f`: Follows the opened inode (file descriptor). If the file is unlinked or rotated, `tail` continues reading the dead inode until terminated.
- `-F`: Follows by file name. Re-checks directory entries and re-establishes tracking if the file is recreated or replaced.

---

## 9. Best Practices

1. **Always Use `tail -F` (Capital F) for Production Log Streaming**:
   - *Guidance*: Default all log monitoring to `tail -F`.
   - *Authoritative Justification*: GNU documentation explains that `-F` handles log file renaming, deletion, and recreation automatically.
2. **Use `tail -n +2` for Header Stripping**:
   - *Guidance*: Use `tail -n +2` instead of complex `sed` or `awk` invocations to skip header rows in pipelines.
   - *Authoritative Justification*: Standardized by POSIX.1-2024 and optimized for streaming throughput in Coreutils.
3. **Use `--pid` in Automated Test Harnesses**:
   - *Guidance*: Bind `tail -f` to child PID in background integration tests.
   - *Authoritative Justification*: Prevents orphaned `tail` background processes from leaking memory after the watched test script terminates.

---

## References

1. **GNU Coreutils tail Manual**: [https://www.gnu.org/software/coreutils/manual/html_node/tail-invocation.html](https://www.gnu.org/software/coreutils/manual/html_node/tail-invocation.html)
2. **POSIX.1-2024 tail Specification**: The Open Group Base Specifications Issue 8. [https://pubs.opengroup.org/onlinepubs/9799919799/utilities/tail.html](https://pubs.opengroup.org/onlinepubs/9799919799/utilities/tail.html)
