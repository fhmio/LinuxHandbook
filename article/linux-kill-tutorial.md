---
title: "Linux Command Tutorial: kill"
date: 2026-09-14T00:00:00+00:00
categories: ['Technology']
tags:
  - 'Linux'
  - 'util-linux'
  - 'kill'
  - 'Linux Command Tutorial'
draft: false
slug: "linux-kill-tutorial"
description: "Authoritative reference tutorial for kill, detailing POSIX signal transmission, process termination gracefully and forcefully, and process group management."
upstream_suite: "util-linux"
upstream_version: "util-linux 2.40"
posix_standard: "posix-standard-with-gnu-extensions"
research_date: "2026-09-14"
---

The **Linux Command Tutorial** series provides rigorous, upstream-verified references for essential system commands across Linux distributions and UNIX-like environments. Each article focuses on a single executable, combining exhaustive option documentation, verified real-world examples, security boundaries, and best practices directly derived from official source documentation and POSIX standards.

---

## 1. Introduction

> **Upstream**: util-linux | **POSIX**: POSIX.1-2024 | **Safety Tier**: privileged-system-destructive | **Scope**: process-management

`kill` sends a specific signal to a process or process group. By default, it sends the `SIGTERM` (15) signal, asking the process to gracefully terminate.

- **Upstream Project & Provenance**: The `/bin/kill` executable is traditionally provided by `util-linux` or `procps-ng`. Modern shells (bash, zsh) also provide a built-in `kill` command for job control, which takes precedence.
- **Portability & Standards Baseline**: Standardized in POSIX.1-2024. Signal naming and numbers are generally consistent across all UNIX platforms.
- **Target Research Implementation**: Audited against **util-linux 2.40** (standalone binary) and Bash 5.2 (shell built-in).
- **Applicability & Lifecycle**: The fundamental tool for inter-process communication via signals, primarily used for terminating unresponsive or background processes.

---

## 2. Syntax and Command Model

### 2.1 Canonical Synopsis

```bash
kill [-s signal | -p] [-q sigval] [-a] [--] pid...
kill -l [signal]
```

### 2.2 Execution Model & Adjacency Requirement

- `kill` accepts process IDs (PIDs) as arguments.
- It translates the human-readable signal name (e.g., `TERM`, `KILL`) into an integer signal sent directly to the kernel via the `kill(2)` system call.
- Shell built-in versions of `kill` can also accept job IDs (e.g., `%1`) rather than PIDs.
- Unprivileged users can only send signals to processes running under their own UID. Superusers (`root`) can send signals to any process.

---

## 3. Options

### 3.1 Primary Flags

| Short Flag | Long Flag | Description | POSIX Defined |
|:---|:---|:---|:---:|
| `-s` | `--signal SIGNAL` | Specify the signal to send. May be a name (e.g., `KILL`) or a number (e.g., `9`). | Yes |
| `-l` | `--list` | List all supported signal names. | Yes |
| `-L` | `--table` | List all supported signal names and their corresponding numbers. | No |
| `-p` | `--pid` | Print the process ID(s) that would be signaled, but do not actually send the signal. | No |

### 3.2 Common Standard Signals

| Signal Number | Signal Name | Description | Can be caught/ignored? |
|:---:|:---|:---|:---:|
| `1` | `SIGHUP` | Hangup. Often used to instruct a daemon to reload its configuration. | Yes |
| `2` | `SIGINT` | Interrupt. Emitted by pressing `Ctrl+C`. | Yes |
| `9` | `SIGKILL` | Kill. Forcibly terminates the process immediately. | **No** |
| `15`| `SIGTERM` | Terminate. Requests graceful shutdown. (Default). | Yes |
| `18`| `SIGCONT` | Continue. Resumes a paused process. | No |
| `19`| `SIGSTOP` | Stop. Pauses the process without terminating it. | **No** |

---

## 4. Basic Usage

### 4.1 Quick-Reference Cheatsheet Card

| Operation | Command | Notes |
|:---|:---|:---|
| Gracefully kill a process | `kill 1234` | Sends `SIGTERM` (15) to PID 1234. |
| Forcibly kill a process | `kill -9 1234` | Sends `SIGKILL` (9). Process cannot ignore this. |
| Reload daemon config | `kill -HUP 1234` | Sends `SIGHUP` (1). Common for Nginx/Apache. |
| Pause a process | `kill -STOP 1234` | Freezes PID 1234. Resumes with `SIGCONT`. |
| List available signals | `kill -l` | Prints list of signals supported by the kernel. |

### 4.2 Gracefully Terminating a Process

Identify the PID (using `ps` or `pgrep`) and issue `kill`. This asks the process to clean up resources before exiting:

```console
$ kill 4567
```

### 4.3 Listing Signals

To view the names and numbers of signals:

```console
$ /bin/kill -L
 1 HUP      2 INT      3 QUIT     4 ILL      5 TRAP     6 ABRT     7 BUS
 8 FPE      9 KILL    10 USR1    11 SEGV    12 USR2    13 PIPE    14 ALRM
15 TERM    16 STKFLT  17 CHLD    18 CONT    19 STOP    20 TSTP    21 TTIN
```

---

## 5. Practical Operations

### 5.1 The Last Resort: SIGKILL (-9)

If a process is deadlocked and ignores `SIGTERM`, you must use `SIGKILL`. The kernel removes the process directly without allowing it to clean up temporary files or network sockets.

```console
$ kill -9 8910
```

### 5.2 Reloading Configuration without Downtime

Many system daemons (like `nginx`, `sshd`, or `haproxy`) interpret `SIGHUP` (Signal 1) as a command to re-read their configuration files and reopen log files without dropping active connections.

```console
$ sudo kill -s HUP 1054
```

### 5.3 Pausing and Resuming High-CPU Processes

If a background task is consuming too much CPU and you need temporary priority for another task, you can pause it with `SIGSTOP` and resume it later with `SIGCONT`:

```console
$ kill -STOP 3345
# (Later...)
$ kill -CONT 3345
```

---

## 6. Advanced Usage

### 6.1 Killing Process Groups (Negative PIDs)

In UNIX, processes belong to a Process Group ID (PGID). If you want to kill an entire process tree (e.g., a shell script and all of its spawned child commands), you can send the signal to the negative PGID.

```console
# If the PGID is 4000, kill the entire group:
$ kill -TERM -4000
```

### 6.2 Using the Shell Built-in with Job IDs

If you run a task in the background using `&`, bash assigns it a job ID. You can kill it without knowing the PID by prefixing the job number with `%`.

```console
$ sleep 900 &
[1] 5566
$ kill %1
```

---

## 7. Exit Status, Environment, and Configuration

### 7.1 Exit Status Codes

| Exit Code | Meaning |
|:---:|:---|
| `0` | Success (At least one signal was sent successfully). |
| `1` | General error (e.g., process does not exist, permission denied). |
| `64` | Partial success (when multiple PIDs were specified, and at least one failed). |

### 7.2 Configuration Files

`kill` does not rely on any external configuration files. It interfaces directly with the kernel's signal dispatch mechanism.

---

## 8. Safety, Security, and Portability

### 8.1 The Risk of SIGKILL

> [!WARNING]
> You should almost never use `kill -9` as a first resort. `SIGKILL` destroys the process immediately. The process is not given a chance to commit database transactions, release shared memory, or delete temporary lock files. This can leave databases in inconsistent states and require manual cleanup. Always try `SIGTERM` (the default) first.

### 8.2 Built-in vs. Executable

There are subtle differences between the shell built-in `kill` and the binary `/bin/kill`. The built-in understands job control syntax (`%1`), whereas the standalone binary does not. If you are writing a script that uses `env kill` or `find -exec kill`, it will use the standalone binary and cannot process `%` arguments.

### 8.3 Uncatchable Signals

`SIGKILL` (9) and `SIGSTOP` (19) are hardcoded into the kernel as uncatchable. No application can trap, block, or ignore these signals.

---

## 9. Best Practices

1. **Follow the Escalation Path**:
   - *Guidance*: Always attempt `kill -15` (SIGTERM) first. Wait 5 seconds. If the process remains, escalate to `kill -2` (SIGINT) or `kill -1` (SIGHUP). Only if all graceful methods fail should you use `kill -9` (SIGKILL).
2. **Be Careful with PID 1**:
   - *Guidance*: PID 1 (`init` or `systemd`) generally ignores `SIGTERM` and `SIGKILL`. Do not attempt to kill PID 1 to reboot the system; use `/sbin/reboot`.
3. **Use Process Names for Targeting**:
   - *Guidance*: If you don't know the exact PID, use `pkill` or `killall` rather than parsing `ps aux | grep ...` outputs.

---

## References

1. **util-linux kill Manual Page**: `man 1 kill`
2. **Bash Builtin Manual**: `man 1 bash` (Search for "kill")
3. **POSIX Specification**: [https://pubs.opengroup.org/onlinepubs/9699919799/utilities/kill.html](https://pubs.opengroup.org/onlinepubs/9699919799/utilities/kill.html)
