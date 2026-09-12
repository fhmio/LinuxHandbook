---
title: "Linux Command Tutorial: ps"
date: 2026-09-12T00:00:00+00:00
categories: ['Technology']
tags:
  - 'Linux'
  - 'procps-ng'
  - 'ps'
  - 'Linux Command Tutorial'
draft: false
slug: "linux-ps-tutorial"
description: "Authoritative reference tutorial for ps (procps-ng), detailing UNIX/BSD/GNU option syntax, process state codes, thread inspection, custom output formats, and POSIX portability."
upstream_suite: "procps-ng"
upstream_version: "procps-ng 4.0.4"
posix_standard: "POSIX.1-2024"
research_date: "2026-09-12"
---

The **Linux Command Tutorial** series provides rigorous, upstream-verified references for essential system commands across Linux distributions and UNIX-like environments. Each article focuses on a single executable, combining exhaustive option documentation, verified real-world examples, security boundaries, and best practices directly derived from official source documentation and POSIX standards.

---

## 1. Introduction

`ps` (process status) displays information about active processes currently running on the system. It inspects the Linux `/proc` virtual pseudo-filesystem, parsing `/proc/[pid]/stat`, `status`, `cmdline`, and cgroups to report CPU, memory, thread hierarchy, and execution states.

- **Upstream Project & Provenance**: Maintained within the **procps-ng** project (`procps-ng`).
- **Portability & Standards Baseline**: Standardized in **IEEE Std 1003.1-2024 (POSIX.1-2024)**. Linux `ps` is unique in supporting three distinct syntax conventions: UNIX (prefixed by `-`), BSD (no hyphen), and GNU long options (prefixed by `--`).
- **Target Research Implementation**: Audited against **procps-ng 4.0.4** (`ps(1)`).
- **Applicability & Lifecycle**: The foundational tool for point-in-time process inspection, monitoring resource usage, and script-based pid resolution.

---

## 2. Syntax and Command Model

### 2.1 The Three Syntax Conventions

1. **UNIX (POSIX) Style**: Options prefixed with a single hyphen (`-`):
   ```bash
   ps -ef
   ```
2. **BSD Style**: Options specified without hyphens:
   ```bash
   ps aux
   ```
3. **GNU Long Options**: Options prefixed with double hyphens (`--`):
   ```bash
   ps --forest --sort=-%mem
   ```

*Note on syntax collision*: `ps -u` (UNIX) queries processes owned by a specific user list; `ps u` (BSD) activates user-oriented detailed format. Mixing styles without awareness can lead to syntax confusion.

---

## 3. Options

### 3.1 Process Selection Flags

| Flag | Style | Description | POSIX Defined |
|:---|:---:|:---|:---:|
| `-A`, `-e` | UNIX | Select all processes on the system. | Yes |
| `a` | BSD | Select all processes with a TTY, including other users' processes. | No |
| `x` | BSD | Select processes without controlling TTYs (daemons, background workers). | No |
| `-u user` | UNIX | Select processes by effective user ID or name. | Yes |
| `-p pid` | UNIX | Select processes by Process ID. | Yes |
| `-C cmd` | UNIX | Select by command executable name. | No |

### 3.2 Output Formatting Flags

| Flag | Style | Description |
|:---|:---:|:---|
| `-f` | UNIX | Full-format listing (UID, PID, PPID, C, STIME, TTY, TIME, CMD). |
| `-l` | UNIX | Long format (F, S, UID, PID, PPID, C, PRI, NI, ADDR, SZ, WCHAN, TTY, TIME, CMD). |
| `u` | BSD | User-oriented format (USER, PID, %CPU, %MEM, VSZ, RSS, TTY, STAT, START, TIME, COMMAND). |
| `-o format` | UNIX | User-defined custom format table. |
| `-H`, `--forest` | Both | Display ASCII process hierarchy tree. |

---

## 4. Basic Usage

### 4.1 Standard BSD Process Snapshot (`aux`)

```bash
ps aux | head -n 5
```
```console
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root         1  0.0  0.1 168340 12892 ?        Ss   Sep10   0:04 /sbin/init
root         2  0.0  0.0      0     0 ?        S    Sep10   0:00 [kthreadd]
root         3  0.0  0.0      0     0 ?        I<   Sep10   0:00 [rcu_gp]
syslog    1120  0.0  0.0 220450  4120 ?        Ssl  Sep10   0:01 /usr/sbin/rsyslogd -n
```

### 4.2 Standard POSIX Full Listing (`-ef`)

```bash
ps -ef | head -n 4
```
```text
UID        PID  PPID  C STIME TTY          TIME CMD
root         1     0  0 Sep10 ?        00:00:04 /sbin/init
root         2     0  0 Sep10 ?        00:00:00 [kthreadd]
daemon     412     1  0 Sep10 ?        00:00:00 /usr/sbin/atd -f
```

---

## 5. Practical Operations

### 5.1 Custom Machine-Readable Output via `-o`

Extracting precisely the PID, memory usage, CPU percentage, and command path:

```bash
ps -eo pid,ppid,%cpu,%mem,rss,comm --sort=-rss | head -n 5
```
```text
  PID  PPID %CPU %MEM   RSS COMMAND
 4512  4500  1.2  8.4 689400 mysqld
 8912     1  0.5  4.2 345000 java
 1204     1  0.0  1.8 148000 node
  412     1  0.0  0.2  16800 systemd-journal
```
- **Technical Analysis**: `rss` reports Resident Set Size (actual physical memory in KiB); `--sort=-rss` sorts the entire process table descending by RAM consumption.

### 5.2 Visualizing Parent-Child Process Trees

Inspecting service sub-worker relationships using `--forest`:

```bash
ps -ef --forest | grep -A 4 nginx
```
```text
root      4512     1  0 08:00 ?        00:00:00 nginx: master process /usr/sbin/nginx
www-data  4513  4512  0 08:00 ?        00:00:04  \_ nginx: worker process
www-data  4514  4512  0 08:00 ?        00:00:04  \_ nginx: worker process
www-data  4515  4512  0 08:00 ?        00:00:04  \_ nginx: worker process
```

### 5.3 Thread-Level Process Inspection

Viewing all execution threads (`LWP`) belonging to a specific multi-threaded application:

```bash
ps -T -p 4512
```
```text
  PID   LWP TTY          TIME CMD
 4512  4512 ?        00:00:01 mysqld
 4512  4513 ?        00:00:14 mysqld
 4512  4514 ?        00:00:00 mysqld
```

---

## 6. Advanced Usage

### 6.1 Decoding the `STAT` Process State Codes

The `STAT` column encodes Linux kernel scheduler states:
- **Primary States**:
  - `R`: Running or runnable (on run queue).
  - `S`: Interruptible sleep (waiting for an event/input).
  - `D`: Uninterruptible sleep (usually blocked on synchronous disk/NFS I/O). Cannot be killed by `SIGKILL`.
  - `Z`: Defunct / Zombie (terminated, waiting for parent to call `wait()`).
  - `T`: Stopped by job control signal (`SIGTSTP` or `SIGSTOP`).
- **Additional Modifiers**:
  - `<`: High-priority (nice < 0).
  - `N`: Low-priority (nice > 0).
  - `s`: Session leader.
  - `l`: Multi-threaded.
  - `+`: Foreground process group.

---

## 7. Exit Status, Environment, and Configuration

### 7.1 Exit Status Codes

| Exit Code | Meaning |
|:---:|:---|
| `0` | Success: process table inspected. |
| `>0` | An error occurred (syntax error in `-o`, PID not found, permission failure). |

---

## 8. Safety, Security, and Portability

### 8.1 Command-Line Truncation and Environment Leaks

- `/proc/[pid]/cmdline` exposes arguments passed to commands. Any secret passed directly via command line (e.g. `mysql -pSECRET`) is visible to every local user running `ps aux`.
- In shared environments, administrators should mount `/proc` with `hidepid=2` to ensure unprivileged users can only inspect their own processes.

---

## 9. Best Practices

1. **Use `ps -eo ...` for Shell Automation**:
   - *Guidance*: Avoid parsing `ps aux` in scripts; use `ps -eo pid=,comm=`.
   - *Authoritative Justification*: Appending `=` suppresses the header row, outputting deterministic whitespace-delimited columns.
2. **Sort at the Source via `--sort`**:
   - *Guidance*: Use `ps --sort=-%cpu` instead of piping into external `sort`.
   - *Authoritative Justification*: procps-ng performs in-memory numeric sorting before output, preserving table alignment.
3. **Inspect Zombie Processes Promptly**:
   - *Guidance*: Audit `STAT` column for `Z`.
   - *Authoritative Justification*: Zombie processes retain PID entries in kernel process tables; excess zombies can lead to PID exhaustion.

---

## References

1. **procps-ng ps(1) Manual**: [https://man7.org/linux/man-pages/man1/ps.1.html](https://man7.org/linux/man-pages/man1/ps.1.html)
2. **POSIX.1-2024 ps Specification**: The Open Group Base Specifications Issue 8. [https://pubs.opengroup.org/onlinepubs/9799919799/utilities/ps.html](https://pubs.opengroup.org/onlinepubs/9799919799/utilities/ps.html)
