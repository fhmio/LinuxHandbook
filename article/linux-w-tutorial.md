---
title: "Linux Command Tutorial: w"
date: 2026-09-12T00:00:00+00:00
categories: ['Technology']
tags:
  - 'Linux'
  - 'procps-ng'
  - 'w'
  - 'Linux Command Tutorial'
draft: false
slug: "linux-w-tutorial"
description: "Authoritative reference tutorial for w (procps-ng), detailing logged-in user tracking, utmp accounting, idle time, process execution, and security monitoring."
upstream_suite: "procps-ng"
upstream_version: "procps-ng 4.0.4"
posix_standard: "None"
research_date: "2026-09-12"
---

The **Linux Command Tutorial** series provides rigorous, upstream-verified references for essential system commands across Linux distributions and UNIX-like environments. Each article focuses on a single executable, combining exhaustive option documentation, verified real-world examples, security boundaries, and best practices directly derived from official source documentation and POSIX standards.

---

## 1. Introduction

> **Upstream**: procps-ng 4.0.4 | **POSIX**: De-facto Standard (Not POSIX standardized) | **Safety Tier**: safe-read-only | **Scope**: user-session-inspection

`w` displays information about the users currently logged in to the system, paired with the commands each user is running. The header displays the current system time, uptime, count of active users, and system load averages over the last 1, 5, and 15 minutes.

- **Upstream Project & Provenance**: Maintained within **procps-ng** (`procps-ng`).
- **Portability & Standards Baseline**: `w` is an industry-standard UNIX administrative tool; not defined in POSIX.1-2024.
- **Target Research Implementation**: Audited against **procps-ng 4.0.4** (`w(1)`).
- **Applicability & Lifecycle**: The standard command for administrative auditing of active logins, interactive sessions, and current user activity.

---

## 2. Syntax and Command Model

### 2.1 Canonical Synopsis

```bash
w [options] [user]
```

### 2.2 Execution Model & System Sources

- **User Accounting**: `w` reads the system login accounting file (traditionally `/var/run/utmp` or `/run/utmp`).
- **Process Activity**: It cross-references active terminal devices (`TTY`) with `/proc` to determine the foreground process group running on each terminal.

---

## 3. Options

### 3.1 Primary Flags

| Flag | Long Flag | Description | Default |
|:---|:---|:---|:---|
| `-h` | `--no-header` | Do not print the system summary header line. | Header printed |
| `-u` | N/A | Ignore username when calculating process and CPU times. | Standard |
| `-s` | `--short` | Short format: omit login time, JCPU, and PCPU times. | Full format |
| `-f` | `--from` | Toggle printing the remote hostname or IP in the FROM field. | Enabled |
| `-i` | `--ip-addr` | Display IP addresses instead of hostnames in the FROM field. | Hostnames |
| `-o` | `--old-style` | Old style output for idle times under a minute (prints blank). | Standard |

---

## 4. Basic Usage

### 4.1 Quick-Reference Cheatsheet Card

| Operation | Command | Notes |
|:---|:---|:---|
| Show logged-in users | `w` | Displays user sessions, idle time, and current command |
| Filter by specific user | `w deploy` | Restricts session report to username |
| Numeric IP addresses | `w -i` | Shows IP addresses without reverse DNS delays |
| Short format | `w -s` | Omits login time, JCPU, and PCPU columns |
| Suppress summary header | `w -h` | Outputs pure session table for parsing |
| Scriptable user list | `w -h \| awk '{print $1, $3}'` | Extracts user and source IP/host |

### 4.2 Standard Full Output

```bash
w
```
```console
 11:40:12 up 14 days,  4:07,  2 users,  load average: 0.12, 0.18, 0.14
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
admin    pts/0    192.168.1.45     10:15    1.00s  0.15s  0.02s w
deploy   pts/1    bastion.corp     09:30   42:10   1.20s  0.45s python3 worker.py
```

### 4.3 Filtering by Specific User

```bash
w deploy
```

---

## 5. Practical Operations

### 5.1 Resolving Connecting IP Addresses Strictly via `-i`

Disabling reverse DNS lookups to avoid delays when auditing remote connections:

```bash
w -i
```
```console
 11:42:00 up 14 days,  4:09,  1 user,  load average: 0.05, 0.10, 0.08
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
admin    pts/0    192.168.1.45     10:15    0.00s  0.12s  0.01s w -i
```

### 5.2 Parsing Without Header for Automation

```bash
w -h | awk '{print $1, $2, $3}'
```
```text
admin pts/0 192.168.1.45
```

---

## 6. Advanced Usage

### 6.1 Understanding JCPU and PCPU Metrics

- `JCPU`: The total time used by all processes attached to the terminal since the session began. It includes background and completed jobs.
- `PCPU`: The CPU time used by the current foreground process running on the terminal (the command shown under the `WHAT` field).

---

## 7. Exit Status, Environment, and Configuration

### 7.1 Exit Status Codes

| Exit Code | Meaning |
|:---:|:---|
| `0` | Clean execution. |
| `>0` | Error (unreadable utmp file or invalid command-line flag). |

### 7.2 Environment Variables

- `PROCPS_USERLEN`: Overrides the default username column display width (default 8 characters).
- `PROCPS_FROMLEN`: Overrides the default hostname/IP column display width (default 16 characters).

---

## 8. Safety, Security, and Portability

### 8.1 Spoofed `WHAT` Display

> [!WARNING]
> The `WHAT` column displays the foreground process as reported in `/proc/[pid]/cmdline`. Unprivileged processes can rewrite their own process title via `prctl(PR_SET_NAME)` or by altering `argv[0]`. Never treat the `WHAT` column as tamper-proof forensic evidence during security investigations; verify via kernel audit logs (`auditd`).

---

## 9. Best Practices

1. **Use `-i` for Immediate Execution on Slow Networks**:
   - *Guidance*: Pass `w -i` on servers where reverse DNS lookups are slow or unconfigured.
   - *Authoritative Justification*: Prevents DNS timeouts from blocking terminal output.
2. **Export `PROCPS_USERLEN=16` on Modern Systems**:
   - *Guidance*: Expand username display width in environments with long usernames.
   - *Authoritative Justification*: Prevents truncation of usernames exceeding 8 characters.

---

## References

1. **procps-ng w(1) Manual**: [https://man7.org/linux/man-pages/man1/w.1.html](https://man7.org/linux/man-pages/man1/w.1.html)
2. **Linux utmp(5) Documentation**: [https://man7.org/linux/man-pages/man5/utmp.5.html](https://man7.org/linux/man-pages/man5/utmp.5.html)
