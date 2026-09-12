---
title: "Linux Command Tutorial: pkill"
date: 2026-09-12T00:00:00+00:00
categories: ['Technology']
tags:
  - 'Linux'
  - 'procps-ng'
  - 'pkill'
  - 'Linux Command Tutorial'
draft: false
slug: "linux-pkill-tutorial"
description: "Authoritative reference tutorial for pkill (procps-ng), detailing signal dispatch by process pattern, user targeting (-u), exact name matching (-x), and safety boundaries."
upstream_suite: "procps-ng"
upstream_version: "procps-ng 4.0.4"
posix_standard: "None"
research_date: "2026-09-12"
---

The **Linux Command Tutorial** series provides rigorous, upstream-verified references for essential system commands across Linux distributions and UNIX-like environments. Each article focuses on a single executable, combining exhaustive option documentation, verified real-world examples, security boundaries, and best practices directly derived from official source documentation and POSIX standards.

---

## 1. Introduction

`pkill` sends specified signals (by default `SIGTERM`) to processes matching selection criteria. It combines process discovery with signal delivery, eliminating the need to look up PIDs manually before invoking `kill`.

- **Upstream Project & Provenance**: Maintained within **procps-ng** (`procps-ng`).
- **Portability & Standards Baseline**: `pkill` is a de facto standard across UNIX and Linux systems; not defined in POSIX.1-2024.
- **Target Research Implementation**: Audited against **procps-ng 4.0.4** (`pkill(1)`).
- **Applicability & Lifecycle**: The standard command for terminating processes by name, killing user sessions, or broadcasting configuration reloads (`SIGHUP`).

---

## 2. Syntax and Command Model

### 2.1 Canonical Synopsis

```bash
pkill [options] pattern
```

### 2.2 Execution Model & Signal Default

- `pkill` locates all processes matching `pattern` and invokes the `kill(2)` system call on each matched PID.
- **Default Signal**: If no signal is explicitly specified, `pkill` transmits **`SIGTERM` (Signal 15)**, requesting graceful process shutdown.
- Signals can be specified numerically (`-9`) or symbolically (`-KILL`, `--signal SIGTERM`).

---

## 3. Options

### 3.1 Primary Flags

| Flag | Description | Default | Upstream Note |
|:---|:---|:---|:---|
| `-SIGNAL` | Signal to send (e.g. `-9`, `-HUP`, `-INT`). | `SIGTERM` (15) | Graceful termination |
| `-x` | Exact match: require pattern to match the entire name. | Substring | **Critical safety flag** |
| `-f` | Match pattern against full command line arguments. | Basename | Required for scripts |
| `-u user` | Target only processes owned by effective user ID or name. | All users | User scoping |
| `-U user` | Target only processes owned by real user ID or name. | All users | User scoping |
| `-e` | Display what process was killed (echo mode). | Silent | Auditability |
| `-c` | Suppress normal signal dispatch; display count of matched processes. | Signal dispatch | Dry-run safety |

---

## 4. Basic Usage

### 4.1 Graceful Process Termination

```bash
pkill -x nginx
```
- Sends `SIGTERM` to all processes named exactly `nginx`.

### 4.2 Reloading Service Configuration via SIGHUP

```bash
pkill -HUP -x rsyslogd
```

---

## 5. Practical Operations

### 5.1 Safe Termination with Echo Mode (`-e`)

Visualizing which processes were signaled:

```bash
pkill -e -x php-fpm
```
```text
php-fpm killed (pid 4512)
php-fpm killed (pid 4513)
php-fpm killed (pid 4514)
```

### 5.2 Forcefully Terminating Frozen Processes (`SIGKILL`)

If an application is unresponsive to `SIGTERM`:

```bash
pkill -9 -x worker_process
```
- **Technical Analysis**: `SIGKILL` (9) is handled directly by the kernel and cannot be caught, ignored, or blocked by the target process.

### 5.3 Terminating All Processes of a Specific User

Logging off a rogue or terminated user completely:

```bash
sudo pkill -u baduser
```
- Transmits `SIGTERM` to every process owned by `baduser`.

---

## 6. Advanced Usage

### 6.1 Safe Two-Stage Dry-Run Pattern

Because `pkill` without `-x` matches substrings, accidentally killing critical services is a serious risk (e.g. `pkill sh` matching `sshd` and killing remote administration).

**The Safe Two-Stage Pattern**:
1. Run `pgrep` with identical flags first to inspect matching processes:
   ```bash
   pgrep -la "worker.py"
   ```
2. Once the target list is verified, execute `pkill` with the identical pattern:
   ```bash
   pkill -f "worker.py"
   ```

---

## 7. Exit Status, Environment, and Configuration

### 7.1 Exit Status Codes

| Exit Code | Meaning |
|:---:|:---|
| `0` | One or more processes were matched and signaled. |
| `1` | No processes were matched. |
| `2` | Syntax error in options. |
| `3` | Fatal error occurred. |

---

## 8. Safety, Security, and Portability

### 8.1 Privilege Requirements

- An unprivileged user can only send signals to processes they own.
- Sending signals to processes owned by other users or system daemons requires root (`CAP_KILL`).
- Processes in the `D` state (uninterruptible sleep waiting for hardware I/O) cannot be killed, even by `pkill -9`.

---

## 9. Best Practices

1. **Always Use `-x` for Binary Names**:
   - *Guidance*: Write `pkill -x <binary>` instead of `pkill <binary>`.
   - *Authoritative Justification*: Prevents catastrophic substring matches (e.g. `pkill sh` terminating `sshd`).
2. **Never Default to `SIGKILL` (`-9`)**:
   - *Guidance*: Always attempt `SIGTERM` (default) first before resorting to `SIGKILL`.
   - *Authoritative Justification*: `SIGKILL` prevents applications from flushing database buffers, closing network sockets, or unlinking lock files.
3. **Verify with `pgrep` Before Executing `pkill`**:
   - *Guidance*: Run `pgrep -a` before running `pkill -f`.
   - *Authoritative Justification*: Discloses the exact process candidates before signal transmission.

---

## References

1. **procps-ng pkill(1) Manual**: [https://man7.org/linux/man-pages/man1/pkill.1.html](https://man7.org/linux/man-pages/man1/pkill.1.html)
2. **Linux signal(7) Overview**: [https://man7.org/linux/man-pages/man7/signal.7.html](https://man7.org/linux/man-pages/man7/signal.7.html)
