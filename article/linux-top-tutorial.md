---
title: "Linux Command Tutorial: top"
date: 2026-09-12T00:00:00+00:00
categories: ['Technology']
tags:
  - 'Linux'
  - 'procps-ng'
  - 'top'
  - 'Linux Command Tutorial'
draft: false
slug: "linux-top-tutorial"
description: "Authoritative reference tutorial for top (procps-ng), detailing real-time CPU states, memory metrics (RES/VIRT/SHR), interactive hotkeys, and batch execution (-b)."
upstream_suite: "procps-ng"
upstream_version: "procps-ng 4.0.4"
posix_standard: "None"
research_date: "2026-09-12"
---

The **Linux Command Tutorial** series provides rigorous, upstream-verified references for essential system commands across Linux distributions and UNIX-like environments. Each article focuses on a single executable, combining exhaustive option documentation, verified real-world examples, security boundaries, and best practices directly derived from official source documentation and POSIX standards.

---

## 1. Introduction

> **Upstream**: procps-ng 4.0.4 | **POSIX**: De-facto Standard (Not POSIX standardized) | **Safety Tier**: safe-read-only | **Scope**: interactive-system-monitoring

`top` provides a dynamic, real-time view of running system processes. It continuously refreshes a summary of system resource utilization (CPU load, memory allocation, swap pressure) paired with an ordered list of tasks ranked by CPU or memory consumption.

- **Upstream Project & Provenance**: Maintained within **procps-ng** (`procps-ng`).
- **Portability & Standards Baseline**: `top` is a de facto Linux monitoring utility; it is not specified in POSIX.1-2024.
- **Target Research Implementation**: Audited against **procps-ng 4.0.4** (`top(1)`).
- **Applicability & Lifecycle**: The standard terminal dashboard for live performance diagnostics, bottleneck triage, and process management.

---

## 2. Syntax and Command Model

### 2.1 Canonical Synopsis

```bash
top [-b] [-c] [-d delay] [-H] [-i] [-n iterations] [-p pidlist] [-u | -U user]
```

### 2.2 Execution Modes

- **Interactive Full-Screen Mode**: Default mode using the terminal curses library, updating every 3.0 seconds by default and responding to single-key interactive commands.
- **Batch Mode (`-b`)**: Disables curses screen positioning, outputting sequential plain-text iterations suitable for redirection to logs or script parsing.

---

## 3. Options and Interactive Hotkeys

### 3.1 Command-Line Startup Flags

| Flag | Description | Default |
|:---|:---|:---|
| `-b` | Batch mode operation (plain text stream). | Interactive curses |
| `-n N` | Number of iterations before exiting (especially useful with `-b`). | Continuous |
| `-d SEC`| Delay interval between screen refreshes. | `3.0` seconds |
| `-p PID`| Monitor only the specified process ID(s). | All processes |
| `-u USER`| Monitor only processes owned by `USER`. | All users |
| `-c` | Toggle display between binary name and full command line arguments. | Short name |
| `-H` | Thread mode: display individual kernel threads instead of process tasks. | Process tasks |

### 3.2 Interactive Runtime Hotkeys

| Hotkey | Action |
|:---:|:---|
| `M` | Sort process table by Memory consumption (`%MEM`). |
| `P` | Sort process table by CPU consumption (`%CPU`) (default). |
| `N` | Sort process table by Process ID (`PID`). |
| `T` | Sort process table by cumulative execution time (`TIME+`). |
| `1` | Toggle individual CPU core utilization breakdown in summary header. |
| `k` | Kill a process (prompts for PID and signal number). |
| `r` | Renice a process (prompts for PID and nice value). |
| `q` | Quit `top`. |

---

## 4. Basic Usage

### 4.1 Quick-Reference Cheatsheet Card

| Operation | Command / Key | Notes |
|:---|:---|:---|
| Launch monitor | `top` | Interactive real-time process viewer |
| Monitor specific PID | `top -p 1234` | Filters view to single process ID |
| Monitor by user | `top -u www-data` | Filters tasks to specific username |
| Thread-level view | `top -H -p 1234` | Shows threads instead of process tasks |
| Single-shot text report | `top -b -n 1 > snapshot.txt` | Batch mode export without curses codes |
| Sort by memory | Key `M` | In interactive mode, sorts by RAM usage |
| Toggle per-CPU view | Key `1` | Shows utilization of each CPU core |

### 4.2 Launching Interactive Monitor

```bash
top
```

### 4.3 Restricting to a Specific Process

```bash
top -p 4512
```

---

## 5. Practical Operations

### 5.1 Single-Shot Diagnostic Snapshot in Batch Mode

Capturing a point-in-time report to a file without interactive curses formatting:

```bash
top -b -n 1 > system_snapshot.txt
```
```console
top - 11:30:15 up 14 days,  3:57,  2 users,  load average: 0.18, 0.22, 0.15
Tasks: 215 total,   1 running, 214 sleeping,   0 stopped,   0 zombie
%Cpu(s):  1.5 us,  0.8 sy,  0.0 ni, 97.2 id,  0.2 wa,  0.0 hi,  0.3 si,  0.0 st
MiB Mem :  15920.4 total,   4812.1 free,   6120.8 used,   4987.5 buff/cache
MiB Swap:   2048.0 total,   2048.0 free,      0.0 used.   9412.3 avail Mem 

  PID USER      PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND
 4512 admin     20   0  689400 345200  18400 S   2.3   2.1   4:15.22 mysqld
 1200 syslog    20   0  220450   4120   3100 S   0.3   0.0   0:45.10 rsyslogd
```

### 5.2 Thread-Level CPU Profiling (`-H`)

Diagnosing which specific worker thread inside a JVM or database is causing 100% CPU usage:

```bash
top -H -p 4512
```
- Lists individual Light Weight Processes (LWP) and their distinct CPU consumption percentages.

---

## 6. Advanced Usage

### 6.1 Deciphering Memory Metrics: VIRT vs RES vs SHR

- `VIRT` (Virtual Image): The total amount of virtual memory allocated to the task, including mapped libraries, anonymous memory, and allocated but uncommitted pages.
- `RES` (Resident Set Size): The actual non-swapped **physical RAM** currently occupied by the task.
- `SHR` (Shared Memory): Memory that may potentially be shared with other processes (e.g. shared libraries, IPC shared memory).

### 6.2 CPU State Indicators Breakdown

- `us` (User): Percentage of CPU spent in user space running un-niced code.
- `sy` (System): Percentage spent in kernel space executing system calls.
- `id` (Idle): Percentage of time CPU is waiting with no work.
- `wa` (I/O Wait): Percentage of time CPU is idle while waiting for outstanding disk or network I/O to return. A high `wa` indicates a storage bottleneck, not a CPU capacity problem.
- `st` (Steal): Percentage of CPU cycles involuntarily taken away by the hypervisor in virtualized/cloud instances.

---

## 7. Exit Status, Environment, and Configuration

### 7.1 Exit Status Codes

| Exit Code | Meaning |
|:---:|:---|
| `0` | Clean termination (user pressed `q` or `-n` iteration limit reached). |
| `>0` | Command line parameter error, missing permissions, or invalid PID. |

### 7.2 Configuration File

Interactive customizations (colors, fields, sort order) can be persisted by pressing `W`, which saves settings to `~/.config/procps/toprc` or `~/.toprc`.

---

## 8. Safety, Security, and Portability

### 8.1 Signal Sending via `k`

> [!WARNING]
> Sending termination signals via the interactive `k` key defaults to `SIGTERM` (15). Avoid prematurely resorting to `SIGKILL` (9), which prevents applications from flushing database buffers or removing lockfiles.

---

## 9. Best Practices

1. **Use Batch Mode (`-b -n 1`) for Automated Incident Bundles**:
   - *Guidance*: Capture `top -b -n 1` in crash report scripts.
   - *Authoritative Justification*: Upstream documentation explains that batch mode produces clean, ANSI-free ASCII tables.
2. **Examine `wa` Before Blaming CPU Constraints**:
   - *Guidance*: If load average is high but `us+sy` is low, check `wa`.
   - *Authoritative Justification*: A high `wa` indicates disk saturation or NFS latency, where faster CPUs will not resolve performance degradation.
3. **Toggle `1` on Multi-Socket/Multi-Core Hosts**:
   - *Guidance*: Press `1` to expose individual CPU cores.
   - *Authoritative Justification*: Identifies single-threaded bottlenecks where one core is pegged at 100% while overall average load appears low.

---

## References

1. **procps-ng top(1) Manual**: [https://man7.org/linux/man-pages/man1/top.1.html](https://man7.org/linux/man-pages/man1/top.1.html)
2. **Linux /proc filesystem Documentation**: [https://docs.kernel.org/filesystems/proc.html](https://docs.kernel.org/filesystems/proc.html)
