---
title: "Linux Command Tutorial: lsblk"
date: 2026-09-12T00:00:00+00:00
categories: ['Technology']
tags:
  - 'Linux'
  - 'util-linux'
  - 'lsblk'
  - 'Linux Command Tutorial'
draft: false
slug: "linux-lsblk-tutorial"
description: "Authoritative reference tutorial for lsblk (util-linux), detailing block device topology discovery, partition hierarchies, JSON output, storage sizes, and filesystem metadata extraction."
upstream_suite: "util-linux"
upstream_version: "util-linux 2.40"
posix_standard: "None"
research_date: "2026-09-12"
---

The **Linux Command Tutorial** series provides rigorous, upstream-verified references for essential system commands across Linux distributions and UNIX-like environments. Each article focuses on a single executable, combining exhaustive option documentation, verified real-world examples, security boundaries, and best practices directly derived from official source documentation and POSIX standards.

---

## 1. Introduction

> **Upstream**: util-linux 2.40 | **POSIX**: Linux-Specific (util-linux extension) | **Safety Tier**: safe-read-only | **Scope**: block-device-inspection

`lsblk` lists information about all available or specified block devices. It interrogates the Linux `sysfs` filesystem (`/sys/block`, `/sys/class/block`) and the `udev` database, rendering hierarchical tree relationships between physical disks, partitions, LVM logical volumes, Software RAID arrays, and loop devices.

- **Upstream Project & Provenance**: Maintained within **util-linux** as part of the core `misc-utils` toolchain.
- **Portability & Standards Baseline**: Linux-specific utility dependent on Linux `sysfs` and `udev` architectures; not standardized in IEEE Std 1003.1-2024 (POSIX.1-2024).
- **Target Research Implementation**: Audited against **util-linux 2.40** (`lsblk(8)`).
- **Applicability & Lifecycle**: The standard command for storage discovery, replacing legacy manual inspection of `/proc/partitions`.

---

## 2. Syntax and Command Model

### 2.1 Canonical Synopsis

```bash
lsblk [options] [device...]
```

### 2.2 Execution & Data Model

`lsblk` traverses the kernel's block layer representation:
- By default, it displays block devices in a tree structure depicting master/slave and parent/partition relationships.
- It can query physical block devices (e.g., `/dev/sda`, `/dev/nvme0n1`), virtual block devices (e.g., `/dev/loop0`, `/dev/zram0`), and mapped device nodes (Device Mapper / LVM / LUKS).
- Attributes such as filesystem UUIDs and labels are resolved through `libblkid`, while topology metrics (I/O alignment, sector sizes) are extracted directly from `sysfs`.

---

## 3. Options

### 3.1 Device Filtering and Selection

| Option | Long Option | Description | Default |
|:---|:---|:---|:---|
| `-a` | `--all` | List all devices, including empty devices and unallocated RAM disks. | Excludes empty |
| `-d` | `--nodeps` | Do not print slave devices or partitions (show top-level disks only). | Hierarchical tree |
| `-e list` | `--exclude list` | Exclude devices matching comma-separated major numbers (e.g. `-e 7` for loop). | No exclusions |
| `-I list` | `--include list` | Include only devices matching comma-separated major device numbers. | All block devices |
| `-s` | `--inverse` | Print device dependencies in inverse order (partitions/holders first). | Parent first |
| `-z` | `--zoned` | Print zoned block device information (e.g. host-aware, host-managed). | Standard block |

### 3.2 Output Formatting and Attributes

| Option | Long Option | Description | Default |
|:---|:---|:---|:---|
| `-b` | `--bytes` | Print device `SIZE` in exact bytes rather than human-readable units. | Human-readable (G, M) |
| `-D` | `--discard` | Print device discard (TRIM/UNMAP) capabilities and alignment. | Off |
| `-f` | `--fs` | Output filesystem information (FSTYPE, FSSIZE, FSAVAIL, FSUSE%, MOUNTPOINTS, LABEL, UUID). | Basic columns |
| `-J` | `--json` | Produce machine-readable JSON output. | Text table |
| `-l` | `--list` | Output in flat list format instead of tree format. | Tree format |
| `-m` | `--perms` | Output device permission attributes (OWNER, GROUP, MODE). | Off |
| `-n` | `--noheadings` | Suppress column header row. | Headers printed |
| `-o list` | `--output list` | Output specified comma-separated columns (e.g. `NAME,SIZE,TYPE,MOUNTPOINTS`). | Standard columns |
| `-p` | `--paths` | Print full device node paths (e.g. `/dev/sda1` instead of `sda1`). | Short names |
| `-P` | `--pairs` | Output key="value" pairs suitable for shell evaluation. | Tabular text |
| `-r` | `--raw` | Output raw, unaligned space-separated values. | Tabular text |
| `-t` | `--topology` | Print block device topology metrics (alignment, minimum/optimal I/O size). | Off |
| `-x col` | `--sort col` | Sort output rows according to specified column name. | Device order |

---

## 4. Basic Usage

### 4.1 Quick-Reference Cheatsheet Card

| Operation | Command | Notes |
|:---|:---|:---|
| List block device tree | `lsblk` | Default hierarchy of disks, partitions, LVM |
| Filesystems and UUIDs | `lsblk -f` | Displays FSTYPE, LABEL, UUID, mountpoints |
| Physical disks only | `lsblk -d -o NAME,MODEL,SIZE,ROTA,TRAN` | Suppresses partitions; shows drive specs |
| Exclude loop devices | `lsblk -e 7` | Cleans clutter from snap/container mounts |
| Machine-readable JSON | `lsblk -J -o NAME,SIZE,TYPE,MOUNTPOINTS` | Structured JSON output for automation |
| Exact byte sizing | `lsblk -b -o NAME,SIZE` | Outputs raw integer bytes without unit suffixes |
| SSD TRIM / discard support | `lsblk -D` | Audits hardware TRIM and unmap capabilities |

### 4.2 Default Storage Tree

Running `lsblk` without parameters displays all non-empty block devices with their default attributes (`NAME`, `MAJ:MIN`, `RM`, `SIZE`, `RO`, `TYPE`, `MOUNTPOINTS`):

```bash
lsblk
```
```console
NAME        MAJ:MIN RM   SIZE RO TYPE MOUNTPOINTS
sda           8:0    0 476.9G  0 disk 
├─sda1        8:1    0   512M  0 part /boot/efi
├─sda2        8:2    0     1G  0 part /boot
└─sda3        8:3    0 475.4G  0 part 
  ├─vg-root 254:0    0    50G  0 lvm  /
  └─vg-home 254:1    0 425.4G  0 lvm  /home
sdb           8:16   0   1.8T  0 disk 
└─sdb1        8:17   0   1.8T  0 part /data
sr0          11:0    1  1024M  0 rom  
```

### 4.3 Inspecting a Specific Disk

Target a specific drive to isolate its partition scheme and volume groups:

```bash
lsblk /dev/sda
```
```console
NAME        MAJ:MIN RM   SIZE RO TYPE MOUNTPOINTS
sda           8:0    0 476.9G  0 disk 
├─sda1        8:1    0   512M  0 part /boot/efi
├─sda2        8:2    0     1G  0 part /boot
└─sda3        8:3    0 475.4G  0 part 
  ├─vg-root 254:0    0    50G  0 lvm  /
  └─vg-home 254:1    0 425.4G  0 lvm  /home
```

---

## 5. Practical Operations

### 5.1 Inspecting Filesystems, UUIDs, and Mount Points

Use `-f` (`--fs`) to audit filesystems, volume labels, and UUID identifiers across all partitions:

```bash
lsblk -f
```
```console
NAME        FSTYPE      FSVER LABEL       UUID                                 FSAVAIL FSUSE% MOUNTPOINTS
sda                                                                                           
├─sda1      vfat        FAT32 BOOT_EFI    4A2F-89E1                             504.9M     1% /boot/efi
├─sda2      ext4        1.0   BOOT        d281a8b1-36ce-4458-9584-913dcad2e7b1  750.2M    21% /boot
└─sda3      LVM2_member LVM2  vg          9F4C2D-318e-4a6c-94df-12ac94c8e761                  
  ├─vg-root ext4        1.0   ROOT        c80f12da-4b71-496a-b27e-85a03eef3a82   32.4G    29% /
  └─vg-home xfs               HOME        e3124578-838d-4f16-9284-8846c92aa7d1  283.4G    39% /home
sdb                                                                                           
└─sdb1      xfs               DATA        b6a9c1e2-5401-447a-9a99-4d6428c40ff2    1.2T    33% /data
```

### 5.2 Physical Disk Inventory Without Partition Noise

When performing hardware inventory, identify physical drives, transport types, and rotation status using `-d` (`--nodeps`):

```bash
lsblk -d -o NAME,MODEL,SIZE,ROTA,TRAN,TYPE
```
```console
NAME  MODEL                SIZE ROTA TRAN   TYPE
sda   Samsung SSD 980 500G 476.9G    0 nvme   disk
sdb   WDC WD20EZAZ-00L9GB0   1.8T    1 sata   disk
```
*Note*: `ROTA=0` indicates non-rotational media (SSD/NVMe), while `ROTA=1` designates rotational HDDs.

### 5.3 Auditing SSD TRIM / Discard Support

Verify whether attached block storage devices support TRIM/discard operations via `-D` (`--discard`):

```bash
lsblk -D
```
```console
NAME        DISC-ALN DISC-GRAN DISC-MAX DISC-ZERO
sda                0      512B       2G         0
├─sda1             0      512B       2G         0
├─sda2             0      512B       2G         0
└─sda3             0      512B       2G         0
  ├─vg-root        0      512B       2G         0
  └─vg-home        0      512B       2G         0
sdb                0        0B       0B         0
```
*Note*: Non-zero values in `DISC-MAX` indicate active hardware discard capability.

### 5.4 Filtering Out Loopback Clutter

Systems running `snapd` or container runtimes often display dozens of `/dev/loop` devices. Suppress them by excluding major device number `7`:

```bash
lsblk -e 7
```
```console
NAME   MAJ:MIN RM   SIZE RO TYPE MOUNTPOINTS
sda      8:0    0 476.9G  0 disk 
├─sda1   8:1    0   512M  0 part /boot/efi
└─sda2   8:2    0 476.4G  0 part /
```

---

## 6. Advanced Usage

### 6.1 Machine-Readable JSON Output for Automation

Export comprehensive block device topology directly to JSON format with `-J` (`--json`):

```bash
lsblk -J -o NAME,SIZE,TYPE,FSTYPE,MOUNTPOINTS /dev/sda1
```
```json
{
   "blockdevices": [
      {
         "name": "sda1",
         "size": "512M",
         "type": "part",
         "fstype": "vfat",
         "mountpoints": [
            "/boot/efi"
         ]
      }
   ]
}
```

Parse and query storage topology using `jq`:

```bash
lsblk -J -o NAME,FSTYPE,MOUNTPOINTS | jq -r '.blockdevices[] | .. | objects | select(.fstype=="ext4") | .mountpoints[]'
```

### 6.2 Key-Value Pairs for Shell Script Evaluation

Generate unambiguous key-value pairs formatted with `-P` (`--pairs`):

```bash
lsblk -P -o NAME,SIZE,TYPE,UUID /dev/sda1
```
```text
NAME="sda1" SIZE="512M" TYPE="part" UUID="4A2F-89E1"
```

Iterate safely across block devices within a bash loop:

```bash
while IFS= read -r line; do
    eval "$line"
    echo "Device /dev/$NAME has UUID $UUID and size $SIZE"
done < <(lsblk -P -o NAME,SIZE,UUID -n -p /dev/sda*)
```

### 6.3 Exact Byte Sizing for Capacity Mathematics

For exact partitioning calculations, suppress human-friendly unit suffixes (`G`, `M`) and output raw integer byte counts with `-b`:

```bash
lsblk -b -n -o NAME,SIZE /dev/sda1
```
```text
sda1 536870912
```

---

## 7. Exit Status, Environment, and Configuration

### 7.1 Exit Status

| Exit Code | Meaning |
|:---|:---|
| `0` | Success: device information successfully gathered and printed. |
| `1` | Failure: device not found, invalid column specified, or kernel sysfs access error. |

### 7.2 Environment Variables

| Variable | Description |
|:---|:---|
| `LSBLK_DEBUG` | Enables internal execution tracing (e.g. `all` or numeric masks). |
| `LIBBLKID_DEBUG` | Traces `libblkid` probing and token extraction routines. |
| `LIBMOUNT_DEBUG` | Traces mountpoint identification and table parsing. |

### 7.3 Relevant Kernel Interfaces

| Path | Purpose |
|:---|:---|
| `/sys/block` | Directory containing symlinks to all top-level kernel block devices. |
| `/sys/dev/block` | Lookup directory indexing devices by `<major>:<minor>` number. |
| `/run/udev/data` | `udev` database holding hardware metadata, vendor strings, and serial numbers. |

---

## 8. Safety, Security, and Portability

### 8.1 Read-Only Operation

> [!NOTE]
> `lsblk` is a completely non-destructive query tool. It gathers block device metadata directly from `sysfs` and `udev` without writing to or locking storage media, and operates safely under unprivileged accounts.

### 8.2 Safe Identification Before Destructive Operations

> [!WARNING]
> Always verify block device identities with `lsblk -o NAME,SIZE,MODEL,TRAN` prior to issuing destructive commands (`mkfs`, `fdisk`, `dd`). Device path letters (`/dev/sda`, `/dev/sdb`) can shift non-deterministically across reboots or after bus re-scans.

### 8.3 Portability Constraints

`lsblk` depends strictly on the Linux kernel `/sys` hierarchy and `udev`. It is not present on BSD distributions or macOS. Cross-platform scripts should use POSIX `df` or platform-specific tools (`geom` on FreeBSD, `diskutil` on macOS).

---

## 9. Best Practices

### 9.1 Always Use `-b` or `-J` in Automation Scripts

*Upstream Rationale*: `lsblk(8)` notes that default sizes use binary prefixes (`KiB`, `MiB`, `GiB`, printed as `K`, `M`, `G`) with fractional rounding. Performing capacity arithmetic or equality checks against human-readable strings introduces rounding errors. Always specify `-b` (`--bytes`) or `-J` (`--json`) for machine consumption.

### 9.2 Filter Virtual Loop Devices With `-e 7` on Container Hosts

*Upstream Rationale*: Package managers like Snap and container systems dynamically attach loopback devices, cluttering default terminal output with dozens of immutable squashfs mounts. Passing `-e 7` excludes loop devices by their standard major device number, restoring focus to physical disks.

### 9.3 Identify Partitions by UUID Rather Than Device Nodes

*Upstream Rationale*: Linux device node assignments (`/dev/sdX`) are non-deterministic across hardware topology changes, bus re-scans, and reboots. Use `lsblk -f` or `lsblk -o NAME,UUID` to extract permanent filesystem UUIDs for persistent configuration in `/etc/fstab`.

---

## References

1. `lsblk(8)` — Linux man page, util-linux project: <https://man7.org/linux/man-pages/man8/lsblk.8.html>
2. util-linux source repository (`misc-utils/lsblk.8.adoc`): <https://github.com/util-linux/util-linux/blob/master/misc-utils/lsblk.8.adoc>
3. Linux Kernel Block Layer Documentation: <https://docs.kernel.org/block/index.html>
