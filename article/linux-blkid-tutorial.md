---
title: "Linux Command Tutorial: blkid"
date: 2026-09-12T00:00:00+00:00
categories: ['Technology']
tags:
  - 'Linux'
  - 'util-linux'
  - 'blkid'
  - 'Linux Command Tutorial'
draft: false
slug: "linux-blkid-tutorial"
description: "Authoritative reference tutorial for blkid (util-linux), detailing block device attribute extraction, UUID and filesystem label probing, token searches, cache management, and fstab integration."
upstream_suite: "util-linux"
upstream_version: "util-linux 2.40"
posix_standard: "None"
research_date: "2026-09-12"
---

The **Linux Command Tutorial** series provides rigorous, upstream-verified references for essential system commands across Linux distributions and UNIX-like environments. Each article focuses on a single executable, combining exhaustive option documentation, verified real-world examples, security boundaries, and best practices directly derived from official source documentation and POSIX standards.

---

## 1. Introduction

`blkid` is a command-line utility for locating and printing block device attributes. It queries filesystem superblocks, volume managers, and partition tables using `libblkid` to extract persistent identifiers such as Universally Unique Identifiers (UUIDs), filesystem labels (`LABEL`), filesystem types (`TYPE`), and partition GUIDs (`PARTUUID`).

- **Upstream Project & Provenance**: Maintained under **util-linux** as part of the `misc-utils` toolchain, powered by `libblkid`.
- **Portability & Standards Baseline**: Linux-specific block device identification tool; not standardized in IEEE Std 1003.1-2024 (POSIX.1-2024).
- **Target Research Implementation**: Audited against **util-linux 2.40** (`blkid(8)`).
- **Applicability & Lifecycle**: The standard utility for obtaining persistent device tokens required for `/etc/fstab`, bootloader entries, and udev rules.

---

## 2. Syntax and Command Model

### 2.1 Canonical Synopsis

```bash
blkid [options] [device...]
blkid -t token [options] [device...]
blkid -L label
blkid -U uuid
```

### 2.2 Probing Architecture & Cache Operation

`blkid` operates in two primary probing modes:
- **Cached Probing (Default)**: Reads attributes from the system cache file (`/run/blkid/blkid.tab` or `/etc/blkid.tab`). It verifies that listed devices still exist in `/proc/partitions` and updates the cache if run with root privileges.
- **Low-Level Probing (`-p`)**: Bypasses the cache entirely and reads directly from the physical block device superblock, probing magic numbers, filesystem headers, and RAID metadata.

---

## 3. Options

### 3.1 Identification and Token Matching

| Option | Long Option | Description | Default |
|:---|:---|:---|:---|
| `-t token` | `--match-token token` | Search for devices matching `NAME=value` (e.g. `TYPE=ext4`, `LABEL=data`). | All devices |
| `-l` | `--list-one` | Look up only the first device matching the specified `-t` token. | All matches |
| `-L label` | `--label label` | Look up device by filesystem label (equivalent to `-l -t LABEL=label -o device`). | Standard lookup |
| `-U uuid` | `--uuid uuid` | Look up device by UUID (equivalent to `-l -t UUID=uuid -o device`). | Standard lookup |
| `-n list` | `--match-types list` | Filter probe to specific filesystem types (comma-separated). | All filesystems |
| `-u list` | `--usages list` | Filter probe to specific usage categories (e.g. `filesystem`, `raid`, `crypto`). | All usages |

### 3.2 Output Formatting and Cache Control

| Option | Long Option | Description | Default |
|:---|:---|:---|:---|
| `-o format` | `--output format` | Specify output format: `full`, `value`, `device`, `export`, `list`, or `udev`. | `full` |
| `-s tag` | `--match-tag tag` | Display only specified tag (e.g. `-s UUID`, `-s TYPE`). May be repeated. | All tags |
| `-p` | `--probe` | Perform low-level superblock probing directly on device, bypassing cache. | Cache enabled |
| `-i` | `--info` | Print I/O limits and alignment data (I/O size, alignment offset). | Standard attributes |
| `-k` | `--list-filesystems`| List all recognized filesystems and partition table types and exit. | Off |
| `-c file` | `--cache-file file` | Read/write from specified cache file (`/dev/null` disables cache entirely). | System cache |
| `-d` | `--no-cache` | Don't verify cache (do not check whether cached devices exist). | Verification on |
| `-g` | `--garbage-collect` | Perform garbage collection on blkid cache, removing dead devices. | Off |

---

## 4. Basic Usage

### 4.1 Listing All Block Device Attributes

Running `blkid` without arguments lists all recognized block devices and their associated metadata tokens:

```console
$ sudo blkid
/dev/sda1: UUID="4A2F-89E1" BLOCK_SIZE="512" TYPE="vfat" PARTLABEL="EFI System" PARTUUID="19a0f421-4d32-45e8-b83a-d435789a42e1"
/dev/sda2: UUID="d281a8b1-36ce-4458-9584-913dcad2e7b1" BLOCK_SIZE="4096" TYPE="ext4" PARTUUID="234c98d1-419b-4b12-921c-423589cba112"
/dev/sda3: UUID="c80f12da-4b71-496a-b27e-85a03eef3a82" BLOCK_SIZE="4096" TYPE="ext4" PARTUUID="385b12da-519c-4912-984e-512398412034"
/dev/sdb1: LABEL="DATA_STORE" UUID="b6a9c1e2-5401-447a-9a99-4d6428c40ff2" BLOCK_SIZE="4096" TYPE="xfs" PARTUUID="9fa12345-6789-abcd-ef01-23456789abcd"
```

### 4.2 Querying a Specific Block Device

Inspect the tokens of a single partition:

```console
$ sudo blkid /dev/sda2
/dev/sda2: UUID="d281a8b1-36ce-4458-9584-913dcad2e7b1" BLOCK_SIZE="4096" TYPE="ext4" PARTUUID="234c98d1-419b-4b12-921c-423589cba112"
```

---

## 5. Practical Operations

### 5.1 Extracting Pure UUID Value for `/etc/fstab`

Combine `-s UUID` with `-o value` to retrieve the bare UUID string without quotation marks or variable names, ideal for scripting:

```console
$ sudo blkid -s UUID -o value /dev/sda2
d281a8b1-36ce-4458-9584-913dcad2e7b1
```

Directly construct an `/etc/fstab` entry:

```bash
UUID=$(sudo blkid -s UUID -o value /dev/sda2)
echo "UUID=$UUID /boot ext4 defaults 0 2" | sudo tee -a /etc/fstab
```

### 5.2 Locating Device by Filesystem Label or UUID

Find the device node corresponding to a filesystem volume label:

```console
$ sudo blkid -L DATA_STORE
/dev/sdb1
```

Resolve a known UUID to its current active kernel device node:

```console
$ sudo blkid -U d281a8b1-36ce-4458-9584-913dcad2e7b1
/dev/sda2
```

### 5.3 Filtering Devices by Filesystem Type

Identify all partitions formatted with `xfs`:

```console
$ sudo blkid -t TYPE=xfs
/dev/sdb1: LABEL="DATA_STORE" UUID="b6a9c1e2-5401-447a-9a99-4d6428c40ff2" BLOCK_SIZE="4096" TYPE="xfs" PARTUUID="9fa12345-6789-abcd-ef01-23456789abcd"
```

### 5.4 Low-Level Probing After Reformatting

When a block device has been reformatted with `mkfs`, the system cache might return old superblock tokens. Use `-p` to force an immediate hardware read:

```console
$ sudo blkid -p /dev/sdb1
/dev/sdb1: LABEL="NEW_STORE" UUID="a1b2c3d4-e5f6-7890-1234-567890abcdef" BLOCK_SIZE="4096" TYPE="ext4" USAGE="filesystem" PART_ENTRY_SCHEME="gpt" PART_ENTRY_NAME="data" PART_ENTRY_UUID="9fa12345-6789-abcd-ef01-23456789abcd" PART_ENTRY_TYPE="0fc63daf-8483-4772-8e79-3d69d8477de4" PART_ENTRY_NUMBER="1" PART_ENTRY_OFFSET="2048" PART_ENTRY_SIZE="3907026944" PART_ENTRY_DISK="8:16"
```

---

## 6. Advanced Usage

### 6.1 Shell Variable Export Format (`-o export`)

Generate unambiguous key-value pairs formatted for direct shell sourcing:

```console
$ sudo blkid -o export /dev/sda2
DEVNAME=/dev/sda2
UUID=d281a8b1-36ce-4458-9584-913dcad2e7b1
BLOCK_SIZE=4096
TYPE=ext4
PARTUUID=234c98d1-419b-4b12-921c-423589cba112
```

Evaluate directly within a shell script:

```bash
eval "$(sudo blkid -o export /dev/sda2)"
echo "Mounted filesystem type is: $TYPE on partition: $PARTUUID"
```

### 6.2 Udev Environment Format (`-o udev`)

Display device properties formatted as environment variables matching udev rules:

```console
$ sudo blkid -o udev /dev/sda1
ID_FS_UUID=4A2F-89E1
ID_FS_UUID_ENC=4A2F-89E1
ID_FS_BLOCK_SIZE=512
ID_FS_TYPE=vfat
ID_PART_ENTRY_SCHEME=gpt
ID_PART_ENTRY_NAME=EFI\x20System
ID_PART_ENTRY_UUID=19a0f421-4d32-45e8-b83a-d435789a42e1
ID_PART_ENTRY_TYPE=c12a7328-f81f-11d2-ba4b-00a0c93ec93b
ID_PART_ENTRY_NUMBER=1
```

### 6.3 Cache Maintenance and Garbage Collection

When storage devices are detached or hot-unplugged, the cache file may retain obsolete entries. Run `-g` to remove deleted devices:

```console
$ sudo blkid -g
```

---

## 7. Exit Status, Environment, and Configuration

### 7.1 Exit Status

| Exit Code | Meaning |
|:---|:---|
| `0` | Success: requested device or token found and printed. |
| `2` | Not found: specified token, label, UUID, or device could not be located. |
| `4` | Error: invalid arguments, usage error, or fatal I/O failure. |

### 7.2 Environment Variables

| Variable | Description |
|:---|:---|
| `LIBBLKID_DEBUG` | Enables debugging output for `libblkid` probing passes (`all` or bitmasks). |
| `BLKID_DEBUG` | Traces command-line parsing and cache management. |

### 7.3 Cache File Locations

| File Path | Role |
|:---|:---|
| `/run/blkid/blkid.tab` | Ephemeral runtime cache file on modern systemd-based Linux systems. |
| `/etc/blkid.tab` | Legacy static cache file used on older distributions without tmpfs `/run`. |

---

## 8. Safety, Security, and Portability

### 8.1 Read-Only Safety Profile

`blkid` is strictly a non-destructive query and probing utility. It does not alter filesystem data, partition tables, or block device payloads.

### 8.2 Privilege Boundaries

- Standard unprivileged users can query `/etc/blkid.tab` or `/run/blkid/blkid.tab` to inspect previously probed attributes.
- Low-level direct probing (`-p`) or updating stale cache entries requires `root` privileges (`CAP_SYS_ADMIN`) because reading raw block devices requires access to restricted `/dev` device nodes.

### 8.3 Portability Constraints

`blkid` is specific to Linux and relies on `libblkid`. macOS and BSD distributions do not provide `blkid`; similar functionality on FreeBSD is provided by `glabel` or `geom`.

---

## 9. Best Practices

### 9.1 Always Use `UUID=` in `/etc/fstab` Instead of Device Node Paths

*Upstream Rationale*: Linux device node paths (such as `/dev/sda1` or `/dev/nvme0n1p2`) are assigned dynamically at boot time based on controller enumeration speed. Adding a drive or altering SATA/NVMe cabling changes device node names, causing boot failure. UUIDs remain invariant across hardware alterations.

### 9.2 Use `-p` (Low-Level Probe) Immediately After Reformatting

*Upstream Rationale*: `blkid(8)` documents that the default cache may retain outdated superblock identifiers if a partition was recently overwritten with `mkfs` or `dd`. Always supply `-p` or pass `-c /dev/null` when probing freshly formatted storage.

### 9.3 Extract Clean Tokens With `-s UUID -o value` in Scripts

*Upstream Rationale*: Parsing standard `blkid` output using regular expressions or `awk` is prone to errors when volume labels contain spaces or special characters. Specifying `-s UUID -o value` guarantees that `blkid` returns only the isolated, unquoted token value.

---

## References

1. `blkid(8)` — Linux man page, util-linux project: <https://man7.org/linux/man-pages/man8/blkid.8.html>
2. util-linux source repository (`misc-utils/blkid.8.adoc`): <https://github.com/util-linux/util-linux/blob/master/misc-utils/blkid.8.adoc>
3. `libblkid` documentation and source code: <https://github.com/util-linux/util-linux/tree/master/libblkid>
