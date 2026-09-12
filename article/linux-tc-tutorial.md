---
title: "Linux Command Tutorial: tc"
date: 2026-09-12T00:00:00+00:00
categories: ['Technology']
tags:
  - 'Linux'
  - 'iproute2'
  - 'tc'
  - 'Linux Command Tutorial'
draft: false
slug: "linux-tc-tutorial"
description: "Authoritative reference tutorial for tc (iproute2), detailing Linux kernel traffic control, queuing disciplines (qdiscs), classful traffic shaping, filter classifiers, eBPF attachments, and bufferbloat mitigation."
upstream_suite: "iproute2"
upstream_version: "iproute2 6.13"
posix_standard: "None"
research_date: "2026-09-12"
---

The **Linux Command Tutorial** series provides rigorous, upstream-verified references for essential system commands across Linux distributions and UNIX-like environments. Each article focuses on a single executable, combining exhaustive option documentation, verified real-world examples, security boundaries, and best practices directly derived from official source documentation and POSIX standards.

---

## 1. Introduction

> **Upstream**: iproute2 (iproute2 6.13) | **POSIX**: Linux-Specific (iproute2 extension) | **Safety Tier**: privileged-network-state-altering | **Scope**: traffic-control-qos

`tc` (Traffic Control) configures the Linux kernel networking subsystem's packet scheduling, queuing disciplines (qdiscs), traffic shaping, policing, and prioritization mechanisms. It controls how packets are queued, delayed, throttled, or dropped on network interfaces.

- **Upstream Project & Provenance**: Maintained within **iproute2** (`iproute2`) in direct coordination with the Linux kernel networking subsystem.
- **Portability & Standards Baseline**: Linux-specific kernel interface utility; not standardized in IEEE Std 1003.1-2024 (POSIX.1-2024).
- **Target Research Implementation**: Audited against **iproute2 6.13** (`tc(8)`).
- **Applicability & Lifecycle**: The definitive tool for Quality of Service (QoS), WAN simulation, bandwidth rate limiting, and eBPF packet filter attachment.

---

## 2. Syntax and Command Model

### 2.1 Canonical Synopsis

```bash
tc [OPTIONS] OBJECT { COMMAND | help }
tc [OPTIONS] qdisc [ add | change | replace | del ] dev DEV [ root | ingress | parent CLASSID ] [ handle QHANDLE ] [ qdisc-type ] [ qdisc-args ]
tc [OPTIONS] class [ add | change | replace | del ] dev DEV parent CLASSID [ classid CLASSID ] [ qdisc-type ] [ qdisc-args ]
tc [OPTIONS] filter [ add | change | replace | del ] dev DEV [ parent CLASSID | root ] [ protocol PROTO ] [ prio PRIO ] [ filter-type ] [ filter-args ]
```

### 2.2 Core Architectural Objects

Linux kernel traffic control is organized around four fundamental building blocks:

```text
       +---------------------------------------------+
       |             Root Qdisc (handle 1:)          |
       +---------------------------------------------+
                             |
       +---------------------------------------------+
       |             Root Class (classid 1:1)        |
       +---------------------------------------------+
               /                             \
+-----------------------------+   +-----------------------------+
| Interactive Class (1:10)    |   | Bulk Transfer Class (1:20)  |
| (rate 20Mbit, ceil 100Mbit) |   | (rate 80Mbit, ceil 100Mbit) |
+-----------------------------+   +-----------------------------+
```

1. **Qdisc (Queuing Discipline)**: Algorithm governing packet egress ordering and buffering (e.g. `fq_codel`, `cake`, `tbf`, `htb`, `netem`).
2. **Class**: Sub-queues within classful qdiscs (e.g., HTB) forming a hierarchical tree with assigned bandwidth slices.
3. **Filter**: Classifiers matching packet headers (IP addresses, ports, TOS/DSCP bits, or eBPF bytecode) and directing them to designated classes.
4. **Action**: Operations triggered upon packet classification (e.g., `police`, `drop`, `mirred` redirect).

---

## 3. Options

### 3.1 Global Command-Line Flags

| Option | Long Option | Description | Default |
|:---|:---|:---|:---|
| `-s` | `-stats`, `-statistics` | Print detailed packet and byte counters, dropped packets, and overlimits. | Summary view |
| `-d` | `-details` | Print detailed configuration parameters for qdiscs and classes. | Basic view |
| `-r` | `-raw` | Dump raw hex/binary parameter structures. | Decoded text |
| `-p` | `-pretty` | Format and decode packet action parameters cleanly. | Compact text |
| `-j` | `-json` | Emit structured JSON data. | Formatted text |
| `-c[=when]` | `-color[=when]` | Colorize terminal output (`auto`, `always`, `never`). | auto |
| `-b file` | `-batch file` | Execute multiple `tc` commands from a batch file. | CLI input |
| `-n ns` | `-netns ns` | Execute traffic control command inside specified network namespace. | Host namespace |

---

## 4. Basic Usage

### 4.1 Quick-Reference Cheatsheet Card

| Operation | Command Pattern | Copyable One-Liner | Notes |
|:---|:---|:---|:---|
| View active qdiscs | `tc qdisc show` | `tc qdisc show` | Displays root packet schedulers on all devices |
| Detailed statistics | `tc -s qdisc show dev [dev]` | `tc -s qdisc show dev eth0` | Inspect byte counters, drops, and overlimits |
| Enable FQ-CoDel | `tc qdisc replace dev [dev] root fq_codel` | `sudo tc qdisc replace dev eth0 root fq_codel` | Mitigates bufferbloat and latency spikes |
| Rate-limit bandwidth | `tc qdisc add dev [dev] root tbf ...` | `sudo tc qdisc add dev eth0 root tbf rate 10mbit burst 32kbit latency 400ms` | Enforces strict outbound bandwidth throttling |
| Simulate WAN latency | `tc qdisc add dev [dev] root netem ...` | `sudo tc qdisc add dev eth0 root netem delay 100ms 10ms loss 2%` | Injects synthetic delay, jitter, and packet loss |
| Delete root qdisc | `tc qdisc del dev [dev] root` | `sudo tc qdisc del dev eth0 root` | Resets interface to kernel default scheduling |

### 4.2 Viewing Active Queuing Disciplines

Inspect the active root qdiscs configured across all network devices:

```bash
tc qdisc show
```

Output:

```console
qdisc noqueue 0: dev lo root refcnt 2 
qdisc fq_codel 0: dev eth0 root refcnt 2 limit 10240p flows 1024 quantum 1514 target 5ms interval 100ms memory_limit 32Mb ecn drop_batch 64 
```

### 4.3 Inspecting Transmission and Drop Statistics

Display real-time traffic statistics, packet counts, and dropped packets on an interface:

```bash
tc -s qdisc show dev eth0
```

Output:

```console
qdisc fq_codel 0: root refcnt 2 limit 10240p flows 1024 quantum 1514 target 5ms interval 100ms 
 Sent 14829104 bytes 12891 pkt (dropped 0, overlimits 0 requeues 0) 
 backlog 0b 0p requeues 0
  maxpacket 1514 drop_overlimit 0 new_flow_count 148 ecn_mark 0
  new_flows_len 0 old_flows_len 0
```

---

## 5. Practical Operations

### 5.1 Mitigating Bufferbloat with FQ-CoDel

Bufferbloat occurs when network queues grow excessively large, causing massive latency spikes under high load. Replace the interface qdisc with `fq_codel` (Fair Queuing Controlled Delay):

```bash
sudo tc qdisc replace dev eth0 root fq_codel
```

Verify active parameters:

```bash
tc qdisc show dev eth0
```

Output:

```console
qdisc fq_codel 0: dev eth0 root refcnt 2 limit 10240p flows 1024 target 5ms interval 100ms
```

### 5.2 Bandwidth Rate-Limiting via Token Bucket Filter (TBF)

Apply strict rate-limiting to outbound interface traffic using the `tbf` qdisc:

```bash
sudo tc qdisc add dev eth0 root tbf rate 10mbit burst 32kbit latency 400ms
```

Inspect the enforced limits:

```bash
tc qdisc show dev eth0
```

Output:

```console
qdisc tbf 8001: dev eth0 root refcnt 2 rate 10Mbit burst 4Kb lat 400ms 
```

### 5.3 Simulating Network Latency and Packet Loss with NetEm

Simulate degraded WAN conditions (e.g. satellite or cross-continental links) for testing distributed systems:

```bash
sudo tc qdisc add dev eth0 root netem delay 100ms 10ms loss 2%
```

Verify reachability latency under emulation:

```bash
ping -c 3 192.168.1.1
```

Output:

```console
PING 192.168.1.1 (192.168.1.1) 56(84) bytes of data.
64 bytes from 192.168.1.1: icmp_seq=1 ttl=64 time=104 ms
64 bytes from 192.168.1.1: icmp_seq=2 ttl=64 time=92.4 ms
64 bytes from 192.168.1.1: icmp_seq=3 ttl=64 time=108 ms
```

### 5.4 Deleting Rules and Restoring Default Scheduling

Remove custom queuing disciplines and reset the interface back to kernel defaults:

```bash
sudo tc qdisc del dev eth0 root
```

---

## 6. Advanced Usage

### 6.1 Hierarchical Token Bucket (HTB) Multi-Tier Shaping

Configure a hierarchical tree allocating guaranteed minimums and bursting caps for interactive SSH versus bulk transfers:

```bash
# 1. Attach root HTB qdisc with default class 20
sudo tc qdisc add dev eth0 root handle 1: htb default 20

# 2. Create parent root class with 100 Mbit total bandwidth
sudo tc class add dev eth0 parent 1: classid 1:1 htb rate 100mbit ceil 100mbit

# 3. Create high-priority interactive class (SSH) with 20 Mbit rate, can burst to 100 Mbit
sudo tc class add dev eth0 parent 1:1 classid 1:10 htb rate 20mbit ceil 100mbit prio 1

# 4. Create bulk traffic class with 80 Mbit rate
sudo tc class add dev eth0 parent 1:1 classid 1:20 htb rate 80mbit ceil 100mbit prio 2

# 5. Filter SSH traffic (port 22) into class 1:10 using u32 classifier
sudo tc filter add dev eth0 protocol ip parent 1:0 prio 1 u32 match ip dport 22 0xffff flowid 1:10
```

Audit the class hierarchy:

```bash
tc class show dev eth0
```

Output:

```console
class htb 1:1 root rate 100Mbit ceil 100Mbit burst 1600b cburst 1600b 
class htb 1:10 parent 1:1 prio 1 rate 20Mbit ceil 100Mbit burst 1600b cburst 1600b 
class htb 1:20 parent 1:1 prio 2 rate 80Mbit ceil 100Mbit burst 1600b cburst 1600b 
```

### 6.2 Attaching eBPF Classifiers to Interface Ingress

Modern high-speed packet inspection attaches compiled eBPF programs directly to the `clsact` queuing discipline:

```bash
# 1. Attach clsact qdisc (supports both ingress and egress eBPF hooks)
sudo tc qdisc add dev eth0 clsact

# 2. Load compiled eBPF ELF program into ingress hook
sudo tc filter add dev eth0 ingress bpf da obj filter.o sec tc_ingress
```

Inspect the attached eBPF filter:

```bash
tc filter show dev eth0 ingress
```

Output:

```console
filter protocol all pref 49152 bpf chain 0 
filter protocol all pref 49152 bpf chain 0 handle 0x1 filter.o:[tc_ingress] direct-action not_in_hw id 48 tag a1b2c3d4e5f6
```

---

## 7. Exit Status, Environment, and Configuration

### 7.1 Exit Status

| Exit Code | Meaning |
|:---|:---|
| `0` | Success: traffic control parameters updated or queried successfully. |
| `1` | Failure: syntax error, unrecognized qdisc type, or invalid netlink argument. |
| `2` | Kernel rejected operation (e.g. device does not exist or duplicate handle). |

### 7.2 Environment Variables

| Variable | Description |
|:---|:---|
| `TC_LIB_DIR` | Directory holding `tc` shared library modules (defaults to `/usr/lib/tc` or `/usr/lib64/tc`). |

### 7.3 Relevant Kernel Interfaces

| Interface | Purpose |
|:---|:---|
| `NETLINK_ROUTE` | Kernel Netlink bus carrying `RTM_NEWQDISC`, `RTM_DELQDISC`, and `RTM_GETQDISC` messages. |
| `/proc/net/dev` | Global packet counter interface reflecting drop and error events. |

---

## 8. Safety, Security, and Portability

### 8.1 Administrative Hazards and Remote Lockout

> [!WARNING]
> **Remote Lockout Hazard**: Applying aggressive bandwidth throttling or packet loss to the management interface of a remote server can render SSH completely unusable. Always stage complex traffic shaping scripts with an automated watchdog rollback timer (e.g. `( sleep 60 && sudo tc qdisc del dev eth0 root ) &`).

`tc` commands that throttle bandwidth or apply aggressive packet loss can render an SSH session unresponsive:
- Never apply severe `netem` loss or low `tbf` rates directly to the management interface of a remote host without a safety timer.
- Always stage complex traffic shaping scripts using a fallback watchdog:
  ```bash
  ( sleep 60 && sudo tc qdisc del dev eth0 root ) &
  ```

### 8.2 Privilege Boundaries

Configuring queuing disciplines and traffic shaping requires `CAP_NET_ADMIN` privileges. Unprivileged users may only read and query active qdiscs.

### 8.3 Portability Constraints

`tc` is exclusive to the Linux kernel networking stack. BSD distributions (FreeBSD, OpenBSD) utilize PF (Packet Filter) with `altq` or `dummynet` for traffic shaping.

---

## 9. Best Practices

### 9.1 Monitor Dropped Packets with `tc -s` to Detect Buffer Starvation

> [!TIP]
> **Monitor Drops to Avoid Starvation**: Regularly audit `dropped` and `overlimits` counters using `tc -s qdisc show dev <dev>` to verify that burst and buffer parameters accommodate normal TCP window fluctuations.

*Upstream Rationale*: `tc(8)` documentation emphasizes that misconfigured rate limits or undersized burst buffers result in excessive drops and TCP window collapse. Regularly audit `dropped` and `overlimits` counters using `tc -s qdisc show dev <dev>` to verify that burst parameters accommodate normal TCP window fluctuations.

### 9.2 Prefer Modern CoDel / CAKE Over Legacy FIFO Queues

> [!NOTE]
> Modern active queue management (AQM) algorithms (`fq_codel` and `cake`) automatically isolate flows and manage delay, keeping latency low even under full link saturation.

*Upstream Rationale*: Traditional `pfifo_fast` queues allow large buffer bloat under saturated connections, inflating round-trip times by hundreds of milliseconds. Modern active queue management (AQM) algorithms (`fq_codel` and `cake`) automatically isolate flows and manage delay, keeping latency low even under full link saturation.

### 9.3 Clean Up Test Configurations Explicitly

> [!IMPORTANT]
> **Clean Up Emulation Rules**: Traffic control rules persist in the kernel until explicitly removed or until reboot. Leaving test `netem` rules active on staging or production interfaces causes phantom network degradation. Always issue `tc qdisc del dev <dev> root` after tests complete.

*Upstream Rationale*: Traffic control rules persist in the kernel until explicitly removed or until the system reboots. Leaving test `netem` rules active on production or staging interfaces can cause phantom network degradation. Always issue `tc qdisc del dev <dev> root` upon concluding testing.

---

## References

1. `tc(8)` — Linux man page, iproute2 project: <https://man7.org/linux/man-pages/man8/tc.8.html>
2. `tc-tbf(8)` — Token Bucket Filter man page: <https://man7.org/linux/man-pages/man8/tc-tbf.8.html>
3. `tc-netem(8)` — Network Emulator man page: <https://man7.org/linux/man-pages/man8/tc-netem.8.html>
4. iproute2 Git repository, Linux Kernel Archives: <https://git.kernel.org/pub/scm/network/iproute2/iproute2.git/>
