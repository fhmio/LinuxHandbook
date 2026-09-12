---
title: "Linux Command Tutorial: ip"
date: 2026-09-12T00:00:00+00:00
categories: ['Technology']
tags:
  - 'Linux'
  - 'iproute2'
  - 'ip'
  - 'Linux Command Tutorial'
draft: false
slug: "linux-ip-tutorial"
description: "Authoritative reference tutorial for ip (iproute2), detailing network interface administration, IP addressing, routing table management, network namespaces, neighbor discovery, and Netlink subsystem interaction."
upstream_suite: "iproute2"
upstream_version: "iproute2 6.13"
posix_standard: "None"
research_date: "2026-09-12"
---

The **Linux Command Tutorial** series provides rigorous, upstream-verified references for essential system commands across Linux distributions and UNIX-like environments. Each article focuses on a single executable, combining exhaustive option documentation, verified real-world examples, security boundaries, and best practices directly derived from official source documentation and POSIX standards.

---

## 1. Introduction

`ip` is the primary command-line utility for configuring and monitoring network devices, IP addresses, routing tables, network namespaces, policy routing rules, and ARP/NDISC neighbor caches in the Linux kernel. It interacts directly with the kernel's `rtnetlink` subsystem.

- **Upstream Project & Provenance**: Maintained within **iproute2** (`iproute2`), developed alongside the Linux kernel networking subsystem.
- **Portability & Standards Baseline**: Linux-specific network management tool; not standardized in IEEE Std 1003.1-2024 (POSIX.1-2024). It replaces obsolete `net-tools` (`ifconfig`, `route`, `arp`).
- **Target Research Implementation**: Audited against **iproute2 6.13** (`ip(8)`).
- **Applicability & Lifecycle**: The standard networking command across all modern Linux distributions, cloud environments, and container runtimes.

---

## 2. Syntax and Command Model

### 2.1 Canonical Synopsis

```bash
ip [OPTIONS] OBJECT { COMMAND | help }
```

### 2.2 Object-Oriented Architecture

`ip` structures network administration into distinct kernel objects:

| Object | Abbreviation | Purpose |
|:---|:---|:---|
| `link` | `l` | Network interfaces (physical, virtual, veth, bridge, bond, VLAN). |
| `address` | `a`, `addr` | Protocol addresses (IPv4 / IPv6) assigned to network interfaces. |
| `route` | `r` | Kernel routing tables (unicast, local, broadcast, multipath). |
| `rule` | `ru` | Routing Policy Database (RPDB) for source- and mark-based policy routing. |
| `neighbor` | `n`, `neigh` | ARP (IPv4) and Neighbor Discovery (IPv6) cache tables. |
| `netns` | `netns` | Linux network namespaces for process and container isolation. |
| `tunnel` | `t` | Encapsulation tunnels (GRE, IPIP, SIT, VTI). |
| `vrf` | `vrf` | Virtual Routing and Forwarding domains. |
| `monitor` | `m` | Real-time stream of kernel Netlink networking events. |

### 2.3 Process and Communication Model

Unlike legacy tools that parsed `/proc/net/dev` text files or issued `ioctl` system calls, `ip` communicates with the kernel via **AF_NETLINK** sockets using `NETLINK_ROUTE`. This allows atomic updates, zero-copy socket transfers, and real-time asynchronous event subscription.

---

## 3. Options

### 3.1 Global Command-Line Flags

| Option | Long Option | Description | Default |
|:---|:---|:---|:---|
| `-4` | | Restrict protocol scope strictly to IPv4. | Dual-stack |
| `-6` | | Restrict protocol scope strictly to IPv6. | Dual-stack |
| `-j` | `-json` | Output records in structured JSON format. | Human-readable text |
| `-p` | `-pretty` | Pretty-print JSON output with indentation and line breaks. | Compact JSON |
| `-o` | `-oneline` | Output each record on a single line, replacing line breaks with backslashes. | Multi-line text |
| `-s` | `-stats`, `-statistics` | Output detailed interface transmission and packet statistics. | Summary only |
| `-d` | `-details` | Output detailed protocol parameters and driver attributes. | Basic attributes |
| `-c[=when]` | `-color[=when]` | Colorize output (`auto`, `always`, `never`). | auto |
| `-n ns` | `-netns ns` | Execute command in the specified network namespace. | Host namespace |
| `-b file` | `-batch file` | Read commands from a file and execute them in a single batch transaction. | Interactive CLI |
| `-force` | | Continue batch processing even if errors occur. | Terminate on error |
| `-br` | `-brief` | Print concise, tabular summaries for `link` and `addr` objects. | Detailed view |

---

## 4. Basic Usage

### 4.1 Inspecting Network Interfaces (`ip link`)

List all network devices and their physical link states using concise tabular formatting:

```console
$ ip -br link show
lo               UNKNOWN        00:00:00:00:00:00 <LOOPBACK,UP,LOWER_UP> 
eth0             UP             52:54:00:12:34:56 <BROADCAST,MULTICAST,UP,LOWER_UP> 
wlan0            DOWN           00:15:af:3b:cd:ef <BROADCAST,MULTICAST> 
```

View complete link-layer parameters for a specific interface:

```console
$ ip link show eth0
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP mode DEFAULT group default qlen 1000
    link/ether 52:54:00:12:34:56 brd ff:ff:ff:ff:ff:ff
```

### 4.2 Querying IP Addresses (`ip addr`)

Display IPv4 and IPv6 addresses assigned to all interfaces:

```console
$ ip -br addr show
lo               UNKNOWN        127.0.0.1/8 ::1/128 
eth0             UP             192.168.1.50/24 2001:db8::50/64 fe80::5054:ff:fe12:3456/64 
```

### 4.3 Inspecting Routing Tables (`ip route`)

Display the active kernel IPv4 routing table:

```console
$ ip route show
default via 192.168.1.1 dev eth0 proto dhcp src 192.168.1.50 metric 100 
192.168.1.0/24 dev eth0 proto kernel scope link src 192.168.1.50 metric 100 
```

---

## 5. Practical Operations

### 5.1 Assigning and Removing IP Addresses

Assign a static IPv4 address with subnet prefix to an interface:

```bash
sudo ip addr add 10.0.0.15/24 dev eth0
```

Verify the assignment:

```console
$ ip addr show dev eth0
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    inet 192.168.1.50/24 brd 192.168.1.255 scope global dynamic eth0
    inet 10.0.0.15/24 scope global secondary eth0
```

Remove an address assignment:

```bash
sudo ip addr del 10.0.0.15/24 dev eth0
```

### 5.2 Controlling Link Operational State

Bring a network interface administratively up or down:

```bash
# Bring interface down
sudo ip link set dev eth0 down

# Change MAC address while interface is down
sudo ip link set dev eth0 address 52:54:00:ab:cd:ef

# Bring interface back up
sudo ip link set dev eth0 up
```

### 5.3 Managing Default Gateways and Static Routes

Add a static route directed to an internal network via a dedicated router:

```bash
sudo ip route add 172.16.0.0/16 via 192.168.1.254 dev eth0
```

Replace or set the default gateway:

```bash
sudo ip route replace default via 192.168.1.1 dev eth0
```

Delete an unwanted route:

```bash
sudo ip route del 172.16.0.0/16
```

### 5.4 Network Isolation with Network Namespaces (`netns`)

Create an isolated network namespace for secure testing or container execution:

```bash
# Create namespace
sudo ip netns add sandbox

# Create a virtual ethernet pair (veth)
sudo ip link add veth-host type veth peer name veth-guest

# Move one end into the sandbox namespace
sudo ip link set veth-guest netns sandbox

# Configure IP addressing inside the namespace
sudo ip -n sandbox addr add 10.200.1.2/24 dev veth-guest
sudo ip -n sandbox link set veth-guest up
sudo ip -n sandbox link set lo up

# Configure host side
sudo ip addr add 10.200.1.1/24 dev veth-host
sudo ip link set veth-host up
```

Test network reachability across the namespace boundary:

```console
$ sudo ip netns exec sandbox ping -c 2 10.200.1.1
PING 10.200.1.1 (10.200.1.1) 56(84) bytes of data.
64 bytes from 10.200.1.1: icmp_seq=1 ttl=64 time=0.045 ms
64 bytes from 10.200.1.1: icmp_seq=2 ttl=64 time=0.038 ms
```

---

## 6. Advanced Usage

### 6.1 Machine-Readable JSON Output for Automation

Combine `-j` and `-p` to export network configuration directly into structured JSON:

```console
$ ip -j -p addr show dev eth0
[
  {
    "ifindex": 2,
    "ifname": "eth0",
    "flags": [
      "BROADCAST",
      "MULTICAST",
      "UP",
      "LOWER_UP"
    ],
    "mtu": 1500,
    "addr_info": [
      {
        "family": "inet",
        "local": "192.168.1.50",
        "prefixlen": 24,
        "scope": "global",
        "label": "eth0"
      }
    ]
  }
]
```

Extract the primary IPv4 address reliably with `jq`:

```bash
ip -j addr show dev eth0 | jq -r '.[0].addr_info[] | select(.family=="inet") | .local'
# Output: 192.168.1.50
```

### 6.2 Monitoring Real-Time Kernel Network Events

Use `ip monitor` to stream live Netlink events (IP address assignments, link carrier changes, routing table modifications):

```console
$ ip monitor link address route
[LINK] 2: eth0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc fq_codel state DOWN group default
[LINK] 2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default
[ADDR] 2: eth0    inet 192.168.1.155/24 scope global dynamic eth0
[ROUTE] 192.168.1.0/24 dev eth0 proto kernel scope link src 192.168.1.155
```

### 6.3 Batch Command Execution via `-b`

Execute complex, multi-statement network configurations atomically using a batch script:

```bash
cat << 'EOF' > /tmp/network-setup.batch
link set dev eth0 mtu 9000
addr add 10.10.10.5/24 dev eth0
route add 10.20.0.0/16 via 10.10.10.1 dev eth0
EOF

sudo ip -b /tmp/network-setup.batch
rm /tmp/network-setup.batch
```

---

## 7. Exit Status, Environment, and Configuration

### 7.1 Exit Status

| Exit Code | Meaning |
|:---|:---|
| `0` | Success: requested object operation completed without errors. |
| `1` | Failure: invalid syntax, parameter error, or operation rejected by kernel Netlink. |
| `2` | Batch execution error (returned when `-b` encounters a failure). |

### 7.2 Environment Variables

| Variable | Description |
|:---|:---|
| `IP_VRF_EXEC` | Configures shell behavior when spawning processes inside VRF domains. |
| `COLORFGBG` | Used by `ip` to determine default terminal color contrast schemes. |

### 7.3 Relevant System Files

| File | Purpose |
|:---|:---|
| `/etc/iproute2/rt_tables` | Human-readable names mapped to numeric kernel routing table IDs. |
| `/etc/iproute2/rt_scopes` | Scope definitions (`global`, `site`, `link`, `host`, `nowhere`). |
| `/var/run/netns/` | Bind mounts holding network namespace file descriptors. |

---

## 8. Safety, Security, and Portability

### 8.1 Privileged State Mutation Hazards

`ip` commands that alter interfaces, addresses, or routes require `CAP_NET_ADMIN` privileges. Modifying routes or link states on remote SSH sessions risks immediate loss of connectivity:
- Always test complex route or interface changes with timed fallback commands (`sudo ip ... ; sleep 30 ; sudo reboot`).
- Avoid running `ip link set dev <iface> down` on remote primary uplinks.

### 8.2 Atomic Replacement vs Collision

Use `ip route replace` instead of `ip route del` followed by `ip route add` to avoid transient packet loss windows during routing updates.

### 8.3 Portability Constraints

`ip` is exclusive to Linux. BSD systems (FreeBSD, OpenBSD) and macOS do not implement the Linux Netlink protocol; they utilize BSD `ifconfig`, `route`, and the PF/routing socket subsystem.

---

## 9. Best Practices

### 9.1 Cease Using Deprecated `net-tools`

*Upstream Rationale*: `net-tools` (`ifconfig`, `route`, `arp`) was declared unmaintained over two decades ago. It cannot display secondary IPv4 addresses configured on the same interface, lacks complete IPv6 and VLAN support, and relies on slow `ioctl` polling. Modern Linux administration mandates `iproute2`.

### 9.2 Always Use Explicit CIDR Prefix Notation

*Upstream Rationale*: Assigning an address without an explicit prefix (e.g. `ip addr add 192.168.1.5 dev eth0`) defaults to `/32` (host scope) rather than inferring classful `/24` subnets. Always supply the exact prefix length (e.g., `192.168.1.5/24`).

### 9.3 Consume Structured JSON (`-j`) in Automation

*Upstream Rationale*: Default text formatting from `ip` varies across kernel versions and configuration flags. Piping text into `awk` or `grep` is fragile. Always invoke `ip -j` paired with `jq` or native Python JSON parsers for production scripts.

---

## References

1. `ip(8)` — Linux man page, iproute2 project: <https://man7.org/linux/man-pages/man8/ip.8.html>
2. iproute2 Git repository, Linux Kernel Archives: <https://git.kernel.org/pub/scm/network/iproute2/iproute2.git/>
3. Linux Foundation iproute2 Documentation Wiki: <https://wiki.linuxfoundation.org/networking/iproute2>
