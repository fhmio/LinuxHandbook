---
title: "Linux Command Tutorial: findmnt"
date: 2026-09-12T00:00:00+00:00
categories: ['Technology']
tags:
  - 'Linux'
  - 'util-linux'
  - 'findmnt'
  - 'Linux Command Tutorial'
draft: false
slug: "linux-findmnt-tutorial"
description: "Authoritative reference tutorial for findmnt (util-linux), detailing mount table inspection, tree visualization, fstab verification, JSON formatting, and kernel mountinfo monitoring."
upstream_suite: "util-linux"
upstream_version: "util-linux 2.40"
posix_standard: "None"
research_date: "2026-09-12"
---

The **Linux Command Tutorial** series provides rigorous, upstream-verified references for essential system commands across Linux distributions and UNIX-like environments. Each article focuses on a single executable, combining exhaustive option documentation, verified real-world examples, security boundaries, and best practices directly derived from official source documentation and POSIX standards.

---

## 1. Introduction

> **Upstream**: util-linux 2.40 | **POSIX**: Linux-Specific (util-linux extension) | **Safety Tier**: safe-read-only | **Scope**: mount-hierarchy-inspection

`findmnt` searches and lists mounted filesystems or queries configuration files such as `/etc/fstab`, `/etc/mtab`, or `/proc/self/mountinfo`. It provides structured, hierarchical tree views, flat tables, and machine-readable output formats for inspecting Virtual File System (VFS) mounts.

- **Upstream Project & Provenance**: Developed and maintained under **util-linux** as part of the `misc-utils` subsystem, powered by `libmount`.
- **Portability & Standards Baseline**: `findmnt` is a Linux-specific system utility; it is not standardized in IEEE Std 1003.1-2024 (POSIX.1-2024).
- **Target Research Implementation**: Audited against **util-linux 2.40** (`findmnt(8)`).
- **Applicability & Lifecycle**: Active and standard across modern Linux systems, superseding ad-hoc parsing of `/etc/mtab` and `/proc/mounts`.

---

## 2. Syntax and Command Model

### 2.1 Canonical Synopsis

```bash
findmnt [options]
findmnt [options] device | mountpoint
findmnt [options] [--source device] [--target mountpoint]
```

### 2.2 Execution & Data Sources

`findmnt` queries one of three distinct filesystem configuration or status sources:
- **Kernel Mounts (Default)**: Reads `/proc/self/mountinfo`, reflecting active kernel VFS mount points, namespace propagation flags, and active options.
- **Fstab (`-s`, `--fstab`)**: Reads `/etc/fstab`, displaying static mount definitions configured for boot-time or on-demand mounting.
- **Mtab (`-m`, `--mtab`)**: Reads `/etc/mtab` (typically a symbolic link to `/proc/self/mounts`).

When a single argument is supplied without flags, `findmnt` evaluates it first as a mount point target (`TARGET`), and if not found, as a source block device or export (`SOURCE`).

---

## 3. Options

### 3.1 Source and Filtering Options

| Option | Long Option | Description | Default |
|:---|:---|:---|:---|
| `-s` | `--fstab` | Search `/etc/fstab` definitions instead of kernel mounts. | Kernel mountinfo |
| `-m` | `--mtab` | Search `/etc/mtab` instead of kernel mountinfo. | Kernel mountinfo |
| `-k` | `--kernel` | Search `/proc/self/mountinfo` (active kernel mounts). | Enabled by default |
| `-t list` | `--types list` | Filter by filesystem types (comma-separated, e.g. `ext4,xfs`). Prefix with `no` to invert. | All types |
| `-O list` | `--options list` | Filter by mount options (e.g. `ro`, `noexec`, `nosuid`). Prefix with `no` to invert. | All options |
| `-S dev` | `--source dev` | Explicitly filter by source device, UUID, LABEL, or PARTUUID. | Unfiltered |
| `-T path` | `--target path` | Search for mountpoint containing the given file or directory path. | Unfiltered |
| `-M dir` | `--mountpoint dir` | Explicitly search for exact mountpoint directory. | Unfiltered |

### 3.2 Output Formatting Options

| Option | Long Option | Description | Default |
|:---|:---|:---|:---|
| `-l` | `--list` | Output in flat list format instead of default hierarchical tree. | Tree format |
| `-a` | `--ascii` | Use ASCII line drawing characters instead of UTF-8 box characters. | UTF-8 |
| `-J` | `--json` | Output mount information as structured JSON. | Text table |
| `-D` | `--df` | Mimic `df` output columns (SOURCE, FSTYPE, SIZE, USED, AVAIL, USE%, TARGET). | Standard columns |
| `-o list` | `--output list` | Comma-separated list of columns to output (e.g. `TARGET,SOURCE,FSTYPE,OPTIONS`). | Default tree columns |
| `-n` | `--noheadings` | Suppress table header rows. | Headers printed |
| `-r` | `--raw` | Output raw tabular data without column alignment or padding. | Formatted table |
| `-u` | `--notruncate` | Do not truncate long column values to fit terminal width. | Truncated |
| `--verify` | `--verify` | Verify `/etc/fstab` syntax, check target directories, and validate options. | Disabled |
| `-p` | `--poll[=list]` | Monitor `/proc/self/mountinfo` for changes (mount/umount events). | Disabled |
| `-w ms` | `--timeout ms` | Exit polling mode after specified milliseconds. | Infinite polling |

---

## 4. Basic Usage

### 4.1 Quick-Reference Cheatsheet Card

| Operation | Command | Notes |
|:---|:---|:---|
| Visual mount tree | `findmnt` | Hierarchical ASCII/UTF-8 tree of active mounts |
| Verify fstab file | `findmnt --verify` | Validates `/etc/fstab` syntax and paths before reboot |
| Find mount owning path | `findmnt -T /var/log` | Resolves mountpoint containing file or directory |
| Mimic df disk usage | `findmnt -D` | Displays capacity, used, avail, and use% |
| JSON output for scripts | `findmnt -J -o TARGET,SOURCE,FSTYPE` | Emits structured JSON dataset |
| Real-time event monitor | `findmnt --poll` | Monitors `/proc/self/mountinfo` for mount/umount events |
| Filter by filesystem type | `findmnt -t ext4,xfs` | Shows only specified filesystem drivers |

### 4.2 Default Hierarchical Mount Tree

Running `findmnt` with no arguments produces a tree representation of all active kernel mount points:

```bash
findmnt
```
```console
TARGET                                SOURCE      FSTYPE      OPTIONS
/                                     /dev/sda2   ext4        rw,relatime,errors=remount-ro
├─/sys                                sysfs       sysfs       rw,nosuid,nodev,noexec,relatime
├─/proc                               proc        proc        rw,nosuid,nodev,noexec,relatime
├─/dev                                udev        devtmpfs    rw,nosuid,relatime,size=4012032k,nr_inodes=1003008,mode=755
│ └─/dev/pts                          devpts      devpts      rw,nosuid,noexec,relatime,gid=5,mode=620,ptmxmode=000
├─/boot/efi                           /dev/sda1   vfat        rw,relatime,fmask=0077,dmask=0077,codepage=437,iocharset=ascii,shortname=mixed,utf8,errors=remount-ro
└─/home                               /dev/sdb1   xfs         rw,relatime,attr2,inode64,logbufs=8,logbsize=32k,noquota
```

### 4.3 Querying a Specific Mount Point or Device

Inspect the exact mount details of a directory:

```bash
findmnt /home
```
```console
TARGET SOURCE    FSTYPE OPTIONS
/home  /dev/sdb1 xfs    rw,relatime,attr2,inode64,logbufs=8,logbsize=32k,noquota
```

Query by source device:

```bash
findmnt /dev/sda1
```
```console
TARGET    SOURCE    FSTYPE OPTIONS
/boot/efi /dev/sda1 vfat   rw,relatime,fmask=0077,dmask=0077,codepage=437,iocharset=ascii,shortname=mixed,utf8,errors=remount-ro
```

---

## 5. Practical Operations

### 5.1 Verifying `/etc/fstab` Before System Reboot

Administrators should always verify `/etc/fstab` integrity after modifying mount definitions to prevent unbootable systems:

> [!IMPORTANT]
> Always execute `findmnt --verify` after modifying `/etc/fstab`. It parses every directive, verifies target directory existence, and detects deprecated or malformed options, preventing catastrophic system boot lockouts.

```bash
findmnt --verify
```
```console
Success: no errors found in /etc/fstab
```

When an invalid option, missing directory, or broken identifier exists, `findmnt --verify` flags the exact line and failure reason:

```console
/etc/fstab: [line 9]: target '/data/backup' does not exist
/etc/fstab: [line 11]: unknown mount option 'noatimeee'
FAILED: 2 errors found in /etc/fstab
```

### 5.2 Disk Space Overview with `df`-Style Columns

`findmnt -D` presents filesystem capacity and utilization alongside VFS metadata:

```bash
findmnt -D
```
```console
SOURCE     FSTYPE      SIZE   USED  AVAIL USE% TARGET
/dev/sda2  ext4       49.1G  14.2G  32.4G  29% /
udev       devtmpfs    3.8G      0   3.8G   0% /dev
/dev/sda1  vfat      511.0M   6.1M 504.9M   1% /boot/efi
/dev/sdb1  xfs       465.8G 182.4G 283.4G  39% /home
```

### 5.3 Locating the Filesystem Owning an Arbitrary Path

When debugging storage exhaustion or determining whether a file resides on an NFS share, SSD, or tmpfs, use `-T` (`--target`):

```bash
findmnt -T /var/log/audit/audit.log
```
```console
TARGET SOURCE    FSTYPE OPTIONS
/      /dev/sda2 ext4   rw,relatime,errors=remount-ro
```

### 5.4 Filtering Read-Only or Specific Filesystem Types

List all active mounts configured with read-only permissions (`ro`):

```bash
findmnt -O ro
```
```console
TARGET                   SOURCE     FSTYPE OPTIONS
/sys/fs/cgroup/memory    cgroup     cgroup ro,nosuid,nodev,noexec,relatime,memory
/var/lib/snapd/snaps/core /dev/loop0 squashfs ro,nodev,relatime
```

Filter by filesystem type to display only physical disk partitions (`ext4,xfs,btrfs`):

```bash
findmnt -t ext4,xfs,btrfs
```
```console
TARGET SOURCE    FSTYPE OPTIONS
/      /dev/sda2 ext4   rw,relatime,errors=remount-ro
/home  /dev/sdb1 xfs    rw,relatime,attr2,inode64,logbufs=8,logbsize=32k,noquota
```

---

## 6. Advanced Usage

### 6.1 Structured JSON Output for Automation

Modern infrastructure tools parse JSON rather than screen-scraping text tables. `findmnt -J` emits structured JSON representations:

```bash
findmnt -J -o TARGET,SOURCE,FSTYPE,OPTIONS /home
```
```json
{
   "filesystems": [
      {
         "target": "/home",
         "source": "/dev/sdb1",
         "fstype": "xfs",
         "options": "rw,relatime,attr2,inode64,logbufs=8,logbsize=32k,noquota"
      }
   ]
}
```

Extract the source device programmatically with `jq`:

```bash
findmnt -J -o TARGET,SOURCE /home | jq -r '.filesystems[0].source'
```
```text
/dev/sdb1
```

### 6.2 Monitoring Mount and Unmount Events

The `-p` (`--poll`) option monitors `/proc/self/mountinfo` in real time, reacting to storage attachment, container volume binds, and unmount operations:

```bash
findmnt --poll
```
```console
ACTION     TARGET         SOURCE     FSTYPE OPTIONS
mount      /mnt/usb       /dev/sdc1  ext4   rw,relatime
umount     /mnt/usb
```

Limit polling duration using `--timeout`:

```bash
findmnt --poll --timeout 10000
```

### 6.3 Raw Output for Shell Pipelines

For shell scripts requiring minimal processing overhead without JSON parsers, combine `-r` (raw), `-n` (no headings), and custom columns:

```bash
while read -r target source fstype; do
    echo "Filesystem $source ($fstype) is mounted at $target"
done < <(findmnt -rn -o TARGET,SOURCE,FSTYPE -t ext4,xfs)
```

---

## 7. Exit Status, Environment, and Configuration

### 7.1 Exit Status

| Exit Code | Meaning |
|:---|:---|
| `0` | Success: matching filesystem found, verification passed, or information successfully listed. |
| `1` | Failure: no matching filesystem found, invalid option arguments, or fstab verification failed. |

### 7.2 Environment Variables

| Variable | Description |
|:---|:---|
| `LIBMOUNT_DEBUG` | Enables debugging output for `libmount` operations (e.g. `all`, `parse`, `tab`). |
| `FINDMNT_DEBUG` | Set to `all` or numeric masks to debug internal `findmnt` execution flow. |

### 7.3 Relevant System Files

| File | Role |
|:---|:---|
| `/proc/self/mountinfo` | Primary kernel mount metadata source containing mount IDs, parent IDs, major:minor device numbers, root paths, mount points, and propagation flags. |
| `/etc/fstab` | Static filesystem mount table queried with `-s` and audited with `--verify`. |
| `/etc/mtab` | Legacy mount table queried with `-m`. |

---

## 8. Safety, Security, and Portability

### 8.1 Read-Only Execution Safety

> [!NOTE]
> `findmnt` is an entirely non-destructive query utility that reads kernel memory structures directly via `/proc/self/mountinfo`. It does not alter filesystems, mount states, or storage tables, and can be run safely by unprivileged users in production environments.

### 8.2 Path Resolution and Symbolic Links

When resolving paths with `-T`, `findmnt` resolves symbolic links using `realpath(3)` to determine the actual VFS mount point governing the canonical filesystem path.

### 8.3 Portability Considerations

- `findmnt` relies on Linux-specific `/proc/self/mountinfo` interfaces and `libmount`. It is not portable to macOS (Darwin), FreeBSD, or Solaris.
- On non-Linux UNIX systems, POSIX-compliant scripts should inspect mounts via `mount` (without arguments) or `df -P`.

---

## 9. Best Practices

### 9.1 Always Run `findmnt --verify` After Editing `/etc/fstab`

*Upstream Rationale*: `findmnt(8)` documents `--verify` as a syntax and prerequisite validator. Syntax typos or referencing nonexistent UUIDs in `/etc/fstab` can trigger system boot failures or drop emergency shells. Running `findmnt --verify` immediately after editing catches syntax errors and missing directories prior to reboot.

### 9.2 Prefer `findmnt -T` Over Parsing `df` or Grepping Mount Tables

*Upstream Rationale*: Determining the mount point of a given path by matching strings against `/proc/mounts` fails when nested mounts, bind mounts, or relative paths are involved. `findmnt -T <path>` leverages kernel VFS traversal logic to accurately identify the containing mount point.

### 9.3 Use Structured Formats (`-J` or `-r -n`) in Automated Scripts

*Upstream Rationale*: The default tree output of `findmnt` uses multi-byte UTF-8 line drawing glyphs (`├─`, `└─`) intended for human readability in terminal emulators. Parsing default tree output with `awk` or `cut` leads to fragile scripts. Always specify explicit columns (`-o TARGET,SOURCE`) combined with `-J` (JSON) or `-r` (raw unaligned) in automation workflows.

---

## References

1. `findmnt(8)` — Linux man page, util-linux project: <https://man7.org/linux/man-pages/man8/findmnt.8.html>
2. util-linux source repository (`misc-utils/findmnt.8.adoc`): <https://github.com/util-linux/util-linux/blob/master/misc-utils/findmnt.8.adoc>
3. `mountinfo` specification — Linux Kernel Documentation: <https://docs.kernel.org/filesystems/proc.html#mountinfo>
