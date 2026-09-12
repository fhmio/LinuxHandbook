---
title: "Linux Command Tutorial: fdisk"
date: 2026-09-12T00:00:00+00:00
categories: ['Technology']
tags:
  - 'Linux'
  - 'util-linux'
  - 'fdisk'
  - 'Linux Command Tutorial'
draft: false
slug: "linux-fdisk-tutorial"
description: "Authoritative reference tutorial for fdisk (util-linux), detailing disk partition table manipulation, MBR and GPT partition management, sector alignment, non-interactive scripting, and kernel partition table re-reading."
upstream_suite: "util-linux"
upstream_version: "util-linux 2.40"
posix_standard: "None"
research_date: "2026-09-12"
---

The **Linux Command Tutorial** series provides rigorous, upstream-verified references for essential system commands across Linux distributions and UNIX-like environments. Each article focuses on a single executable, combining exhaustive option documentation, verified real-world examples, security boundaries, and best practices directly derived from official source documentation and POSIX standards.

---

## 1. Introduction

`fdisk` is a dialog-driven and scriptable partition table manipulator for block devices. It inspects, creates, alters, and deletes partitions on disks formatted with GUID Partition Table (GPT), Master Boot Record (MBR/DOS), Sun, or SGI partition schemes.

- **Upstream Project & Provenance**: Maintained within **util-linux** under the `fdisks` subsystem, built upon `libfdisk`.
- **Portability & Standards Baseline**: Linux-specific system management tool; not standardized in IEEE Std 1003.1-2024 (POSIX.1-2024).
- **Target Research Implementation**: Audited against **util-linux 2.40** (`fdisk(8)`).
- **Applicability & Lifecycle**: The foundational low-level tool for disk partitioning, supporting both traditional MBR and modern GPT disks.

---

## 2. Syntax and Command Model

### 2.1 Canonical Synopsis

```bash
fdisk [options] device
fdisk -l [device...]
```

### 2.2 Execution & In-Memory Buffer Model

`fdisk` operates on a staging buffer in user-space memory:
- **In-Memory Modification**: All partition creation (`n`), deletion (`d`), type changes (`t`), and label initialization (`g`, `o`) occur strictly in memory.
- **Commit Boundary (`w`)**: Disk structures are only modified when the user explicitly issues the `w` (write) command.
- **Abort Boundary (`q`)**: Exiting with `q` (quit) terminates the session without committing any changes to the physical disk.
- **Kernel Notification**: Upon writing (`w`), `fdisk` calls the `BLKRRPART` `ioctl` to instruct the kernel to re-read the partition table.

### 2.3 Interactive Command Summary

| Command | Action |
|:---|:---|
| `m` | Print the interactive command menu and help text. |
| `p` | Print the current in-memory partition table. |
| `n` | Add a new partition. |
| `d` | Delete an existing partition. |
| `t` | Change a partition type / partition type GUID. |
| `g` | Create a new, empty GPT partition table. |
| `o` | Create a new, empty DOS/MBR partition table. |
| `v` | Verify the partition table integrity and detect overlapping sectors. |
| `w` | Write partition table to disk and exit (commits all modifications). |
| `q` | Quit without saving changes. |

---

## 3. Options

### 3.1 Command-Line Options

| Option | Long Option | Description | Default |
|:---|:---|:---|:---|
| `-l` | `--list` | List partition tables for specified devices (or all devices if omitted) and exit. | Interactive mode |
| `-b size` | `--sector-size size` | Explicitly specify physical sector size (512, 1024, 2048, 4096). | Hardware probed |
| `-B` | `--protect-boot` | Do not wipe bootloader boot code when creating a new disk label. | Normal label creation |
| `-c[=mode]` | `--compatibility[=mode]` | Set compatibility mode (`dos` or `nondos`). | nondos |
| `-L[=when]` | `--color[=when]` | Colorize output (`auto`, `always`, `never`). | auto |
| `-o list` | `--output list` | Specify comma-separated output columns for `--list` display. | Default columns |
| `-t type` | `--type type` | Restrict partition type listing to specified label type (e.g. `gpt`, `dos`). | All types |
| `-u[=unit]` | `--units[=unit]` | Display units (`sectors` or `cylinders`). | sectors |
| `-w when` | `--wipe when` | Wipe filesystem, RAID, and partition-table signatures (`auto`, `never`, `always`). | auto |
| `-W when` | `--wipe-partitions when` | Wipe signatures from newly created partitions (`auto`, `never`, `always`). | auto |

---

## 4. Basic Usage

### 4.1 Listing All Partition Tables

Query all system block storage devices in read-only mode using `-l`:

```console
$ sudo fdisk -l
Disk /dev/sda: 476.94 GiB, 512110190592 bytes, 1000215216 sectors
Disk model: Samsung SSD 980 500GB
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: gpt
Disk identifier: 7E5A2A11-9F3C-4328-98C3-324F159C2056

Device         Start        End   Sectors   Size Type
/dev/sda1       2048    1050623   1048576   512M EFI System
/dev/sda2    1050624    3147775   2097152     1G Linux filesystem
/dev/sda3    3147776 1000214527 997066752 475.4G Linux LVM
```

### 4.2 Querying a Specific Block Device

Target a single drive without listing unrelated devices:

```console
$ sudo fdisk -l /dev/sdb
Disk /dev/sdb: 1.82 TiB, 2000398934016 bytes, 3907029168 sectors
Disk model: WDC WD20EZAZ-00L
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 4096 bytes
I/O size (minimum/optimal): 4096 bytes / 4096 bytes
Disklabel type: gpt
Disk identifier: A91B24E3-5572-4B61-912A-6A792E5B1012

Device     Start        End    Sectors  Size Type
/dev/sdb1   2048 3907028991 3907026944  1.8T Linux filesystem
```

---

## 5. Practical Operations

### 5.1 Interactive Partitioning Workflow (Creating a GPT Partition)

To initialize a raw storage disk `/dev/sdc` with a GPT label and a single partition:

```console
$ sudo fdisk /dev/sdc

Welcome to fdisk (util-linux 2.40).
Changes will remain in memory only, until you decide to write them.
Be careful before using the write command.

Command (m for help): g
Created a new GPT disklabel (GUID: B8D3E421-1F3B-4D2A-98F1-44E2319A5B87).

Command (m for help): n
Partition number (1-128, default 1): 1
First sector (2048-209715166, default 2048): 2048
Last sector, +/-sectors or +/-size{K,M,G,T,P} (2048-209715166, default 209715166): +50G

Created a new partition 1 of type 'Linux filesystem' and of size 50 GiB.

Command (m for help): p
Disk /dev/sdc: 100 GiB, 107374182400 bytes, 209715200 sectors
Units: sectors of 1 * 512 = 512 bytes
Disklabel type: gpt

Device        Start       End   Sectors Size Type
/dev/sdc1      2048 104859647 104857600  50G Linux filesystem

Command (m for help): w
The partition table has been altered.
Calling ioctl() to re-read partition table.
Syncing disks.
```

### 5.2 Changing a Partition Type (e.g. Linux Swap or EFI)

Change the type identifier of partition 1 to Linux swap:

```console
$ sudo fdisk /dev/sdc

Command (m for help): t
Partition number (1, default 1): 1
Partition type or alias (type L to list all): swap

Changed type of partition 'Linux filesystem' to 'Linux swap'.

Command (m for help): w
The partition table has been altered.
Calling ioctl() to re-read partition table.
Syncing disks.
```

### 5.3 Deleting an Existing Partition

Remove an unwanted partition from the in-memory staging table:

```console
$ sudo fdisk /dev/sdc

Command (m for help): d
Partition number (1, default 1): 1
Partition 1 has been deleted.

Command (m for help): w
The partition table has been altered.
Calling ioctl() to re-read partition table.
Syncing disks.
```

---

## 6. Advanced Usage

### 6.1 Non-Interactive Scripting via Heredocs

Automated provisioning scripts can pipe commands into `fdisk` using here-documents:

```bash
# Non-interactively create a GPT label and a 10G partition on /dev/sdc
sudo fdisk /dev/sdc <<EOF
g
n
1
2048
+10G
w
EOF
```

*Note*: For robust scripted partitioning without interactive prompts, upstream util-linux recommends `sfdisk` (`sfdisk(8)`), which is designed specifically for automation.

### 6.2 Handling Busy Kernel Partition Tables

When writing a partition table to a disk where other partitions are actively mounted, the kernel `ioctl(BLKRRPART)` call may report that the device is busy:

```text
Re-reading the partition table failed.: Device or resource busy
The kernel still uses the old table. The new table will be used at the next reboot or you can run partx(8) or kpartx(8).
```

Force the kernel to update partition table mappings for a specific partition without rebooting:

```bash
# Inform kernel of changes to partition 1 on /dev/sdc
sudo partx -u /dev/sdc1 /dev/sdc

# Or trigger a full partition rescan via partprobe
sudo partprobe /dev/sdc
```

### 6.3 Sector Alignment Verification

Modern block devices use 4096-byte (4K) physical sectors. If partitions do not start on sector boundaries divisible by 8 (for 512-byte logical emulation), write amplification degrades performance. `fdisk` automatically enforces 2048-sector (1 MiB) alignment:

```bash
# Check starting sector divisibility by 2048
sudo fdisk -l /dev/sda | awk '$1 ~ /\/dev\// {print $1, $2, ($2 % 2048 == 0 ? "ALIGNED" : "MISALIGNED")}'
```

---

## 7. Exit Status, Environment, and Configuration

### 7.1 Exit Status

| Exit Code | Meaning |
|:---|:---|
| `0` | Success: command completed, listing printed, or partition table committed. |
| `1` | Failure: invalid arguments, hardware I/O error, or permission denied. |

### 7.2 Environment Variables

| Variable | Description |
|:---|:---|
| `LIBFDISK_DEBUG` | Enables debugging output for `libfdisk` backend routines (`all` or comma-separated masks). |
| `FDISK_DEBUG` | Traces interactive UI events and dialog parsing. |

### 7.3 Relevant Kernel Interfaces

| Interface | Purpose |
|:---|:---|
| `BLKRRPART` | Kernel `ioctl` invoked by `fdisk` upon `w` to re-read partition tables. |
| `/proc/partitions` | Kernel view of registered block devices and active partition boundaries. |

---

## 8. Safety, Security, and Portability

### 8.1 Destructive Impact and Execution Safety

`fdisk` modifies low-level disk structures. Writing to the wrong device (`/dev/sda` instead of `/dev/sdb`) permanently overwrites partition headers, filesystem superblocks, and boot records. Always double-check target device names with `lsblk` before running `fdisk`.

### 8.2 Privilege Boundaries

Modifying partition tables requires `CAP_SYS_ADMIN` capability, typically achieved via `sudo` or the `root` user account. Unprivileged users cannot open raw block device nodes for writing.

### 8.3 Signature Wiping Safeguards

Modern `fdisk` automatically detects existing filesystem or RAID signatures on sectors assigned to new partitions. It prompts before wiping existing signatures to prevent accidental data destruction:

```text
Created a new partition 1 of type 'Linux filesystem' and of size 50 GiB.
Partition #1 contains a ext4 signature.
Do you want to remove the signature? [Y]es/[N]o:
```

---

## 9. Best Practices

### 9.1 Always Back Up Partition Tables Before Modification

*Upstream Rationale*: `fdisk(8)` and `sfdisk(8)` manuals emphasize that partition table changes can result in unbootable systems or lost partition boundaries. Always dump the existing partition table prior to running `fdisk`:

```bash
sudo sfdisk -d /dev/sda > sda_partition_backup.dump
```

To restore the backup if an error occurs:

```bash
sudo sfdisk /dev/sda < sda_partition_backup.dump
```

### 9.2 Prefer GPT Over MBR for Modern Deployments

*Upstream Rationale*: MBR (DOS disklabel) is limited to 2 TiB disk capacities, a maximum of four primary partitions, and lacks redundant partition headers. GPT supports disks up to 8 ZiB, provides 128 partition slots by default, and maintains secondary backup headers at the end of the physical disk.

### 9.3 Maintain 1 MiB (2048-Sector) Alignment

*Upstream Rationale*: Modern Advanced Format hard drives (4Kn / 512e) and solid-state drives (SSDs) organize physical storage into 4096-byte pages and multi-megabyte erase blocks. Starting partitions at sector 2048 (1 MiB offset) ensures perfect alignment across all physical page boundaries.

---

## References

1. `fdisk(8)` — Linux man page, util-linux project: <https://man7.org/linux/man-pages/man8/fdisk.8.html>
2. util-linux source repository (`fdisks/fdisk.8.adoc`): <https://github.com/util-linux/util-linux/blob/master/fdisks/fdisk.8.adoc>
3. UEFI Forum, Unified Extensible Firmware Interface (UEFI) Specification (GPT Partitioning): <https://uefi.org/specifications>
