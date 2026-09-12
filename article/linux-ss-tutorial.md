---
title: "Linux Command Tutorial: ss"
date: 2026-09-12T00:00:00+00:00
categories: ['Technology']
tags:
  - 'Linux'
  - 'iproute2'
  - 'ss'
  - 'Linux Command Tutorial'
draft: false
slug: "linux-ss-tutorial"
description: "Authoritative reference tutorial for ss (iproute2), detailing socket statistics inspection, TCP/UDP connection auditing, Netlink sock_diag querying, process mapping, and state filtering."
upstream_suite: "iproute2"
upstream_version: "iproute2 6.13"
posix_standard: "None"
research_date: "2026-09-12"
---

The **Linux Command Tutorial** series provides rigorous, upstream-verified references for essential system commands across Linux distributions and UNIX-like environments. Each article focuses on a single executable, combining exhaustive option documentation, verified real-world examples, security boundaries, and best practices directly derived from official source documentation and POSIX standards.

---

## 1. Introduction

`ss` (Socket Statistics) is a high-performance utility for inspecting active network sockets, listening ports, protocol statistics, and connection metadata. It extracts socket diagnostic information directly from the Linux kernel via the `sock_diag` Netlink subsystem.

- **Upstream Project & Provenance**: Maintained within **iproute2** (`iproute2`).
- **Portability & Standards Baseline**: Linux-specific diagnostic tool; not standardized in IEEE Std 1003.1-2024 (POSIX.1-2024). It modernizes and supersedes legacy `netstat`.
- **Target Research Implementation**: Audited against **iproute2 6.13** (`ss(8)`).
- **Applicability & Lifecycle**: The standard utility for socket inspection across modern Linux servers, container engines, and troubleshooting workflows.

---

## 2. Syntax and Command Model

### 2.1 Canonical Synopsis

```bash
ss [options] [filter]
```

### 2.2 Kernel Communication Architecture

Legacy tools like `netstat` read socket data by sequentially scanning `/proc/net/tcp`, `/proc/net/udp`, and `/proc/net/raw`. On systems handling tens of thousands of concurrent connections, reading these `/proc` virtual files acquires global kernel lock mechanisms and imposes heavy CPU overhead.

`ss` bypasses `/proc` by communicating with the kernel via **`NETLINK_INET_DIAG`** (`sock_diag`). The kernel filters and delivers binary socket structures directly over Netlink sockets, providing:
- Constant-time $O(1)$ query initiation and high-throughput streaming.
- In-kernel state and port filtering before user-space delivery.
- Access to advanced TCP metrics (RTT, congestion window, socket buffer memory).

---

## 3. Options

### 3.1 Protocol Selection Flags

| Option | Long Option | Description | Default |
|:---|:---|:---|:---|
| `-t` | `--tcp` | Display TCP sockets. | All protocols |
| `-u` | `--udp` | Display UDP sockets. | All protocols |
| `-d` | `--dccp` | Display DCCP sockets. | All protocols |
| `-w` | `--raw` | Display RAW sockets. | All protocols |
| `-x` | `--unix` | Display Unix domain sockets. | All protocols |
| `-4` | `--ipv4` | Restrict display strictly to IPv4 sockets. | Dual-stack |
| `-6` | `--ipv6` | Restrict display strictly to IPv6 sockets. | Dual-stack |

### 3.2 Display and Filtering Options

| Option | Long Option | Description | Default |
|:---|:---|:---|:---|
| `-a` | `--all` | Display both listening and non-listening (established/closing) sockets. | Non-listening only |
| `-l` | `--listening` | Display only listening sockets. | Non-listening only |
| `-n` | `--numeric` | Do not resolve service port names or host addresses to hostnames. | Resolved names |
| `-r` | `--resolve` | Resolve numeric IP addresses to hostnames via DNS. | Numeric IPs |
| `-p` | `--processes` | Show process names and PIDs holding socket file descriptors. | Off |
| `-e` | `--extended` | Display extended socket attributes (uid, inode, timer). | Off |
| `-m` | `--memory` | Display socket memory usage (`rmem`, `wmem`, buffer allocation). | Off |
| `-i` | `--info` | Display internal kernel TCP statistics (RTT, cwnd, MSS, retransmissions). | Off |
| `-s` | `--summary` | Print summary socket statistics and exit. | Full list |
| `-H` | `--no-header` | Suppress the table header row. | Header printed |
| `-K` | `--kill` | Forcefully close matching sockets (requires `CAP_NET_ADMIN`). | Query only |
| `-Z` | `--context` | Display SELinux security contexts for sockets and processes. | Off |

---

## 4. Basic Usage

### 4.1 System Socket Summary

Retrieve a high-level statistical overview of all active sockets across protocols:

```console
$ ss -s
Total: 345
TCP:   38 (estab 14, closed 12, orphaned 0, timewait 6)

Transport Total     IP        IPv6
RAW	  1         0         1        
UDP	  9         6         3        
TCP	  26        18        8        
INET	  36        24        12       
FRAG	  0         0         0        
```

### 4.2 Listing Active Listening Ports

Audit all listening TCP and UDP sockets with numeric addresses and process attribution:

```console
$ sudo ss -tulpn
Netid State  Recv-Q Send-Q Local Address:Port  Peer Address:PortProcess                                     
udp   UNCONN 0      0            0.0.0.0:5353       0.0.0.0:*    users:(("avahi-daemon",pid=612,fd=12))      
udp   UNCONN 0      0            0.0.0.0:68         0.0.0.0:*    users:(("systemd-network",pid=498,fd=19))   
tcp   LISTEN 0      128          0.0.0.0:22         0.0.0.0:*    users:(("sshd",pid=789,fd=3))               
tcp   LISTEN 0      4096       127.0.0.1:6379       0.0.0.0:*    users:(("redis-server",pid=845,fd=6))       
tcp   LISTEN 0      128             [::]:22            [::]:*    users:(("sshd",pid=789,fd=4))               
```

---

## 5. Practical Operations

### 5.1 Inspecting Established TCP Connections

Filter for active, connected TCP sessions without displaying passive listeners:

```console
$ ss -tan state established
Recv-Q Send-Q  Local Address:Port   Peer Address:Port
0      0       192.168.1.50:22      192.168.1.10:54210
0      64      192.168.1.50:22      192.168.1.12:51884
0      0       192.168.1.50:48922   93.184.216.34:443
```

### 5.2 Filtering by Port or Remote Host

Filter sockets by source or destination port using `ss` filter expressions:

```console
$ ss -tan '( sport = :ssh or dport = :ssh )'
State       Recv-Q Send-Q Local Address:Port  Peer Address:Port
ESTAB       0      0      192.168.1.50:22     192.168.1.10:54210
ESTAB       0      64     192.168.1.50:22     192.168.1.12:51884
```

Filter by destination IP subnet:

```console
$ ss -tan dst 192.168.1.0/24
State       Recv-Q Send-Q Local Address:Port  Peer Address:Port
ESTAB       0      0      192.168.1.50:22     192.168.1.10:54210
```

### 5.3 Diagnosing TCP Congestion and Latency with `-i`

Inspect internal kernel TCP metrics such as Round-Trip Time (RTT), congestion window (`cwnd`), and Maximum Segment Size (`mss`):

```console
$ ss -ti dst 93.184.216.34
State Recv-Q Send-Q Local Address:Port  Peer Address:Port
ESTAB 0      0      192.168.1.50:48922  93.184.216.34:443
	 cubic wscale:7,7 rto:240 rtt:32.415/4.120 ato:40 mss:1460 rcvspace:64240 ssthresh:10 cwnd:10
```
*Metrics analysis*:
- `rtt:32.415/4.120`: Mean RTT of 32.415 ms with 4.120 ms variance.
- `cwnd:10`: Active congestion window sizing in segments.
- `cubic`: Active TCP congestion control algorithm.

### 5.4 Auditing Unix Domain Sockets

Inspect local inter-process communication (IPC) sockets:

```console
$ ss -x -a
Netid State  Recv-Q Send-Q Local Address:Port             Peer Address:Port
u_str LISTEN 0      4096   /run/systemd/private           14892             * 0
u_str LISTEN 0      4096   /run/dbus/system_bus_socket    16234             * 0
u_str ESTAB  0      0      /run/systemd/journal/stdout    18291             * 18290
```

---

## 6. Advanced Usage

### 6.1 Socket Memory Allocation Auditing (`-m`)

Examine socket buffer queue utilization to identify network buffer bloat or starvation:

```console
$ ss -tm dst 93.184.216.34
State Recv-Q Send-Q Local Address:Port  Peer Address:Port
ESTAB 0      0      192.168.1.50:48922  93.184.216.34:443
	 skmem:(r0,rb131072,t0,tb262144,f0,w0,o0,bl0,d0)
```
*Key memory fields*:
- `rb131072`: Maximum receive buffer quota in bytes.
- `tb262144`: Maximum transmit buffer quota in bytes.
- `r0`, `t0`: Currently allocated bytes in receive and transmit queues.

### 6.2 Complex TCP State Matching

`ss` understands all standard TCP state definitions (`established`, `syn-sent`, `syn-recv`, `fin-wait-1`, `fin-wait-2`, `time-wait`, `closed`, `close-wait`, `last-ack`, `listening`, `closing`):

```bash
# Count connections stuck in TIME-WAIT state
ss -H -tan state time-wait | wc -l

# Identify unacknowledged connections (potential SYN flood attack)
ss -tan state syn-recv
```

### 6.3 Programmatic Port Scanning Detection

Identify client IP addresses opening excessive simultaneous connections to port 80/443:

```bash
ss -tan state established '( dport = :http or dport = :https )' \
  | awk '{print $4}' \
  | cut -d: -f1 \
  | sort \
  | uniq -c \
  | sort -nr \
  | head -n 10
```

---

## 7. Exit Status, Environment, and Configuration

### 7.1 Exit Status

| Exit Code | Meaning |
|:---|:---|
| `0` | Success: socket data retrieved and formatted successfully. |
| `1` | Failure: invalid filter expression, unrecognized option, or Netlink error. |

### 7.2 Environment Variables

| Variable | Description |
|:---|:---|
| `PROC_NET_TCP` | Can override default `/proc/net/tcp` path if Netlink fallback is triggered. |
| `COLORFGBG` | Configures terminal color rendering. |

### 7.3 Relevant Kernel Interfaces

| Interface | Purpose |
|:---|:---|
| `NETLINK_INET_DIAG` | Primary kernel Netlink family providing binary socket table dumps. |
| `/proc/net/sockstat` | High-level summary counters queried by `ss -s`. |

---

## 8. Safety, Security, and Portability

### 8.1 Read-Only Safety and Socket Killing

`ss` is primarily a safe, read-only diagnostic utility. However, passing `-K` (`--kill`) directs the kernel to forcefully abort matching open sockets (`SOCK_DESTROY`). This requires `CAP_NET_ADMIN` and should never be executed without exact filter parameters.

### 8.2 Process Visibility Boundaries

When run as an unprivileged user, `ss -p` cannot resolve PIDs or process names for sockets owned by other system users. To obtain complete process mapping across all daemons, execute `ss` with `sudo` or as `root`.

### 8.3 Portability Constraints

`ss` depends directly on Linux `sock_diag` Netlink facilities. It is not portable to BSD systems or macOS. On non-Linux UNIX systems, administrators must rely on BSD `netstat` or `sockstat`.

---

## 9. Best Practices

### 9.1 Always Use `-n` in High-Load or Emergency Audits

*Upstream Rationale*: `ss(8)` documentation notes that resolving DNS hostnames and service port strings incurs network round-trips and `/etc/services` lookups. During network degradation or high connection volume, DNS lookups stall terminal output. Always pass `-n` (`--numeric`) for immediate results.

### 9.2 Prefer `ss` Over `netstat` on Production Servers

*Upstream Rationale*: `netstat` is obsolete and reads through `/proc/net/` text tables while holding kernel socket locks. Under heavy server loads (e.g. 50,000+ sockets), running `netstat` induces severe kernel latency spikes. `ss` utilizes zero-copy Netlink binary streams with negligible overhead.

### 9.3 Leverage Built-in TCP State Filters

*Upstream Rationale*: Filtering connection states using `grep` (e.g. `ss -a | grep TIME-WAIT`) transfers unnecessary socket records across user-space and risks false positives from IP addresses containing substring matches. Use native `state <state-name>` syntax to execute filtering directly within `ss`.

---

## References

1. `ss(8)` — Linux man page, iproute2 project: <https://man7.org/linux/man-pages/man8/ss.8.html>
2. iproute2 Git repository, Linux Kernel Archives: <https://git.kernel.org/pub/scm/network/iproute2/iproute2.git/>
3. Linux Kernel `sock_diag` subsystem documentation: <https://www.kernel.org/doc/html/latest/networking/netlink_spec/sock_diag.html>
