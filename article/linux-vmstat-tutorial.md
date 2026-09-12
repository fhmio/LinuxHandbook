---
title: "Linux Command Tutorial: vmstat"
date: 2026-09-12T00:00:00+00:00
categories: ['Technology']
tags:
  - 'Linux'
  - 'procps-ng'
  - 'vmstat'
  - 'Linux Command Tutorial'
draft: false
slug: "linux-vmstat-tutorial"
description: "Authoritative reference tutorial for vmstat (procps-ng), detailing virtual memory statistics, run queue states, swap activity (si/so), and I/O bottlenecks."
upstream_suite: "procps-ng"
upstream_version: "procps-ng 4.0.4"
posix_standard: "None"
research_date: "2026-09-12"
---

The **Linux Command Tutorial** series provides rigorous, upstream-verified references for essential system commands across Linux distributions and UNIX-like environments. Each article focuses on a single executable, combining exhaustive option documentation, verified real-world examples, security boundaries, and best practices directly derived from official source documentation and POSIX standards.

---

## 1. Introduction

> **Upstream**: procps-ng 4.0.4 | **POSIX**: De-facto Standard (Not POSIX standardized) | **Safety Tier**: safe-read-only | **Scope**: virtual-memory-statistics

`vmstat` (virtual memory statistics) reports point-in-time and continuous information about processes, memory, paging, block I/O, traps, and CPU activity. It provides a compact, single-line snapshot of overall operating system performance and resource contention.

- **Upstream Project & Provenance**: Maintained within **procps-ng** (`procps-ng`).
- **Portability & Standards Baseline**: `vmstat` is an industry-standard UNIX monitoring tool originating from BSD; not defined in POSIX.1-2024.
- **Target Research Implementation**: Audited against **procps-ng 4.0.4** (`vmstat(8)`).
- **Applicability & Lifecycle**: The preferred tool for rapid triage of performance bottlenecks (CPU vs Memory vs Disk I/O).

---

## 2. Syntax and Command Model

### 2.1 Canonical Synopsis

```bash
vmstat [options] [delay [count]]
```

### 2.2 First Line Rule

> [!IMPORTANT]
> **The First Line Rule**: The very first row of statistics output by `vmstat` reflects cumulative averages since the last system boot, **not** current activity. Always discard or ignore the first line when diagnosing active performance issues.

- Subsequent lines display statistics calculated strictly over the specified `delay` sampling interval.
- Therefore, when diagnosing live performance, **ignore the first line** and inspect the subsequent sampling lines.

---

## 3. Options

### 3.1 Primary Flags

| Flag | Description | Default |
|:---|:---|:---|
| `-a` | Active/inactive memory display (displays `inact` and `active` memory). | Buffer/cache |
| `-d` | Display disk statistics. | Memory/CPU table |
| `-f` | Display total number of forks since boot. | N/A |
| `-m` | Display slabinfo (kernel memory allocations). | Standard |
| `-s` | Display a detailed summary table of memory events and counters. | Stream |
| `-S unit` | Output units: `k`, `K`, `m`, `M` (1000 or 1024 bytes). | `K` (1024 bytes) |
| `-t` | Append timestamp to each line of output. | No timestamp |
| `-w` | Wide mode: expands column widths for systems with large RAM. | Standard |

---

## 4. Basic Usage

### 4.1 Quick-Reference Cheatsheet Card

| Operation | Command | Notes |
|:---|:---|:---|
| Sample every 2 seconds | `vmstat 2` | Continuous performance telemetry |
| Sample 5 iterations | `vmstat 1 5` | Updates 5 times at 1-second intervals |
| Wide output with timestamps | `vmstat -t -w 1` | Prevents column overflow and adds timestamp |
| Active/inactive memory | `vmstat -a 2` | Shows active vs inactive memory pages |
| Disk I/O statistics | `vmstat -d` | Reports reads, writes, and sectors per drive |
| Memory summary table | `vmstat -s` | Event counters and cumulative stats |

### 4.2 Continuous Sampling Every 2 Seconds

```bash
vmstat 2 4
```
```console
procs -----------memory---------- ---swap-- -----io---- -system-- ------cpu-----
 r  b   swpd   free   buff  cache   si   so    bi    bo   in   cs us sy id wa st
 1  0      0 481200 320400 5240000    0    0     4    25   45  112  1  1 98  0  0
 2  0      0 481150 320400 5240020    0    0     0   140 1250 2410 12  4 84  0  0
 1  0      0 481100 320400 5240020    0    0     0    80 1190 2380 10  3 87  0  0
 0  0      0 481220 320400 5240020    0    0     0     0  980 1950  4  2 94  0  0
```

---

## 5. Practical Operations

### 5.1 Diagnosing Memory Starvation via `si` and `so`

> [!WARNING]
> If `so` (swap-out) consistently exceeds zero over multiple sampling intervals, physical memory is exhausted and the kernel is forced to page out memory to disk, leading to severe latency and thrashing.

- `si` (Swap-In): Memory paged in from swap disk per second.
- `so` (Swap-Out): Memory paged out to swap disk per second.
- **Rule of Thumb**: Non-zero values in `so` indicate that the system has exhausted physical RAM and is actively writing memory pages to disk swap, causing severe performance degradation.

### 5.2 Detecting CPU Run Queue Saturation via `r`

- `r` (Run queue): The number of runnable processes either running or waiting for CPU runtime.
- **Analysis**: If `r` consistently exceeds the total number of hardware CPU cores (e.g., `r = 16` on an 8-core machine), the system is CPU-saturated and tasks are queuing for execution.

### 5.3 Identifying Disk Bottlenecks via `b` and `wa`

- `b` (Blocked): Number of processes in uninterruptible sleep (`D` state in `ps`).
- `wa` (Wait I/O): Percentage of CPU time waiting for disk I/O.
- **Analysis**: High `b` paired with high `wa` indicates disk saturation or a hung NFS mount, not a CPU shortage.

---

## 6. Advanced Usage

### 6.1 Timestamped Monitoring for Log Bundles

Appending precise timestamps to each line:

```bash
vmstat -t -w 1 3
```
```console
procs -----------------------memory---------------------- ---swap-- -----io---- -system-- --------cpu-------- -----timestamp-----
 r  b       swpd       free       buff      cache   si   so    bi    bo   in     cs  us  sy  id  wa  st                 UTC
 1  0          0    4927488     328089    5365760    0    0     4    25   45    112   1   1  98   0   0 2026-09-12 11:35:00
 0  0          0    4927488     328089    5365760    0    0     0    64 1210   2340   8   2  90   0   0 2026-09-12 11:35:01
 0  0          0    4927488     328089    5365760    0    0     0     0  990   1980   4   1  95   0   0 2026-09-12 11:35:02
```

---

## 7. Exit Status, Environment, and Configuration

### 7.1 Exit Status Codes

| Exit Code | Meaning |
|:---:|:---|
| `0` | Clean execution. |
| `>0` | Invalid interval parameter or missing `/proc` permissions. |

---

## 8. Safety, Security, and Portability

### 8.1 Zero Overhead

`vmstat` reads directly from `/proc/stat` and `/proc/vmstat`. It produces negligible CPU and I/O overhead, making it safe to run continuously in production performance diagnostics.

---

## 9. Best Practices

1. **Always Ignore the First Output Line**:
   - *Guidance*: When analyzing live metrics, discard line 1.
   - *Authoritative Justification*: Upstream documentation confirms line 1 represents historical reboot averages.
2. **Monitor `si`/`so` for Early OOM Detection**:
   - *Guidance*: Alert if `so` remains above 0 for more than 10 consecutive seconds.
   - *Authoritative Justification*: Sustained swapping leads to kernel thrashing and high latency.
3. **Use `-w` (Wide Mode) on Modern High-Memory Servers**:
   - *Guidance*: Pass `vmstat -w` on servers with >32 GB RAM.
   - *Authoritative Justification*: Prevents large byte counters from shifting column alignments.

---

## References

1. **procps-ng vmstat(8) Manual**: [https://man7.org/linux/man-pages/man8/vmstat.8.html](https://man7.org/linux/man-pages/man8/vmstat.8.html)
2. **Linux Virtual Memory Architecture**: [https://docs.kernel.org/admin-guide/sysctl/vm.html](https://docs.kernel.org/admin-guide/sysctl/vm.html)
