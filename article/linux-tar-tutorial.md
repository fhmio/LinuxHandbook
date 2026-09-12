---
title: "Linux Command Tutorial: tar"
date: 2026-09-12T00:00:00+00:00
categories: ['Technology']
tags:
  - 'Linux'
  - 'GNU tar'
  - 'tar'
  - 'Linux Command Tutorial'
draft: false
slug: "linux-tar-tutorial"
description: "Authoritative reference tutorial for tar (GNU tar), detailing tape archive creation, compression filter chaining (gzip, bzip2, xz, zstd), incremental backups, member extraction, and archive inspection."
upstream_suite: "gnu-tar"
upstream_version: "GNU tar 1.35"
posix_standard: "None"
research_date: "2026-09-12"
---

The **Linux Command Tutorial** series provides rigorous, upstream-verified references for essential system commands across Linux distributions and UNIX-like environments. Each article focuses on a single executable, combining exhaustive option documentation, verified real-world examples, security boundaries, and best practices directly derived from official source documentation and POSIX standards.

---

## 1. Introduction

> **Upstream**: gnu-tar (GNU tar 1.35) | **POSIX**: POSIX.1-2024 pax-compatible / GNU extension | **Safety Tier**: unprivileged-filesystem-write | **Scope**: archive-manipulation

`tar` (Tape Archive) is the standard UNIX and Linux archiving utility. It concatenates multiple files, directories, symbolic links, and filesystem metadata into a single sequential archive stream (`tarball`) while preserving UNIX permissions, timestamps, owner/group attributes, and extended attributes.

- **Upstream Project & Provenance**: Maintained by the **GNU Project** under **GNU tar** (`tar`).
- **Portability & Standards Baseline**: Historically rooted in POSIX (ustar / pax interchange formats); POSIX.1-2024 designates `pax` as the standard archiver, but GNU tar represents the universal Linux implementation.
- **Target Research Implementation**: Audited against **GNU tar 1.35** (`tar(1)`).
- **Applicability & Lifecycle**: The foundational tool for source code distribution, system backups, package management, and container image layers.

---

## 2. Syntax and Command Model

### 2.1 Canonical Synopsis

```bash
tar [OPERATION] [OPTIONS] -f ARCHIVE [FILE/DIR...]
```

### 2.2 Execution Model: The Operation Mode Requirement

Every `tar` invocation requires exactly **one** primary operation mode specifying the fundamental action to execute:

| Mode Flag | Long Option | Purpose |
|:---|:---|:---|
| `-c` | `--create` | Create a new archive from specified files or directories. |
| `-x` | `--extract`, `--get` | Extract members from an existing archive into the filesystem. |
| `-t` | `--list` | List the contents of an archive without writing to disk. |
| `-r` | `--append` | Append additional files to the end of an uncompressed archive. |
| `-u` | `--update` | Only append files that are newer than their archive copy. |
| `-d` | `--diff`, `--compare` | Compare files in an archive with corresponding filesystem files. |
| `--delete` | `--delete` | Delete specified members from an uncompressed archive file. |

---

## 3. Options

### 3.1 Compression Filter Flags

| Flag | Long Option | Compression Algorithm | File Extension |
|:---|:---|:---|:---|
| `-z` | `--gzip` | Filter archive through `gzip` (DEFLATE). | `.tar.gz`, `.tgz` |
| `-j` | `--bzip2` | Filter archive through `bzip2` (Burrows-Wheeler). | `.tar.bz2`, `.tbz2` |
| `-J` | `--xz` | Filter archive through `xz` (LZMA2). | `.tar.xz`, `.txz` |
| | `--zstd` | Filter archive through `zstandard` (Zstd). | `.tar.zst` |
| `-a` | `--auto-compress` | Deduce compression filter automatically from archive filename suffix. | Dynamic |

### 3.2 Key Operation Modifiers

| Option | Long Option | Description | Default |
|:---|:---|:---|:---|
| `-f ARCHIVE` | `--file=ARCHIVE` | Use specified archive file or device (use `-` for stdin/stdout). | `/dev/tape` |
| `-v` | `--verbose` | Verbosely list files processed during archiving or extraction. | Silent |
| `-C DIR` | `--directory=DIR` | Change to directory `DIR` before performing operations. | Current directory |
| `-p` | `--preserve-permissions` | Preserve file permissions and access modes upon extraction. | Masked by umask |
| `-k` | `--keep-old-files` | Do not overwrite existing files when extracting; treat as errors. | Overwrites files |
| `--strip-components=N` | `--strip-components=N` | Strip `N` leading path hierarchy components upon extraction. | Full archive path |
| `--exclude=PAT` | `--exclude=PAT` | Exclude files matching specified glob pattern. | All included |
| `--one-file-system` | `--one-file-system` | Stay on local filesystem; do not cross filesystem mount boundaries. | Crosses mounts |
| `-g FILE` | `--listed-incremental=FILE` | Handle modern incremental backups using snapshot metadata file. | Non-incremental |

---

## 4. Basic Usage

### 4.1 Quick-Reference Cheatsheet Card

| Operation | Command Pattern | Copyable One-Liner | Notes |
|:---|:---|:---|:---|
| Create compressed archive | `tar -czvf [archive.tar.gz] [dir]` | `tar -czvf backup.tar.gz /var/www/html/` | Packs and compresses with gzip |
| Auto-compress by suffix | `tar -caf [archive.tar.xz] [dir]` | `tar -caf archive.tar.xz /data/` | Automatically detects compression from suffix |
| List archive members | `tar -tvf [archive]` | `tar -tvf backup.tar.gz` | Inspect contents without extracting |
| Extract archive | `tar -xvf [archive]` | `tar -xvf backup.tar.gz` | Unpacks to current directory |
| Extract to directory | `tar -xvf [archive] -C [dir]` | `tar -xvf backup.tar.gz -C /opt/app/` | Unpacks into targeted location |
| Strip root component | `tar -xvf [archive] -C [dir] --strip-components=1` | `sudo tar -xzvf nginx.tar.gz -C /opt/nginx --strip-components=1` | Removes top-level folder on unpack |
| Stream over SSH | `tar -cf - [dir] \| ssh [host] "tar -xf - -C [dest]"` | `tar -cf - /data/ \| ssh user@remote "tar -xf - -C /backup/"` | Streams archives without local disk staging |

### 4.2 Creating a Compressed Archive

Create a gzip-compressed archive (`-czvf`) of a project directory:

```bash
tar -czvf webapp-backup.tar.gz /var/www/html/
```

Output:

```console
tar: Removing leading `/' from member names
/var/www/html/
/var/www/html/index.html
/var/www/html/style.css
/var/www/html/images/
/var/www/html/images/logo.png
```

*Note*: GNU tar automatically strips leading slashes (`/`) by default to prevent dangerous absolute path overwrites during extraction.

### 4.3 Inspecting Archive Contents Without Extracting (`-tvf`)

Inspect archive members, permissions, ownership, and timestamps prior to unpacking:

```bash
tar -tvf webapp-backup.tar.gz
```

Output:

```console
drwxr-xr-x www-data/www-data 0 2026-09-12 18:00 var/www/html/
-rw-r--r-- www-data/www-data 2415 2026-09-12 18:00 var/www/html/index.html
-rw-r--r-- www-data/www-data 8492 2026-09-12 18:00 var/www/html/style.css
drwxr-xr-x www-data/www-data 0 2026-09-12 18:00 var/www/html/images/
-rw-r--r-- www-data/www-data 45812 2026-09-12 18:00 var/www/html/images/logo.png
```

### 4.4 Extracting an Archive

Extract an archive into the current working directory:

```bash
tar -xzvf webapp-backup.tar.gz
```

---

## 5. Practical Operations

### 5.1 Extracting to a Specific Directory with `--strip-components`

Unpack an archive into a target directory (`-C`) while removing the top-level parent folder:

```bash
# Unpack nginx-1.26.0/ directly into /opt/nginx without creating /opt/nginx/nginx-1.26.0/
sudo tar -xzvf nginx-1.26.0.tar.gz -C /opt/nginx --strip-components=1
```

### 5.2 Creating Modern High-Efficiency Archives with Auto-Compress (`-a`)

Leverage GNU tar's automatic filter deduction by naming the destination archive appropriately:

```bash
# Creates an XZ-compressed archive automatically
tar -caf system-backup.tar.xz /etc /home/user/configs

# Creates a Zstandard-compressed archive automatically
tar -caf fast-backup.tar.zst /var/log
```

### 5.3 Excluding Files and Directories

Exclude development caches, version control data, and temporary files:

```bash
tar -caf project.tar.gz \
  --exclude='.git' \
  --exclude='node_modules' \
  --exclude='*.pyc' \
  --exclude='__pycache__' \
  ./my-project/
```

### 5.4 Auditing Differences Between Archive and Filesystem (`-d`)

Detect whether local configuration files have drifted since an archive was generated:

```bash
tar -dzf system-backup.tar.gz
```

Output:

```console
etc/hosts: Mod time differs
etc/hosts: Size differs
etc/ssh/sshd_config: Contents differ
```

---

## 6. Advanced Usage

### 6.1 Direct Streaming Over SSH Pipelines

Stream archives across network boundaries without staging intermediate `.tar` files on disk:

```bash
# Archive local directory and extract directly onto remote server over SSH
tar -cf - /data/important/ | ssh user@remote.example.com "tar -xf - -C /storage/backup/"
```

### 6.2 Managing Incremental Backups with `--listed-incremental`

Create true incremental backup chains utilizing GNU tar's snapshot catalog:

```bash
# Day 0: Full baseline backup
tar -czvf backup-level0.tar.gz -g /backups/snapshot.snar /home/user/data

# Day 1: Incremental backup (captures only files modified or added since level 0)
tar -czvf backup-level1.tar.gz -g /backups/snapshot.snar /home/user/data
```

### 6.3 Handling Sparse Files Efficiently (`-S`)

Preserve sparse file holes (such as virtual machine disk images or container roots) without inflating archive sizes:

```bash
tar -Scaf disk-images.tar.xz /var/lib/libvirt/images/
```

---

## 7. Exit Status, Environment, and Configuration

### 7.1 Exit Status

| Exit Code | Meaning |
|:---|:---|
| `0` | Success: all files processed successfully. |
| `1` | Some files differ (returned during `--diff` comparison). |
| `2` | Fatal error: archive corrupted, file read error, or extraction aborted. |

### 7.2 Environment Variables

| Variable | Description |
|:---|:---|
| `TAR_OPTIONS` | Default command-line options prepended to every invocation. |
| `TAPE` | Default archive device file path if `-f` is omitted (legacy tape drive default). |

---

## 8. Safety, Security, and Portability

### 8.1 "Tarbomb" Prevention

> [!WARNING]
> **Tarbomb Hazard**: A "tarbomb" is an archive containing hundreds of loose files at the archive root without a parent directory. Extracting it clutters the current working directory. Always inspect archive contents first with `tar -tf archive.tar.gz` or extract into an isolated directory with `-C`.

### 8.2 Absolute Paths and Traversal Safeguards

> [!CAUTION]
> GNU tar automatically strips leading slashes (`/`) and ignores `../` path traversals to prevent malicious archives from overwriting system files. Never specify `-P` (`--absolute-names`) when extracting untrusted third-party archives.

### 8.3 Portability Between GNU and BSD Tar

- Linux distributions utilize **GNU tar**.
- macOS and FreeBSD utilize **BSD tar** (`bsdtar`), built on `libarchive`.
- While basic syntax (`-czvf`, `-xzvf`) is compatible, flags such as `--warning`, `--checkpoint`, or advanced `--listed-incremental` are GNU-specific extensions not supported by BSD tar.

---

## 9. Best Practices

### 9.1 Always Inspect Archives with `-tvf` Prior to Extraction

> [!TIP]
> **Always Inspect Archives with `-tvf` Prior to Extraction**: Verifying permissions, file paths, and member counts prior to extraction prevents accidental file overwrites or unintended directory contamination.

*Upstream Rationale*: `tar(1)` documentation emphasizes that extracting unknown archives can overwrite existing local files or create clutter. Running `tar -tvf` verifies member hierarchy, permissions, and paths before any filesystem writes occur.

### 9.2 Use `-C` to Target Output Directories Explicitly

> [!IMPORTANT]
> **Target Output Directories Explicitly**: Always specify `-C /path/to/target/` to guarantee deterministic extraction boundaries and eliminate reliance on current shell working directories.

*Upstream Rationale*: Relying on the current working directory for extraction creates race conditions in automated scripts and invites accidental file clobbering. Always specify `-C /path/to/target/` to guarantee deterministic extraction boundaries.

### 9.3 Leverage `-a` (`--auto-compress`) in Scripts

*Upstream Rationale*: Hardcoding compression flags (such as `-z` or `-j`) creates brittle scripts that fail or corrupt files when the output archive extension is changed. Supplying `-a` delegates compression format selection directly to the filename extension (`.tar.gz`, `.tar.xz`, `.tar.zst`).

---

## References

1. `tar(1)` — GNU tar reference manual: <https://www.gnu.org/software/tar/manual/tar.html>
2. GNU tar Source Repository: <https://git.savannah.gnu.org/cgit/tar.git>
3. POSIX.1-2024 pax / ustar archive format standard: <https://pubs.opengroup.org/onlinepubs/9799919799/>
