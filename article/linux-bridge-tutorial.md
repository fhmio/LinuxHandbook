---
title: "Linux Command Tutorial: bridge"
date: 2026-09-12T00:00:00+00:00
categories: ['Technology']
tags:
  - 'Linux'
  - 'iproute2'
  - 'bridge'
  - 'Linux Command Tutorial'
draft: false
slug: "linux-bridge-tutorial"
description: "Authoritative reference tutorial for bridge (iproute2), detailing Ethernet bridge management, link state inspection, forwarding database (FDB) administration, VLAN filtering, and multicast database (MDB) tracking."
upstream_suite: "iproute2"
upstream_version: "iproute2 6.13"
posix_standard: "None"
research_date: "2026-09-12"
---

The **Linux Command Tutorial** series provides rigorous, upstream-verified references for essential system commands across Linux distributions and UNIX-like environments. Each article focuses on a single executable, combining exhaustive option documentation, verified real-world examples, security boundaries, and best practices directly derived from official source documentation and POSIX standards.

---

## 1. Introduction

> **Upstream**: iproute2 (iproute2 6.13) | **POSIX**: Linux-Specific (iproute2 extension) | **Safety Tier**: privileged-network-state-altering | **Scope**: ethernet-bridge-management

`bridge` is the dedicated command-line utility for configuring and inspecting Linux Ethernet bridge devices, member port attributes, the Forwarding Database (FDB), VLAN filtering tables, and the Multicast Database (MDB).

- **Upstream Project & Provenance**: Maintained within **iproute2** (`iproute2`) alongside `ip` and `tc`.
- **Portability & Standards Baseline**: Linux-specific Layer 2 management utility; not standardized in IEEE Std 1003.1-2024 (POSIX.1-2024). It modernizes and replaces legacy `brctl` from `bridge-utils`.
- **Target Research Implementation**: Audited against **iproute2 6.13** (`bridge(8)`).
- **Applicability & Lifecycle**: The standard command for virtualization networking, container switch fabrics (KVM, Docker, Kubernetes CNI), and hardware switch offloading (Switchdev).

---

## 2. Syntax and Command Model

### 2.1 Canonical Synopsis

```bash
bridge [OPTIONS] OBJECT { COMMAND | help }
```

### 2.2 Object-Oriented Subsystem Architecture

`bridge` operates across four specialized Layer 2 objects:

| Object | Purpose |
|:---|:---|
| `link` | Inspects and configures member port properties (STP state, hairpin mode, cost, guard). |
| `fdb` | Manages the Forwarding Database (MAC address to port lookup table). |
| `mdb` | Manages the Multicast Database (IGMP/MLD snooping group memberships). |
| `vlan` | Configures per-port VLAN filtering, trunking, and native VLAN tag assignments. |
| `monitor` | Streams real-time Netlink bridge events (FDB updates, link transitions). |

*Note*: Initial bridge creation is handled via `ip link add name br0 type bridge`; `bridge` governs the Layer 2 filtering and forwarding behavior of ports attached to that bridge.

---

## 3. Options

### 3.1 Global Command-Line Flags

| Option | Long Option | Description | Default |
|:---|:---|:---|:---|
| `-s` | `-stats`, `-statistics` | Output detailed forwarding and packet statistics. | Concise output |
| `-d` | `-details` | Output detailed port parameters, operational timers, and STP flags. | Basic summary |
| `-j` | `-json` | Output records formatted as structured JSON. | Human-readable text |
| `-p` | `-pretty` | Indent and pretty-print JSON output. | Compact JSON |
| `-c[=when]` | `-color[=when]` | Colorize output (`auto`, `always`, `never`). | auto |
| `-b file` | `-batch file` | Execute bridge commands from a batch file. | CLI input |
| `-n ns` | `-netns ns` | Execute command in the specified network namespace. | Host namespace |

---

## 4. Basic Usage

### 4.1 Quick-Reference Cheatsheet Card

| Operation | Command Pattern | Copyable One-Liner | Notes |
|:---|:---|:---|:---|
| Inspect bridge ports | `bridge link show` | `bridge link show` | Displays all member ports attached to bridges |
| Detailed port parameters | `bridge -d link show [dev]` | `bridge -d link show dev eth1` | Shows STP, hairpin, guard, and flood flags |
| Forwarding database (FDB) | `bridge fdb show` | `bridge fdb show` | Lists learned and static MAC mappings |
| Add static MAC mapping | `bridge fdb add [mac] dev [port] master static` | `sudo bridge fdb add 00:11:22:33:44:55 dev veth0 master static` | Prevents MAC spoofing on virtual ports |
| Inspect VLAN filtering | `bridge vlan show` | `bridge vlan show` | Lists per-port 802.1Q VLAN memberships |
| Add access VLAN | `bridge vlan add dev [port] vid [id] pvid untagged` | `sudo bridge vlan add dev veth0 vid 100 pvid untagged` | Sets untagged PVID on bridge port |
| Multicast snooping (MDB) | `bridge mdb show` | `bridge mdb show` | Audits IGMP/MLD multicast group memberships |
| Monitor bridge events | `bridge monitor all` | `bridge monitor all` | Streams live Netlink Layer 2 state changes |

### 4.2 Inspecting Bridge Member Ports

Display all network interfaces attached as ports to bridges:

```bash
bridge link show
```

Output:

```console
2: eth1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 master br0 state forwarding priority 32 cost 4 
3: veth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 master br0 state forwarding priority 32 cost 2 
```

View comprehensive port parameters and hardware flags:

```bash
bridge -d link show dev eth1
```

Output:

```console
2: eth1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 master br0 state forwarding priority 32 cost 4 
    hairpin off guard off root_block off fastleave off learning on flood on mcast_flood on bcast_flood on 
```

### 4.3 Inspecting the Forwarding Database (FDB)

List learned and static MAC address mappings:

```bash
bridge fdb show
```

Output:

```console
52:54:00:12:34:56 dev eth1 master br0 permanent
52:54:00:98:76:54 dev eth1 master br0
02:42:0a:00:00:02 dev veth0 master br0
33:33:00:00:00:01 dev eth1 self permanent
```

---

## 5. Practical Operations

### 5.1 Configuring Static MAC Address Entries

Prevent MAC spoofing or fix static forwarding paths for virtual machines by adding static FDB entries:

```bash
sudo bridge fdb add 00:11:22:33:44:55 dev veth0 master static
```

Verify entry addition:

```bash
bridge fdb show dev veth0
```

Output:

```console
00:11:22:33:44:55 dev veth0 master br0 static
```

Delete the static record:

```bash
sudo bridge fdb del 00:11:22:33:44:55 dev veth0 master
```

### 5.2 VLAN Filtering and Trunking (`bridge vlan`)

Modern Linux bridges support hardware-style 802.1Q VLAN filtering:

1. **Enable VLAN filtering on the bridge master**:
   ```bash
   sudo ip link set dev br0 type bridge vlan_filtering 1
   ```

2. **Assign VLAN 100 as untagged Port VLAN ID (PVID) on an access port**:
   ```bash
   sudo bridge vlan add dev veth0 vid 100 pvid untagged
   ```

3. **Configure a trunk port carrying VLANs 100 and 200 tagged**:
   ```bash
   sudo bridge vlan add dev eth1 vid 100
   sudo bridge vlan add dev eth1 vid 200
   ```

4. **Inspect the VLAN table**:
   ```bash
   bridge vlan show
   ```

   Output:

   ```console
   port              vlan-id  
   br0               1 PVID untagged
   eth1              1 PVID untagged
                     100
                     200
   veth0             100 PVID untagged
   ```

### 5.3 Isolating Container Interfaces (Hairpin and Guard Flags)

Secure virtual interfaces attached to bridge switches:

```bash
# Enable hairpin mode (allows inter-container reflection on the same port)
sudo bridge link set dev veth0 hairpin on

# Enable BPDU guard (disables port if unauthorized Spanning Tree BPDUs arrive)
sudo bridge link set dev veth0 guard on

# Disable flood (prevents unknown unicast flooding to this port)
sudo bridge link set dev veth0 flood off
```

### 5.4 Auditing Multicast Snooping Groups (MDB)

Inspect active IGMP/MLD multicast group subscriptions registered on the bridge:

```bash
bridge mdb show
```

Output:

```console
dev br0 port eth1 grp 239.255.255.250 temp
dev br0 port veth0 grp 224.0.0.251 permanent
```

---

## 6. Advanced Usage

### 6.1 Structured JSON Output for Automation

Combine `-j` and `-p` to export Layer 2 forwarding topologies into JSON:

```bash
bridge -j -p fdb show dev veth0
```

Output:

```json
[
  {
    "mac": "00:11:22:33:44:55",
    "dev": "veth0",
    "master": "br0",
    "flags": [
      "static"
    ]
  }
]
```

Filter MAC entries programmatically using `jq`:

```bash
bridge -j fdb show | jq -r '.[] | select(.flags[]? == "static") | "\(.mac) on \(.dev)"'
```

### 6.2 Monitoring Live Bridge Forwarding Events

Monitor real-time Layer 2 topology transitions, MAC migrations, and STP state changes:

```bash
bridge monitor all
```

Output:

```console
[FDB] 52:54:00:ab:cd:ef dev veth0 master br0
[LINK] 3: veth0: state disabled priority 32 cost 2 
[LINK] 3: veth0: state learning priority 32 cost 2 
[LINK] 3: veth0: state forwarding priority 32 cost 2 
```

### 6.3 Batch Provisioning for Complex Switch Topologies

Deploy large VLAN matrices atomically using a batch configuration file:

```bash
cat << 'EOF' > /tmp/bridge_vlans.batch
vlan add dev eth1 vid 10
vlan add dev eth1 vid 20
vlan add dev eth1 vid 30
vlan add dev veth0 vid 10 pvid untagged
vlan add dev veth1 vid 20 pvid untagged
EOF

sudo bridge -b /tmp/bridge_vlans.batch
rm /tmp/bridge_vlans.batch
```

---

## 7. Exit Status, Environment, and Configuration

### 7.1 Exit Status

| Exit Code | Meaning |
|:---|:---|
| `0` | Success: requested Layer 2 configuration or query completed without error. |
| `1` | Failure: invalid syntax, unknown object, or Netlink command rejected. |
| `2` | Batch execution error (returned by `-b`). |

### 7.2 Environment Variables

| Variable | Description |
|:---|:---|
| `COLORFGBG` | Configures terminal color palettes. |

### 7.3 Relevant Kernel Interfaces

| Interface | Purpose |
|:---|:---|
| `NETLINK_ROUTE` | Kernel Netlink transport carrying `RTM_NEWNEIGH` / `RTM_GETLINK` bridge messages. |
| `/sys/class/net/<bridge>/bridge/` | Sysfs directory containing kernel bridge operational parameters. |

---

## 8. Safety, Security, and Portability

### 8.1 Layer 2 Loop Hazards

> [!CAUTION]
> **Broadcast Storm Risk**: Connecting multiple physical links to a bridge without Spanning Tree Protocol (STP) enabled (`sudo ip link set dev br0 type bridge stp_state 1`) can induce catastrophic Layer 2 loops and broadcast storms, saturating switch links and locking host CPUs.

### 8.2 Privilege Boundaries

Modifying FDB tables, link states, or VLAN assignments requires `CAP_NET_ADMIN` privileges. Non-root users can execute read-only queries (`bridge link show`, `bridge fdb show`).

### 8.3 Portability Constraints

`bridge` is specific to the Linux kernel bridging driver. BSD distributions (FreeBSD, OpenBSD) manage bridge interfaces using `ifconfig bridge0 addm ...` and BSD-specific `ioctl` calls.

---

## 9. Best Practices

### 9.1 Cease Using Deprecated `brctl`

> [!IMPORTANT]
> **Cease Using Deprecated `brctl`**: `brctl` from `bridge-utils` is unmaintained and relies on legacy `ioctl` calls that cannot configure VLAN filtering, FDB offloads, or multicast snooping. Use `bridge` and `ip link`.

*Upstream Rationale*: `brctl` (from `bridge-utils`) is unmaintained and communicates via legacy `ioctl` calls that cannot configure modern Linux kernel bridge features such as VLAN filtering, FDB offloads, or multicast snooping. All modern deployments must use `bridge` and `ip link`.

### 9.2 Enable `vlan_filtering` on Multi-Tenant Virtual Bridges

> [!TIP]
> Setting `vlan_filtering 1` on the bridge master enforces IEEE 802.1Q boundary isolation between virtual machines and containers directly in the kernel fast path.

*Upstream Rationale*: By default, Linux bridges behave as simple unmanaged hubs where all ports share a single broadcast domain. Setting `vlan_filtering 1` enforces IEEE 802.1Q boundary isolation between virtual machines and containers directly in the kernel fast path.

### 9.3 Use BPDU Guard (`guard on`) on Virtual Machine Ports

> [!NOTE]
> Enabling `guard on` (BPDU guard) automatically disables virtual ports if unauthorized Spanning Tree BPDUs arrive from rogue VMs or containers.

*Upstream Rationale*: If a virtual machine or container running on a virtual bridge transmits rogue Spanning Tree BPDUs, it can alter the physical switch network's root bridge topology. Enabling `guard on` automatically disables the port if a BPDU frame is detected.

---

## References

1. `bridge(8)` — Linux man page, iproute2 project: <https://man7.org/linux/man-pages/man8/bridge.8.html>
2. iproute2 Git repository, Linux Kernel Archives: <https://git.kernel.org/pub/scm/network/iproute2/iproute2.git/>
3. Linux Kernel Ethernet Bridge Documentation: <https://docs.kernel.org/networking/bridge.html>
