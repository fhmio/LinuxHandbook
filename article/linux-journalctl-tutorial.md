---
title: "Linux Command Tutorial: journalctl"
date: 2026-09-12T00:00:00+00:00
categories: ['Technology']
tags:
  - 'Linux'
  - 'systemd'
  - 'journalctl'
  - 'Linux Command Tutorial'
draft: false
slug: "linux-journalctl-tutorial"
description: "Authoritative reference tutorial for journalctl (systemd), detailing systemd-journald log querying, boot filtering, service-specific output, real-time log following, and structured JSON export."
upstream_suite: "systemd"
upstream_version: "systemd 256"
posix_standard: "None"
research_date: "2026-09-12"
---

The **Linux Command Tutorial** series provides rigorous, upstream-verified references for essential system commands across Linux distributions and UNIX-like environments. Each article focuses on a single executable, combining exhaustive option documentation, verified real-world examples, security boundaries, and best practices directly derived from official source documentation and POSIX standards.

---

## 1. Introduction

> **Upstream**: systemd (systemd 256) | **POSIX**: Linux-Specific (systemd extension) | **Safety Tier**: safe-read-only | **Scope**: systemd-journal-logging

`journalctl` is the command-line interface for querying and analyzing logs captured by the `systemd-journald` service. It indexes structured binary journal files containing kernel ring buffer messages, system daemon output, stdout/stderr streams from service units, audit events, and syslog entries.

- **Upstream Project & Provenance**: Maintained within **systemd** (`systemd`) as the dedicated client for `systemd-journald`.
- **Portability & Standards Baseline**: Linux-specific logging tool; not standardized in IEEE Std 1003.1-2024 (POSIX.1-2024). It modernizes and consolidates traditional text-based syslog daemons (`rsyslog`, `syslog-ng`).
- **Target Research Implementation**: Audited against **systemd 256** (`journalctl(1)`).
- **Applicability & Lifecycle**: The standard logging inspection tool across all modern systemd-based Linux systems.

---

## 2. Syntax and Command Model

### 2.1 Canonical Synopsis

```bash
journalctl [OPTIONS...] [MATCHES...]
```

### 2.2 Indexed Binary Journal Architecture

Traditional syslog daemons store messages as unindexed plain text in `/var/log/syslog` or `/var/log/messages`. Parsing multi-gigabyte plain text logs requires linear `grep` operations and discards structured metadata.

`systemd-journald` stores logs in indexed binary journal files (`.journal`):
- **Structured Fields**: Every record is an object with explicit key-value fields (e.g. `_PID=789`, `_SYSTEMD_UNIT=sshd.service`, `PRIORITY=6`, `_BOOT_ID=...`).
- **B-Tree Indexing**: Indexed by time, boot ID, unit name, and process metadata, enabling instantaneous time-range queries without sequential file scanning.
- **Cryptographic Sealing**: Supports Forward Secure Sealing (FSS) using Forward Secure Signatures to detect tamper attempts on log files.

---

## 3. Options

### 3.1 Filtering Options

| Option | Long Option | Description | Default |
|:---|:---|:---|:---|
| `-b [ID]` | `--boot[=ID]` | Show messages from specified boot (e.g. `0` for current, `-1` for previous). | Current boot |
| `--list-boots` | `--list-boots` | List all recorded boot IDs, numbers, and timestamp spans. | Query logs |
| `-u UNIT` | `--unit=UNIT` | Filter logs by system unit name (e.g. `-u nginx.service`). | All units |
| `--user-unit=UNIT` | `--user-unit=UNIT` | Filter logs by user session unit name. | All units |
| `-p PRIO` | `--priority=PRIO` | Filter by log severity level (`emerg`, `alert`, `crit`, `err`, `warning`, `notice`, `info`, `debug`). | All levels |
| `-k` | `--dmesg` | Filter strictly to kernel ring buffer messages (equivalent to `dmesg`). | All messages |
| `-S TIME` | `--since=TIME` | Show entries on or newer than specified timestamp or relative expression. | Unbounded |
| `-U TIME` | `--until=TIME` | Show entries on or older than specified timestamp or relative expression. | Unbounded |

### 3.2 Display and Output Formatting

| Option | Long Option | Description | Default |
|:---|:---|:---|:---|
| `-f` | `--follow` | Stream new log messages in real time (equivalent to `tail -f`). | Terminate at end |
| `-n [N]` | `--lines[=N]` | Show most recent `N` entries (default 10 when `-f` is active). | All matching |
| `-r` | `--reverse` | Display log entries in reverse chronological order (newest first). | Chronological |
| `-o FORMAT` | `--output=FORMAT` | Output format: `short`, `short-iso`, `verbose`, `export`, `json`, `json-pretty`, `cat`. | `short` |
| `-x` | `--catalog` | Augment log messages with explanatory text from the message catalog. | Concise |
| `-q` | `--quiet` | Suppress informational banner messages and page breaks. | Informational |
| `--no-pager` | `--no-pager` | Print output directly to stdout without redirecting to a pager (`less`). | Pager enabled |

### 3.3 Storage and Maintenance

| Option | Long Option | Description |
|:---|:---|:---|
| `--disk-usage` | `--disk-usage` | Print current total disk space consumed by active and archived journal files. |
| `--vacuum-size=BYTES` | `--vacuum-size=BYTES` | Remove archived journal files until total disk usage falls below specified size. |
| `--vacuum-time=TIME` | `--vacuum-time=TIME` | Remove archived journal files older than specified time window (e.g. `2weeks`, `3months`). |
| `--verify` | `--verify` | Audit journal files for cryptographic integrity and corruption. |

---

## 4. Basic Usage

### 4.1 Quick-Reference Cheatsheet Card

| Operation | Command Pattern | Copyable One-Liner | Notes |
|:---|:---|:---|:---|
| Recent system logs | `journalctl -n [N] --no-pager` | `journalctl -n 50 --no-pager` | Displays recent entries directly to stdout |
| Filter by unit | `journalctl -u [unit]` | `journalctl -u sshd.service -n 20` | Scopes logs strictly to specific daemon |
| Follow logs live | `journalctl -u [unit] -f` | `journalctl -u nginx.service -f` | Live streaming log tail |
| Errors from prior boot | `journalctl -b -1 -p err` | `journalctl -b -1 -p err` | Quickly diagnoses reasons for past reboot |
| Time window filter | `journalctl --since [time]` | `journalctl --since "30 minutes ago"` | Isolates incident timeframe |
| Kernel ring buffer | `journalctl -k -b 0` | `journalctl -k -b 0 -p warning` | Inspects dmesg warnings from current boot |
| Check disk usage | `journalctl --disk-usage` | `journalctl --disk-usage` | Shows total space consumed by journals |
| Vacuum journal archives | `journalctl --vacuum-size=[size]` | `sudo journalctl --vacuum-size=500M` | Trims older archived journals safely |

### 4.2 Viewing Recent System Logs

Display the most recent 50 system log entries without invoking a pager:

```bash
journalctl -n 50 --no-pager
```

Output:

```console
Sep 12 18:45:01 server CRON[14201]: (root) CMD (/usr/local/bin/backup-check.sh)
Sep 12 18:50:12 server systemd[1]: Starting Daily apt download activities...
Sep 12 18:50:14 server systemd[1]: apt-daily.service: Deactivated successfully.
Sep 12 18:50:14 server systemd[1]: Finished Daily apt download activities.
```

### 4.3 Inspecting Service Logs

Filter entries strictly emitted by a specific daemon:

```bash
journalctl -u sshd.service -n 20
```

Output:

```console
Sep 12 10:00:15 server systemd[1]: Starting OpenSSH server daemon...
Sep 12 10:00:15 server sshd[789]: Server listening on 0.0.0.0 port 22.
Sep 12 10:00:15 server sshd[789]: Server listening on :: port 22.
Sep 12 10:00:15 server systemd[1]: Started OpenSSH server daemon.
Sep 12 10:14:22 server sshd[1024]: Accepted publickey for admin from 192.168.1.10 port 54210 ssh2
```

### 4.4 Streaming Real-Time Service Logs

Follow active service log streams in real time as events occur:

```bash
journalctl -u nginx.service -f
```

---

## 5. Practical Operations

### 5.1 Investigating Errors from Previous Boots

When troubleshooting unexpected reboots, kernel panics, or failed services from a prior system session:

1. **List all recorded boots**:
   ```bash
   journalctl --list-boots
   ```

   Output:

   ```console
   -2 8a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d Wed 2026-09-09 08:00:12 UTC—Wed 2026-09-09 18:30:45 UTC
   -1 1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c Thu 2026-09-10 09:12:00 UTC—Fri 2026-09-11 22:45:10 UTC
    0 9f8e7d6c5b4a3f2e1d0c9b8a7f6e5d4c Sat 2026-09-12 00:00:10 UTC—Sat 2026-09-12 19:15:00 UTC
   ```

2. **Query errors (`-p err`) from the previous boot (`-b -1`)**:
   ```bash
   journalctl -b -1 -p err
   ```

   Output:

   ```console
   Sep 11 22:44:50 server kernel: Out of memory: Killed process 8492 (java) total-vm:8451200kB, anon-rss:4120150kB
   Sep 11 22:45:01 server systemd[1]: myapp.service: Main process exited, code=killed, status=9/KILL
   Sep 11 22:45:01 server systemd[1]: myapp.service: Failed with result 'oom-kill'.
   ```

### 5.2 Time-Window Incident Correlation

Isolate events during a specific outage window across all services:

```bash
journalctl --since "2026-09-12 14:00:00" --until "2026-09-12 14:30:00" --no-pager
```

Use relative time expressions for recent incident analysis:

```bash
# Display logs from the past 30 minutes
journalctl --since "30 minutes ago"

# Display logs generated today
journalctl --since "today"
```

### 5.3 Auditing Kernel Ring Buffer (`dmesg` Integration)

Query kernel hardware discovery, storage attachment, and driver warnings directly from the journal:

```bash
journalctl -k -b 0 -p warning
```

Output:

```console
Sep 12 00:00:11 server kernel: ACPI: button: System will not sleep on any button press
Sep 12 00:00:12 server kernel: nvme nvme0: 8/0/0 default/read/poll queues
Sep 12 00:00:14 server kernel: EXT4-fs (sda2): re-mounted. Opts: errors=remount-ro.
```

### 5.4 Auditing and Vacuuming Journal Disk Usage

Check total storage consumed by journal files:

```bash
journalctl --disk-usage
```

Output:

```console
Archived and active journals take up 1.2G in the file system.
```

Vacuum older archives to free up disk space while preserving recent logs:

```bash
# Retain at most 500 MB of logs
sudo journalctl --vacuum-size=500M

# Retain only logs from the last two weeks
sudo journalctl --vacuum-time=2weeks
```

---

## 6. Advanced Usage

### 6.1 Direct Field Matching via Metadata Tokens

Filter logs using low-level journal metadata fields:

```bash
# Query logs produced by root user (UID 0)
journalctl _UID=0 -n 20

# Query logs produced by a specific PID
journalctl _PID=789

# Match an exact binary path regardless of unit name
journalctl /usr/sbin/sshd
```

Combine multiple field matches (treated as logical `AND`):

```bash
# Match logs from sshd.service where priority is error or higher
journalctl _SYSTEMD_UNIT=sshd.service PRIORITY=3
```

Separate match criteria with `+` to execute logical `OR` queries:

```bash
# Match either nginx.service or php-fpm.service
journalctl _SYSTEMD_UNIT=nginx.service + _SYSTEMD_UNIT=php-fpm.service
```

### 6.2 Structured JSON Export for Log Forwarders

Export log events formatted as structured JSON for ingestion into Elasticsearch, OpenSearch, or SIEM platforms:

```bash
journalctl -u sshd.service -n 1 -o json-pretty
```

Output:

```json
{
	"_BOOT_ID" : "9f8e7d6c5b4a3f2e1d0c9b8a7f6e5d4c",
	"_CAP_EFFECTIVE" : "1ffffffffff",
	"_CMDLINE" : "/usr/sbin/sshd -D [listener] 0 of 10-100 startups",
	"_COMM" : "sshd",
	"_EXE" : "/usr/sbin/sshd",
	"_GID" : "0",
	"_HOSTNAME" : "server",
	"_MACHINE_ID" : "a1b2c3d4e5f6789012345678abcdef01",
	"_PID" : "789",
	"_SOURCE_REALTIME_TIMESTAMP" : "1789214415124000",
	"_SYSTEMD_CGROUP" : "/system.slice/sshd.service",
	"_SYSTEMD_SLICE" : "system.slice",
	"_SYSTEMD_UNIT" : "sshd.service",
	"_TRANSPORT" : "syslog",
	"_UID" : "0",
	"MESSAGE" : "Server listening on 0.0.0.0 port 22.",
	"PRIORITY" : "6",
	"SYSLOG_FACILITY" : "10",
	"SYSLOG_IDENTIFIER" : "sshd",
	"SYSLOG_PID" : "789"
}
```

### 6.3 Verifying Cryptographic Log Integrity (FSS)

On systems configured with Forward Secure Sealing, verify that journal files have not been modified or truncated after creation:

```bash
sudo journalctl --verify
```

---

## 7. Exit Status, Environment, and Configuration

### 7.1 Exit Status

| Exit Code | Meaning |
|:---|:---|
| `0` | Success: matching logs located and printed, or vacuuming completed. |
| `1` | Failure: invalid option arguments, corrupted journal file, or permission denied. |

### 7.2 Environment Variables

| Variable | Description |
|:---|:---|
| `SYSTEMD_PAGER` | Configures the pager binary (defaults to `less`). |
| `SYSTEMD_COLORS` | Controls ANSI color rendering. |

### 7.3 Storage Architecture and Files

| Location | Type | Role |
|:---|:---|:---|
| `/run/log/journal/` | Volatile (`tmpfs`) | Ephemeral logs stored in RAM; cleared upon system reboot. |
| `/var/log/journal/` | Persistent (`disk`) | Permanent indexed journal storage preserved across boots. |
| `/etc/systemd/journald.conf` | Configuration | Primary configuration file governing log retention and disk limits. |

---

## 8. Safety, Security, and Portability

### 8.1 Non-Destructive Operation

> [!NOTE]
> **Read-Only Safety**: `journalctl` is primarily a read-only inspection utility. The only mutating actions are `--vacuum-size` and `--vacuum-time`, which purge old archived logs according to retention limits without corrupting active journals.

### 8.2 Access Control and Privilege Boundaries

> [!IMPORTANT]
> Unprivileged users can only view logs generated by their own user session. Viewing system-wide service logs or kernel ring messages requires `root` privileges or membership in `systemd-journal`, `adm`, or `wheel` groups.

### 8.3 Portability Constraints

`journalctl` depends strictly on `systemd-journald`. Non-systemd systems (Alpine Linux, FreeBSD, macOS) do not support `journalctl` and rely on legacy syslog files.

---

## 9. Best Practices

### 9.1 Combine `-u` With Time Filters for Targeted Troubleshooting

> [!TIP]
> **Scope Queries by Service and Time**: Running unfiltered `journalctl` scans millions of entries. Always constrain queries using `-u <unit>` and time windows (`--since "1 hour ago"` or `-b`) for fast response times.

*Upstream Rationale*: Running `journalctl` without filters forces the utility to load millions of log entries across the entire operating system history. Always scope queries to the target service (`-u <unit>`) and time boundary (`-b` or `--since "1 hour ago"`).

### 9.2 Configure Permanent Journal Retention via `journald.conf`

*Upstream Rationale*: Relying solely on manual `journalctl --vacuum` leads to unpredictable disk growth between administrative sweeps. Configure automated bounds in `/etc/systemd/journald.conf`:
```ini
[Journal]
Storage=persistent
SystemMaxUse=2G
SystemKeepFree=5G
MaxRetentionSec=1month
```

### 9.3 Ingest Logs in JSON (`-o json`) for Monitoring Pipelines

*Upstream Rationale*: Plain text parsing of logs using regular expressions breaks whenever software updates modify log message wording. Exporting logs with `-o json` preserves native structured keys (`_SYSTEMD_UNIT`, `_PID`, `MESSAGE`) directly for automation agents.

---

## References

1. `journalctl(1)` — systemd journal querying manual: <https://www.freedesktop.org/software/systemd/man/latest/journalctl.html>
2. `systemd-journald.service(8)` — systemd journal service reference: <https://www.freedesktop.org/software/systemd/man/latest/systemd-journald.service.html>
3. `journald.conf(5)` — systemd journal configuration manual: <https://www.freedesktop.org/software/systemd/man/latest/journald.conf.html>
4. systemd GitHub Repository: <https://github.com/systemd/systemd>
