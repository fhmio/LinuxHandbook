---
title: "Linux Command Tutorial: mkdir"
date: 2026-09-12T00:00:00+00:00
categories: ['Technology']
tags:
  - 'Linux'
  - 'GNU Coreutils'
  - 'mkdir'
  - 'Linux Command Tutorial'
draft: false
slug: "linux-mkdir-tutorial"
description: "Authoritative reference tutorial for mkdir (GNU Coreutils), detailing directory creation, parent path synthesis (-p), permission modes, and POSIX portability."
upstream_suite: "gnu-coreutils"
upstream_version: "GNU Coreutils 9.11"
posix_standard: "POSIX.1-2024"
research_date: "2026-09-12"
---

The **Linux Command Tutorial** series provides rigorous, upstream-verified references for essential system commands across Linux distributions and UNIX-like environments. Each article focuses on a single executable, combining exhaustive option documentation, verified real-world examples, security boundaries, and best practices directly derived from official source documentation and POSIX standards.

---

## 1. Introduction

> **Upstream**: `GNU Coreutils 9.11` | **POSIX**: `POSIX.1-2024 (with GNU extensions)` | **Safety Tier**: `unprivileged-filesystem-write` | **Scope**: `Directory allocation, parent path synthesis (-p) & permission initialization`

`mkdir` creates directories on the filesystem. It invokes the `mkdirat(2)` system call, allocating directory inodes and initializing the default `.` (current directory) and `..` (parent directory) entries.

- **Upstream Project & Provenance**: Distributed in **GNU Coreutils** (`coreutils`).
- **Portability & Standards Baseline**: Standardized in **IEEE Std 1003.1-2024 (POSIX.1-2024)**. GNU `mkdir` extends POSIX with verbose diagnostics (`-v`) and SELinux security context creation flags (`-Z`).
- **Target Research Implementation**: Audited against **GNU Coreutils 9.11** (`mkdir(1)`).
- **Applicability & Lifecycle**: The standard command for creating new directory paths.

---

## 2. Syntax and Command Model

### 2.1 Canonical Synopsis

```bash
mkdir [OPTION]... DIRECTORY...
```

### 2.2 Execution Model & Umask Interactions

- When a directory is created, its default permissions are set to `0777` (read, write, execute for owner, group, and others) modified by the active process `umask` (e.g., `0777 & ~0022 = 0755`).
- Passing `-m` explicitly sets the octal or symbolic mode bits, overriding the default `umask` calculation for created leaf directories.

---

## 3. Options

### 3.1 Primary Flags

| Short Flag | Long Flag | Description | POSIX Defined |
|:---|:---|:---|:---:|
| `-p` | `--parents` | No error if existing; make parent directories as needed. | Yes |
| `-m` | `--mode=MODE` | Set file mode (as in `chmod`), not `a=rwx - umask`. | Yes |
| `-v` | `--verbose` | Print a message for each created directory. | No |
| `-Z` | N/A | Set SELinux security context to default type. | No |

---

## 4. Basic Usage

### 4.1 Quick Reference & Common Invocations

| Task / Scenario | Command | Key Flags / Behavior |
|:---|:---|:---|
| Create single directory | `mkdir projects` | Creates new directory under current path |
| Create nested path (parents) | `mkdir -p /opt/app/logs` | `-p` synthesizes intermediate parent directories |
| Idempotent creation (no error if exists) | `mkdir -p /var/run/app` | Returns `0` whether path exists or not |
| Create with explicit mode | `mkdir -m 0700 private_keys` | `-m` sets permission bits directly, bypassing umask |
| Verbose creation logging | `mkdir -v -p build/{src,bin}` | `-v` prints each newly allocated path |
| Brace expansion multiple directories | `mkdir -p app/{config,data,logs}` | Generates sibling directories in one command |

### 4.2 Creating a Directory

```bash
mkdir projects
```

### 4.3 Creating Nested Directory Trees

```bash
mkdir -p /opt/myapp/data/logs
```

- Creates `/opt/myapp`, `/opt/myapp/data`, and `/opt/myapp/data/logs` in a single command, returning success (`0`) even if `/opt/myapp` already existed.

---

## 5. Practical Operations

### 5.1 Creating Directories with Restrictive Permissions

Creating a private directory for SSL certificates accessible only by root:

```bash
mkdir -m 0700 -p /etc/ssl/private_keys
```

- **Technical Analysis**: Directly creates the directory with `rwx------` (`0700`) mode, eliminating the race condition of creating a world-readable directory and subsequent `chmod`.

### 5.2 Verbose Directory Creation for Build Scripts

```bash
mkdir -v -p build/{src,obj,bin}
```

*Sample terminal output:*

```console
mkdir: created directory 'build'
mkdir: created directory 'build/src'
mkdir: created directory 'build/obj'
mkdir: created directory 'build/bin'
```

---

## 6. Advanced Usage

### 6.1 Idempotent Directory Initialization in CI/CD

In automated deployment scripts, running `mkdir dir` fails with `File exists` if the directory is already present. Using `-p` guarantees idempotency:

```bash
mkdir -p /var/run/app
```

- Returns exit code `0` whether `/var/run/app` is newly created or previously existed.

---

## 7. Exit Status, Environment, and Configuration

### 7.1 Exit Status Codes

| Exit Code | Meaning |
|:---:|:---|
| `0` | Success: all specified directories created or already exist with `-p`. |
| `>0` | An error occurred (parent path missing without `-p`, permission denied, read-only filesystem). |

---

## 8. Safety, Security, and Portability

### 8.1 Mode Application Nuance with `-p`

> [!WARNING]
> **Intermediate Directory Permission Nuance**: When running `mkdir -m <mode> -p path/to/dir`, the explicit `-m` mode applies **only** to the final leaf directory (`dir`).
>
> Intermediate parent directories (`path/` and `path/to/`) are created with the process default `umask` permissions modified by `u+wx`. If parent paths must also be restricted, create each directory level explicitly.

### 8.2 Existing File Conflicts

> [!NOTE]
> If any component of the requested path already exists as a regular file, symlink to a non-directory, or socket, `mkdir` (even with `-p`) aborts with `Not a directory` or `File exists`.

---

## 9. Best Practices

1. **Always Use `-p` in Shell Scripts and CI Pipelines**:
   > [!TIP]
   > *Guidance*: Default all script directory setups to `mkdir -p`.
   > *Authoritative Justification*: GNU and POSIX documentation confirm that `-p` treats existing directories as non-errors, guaranteeing idempotent execution.

2. **Use `-m` to Avoid Permission Race Conditions**:
   > [!IMPORTANT]
   > *Guidance*: Create sensitive directories using `mkdir -m 0700`.
   > *Authoritative Justification*: Eliminates the security window where a newly created directory is temporarily readable by other users before a separate `chmod` executes.

---

## References

1. **GNU Coreutils mkdir Manual**: [https://www.gnu.org/software/coreutils/manual/html_node/mkdir-invocation.html](https://www.gnu.org/software/coreutils/manual/html_node/mkdir-invocation.html)
2. **POSIX.1-2024 mkdir Specification**: The Open Group Base Specifications Issue 8. [https://pubs.opengroup.org/onlinepubs/9799919799/utilities/mkdir.html](https://pubs.opengroup.org/onlinepubs/9799919799/utilities/mkdir.html)
