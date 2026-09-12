---
title: "Linux Command Tutorial: free"
date: 2026-09-12T00:00:00+00:00
categories: ['Technology']
tags:
  - 'Linux'
  - 'procps-ng'
  - 'free'
  - 'Linux Command Tutorial'
draft: false
slug: "linux-free-tutorial"
description: "Authoritative reference tutorial for free (procps-ng), detailing RAM and swap metrics, available vs free memory, buff/cache semantics, and procps calculation logic."
upstream_suite: "procps-ng"
upstream_version: "procps-ng 4.0.4"
posix_standard: "None"
research_date: "2026-09-12"
---

The **Linux Command Tutorial** series provides rigorous, upstream-verified references for essential system commands across Linux distributions and UNIX-like environments. Each article focuses on a single executable, combining exhaustive option documentation, verified real-world examples, security boundaries, and best practices directly derived from official source documentation and POSIX standards.

---

## 1. Introduction

> **Upstream**: procps-ng 4.0.4 | **POSIX**: Linux-Specific (procps-ng extension) | **Safety Tier**: safe-read-only | **Scope**: memory-inspection

`free` displays the total amount of free and used physical memory (RAM) and swap memory in the system, as well as the memory used by kernel buffers and page caches. It parses `/proc/meminfo` to report accurate, kernel-derived memory statistics.

- **Upstream Project & Provenance**: Maintained within **procps-ng** (`procps-ng`).
- **Portability & Standards Baseline**: `free` is a Linux-specific utility reflecting Linux virtual memory architecture; it is not defined in POSIX.1-2024.
- **Target Research Implementation**: Audited against **procps-ng 4.0.4** (`free(1)`).
- **Applicability & Lifecycle**: The standard command for checking available memory and diagnosing Out-Of-Memory (OOM) risk.

---

## 2. Syntax and Command Model

### 2.1 Canonical Synopsis

```bash
free [options]
```

### 2.2 Execution Model & Memory Metric Definitions

`free` queries `/proc/meminfo` and computes tabular memory columns:
- **total**: Total installed memory (`MemTotal`).
- **used**: Calculated as `total - free - buff/cache`.
- **free**: Unused memory (`MemFree`) that contains no data.
- **shared**: Memory utilized by `tmpfs` and POSIX shared memory (`Shmem`).
- **buff/cache**: Combined kernel block buffers (`Buffers`) and page cache (`Cached` + `SReclaimable`).
- **available**: The kernel's estimate of memory available for starting new applications without swapping (`MemAvailable`).

---

## 3. Options

### 3.1 Display and Unit Flags

| Short Flag | Long Flag | Description | Default |
|:---|:---|:---|:---|
| `-b` | `--bytes` | Display memory in bytes. | KiB |
| `-k` | `--kibi` | Display memory in kibibytes (1024 bytes). | Default |
| `-m` | `--mebi` | Display memory in mebibytes (1,048,576 bytes). | Off |
| `-g` | `--gibi` | Display memory in gibibytes (1,073,741,824 bytes). | Off |
| `-h` | `--human` | Human-readable output; auto-scales to shortest unit. | Off |
| `-w` | `--wide` | Wide mode: separate `buffers` and `cache` into two columns. | Combined |
| `-s N`| `--seconds N` | Continuously display memory metrics every N seconds. | Single-shot |
| `-c N`| `--count N` | Display N updates when used with `-s`. | Infinite |
| `-t` | `--total` | Display a line showing total RAM + Swap. | Off |

---

## 4. Basic Usage

### 4.1 Quick-Reference Cheatsheet Card

| Operation | Command | Notes |
|:---|:---|:---|
| Human-readable summary | `free -h` | Displays RAM/swap in GiB/MiB |
| Megabytes format | `free -m` | Deterministic numeric output for scripting |
| Wide breakdown | `free -h -w` | Separates `buffers` from `cache` |
| Include total row | `free -h -t` | Appends total line combining RAM + Swap |
| Continuous monitoring | `free -h -s 2 -c 5` | Updates every 2 seconds, 5 times |
| Check available memory | `free -m \| awk '/^Mem:/ {print $7}'` | Extracts usable memory without swapping |

### 4.2 Human-Readable Memory Summary

```bash
free -h
```
```console
               total        used        free      shared  buff/cache   available
Mem:            15Gi       5.8Gi       4.2Gi       412Mi       5.5Gi       9.1Gi
Swap:          2.0Gi          0B       2.0Gi
```

### 4.3 Detailed Wide Output

```bash
free -h -w
```
```console
               total        used        free      shared     buffers       cache   available
Mem:            15Gi       5.8Gi       4.2Gi       412Mi       320Mi       5.2Gi       9.1Gi
Swap:          2.0Gi          0B       2.0Gi
```

---

## 5. Practical Operations

### 5.1 Understanding Why "Free" Memory is Low

> [!IMPORTANT]
> **The Available vs Free Distinction**: Linux aggressively utilizes unallocated memory for disk caching (`buff/cache`) to maximize system performance. A low `free` figure is normal and expected. Always evaluate the **`available`** column, which reflects memory that can be immediately provided to applications without forcing swap activity.

- **Linux Kernel Architecture**: The Linux kernel intentionally borrows unused RAM for disk caching (`buff/cache`) to accelerate disk reads.
- **The Golden Rule**: Look at the **`available`** column, **not** the `free` column.
- If applications require more RAM, the kernel instantaneously reclaims page cache without swapping. The `available` column accurately reflects memory ready to be allocated.

### 5.2 Polling Memory Usage During Load Testing

Monitoring memory allocation every 2 seconds for 5 iterations:

```bash
free -h -s 2 -c 5
```

### 5.3 Automated OOM Health Check in Shell Scripts

Extracting the available memory in megabytes for automated threshold alerting:

```bash
free -m | awk '/^Mem:/ {print $7}'
```
```text
9318
```
- Column 7 represents `available` memory in MiB.

---

## 6. Advanced Usage

### 6.1 Inspecting Kernel Slable Cache Reclaimability

Wide mode (`-w`) exposes `buffers` vs `cache`. In modern Linux kernels, `cache` includes both the standard page cache and `SReclaimable` (reclaimable kernel slab memory used for dentries and inodes). `free` accurately accounts for reclaimable slab in the `available` metric.

---

## 7. Exit Status, Environment, and Configuration

### 7.1 Exit Status Codes

| Exit Code | Meaning |
|:---:|:---|
| `0` | Success: `/proc/meminfo` parsed and displayed cleanly. |
| `>0` | An error occurred (invalid command-line option, `/proc/meminfo` unreadable). |

---

## 8. Safety, Security, and Portability

### 8.1 Linux-Specific Kernel Metrics

> [!NOTE]
> `free` directly parses `/proc/meminfo` and is specific to the Linux kernel. It is not available on BSD or macOS systems (which use `vm_stat` or `sysctl vm`).

---

## 9. Best Practices

1. **Evaluate `available`, Never Just `free`**:
   - *Guidance*: Base all monitoring and automated alerts on the `available` metric.
   - *Authoritative Justification*: procps-ng documentation notes that `free` reflects strictly idle memory, whereas `available` accounts for reclaimable caches.
2. **Use `-h` for Terminal Inspection and `-m` for Scripts**:
   - *Guidance*: Use `free -h` for human eyes and `free -m` or `free -b` for shell scripts.
   - *Authoritative Justification*: `-h` produces changing unit suffixes (`Mi`, `Gi`) that complicate numeric comparisons in shell scripts.
3. **Use `-w` When Diagnosing Filesystem Pressure**:
   - *Guidance*: Pass `-w` to inspect separate buffer and cache allocations.
   - *Authoritative Justification*: Discloses whether disk block buffers or VFS inode/dentry caches are driving memory utilization.

---

## References

1. **procps-ng free(1) Manual**: [https://man7.org/linux/man-pages/man1/free.1.html](https://man7.org/linux/man-pages/man1/free.1.html)
2. **Linux /proc/meminfo Documentation**: [https://docs.kernel.org/filesystems/proc.html#meminfo](https://docs.kernel.org/filesystems/proc.html#meminfo)
