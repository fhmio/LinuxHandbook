---
title: "Linux Command Tutorial: killall"
date: 2026-09-14T00:00:00+00:00
categories: ['Technology']
tags:
  - 'Linux'
  - 'psmisc'
  - 'killall'
  - 'Linux Command Tutorial'
draft: false
slug: "linux-killall-tutorial"
description: "Authoritative reference tutorial for killall, detailing process termination by name, exact matching, user filtering, and critical portability warnings against UNIX System V."
upstream_suite: "psmisc"
upstream_version: "psmisc 23.6"
posix_standard: "None"
research_date: "2026-09-14"
---

The **Linux Command Tutorial** series provides rigorous, upstream-verified references for essential system commands across Linux distributions and UNIX-like environments. Each article focuses on a single executable, combining exhaustive option documentation, verified real-world examples, security boundaries, and best practices directly derived from official source documentation and POSIX standards.

---

## 1. Introduction

> **Upstream**: psmisc | **POSIX**: None | **Safety Tier**: privileged-system-destructive | **Scope**: process-management

`killall` sends a signal to all processes running any of the specified commands. Unlike `kill`, which requires Process IDs (PIDs), `killall` matches processes by their executable name.

- **Upstream Project & Provenance**: Provided by the `psmisc` package, which also includes `fuser` and `pstree`.
- **Portability & Standards Baseline**: Not defined in POSIX. 
- **Target Research Implementation**: Audited against **psmisc 23.6**.
- **Applicability & Lifecycle**: Extremely common on Linux systems for batch termination of related processes (e.g., all PHP-FPM workers). However, it is heavily dependent on the Linux `/proc` filesystem naming conventions.

---

## 2. Syntax and Command Model

### 2.1 Canonical Synopsis

```bash
killall [options] [-s signal] name...
```

### 2.2 Execution Model & Adjacency Requirement

- `killall` parses the `/proc` filesystem to match the specified string against the `comm` (command name) field of running processes.
- By default, it sends `SIGTERM` (15) to all matched processes.
- If multiple names are specified, it sends signals to processes matching *any* of the names.
- Like `kill`, an unprivileged user can only target their own processes. Superuser (`root`) privileges are required to kill processes owned by others.

---

## 3. Options

### 3.1 Primary Flags

| Short Flag | Long Flag | Description | POSIX Defined |
|:---|:---|:---|:---:|
| `-s` | `--signal SIGNAL` | Specify the signal to send. May be a name (e.g., `KILL`) or a number (e.g., `9`). | No |
| `-u` | `--user USER` | Kill only processes the specified user owns. | No |
| `-I` | `--ignore-case` | Do case-insensitive process name matching. | No |
| `-e` | `--exact` | Require an exact match for very long names (over 15 characters). | No |
| `-q` | `--quiet` | Do not complain if no processes were killed. | No |
| `-v` | `--verbose` | Report if the signal was successfully sent. | No |
| `-w` | `--wait` | Wait for all killed processes to die before exiting. | No |

---

## 4. Basic Usage

### 4.1 Quick-Reference Cheatsheet Card

| Operation | Command | Notes |
|:---|:---|:---|
| Gracefully kill all instances | `killall nginx` | Sends `SIGTERM` to all `nginx` processes. |
| Forcibly kill all instances | `killall -9 nginx` | Sends `SIGKILL`. Process cannot ignore this. |
| Reload config for instances | `killall -HUP nginx` | Sends `SIGHUP`. Reloads Nginx configuration. |
| Kill instances by user | `killall -u alice python`| Kills only `python` processes owned by Alice. |
| Wait for termination | `killall -w firefox` | Blocks until all `firefox` processes have exited. |

### 4.2 Gracefully Terminating a Process by Name

When a browser or application hangs and spans multiple child processes, terminating them individually by PID is tedious:

```console
$ killall firefox
```

### 4.3 Verifying What Was Killed (`-v`)

To see exactly which PIDs received the signal:

```console
$ killall -v ssh-agent
Killed ssh-agent(32104) with signal 15
Killed ssh-agent(32115) with signal 15
```

---

## 5. Practical Operations

### 5.1 Waiting for Processes to Die (`-w`)

When writing restart scripts, simply running `killall` followed immediately by the startup command might fail if the ports haven't been released yet. The `-w` (wait) flag forces `killall` to poll the `/proc` filesystem and block until all signaled processes have entirely vanished:

```console
# Restarts a daemon reliably
$ sudo killall -w -TERM my_daemon
$ sudo /usr/local/bin/my_daemon
```

### 5.2 Filtering by User Context (`-u`)

If multiple users are running the same utility (e.g., `tmux` or `python`) and you only want to clear out one user's instances:

```console
$ sudo killall -u charlie tmux
```
*(This prevents accidentally destroying other users' active sessions.)*

---

## 6. Advanced Usage

### 6.1 The 15-Character Truncation Limit (`-e`)

Linux traditionally limits the `comm` (command name) field in the kernel to 15 characters. If a process name exceeds 15 characters, `killall` normally matches against the truncated 15-character string.

If you specify `-e` (exact), `killall` bypasses the `comm` field restriction by aggressively reading the `/proc/PID/cmdline` file.

```console
# Without -e, this might match 'my_very_long_pr' which could be a different binary!
$ killall -e my_very_long_process_name
```

---

## 7. Exit Status, Environment, and Configuration

### 7.1 Exit Status Codes

| Exit Code | Meaning |
|:---:|:---|
| `0` | Success (At least one process matched and was successfully signaled). |
| `1` | No processes were matched or signaled. |
| `127` | Command not found (if `psmisc` is not installed). |

### 7.2 Configuration Files

`killall` does not rely on any external configuration files.

---

## 8. Safety, Security, and Portability

### 8.1 The Solaris System V Hazard

> [!CAUTION]
> **CRITICAL PORTABILITY WARNING**: On Linux, `killall process_name` kills specific processes. On pure UNIX System V environments (such as Oracle Solaris and older IBM AIX), `killall` takes no arguments and **kills every process on the system** except for the user's shell, initiating a system shutdown sequence. Never run `killall` in cross-platform scripts without verifying the OS environment. Use `pkill` instead for cross-platform process name matching.

### 8.2 The Risk of Unintended Matches

`killall python` will terminate every Python script running under your user context, regardless of what the script is actually doing. If you need to target a specific script (e.g., `python worker.py`), `killall` will fail because it only matches the executable name (`python`). In such cases, use `pkill -f "worker.py"` instead.

---

## 9. Best Practices

1. **Use `pkill` in Scripts Over `killall`**:
   - *Guidance*: Because of the catastrophic System V behavior, `pkill` (from `procps-ng`) is considered standard and much safer for cross-platform automation.
2. **Always Use `-w` When Restarting Services**:
   - *Guidance*: Ensure ports and locks are released before launching the replacement process.
3. **Use the `-u` Flag When Running as Root**:
   - *Guidance*: If you must use `killall` as root, explicitly bound it to the user context (`killall -u www-data php-fpm`) to prevent accidental collateral damage across other tenants.

---

## References

1. **psmisc killall Manual Page**: `man 1 killall`
2. **Solaris System V killall Warning**: [Wikipedia - killall](https://en.wikipedia.org/wiki/Killall)
