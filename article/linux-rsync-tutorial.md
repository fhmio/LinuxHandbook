---
title: "Linux Command Tutorial: rsync"
date: 2026-09-12T00:00:00+00:00
categories: ['Technology']
tags:
  - 'Linux'
  - 'rsync'
  - 'rsync'
  - 'Linux Command Tutorial'
draft: false
slug: "linux-rsync-tutorial"
description: "Authoritative reference tutorial for rsync (rsync), detailing delta-transfer algorithm file synchronization, archive mode preservation, remote SSH transport, exclusions, and bandwidth limiting."
upstream_suite: "rsync"
upstream_version: "rsync 3.5.0"
posix_standard: "None"
research_date: "2026-09-12"
---

The **Linux Command Tutorial** series provides rigorous, upstream-verified references for essential system commands across Linux distributions and UNIX-like environments. Each article focuses on a single executable, combining exhaustive option documentation, verified real-world examples, security boundaries, and best practices directly derived from official source documentation and POSIX standards.

---

## 1. Introduction

`rsync` (Remote Sync) is a fast, versatile utility for synchronizing files and directory trees locally or across networks. It utilizes a rolling-checksum delta-transfer algorithm that computes differences between source and destination files, transmitting only changed byte blocks over network connections.

- **Upstream Project & Provenance**: Created by Andrew Tridgell and Paul Mackerras, maintained by Wayne Davison and the Samba team under the **rsync** project (`rsync`).
- **Portability & Standards Baseline**: De-facto universal Unix file synchronization utility; not standardized in IEEE Std 1003.1-2024 (POSIX.1-2024).
- **Target Research Implementation**: Audited against **rsync 3.5.0** (`rsync(1)`).
- **Applicability & Lifecycle**: The standard utility for server backups, site mirroring, continuous integration deployments, and disaster recovery.

---

## 2. Syntax and Command Model

### 2.1 Canonical Synopsis

```bash
# Local to local synchronization
rsync [OPTION...] SRC... [DEST]

# Remote synchronization over SSH (Push)
rsync [OPTION...] SRC... [USER@]HOST:DEST

# Remote synchronization over SSH (Pull)
rsync [OPTION...] [USER@]HOST:SRC... [DEST]
```

### 2.2 The Trailing Slash Rule

A fundamental syntactic rule governs source directory handling in `rsync`:
- **Source with Trailing Slash (`/src/dir/`)**: Copies the **contents** of `dir/` directly into destination without creating an extra subdirectory.
- **Source without Trailing Slash (`/src/dir`)**: Copies the directory itself, creating `/dest/dir/`.

```bash
# Copies files inside data into /backup/ (e.g. /backup/file1.txt)
rsync -a /var/data/ /backup/

# Copies data directory into /backup/ (e.g. /backup/data/file1.txt)
rsync -a /var/data /backup/
```

### 2.3 Delta-Transfer Process Model

When synchronizing across remote hosts, `rsync` spawns a client process locally and a remote server process via SSH. The receiver breaks destination files into fixed-size blocks, computes weak rolling checksums and strong MD4/MD5 hashes, and sends them to the sender. The sender matches hashes and transmits only the modified byte blocks.

---

## 3. Options

### 3.1 Primary Synchronization Flags

| Option | Long Option | Description | Default |
|:---|:---|:---|:---|
| `-a` | `--archive` | Archive mode: equivalent to `-rlptgoD` (recurse, preserve symlinks, perms, times, owner, group, devices). | Non-recursive |
| `-v` | `--verbose` | Increase verbosity, printing transferred filenames. | Concise |
| `-q` | `--quiet` | Suppress non-error output messages. | Normal |
| `-z` | `--compress` | Compress file data blocks during network transmission. | Uncompressed |
| `-h` | `--human-readable` | Format byte counts and transfer rates with readable units (`K`, `M`, `G`). | Integer bytes |
| `-n` | `--dry-run` | Perform a trial run without modifying destination filesystems. | Active execution |
| `-P` | | Equivalent to `--partial --progress` (resumes partial files and displays transfer progress). | Off |
| `-c` | `--checksum` | Skip files based on cryptographic checksums rather than mod-time and size. | Quick check (mtime+size) |
| `--delete` | `--delete` | Delete extraneous files from destination not present in source (mirroring). | Retains destination files |
| `--delete-after` | `--delete-after` | Delete extraneous files after transfers conclude rather than during. | Immediate deletion |
| `-e CMD` | `--rsh=CMD` | Specify remote shell command (e.g. `-e "ssh -p 2222"`). | `ssh` |
| `--bwlimit=RATE` | `--bwlimit=RATE` | Limit socket I/O bandwidth (e.g. `10m`, `500k`). | Unlimited |
| `--link-dest=DIR`| `--link-dest=DIR` | Create hard links to unchanged files in reference directory for instant snapshots. | Off |
| `-S` | `--sparse` | Handle sparse files efficiently, preserving storage holes on destination. | Dense allocation |

### 3.2 Filtering and Exclusion Flags

| Option | Long Option | Description |
|:---|:---|:---|
| `--exclude=PAT` | `--exclude=PAT` | Exclude files and directories matching glob pattern `PAT`. |
| `--exclude-from=F`| `--exclude-from=F` | Read exclusion glob patterns line-by-line from file `F`. |
| `--include=PAT` | `--include=PAT` | Explicitly include files matching `PAT` before general exclusions. |

---

## 4. Basic Usage

### 4.1 Local Directory Backup

Synchronize a local directory with archive preservation and human-readable transfer logs:

```console
$ rsync -avh /home/user/documents/ /mnt/backup/documents/
sending incremental file list
./
financial_report_2026.pdf
notes.txt
projects/
projects/architecture_spec.md

sent 4.82M bytes  received 84 bytes  9.64M bytes/sec
total size is 4.81M  speedup is 1.00
```

### 4.2 Safe Dry-Run Validation (`-n`)

Always test backup or synchronization commands with `-n` (`--dry-run`) before modifying production storage:

```console
$ rsync -avhn --delete /home/user/documents/ /mnt/backup/documents/
sending incremental file list
deleting obsolete_draft.docx
financial_report_2026.pdf

sent 284 bytes  received 18 bytes  604.00 bytes/sec
total size is 4.81M  speedup is 15.93 (DRY RUN)
```

---

## 5. Practical Operations

### 5.1 Remote Synchronization Over SSH

Synchronize files to a remote server over an encrypted SSH transport with compression and progress tracking:

```bash
rsync -avzP -e "ssh -p 22022" /var/www/html/ deploy@server.example.com:/var/www/html/
```

Output:

```console
sending incremental file list
index.html
          4.12K 100%    3.93MB/s    0:00:00 (xfr#1, to-chk=24/25)
assets/app.js
        184.92K 100%   12.45MB/s    0:00:00 (xfr#2, to-chk=12/25)

sent 48.12K bytes  received 1.45K bytes  33.05K bytes/sec
total size is 894.12K  speedup is 18.04
```

### 5.2 Strict Directory Mirroring with `--delete`

Ensure the destination directory matches the source precisely by removing extraneous destination files:

```bash
rsync -av --delete /data/production/ /data/mirror/
```

### 5.3 Space-Efficient Incremental Snapshots via `--link-dest`

Implement automated, deduplicated hourly backups without consuming extra disk space for unchanged files:

```bash
# Reference yesterday's backup directory; unchanged files become hard links
rsync -a --delete \
  --link-dest=/backups/2026-09-11/ \
  /home/user/data/ \
  /backups/2026-09-12/
```

*Mechanism*: If a file in `/home/user/data/` has the exact same mtime and size as `/backups/2026-09-11/file`, `rsync` creates a hard link in `/backups/2026-09-12/file` pointing to the existing inode, consuming zero additional disk blocks.

### 5.4 Bandwidth Throttling for Network Conservation

Prevent backup transfers from saturating WAN or VPN uplinks by capping transfer rates:

```bash
# Limit transfer rate to 5 Megabytes per second
rsync -avzP --bwlimit=5M /data/heavy_backups/ remote:/storage/
```

---

## 6. Advanced Usage

### 6.1 Advanced Exclusion and Filtering Rules

Exclude version control files, caches, and build artifacts using exclusion rules:

```bash
rsync -av \
  --exclude='.git/' \
  --exclude='node_modules/' \
  --exclude='*.tmp' \
  --exclude='*.log' \
  /workspace/project/ /opt/deploy/project/
```

Or load patterns from a dedicated `.rsync-ignore` file:

```bash
rsync -av --exclude-from='.rsync-ignore' /src/ /dest/
```

### 6.2 Atomic Transfers via `--delay-updates`

Prevent client services from reading partially written files during a large sync operation:

```bash
rsync -av --delay-updates /var/www/v2/ /var/www/live/
```
*Mechanism*: `rsync` stages all new and modified files into temporary files (`.~tmp~`) during transfer, renaming them atomically into their final destinations in a rapid closing phase.

### 6.3 Checksum-Based Verification (`-c`)

By default, `rsync` relies on "quick check" (file modification time and size equality). For high-security environments or storage corruption validation, force full cryptographic hashing across all files:

```bash
rsync -avc /critical/data/ /backup/critical/
```

---

## 7. Exit Status, Environment, and Configuration

### 7.1 Exit Status

| Exit Code | Meaning |
|:---|:---|
| `0` | Success: synchronization completed without errors. |
| `1` | Syntax or usage error. |
| `2` | Protocol incompatibility. |
| `3` | Errors selecting input/output files or directories. |
| `5` | Error starting client-server protocol. |
| `10` | Error in socket I/O (network dropped or connection timed out). |
| `11` | Error in file I/O (disk full, permission denied, or read error). |
| `12` | Error in rsync protocol data stream. |
| `23` | Partial transfer due to error. |
| `24` | Partial transfer due to vanished source files. |

### 7.2 Environment Variables

| Variable | Description |
|:---|:---|
| `RSYNC_RSH` | Default remote shell command (superseded by `-e`). |
| `RSYNC_PASSWORD` | Password used for authenticating against standalone rsync daemons. |

### 7.3 Daemon Configuration

When running in standalone server mode (`rsync --daemon`), configuration is managed via `/etc/rsyncd.conf`.

---

## 8. Safety, Security, and Portability

### 8.1 Destructive Impact of `--delete`

The `--delete` flag permanently removes files from destination directories. A common disaster occurs when the source directory path is mistyped or empty, causing `rsync` to wipe the entire destination. Always prepend `-n` (`--dry-run`) to verify the file deletion list before executing `--delete` operations.

### 8.2 Privilege Preservation Across Remote Hosts

Archive mode (`-a`) attempts to preserve owner (`-o`) and group (`-g`) IDs. Preserving numeric UIDs and GIDs requires `root` privileges on the destination host. Unprivileged users running `rsync -a` will experience permission warnings unless `--no-owner --no-group` is specified.

### 8.3 Portability Constraints

`rsync` is ubiquitous across modern Linux, BSD, and macOS systems. Version 3.x utilizes a streamlined protocol that maintains backward compatibility with legacy 2.x rsync servers.

---

## 9. Best Practices

### 9.1 Double-Check Trailing Slashes on Source Paths

*Upstream Rationale*: Omitting a trailing slash on source directories copies the parent directory container (e.g. `/dest/source/`), while appending a trailing slash copies the child items directly (e.g. `/dest/`). Always explicitly check trailing slashes on source paths prior to execution.

### 9.2 Always Test with `-n` (`--dry-run`) Before Using `--delete`

*Upstream Rationale*: `rsync(1)` documentation highlights that deleted files cannot be recovered once removed from the destination tree. Running `rsync -avhn --delete` provides complete visibility of scheduled deletions before physical disk writes occur.

### 9.3 Leverage `--link-dest` for Zero-Cost Hourly Snapshots

*Upstream Rationale*: Traditional full backups duplicate identical files across storage arrays, wasting disk space and I/O bandwidth. `--link-dest` utilizes Linux filesystem hard links to create instant, read-accessible, deduplicated differential backups.

---

## References

1. `rsync(1)` — Linux man page, rsync project: <https://download.samba.org/pub/rsync/rsync.1>
2. rsync Project Official Website: <https://rsync.samba.org/>
3. rsync Source Repository: <https://github.com/WayneD/rsync>
