---
title: "Linux Command Tutorial: touch"
date: 2026-09-12T00:00:00+00:00
categories: ['Technology']
tags:
  - 'Linux'
  - 'GNU Coreutils'
  - 'touch'
  - 'Linux Command Tutorial'
draft: false
slug: "linux-touch-tutorial"
description: "Authoritative reference tutorial for touch (GNU Coreutils), detailing file creation, timestamp modification (atime, mtime), reference file syncing, and POSIX portability."
upstream_suite: "gnu-coreutils"
upstream_version: "GNU Coreutils 9.11"
posix_standard: "POSIX.1-2024"
research_date: "2026-09-12"
---

The **Linux Command Tutorial** series provides rigorous, upstream-verified references for essential system commands across Linux distributions and UNIX-like environments. Each article focuses on a single executable, combining exhaustive option documentation, verified real-world examples, security boundaries, and best practices directly derived from official source documentation and POSIX standards.

---

## 1. Introduction

> **Upstream**: `GNU Coreutils 9.11` | **POSIX**: `POSIX.1-2024 (with GNU extensions)` | **Safety Tier**: `unprivileged-filesystem-write` | **Scope**: `Zero-byte file creation & inode timestamp updates (atime/mtime)`

`touch` modifies file timestamps (access time `atime` and modification time `mtime`) or creates empty files when specified targets do not exist. It invokes the `utimensat(2)` system call, enabling timestamp updates with nanosecond precision.

- **Upstream Project & Provenance**: Distributed in **GNU Coreutils** (`coreutils`).
- **Portability & Standards Baseline**: Standardized in **IEEE Std 1003.1-2024 (POSIX.1-2024)**.
- **Target Research Implementation**: Audited against **GNU Coreutils 9.11** (`touch(1)`).
- **Applicability & Lifecycle**: The standard utility for updating build timestamps, forcing Make rebuilds, and provisioning zero-byte sentinel files.

---

## 2. Syntax and Command Model

### 2.1 Canonical Synopsis

```bash
touch [OPTION]... FILE...
```

### 2.2 Execution Model & Inode Timestamps

- In UNIX filesystems, an inode stores three primary timestamps:
  1. `atime`: Last access (read) time.
  2. `mtime`: Last modification (data content change) time.
  3. `ctime`: Last inode metadata status change time.
- `touch` can explicitly set `atime` and `mtime`.
- `ctime` is updated automatically by the kernel to the current system time whenever `atime` or `mtime` is modified; `ctime` cannot be set arbitrarily by users.

---

## 3. Options

### 3.1 Primary Operational Flags

| Short Flag | Long Flag | Description | POSIX Defined |
|:---|:---|:---|:---:|
| `-a` | N/A | Change only the access time (`atime`). | Yes |
| `-m` | N/A | Change only the modification time (`mtime`). | Yes |
| `-c` | `--no-create` | Do not create any files that do not already exist. | Yes |
| `-d` | `--date=STRING` | Parse date string and use it instead of current time. | No |
| `-t` | N/A | Use [[CC]YY]MMDDhhmm[.ss] instead of current time. | Yes |
| `-r` | `--reference=FILE` | Use this reference file's timestamps instead of current time. | Yes |
| `-h` | `--no-dereference` | Affect each symbolic link itself rather than the target. | Yes |

---

## 4. Basic Usage

### 4.1 Quick Reference & Common Invocations

| Task / Scenario | Command | Key Flags / Behavior |
|:---|:---|:---|
| Create empty file / update to now | `touch file.txt` | Creates file if missing or updates atime & mtime |
| Update timestamp without creating | `touch -c file.txt` | `-c` prevents creating file if it does not exist |
| Update modification time only | `touch -m file.txt` | `-m` updates mtime only, leaving atime intact |
| Update access time only | `touch -a file.txt` | `-a` updates atime only |
| Set explicit date/time string | `touch -d "2026-01-01 12:00:00" file.txt` | `-d` parses human date strings |
| Sync timestamps from reference | `touch -r source.bin target.bin` | `-r` copies timestamps from reference file |
| Update symlink itself | `touch -h -m symlink` | `-h` affects symlink instead of dereferencing |

### 4.2 Creating an Empty File

```bash
touch newfile.txt
```

### 4.3 Updating Timestamp to Current Time Without Modification

```bash
touch existing_file.txt
```

---

## 5. Practical Operations

### 5.1 Updating Only Existing Files (Preventing Unintended Creations)

In deployment scripts that touch lockfiles or cache markers:

```bash
touch -c /var/run/app.lock
```

- If `/var/run/app.lock` exists, its timestamps update to now. If missing, `touch` silently does nothing and avoids creating an unwanted file.

### 5.2 Synchronizing Timestamps with a Reference File

Setting a file's timestamps to match an authoritative release binary:

```bash
touch -r /opt/app/bin/server /opt/app/etc/server.conf
```

- Both `atime` and `mtime` of `server.conf` now match `server`.

### 5.3 Setting an Explicit Timestamp for Testing

Simulating an old log file for logrotate testing:

```bash
touch -d "2026-01-01 12:00:00" old_audit.log
```

Verifying with `stat`:

```bash
stat -c "%y" old_audit.log
```

*Sample terminal output:*

```text
2026-01-01 12:00:00.000000000 +0000
```

---

## 6. Advanced Usage

### 6.1 Touching Symbolic Links Directly

By default, `touch` dereferences symlinks and updates the target file. To update the timestamp of the symlink itself:

```bash
touch -h -m current_symlink
```

- Modifies the symlink's own modification timestamp without touching the target.

---

## 7. Exit Status, Environment, and Configuration

### 7.1 Exit Status Codes

| Exit Code | Meaning |
|:---:|:---|
| `0` | Success: all specified file timestamps modified/created. |
| `>0` | An error occurred (permission denied, invalid date string, read-only filesystem). |

---

## 8. Safety, Security, and Portability

### 8.1 Permission Requirements

> [!IMPORTANT]
> **Privilege Boundary for Arbitrary Timestamps**: Setting file timestamps to the **current time** requires write permission on the target file.
>
> However, setting timestamps to an **arbitrary past or future time** (via `-d` or `-t`) requires that the calling process either **owns the file** or holds root privileges (`CAP_FOWNER`).

### 8.2 Inode Metadata ctime Invariance

> [!NOTE]
> `ctime` (status change time) cannot be directly set by users or utilities. The Linux kernel automatically updates `ctime` to the current system clock whenever `atime` or `mtime` is modified.

---

## 9. Best Practices

1. **Use `-c` in Automation to Prevent Spurious File Creation**:
   > [!TIP]
   > *Guidance*: Add `-c` when updating timestamps on state files or triggering watchdog touch operations.
   > *Authoritative Justification*: GNU and POSIX documentation confirm `-c` guarantees no empty file is created if the target path is absent.

2. **Use `-r` for Reproducible Artifact Builds**:
   > [!TIP]
   > *Guidance*: Set build output timestamps to match the source commit using `touch -r`.
   > *Authoritative Justification*: Ensures deterministic build outputs across CI/CD pipelines.

---

## References

1. **GNU Coreutils touch Manual**: [https://www.gnu.org/software/coreutils/manual/html_node/touch-invocation.html](https://www.gnu.org/software/coreutils/manual/html_node/touch-invocation.html)
2. **POSIX.1-2024 touch Specification**: The Open Group Base Specifications Issue 8. [https://pubs.opengroup.org/onlinepubs/9799919799/utilities/touch.html](https://pubs.opengroup.org/onlinepubs/9799919799/utilities/touch.html)
