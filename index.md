---
layout: home

hero:
  name: "LinuxHandbook"
  text: "The Authoritative Linux Reference & Systems Playbook"
  tagline: "Exhaustive option matrices, verified terminal workflows, POSIX.1-2024 compliance, and operational incident playbooks for 53 essential Linux binaries."
  actions:
    - theme: brand
      text: 🚀 Command Catalog (53 Guides)
      link: /article/linux-ls-tutorial
    - theme: alt
      text: ⚡ Operational Playbooks
      link: /#operational-playbooks
    - theme: alt
      text: 📦 GitHub Repository
      link: https://github.com/fhmio/LinuxHandbook

features:
  - icon: 🛡️
    title: Upstream-Verified References
    details: Rigorously researched against official upstream documentation including GNU Coreutils, procps-ng, util-linux, iproute2, and OpenSSH.
  - icon: ⚡
    title: 1-Click Copyable Commands
    details: Isolated, prompt-free command blocks with labeled outputs designed for high-velocity terminal execution.
  - icon: 📐
    title: IEEE POSIX.1-2024 Audited
    details: Precise delineation between portable standard behavior and distribution-specific GNU/Linux kernel features.
  - icon: 🔍
    title: Instant Local Full-Text Search
    details: Built-in client-side search indexed across all command options, exit codes, caveats, and real-world workflows.
---

## ⚡ Operational Playbooks

These incident response and systems administration playbooks organize utilities by practical operational scenario rather than upstream package origin.

### Playbook 1: System Triage & Incident Response

> **Scenario**: Diagnosing CPU/memory resource exhaustion, identifying rogue tasks, inspecting daemon health, and analyzing systemd service failures.

| Command | Role & Operational Focus | Quick-Reference Invocations |
|:---|:---|:---|
| [**top**](/article/linux-top-tutorial) | Interactive dynamic resource monitoring, CPU/Memory per-task triage | `top -b -n 1 \| head -n 25` |
| [**ps**](/article/linux-ps-tutorial) | Exact process snapshots, thread hierarchy, PID tree parentage | `ps -eo pid,ppid,user,%cpu,%mem,cmd --sort=-%cpu \| head` |
| [**free**](/article/linux-free-tutorial) | Physical RAM, swap usage, available memory breakdown | `free -h --wide` |
| [**vmstat**](/article/linux-vmstat-tutorial) | Virtual memory paging, context switches, disk I/O pacing | `vmstat 1 5` |
| [**uptime**](/article/linux-uptime-tutorial) | System elapsed runtime and 1/5/15-minute load averages | `uptime` |
| [**pgrep**](/article/linux-pgrep-tutorial) | Fast process search by name, UID, or full command line | `pgrep -a -u www-data nginx` |
| [**pkill**](/article/linux-pkill-tutorial) | Coordinated signal dispatch to matched process groups | `pkill -TERM -f worker` |
| [**w**](/article/linux-w-tutorial) | Active login sessions, idle times, and user task attribution | `w -u` |
| [**journalctl**](/article/linux-journalctl-tutorial) | Live & boot error logs, service diagnostic queries | `journalctl -u <service> -p err -b` |
| [**systemctl**](/article/linux-systemctl-tutorial) | Daemon lifecycle, service status inspection, failed units | `systemctl --failed` |

### Playbook 2: Storage, Partitions & Filesystem Auditing

> **Scenario**: Storage hardware discovery, fstab syntax validation before reboot, partition alignment, and filesystem mounting.

| Command | Role & Operational Focus | Quick-Reference Invocations |
|:---|:---|:---|
| [**lsblk**](/article/linux-lsblk-tutorial) | Block device hierarchy, SSD TRIM discovery, partition trees | `lsblk -f -o NAME,SIZE,FSTYPE,MOUNTPOINTS,UUID` |
| [**blkid**](/article/linux-blkid-tutorial) | Low-level UUID and filesystem token extraction for fstab | `blkid -s UUID -o value /dev/sdX` |
| [**findmnt**](/article/linux-findmnt-tutorial) | Active VFS mount tree, fstab syntax verification prior to reboot | `findmnt --verify` |
| [**fdisk**](/article/linux-fdisk-tutorial) | Inspect partition layout, sector boundaries, and alignment | `fdisk -l /dev/nvme0n1` |
| [**mount**](/article/linux-mount-tutorial) | Explicit filesystem mounting, read-only remounts, bind mounts | `mount -o remount,ro /data` |
| [**umount**](/article/linux-umount-tutorial) | Clean unmounting, lazy unmounting for busy mount points | `umount -l /mnt/backup` |

### Playbook 3: Network Diagnostics & Socket Inspection

> **Scenario**: Investigating port conflicts, analyzing network interface configurations, and inspecting Netlink socket buffers.

| Command | Role & Operational Focus | Quick-Reference Invocations |
|:---|:---|:---|
| [**ip**](/article/linux-ip-tutorial) | Interface state, IP addressing, routes, network namespaces | `ip -br addr show` |
| [**ss**](/article/linux-ss-tutorial) | High-performance socket statistics, TCP connection filtering | `ss -tulpn` |
| [**bridge**](/article/linux-bridge-tutorial) | Layer 2 Ethernet bridge management, FDB tables, VLAN filtering | `bridge fdb show` |
| [**tc**](/article/linux-tc-tutorial) | Traffic control, egress rate limiting, packet queuing | `tc qdisc show dev eth0` |

### Playbook 4: High-Performance Text Extraction & Log Slicing

> **Scenario**: Parsing multi-gigabyte log files, extracting CSV/JSON fields, counting unique IP addresses, and stream transformations.

| Command | Role & Operational Focus | Quick-Reference Invocations |
|:---|:---|:---|
| [**grep**](/article/linux-grep-tutorial) | Fast PCRE pattern matching, recursive directory search | `grep -rnIP --color=auto 'ERROR' /var/log/` |
| [**sed**](/article/linux-sed-tutorial) | Non-interactive stream editing, regex substitutions | `sed -i 's/foo/bar/g' config.conf` |
| [**awk**](/article/linux-awk-tutorial) | Column extraction, associative arrays, structured formatting | `awk '{print $1, $9}' access.log` |
| [**sort**](/article/linux-sort-tutorial) | High-volume sorting, numeric sorting, human-readable units | `sort -h -k5,5 disk_usage.txt` |
| [**uniq**](/article/linux-uniq-tutorial) | Adjacent duplicate counting and unique entry filtering | `sort access.log \| uniq -c \| sort -rn` |
| [**cut**](/article/linux-cut-tutorial) | Delimited field extraction and byte slicing | `cut -d: -f1,7 /etc/passwd` |
| [**tr**](/article/linux-tr-tutorial) | Fast character translation, uppercase/lowercase, whitespace squeezing | `tr -s ' ' < file.txt` |
| [**head**](/article/linux-head-tutorial) | Quick file inspection, first N lines or bytes | `head -n 20 file.txt` |
| [**tail**](/article/linux-tail-tutorial) | Live log streaming, following rotated files by descriptor | `tail -F -n 50 /var/log/syslog` |

---

## 📦 Upstream Command Catalog (53 Guides)

Access any guide in the left sidebar or click directly into the categories below:

- **GNU Coreutils**: [`ls`](/article/linux-ls-tutorial), [`cp`](/article/linux-cp-tutorial), [`mv`](/article/linux-mv-tutorial), [`rm`](/article/linux-rm-tutorial), [`mkdir`](/article/linux-mkdir-tutorial), [`rmdir`](/article/linux-rmdir-tutorial), [`touch`](/article/linux-touch-tutorial), [`ln`](/article/linux-ln-tutorial).
- **Text & Streams**: [`cat`](/article/linux-cat-tutorial), [`head`](/article/linux-head-tutorial), [`tail`](/article/linux-tail-tutorial), [`grep`](/article/linux-grep-tutorial), [`sed`](/article/linux-sed-tutorial), [`awk`](/article/linux-awk-tutorial), [`sort`](/article/linux-sort-tutorial), [`uniq`](/article/linux-uniq-tutorial), [`cut`](/article/linux-cut-tutorial), [`tr`](/article/linux-tr-tutorial).
- **Search & Traversal**: [`find`](/article/linux-find-tutorial), [`xargs`](/article/linux-xargs-tutorial), [`locate`](/article/linux-locate-tutorial).
- **Process & Monitoring**: [`ps`](/article/linux-ps-tutorial), [`top`](/article/linux-top-tutorial), [`free`](/article/linux-free-tutorial), [`vmstat`](/article/linux-vmstat-tutorial), [`pgrep`](/article/linux-pgrep-tutorial), [`pkill`](/article/linux-pkill-tutorial), [`w`](/article/linux-w-tutorial), [`uptime`](/article/linux-uptime-tutorial).
- **Storage & Partitions**: [`mount`](/article/linux-mount-tutorial), [`umount`](/article/linux-umount-tutorial), [`findmnt`](/article/linux-findmnt-tutorial), [`lsblk`](/article/linux-lsblk-tutorial), [`fdisk`](/article/linux-fdisk-tutorial), [`blkid`](/article/linux-blkid-tutorial).
- **iproute2 Networking**: [`ip`](/article/linux-ip-tutorial), [`ss`](/article/linux-ss-tutorial), [`tc`](/article/linux-tc-tutorial), [`bridge`](/article/linux-bridge-tutorial).
- **OpenSSH Utilities**: [`ssh`](/article/linux-ssh-tutorial), [`sftp`](/article/linux-sftp-tutorial), [`scp`](/article/linux-scp-tutorial), [`ssh-keygen`](/article/linux-ssh-keygen-tutorial), [`ssh-agent`](/article/linux-ssh-agent-tutorial), [`ssh-add`](/article/linux-ssh-add-tutorial), [`ssh-keyscan`](/article/linux-ssh-keyscan-tutorial).
- **Transfer & Archives**: [`curl`](/article/linux-curl-tutorial), [`rsync`](/article/linux-rsync-tutorial), [`tar`](/article/linux-tar-tutorial), [`gzip`](/article/linux-gzip-tutorial), [`xz`](/article/linux-xz-tutorial).
- **systemd Services**: [`systemctl`](/article/linux-systemctl-tutorial), [`journalctl`](/article/linux-journalctl-tutorial).
