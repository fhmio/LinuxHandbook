---
title: "Linux Command Tutorial: mv"
date: 2026-09-12T00:00:00+00:00
categories: ['Technology']
tags:
  - 'Linux'
  - 'GNU Coreutils'
  - 'mv'
  - 'Linux Command Tutorial'
draft: false
slug: "linux-mv-tutorial"
description: "Authoritative reference tutorial for mv (GNU Coreutils), detailing atomic renames, cross-device filesystem moves, backup policies, and POSIX portability."
upstream_suite: "gnu-coreutils"
upstream_version: "GNU Coreutils 9.11"
posix_standard: "POSIX.1-2024"
research_date: "2026-09-12"
---

The **Linux Command Tutorial** series provides rigorous, upstream-verified references for essential system commands across Linux distributions and UNIX-like environments. Each article focuses on a single executable, combining exhaustive option documentation, verified real-world examples, security boundaries, and best practices directly derived from official source documentation and POSIX standards.

---

## 1. Introduction

> **Upstream**: `GNU Coreutils 9.11` | **POSIX**: `POSIX.1-2024 (with GNU extensions)` | **Safety Tier**: `unprivileged-filesystem-write` | **Scope**: `Atomic file renaming, directory relocation & cross-device transfers`

`mv` moves or renames files and directories. When the source and destination reside on the same filesystem, `mv` performs an instantaneous, atomic directory-entry rename via the `rename(2)` system call. When moving across different filesystem boundaries, `mv` transparently copies the data and removes the original source.

- **Upstream Project & Provenance**: Distributed in **GNU Coreutils** (`coreutils`).
- **Portability & Standards Baseline**: Standardized in **IEEE Std 1003.1-2024 (POSIX.1-2024)**. GNU `mv` adds `--backup`, `--target-directory` (`-t`), `--no-target-directory` (`-T`), and granular update controls.
- **Target Research Implementation**: Audited against **GNU Coreutils 9.11** (`mv(1)`).
- **Applicability & Lifecycle**: The standard command for renaming files, relocating directory hierarchies, and atomic file replacements.

---

## 2. Syntax and Command Model

### 2.1 Canonical Synopsis

```bash
# Rename source to destination:
mv [OPTION]... [-T] SOURCE DEST

# Move multiple sources into target directory:
mv [OPTION]... SOURCE... DIRECTORY
mv [OPTION]... -t DIRECTORY SOURCE...
```

### 2.2 Execution Model: Atomic Rename vs Cross-Device Move

- **Same-Filesystem Rename**: Executed via `rename(2)`. The underlying inode number remains identical. If the destination exists, it is atomically replaced without a window where the destination is missing.
- **Cross-Filesystem Move**: When `SOURCE` and `DEST` reside on different mount points (e.g. moving from `/tmp` to `/var`), `rename(2)` fails with `EXDEV`. `mv` catches this error and automatically falls back to copying data blocks and permissions (equivalent to `cp -a`) followed by deleting the source. Cross-device moves are **not atomic**.

---

## 3. Options

### 3.1 Primary Operational Flags

| Short Flag | Long Flag | Description | POSIX Defined |
|:---|:---|:---|:---:|
| `-f` | `--force` | Do not prompt before overwriting an existing destination. | Yes |
| `-i` | `--interactive` | Prompt before overwrite. | Yes |
| `-n` | `--no-clobber` | Do not overwrite an existing file. | No |
| `-u` | `--update[=WHEN]` | Move only when source is newer than destination or destination is missing. | No |
| `-v` | `--verbose` | Explain what is being done. | No |
| `-T` | `--no-target-directory` | Treat destination as a normal file, not a directory. | No |
| `-t` | `--target-directory=DIR` | Move all source arguments into specified directory. | No |
| N/A | `--backup[=CONTROL]` | Make a backup of each existing destination file before overwrite. | No |

---

## 4. Basic Usage

### 4.1 Quick Reference & Common Invocations

| Task / Scenario | Command | Key Flags / Behavior |
|:---|:---|:---|
| Rename file or directory | `mv old_name.txt new_name.txt` | Instantaneous atomic rename (same filesystem) |
| Move files to directory | `mv file1.txt file2.txt /dest/` | Relocates files into destination folder |
| Prompt before overwrite | `mv -i src.txt dst.txt` | `-i` interactive prompt before replacing existing file |
| Do not overwrite existing | `mv -n src.txt dst.txt` | `-n` no-clobber protection against overwrites |
| Update only newer files | `mv -u src.txt dst.txt` | `-u` moves only if source is newer or target is missing |
| Versioned backup before replace | `mv --backup=numbered new.conf current.conf` | Creates `current.conf.~1~` backup before overwrite |
| Atomic directory replacement | `mv -T -f ./build_v2 /var/www/active` | `-T` prevents nesting inside existing directory |
| Batch move via xargs | `... \| xargs -0 mv -t /quarantine/` | `-t` sets destination directory upfront |

### 4.2 Renaming a File

```bash
mv old_name.txt new_name.txt
```

### 4.3 Moving Multiple Files into a Directory

```bash
mv file1.txt file2.txt /var/log/archive/
```

---

## 5. Practical Operations

### 5.1 Atomic Zero-Downtime Deployment via Symlink Swap

Deploying a new release directory atomically on the same filesystem:

```bash
mv -T -f ./build_v2 /var/www/active_release
```

- **Technical Analysis**: Because both paths reside on the same filesystem, the rename completes in a single atomic kernel operation. Web server worker processes never see a half-copied directory.

### 5.2 Moving with Automated Versioned Backups

Preventing accidental data loss during configuration moves:

```bash
mv --backup=numbered -v new_nginx.conf /etc/nginx/nginx.conf
```

*Sample terminal output:*

```console
renamed 'new_nginx.conf' -> '/etc/nginx/nginx.conf' (backup: '/etc/nginx/nginx.conf.~1~')
```

### 5.3 Safe Non-Overwriting Batch Relocations

Moving logs without clobbering existing archives:

```bash
mv -n /var/log/incoming/*.log /var/log/processed/
```

- Silently leaves any file in `/var/log/incoming/` if a file of that name already exists in `/var/log/processed/`.

---

## 6. Advanced Usage

### 6.1 Using `-t` for Clean `find` and `xargs` Integration

Standard `mv` requires the target directory to be the final argument, which complicates `xargs`. Using `-t` puts the target directory first:

```bash
find /tmp/uploads -name "*.tmp" -print0 | xargs -0 mv -t /var/quarantine/
```

- Efficiently processes thousands of files in a single invocation without argument order manipulation.

---

## 7. Exit Status, Environment, and Configuration

### 7.1 Exit Status Codes

| Exit Code | Meaning |
|:---:|:---|
| `0` | Success: all files relocated/renamed. |
| `>0` | An error occurred (cross-device quota failure, permission denied, source file missing). |

---

## 8. Safety, Security, and Portability

### 8.1 Cross-Filesystem Interruption Vulnerabilities

> [!WARNING]
> **Cross-Device Non-Atomicity**: When `SOURCE` and `DEST` reside on different mount points, `rename(2)` fails with `EXDEV`. `mv` falls back to copying data blocks followed by unlinking the source. This operation is **not atomic**.
>
> If a cross-device move is killed mid-transfer (e.g. `SIGKILL`, system crash, or power loss), partial files remain on the destination while the complete file remains on the source.

### 8.2 Traversal Nuances

> [!NOTE]
> Moving a directory across different filesystem mounts fails if the destination filesystem is mounted read-only or lacks adequate inode quotas.

---

## 9. Best Practices

1. **Rely on `mv` for Atomic File Swaps Only on the Same Mount**:
   > [!IMPORTANT]
   > *Guidance*: Verify both paths share the same filesystem (`df -P path1 path2`) before relying on atomicity for production releases.
   > *Authoritative Justification*: GNU documentation notes that cross-device moves fall back to copy-and-unlink, which is non-atomic.

2. **Use `-T` in Deployment Automation**:
   > [!TIP]
   > *Guidance*: Pass `-T` when renaming directories in CI/CD pipelines.
   > *Authoritative Justification*: Prevents `mv` from accidentally moving a release directory inside an existing release directory if the path already exists.

3. **Use `-t` with `xargs` Pipelines**:
   > [!TIP]
   > *Guidance*: Structure automated moves as `mv -t <dir> <files...>`.
   > *Authoritative Justification*: Avoids brittle shell expansion loops and enables batching with `xargs -0`.

---

## References

1. **GNU Coreutils mv Manual**: [https://www.gnu.org/software/coreutils/manual/html_node/mv-invocation.html](https://www.gnu.org/software/coreutils/manual/html_node/mv-invocation.html)
2. **POSIX.1-2024 mv Specification**: The Open Group Base Specifications Issue 8. [https://pubs.opengroup.org/onlinepubs/9799919799/utilities/mv.html](https://pubs.opengroup.org/onlinepubs/9799919799/utilities/mv.html)
3. **Linux rename(2) System Call**: [https://man7.org/linux/man-pages/man2/rename.2.html](https://man7.org/linux/man-pages/man2/rename.2.html)
