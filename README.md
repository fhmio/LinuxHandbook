# LinuxHandbook — The Authoritative Linux Reference & Systems Playbook

> **An authoritative, upstream-verified reference library and operational systems playbook covering 53 essential Linux binaries.**

Every guide provides exhaustive option matrices, verified real-world terminal workflows, exit code specifications, security boundaries, and upstream-cited best practices compliant with **IEEE Std 1003.1-2024 (POSIX.1-2024)** and modern Linux distributions.

[![GitHub CI](https://github.com/fhmio/LinuxHandbook/actions/workflows/ci.yml/badge.svg)](https://github.com/fhmio/LinuxHandbook/actions)
[![Catalog](https://img.shields.io/badge/Catalog-53%20Guides%20Available-blue?style=flat-square)](#-upstream-command-catalog)
[![POSIX](https://img.shields.io/badge/Standard-POSIX.1--2024%20Audited-green?style=flat-square)](#-project-standards--verification)
[![Verification](https://img.shields.io/badge/Validation-100%25%20Verified-brightgreen?style=flat-square)](#-automated-verification-suite)
[![Playbooks](https://img.shields.io/badge/Playbooks-6%20Incident%20Tracks-orange?style=flat-square)](#-operational-playbooks)
[![Docs](https://img.shields.io/badge/Docs-VitePress%20Portal-646cff?style=flat-square)](https://fhmio.github.io/LinuxHandbook/)
[![License](https://img.shields.io/badge/License-MIT-purple?style=flat-square)](https://opensource.org/licenses/MIT)

### Quick Navigation
• [⚡ Operational Playbooks](#-operational-playbooks)
• [📦 Upstream Command Catalog](#-upstream-command-catalog)
• [🛡️ Execution Safety Tiers](#-execution-safety-tiers)
• [📐 Quality Standards & Verification](#-project-standards--verification)

---

## ⚡ Operational Playbooks

These incident response and systems administration playbooks organize utilities by practical operational scenario rather than upstream package origin.

### Playbook 1: System Triage & Incident Response

> **Scenario**: Diagnosing CPU/memory resource exhaustion, identifying rogue tasks, inspecting daemon health, and analyzing systemd service failures.

| Command | Role & Operational Focus | Quick-Reference Invocations |
|:---|:---|:---|
| [`top`](./article/linux-top-tutorial.md) | Interactive dynamic resource monitoring, CPU/Memory per-task triage | `top -b -n 1 | head -n 25` |
| [`ps`](./article/linux-ps-tutorial.md) | Exact process snapshots, thread hierarchy, PID tree parentage | `ps -eo pid,ppid,user,%cpu,%mem,cmd --sort=-%cpu | head` |
| [`free`](./article/linux-free-tutorial.md) | Physical RAM, swap usage, available memory breakdown | `free -h --wide` |
| [`vmstat`](./article/linux-vmstat-tutorial.md) | Virtual memory paging, context switches, disk I/O pacing | `vmstat 1 5` |
| [`uptime`](./article/linux-uptime-tutorial.md) | System elapsed runtime and 1/5/15-minute load averages | `uptime` |
| [`pgrep`](./article/linux-pgrep-tutorial.md) | Fast process search by name, UID, or full command line | `pgrep -a -u www-data nginx` |
| [`pkill`](./article/linux-pkill-tutorial.md) | Coordinated signal dispatch to matched process groups | `pkill -TERM -f worker` |
| [`w`](./article/linux-w-tutorial.md) | Active login sessions, idle times, and user task attribution | `w -u` |
| [`journalctl`](./article/linux-journalctl-tutorial.md) | Live & boot error logs, service diagnostic queries | `journalctl -u <service> -p err -b` |
| [`systemctl`](./article/linux-systemctl-tutorial.md) | Daemon lifecycle, service status inspection, failed units | `systemctl --failed` |

### Playbook 2: Storage, Partitions & Filesystem Auditing

> **Scenario**: Storage hardware discovery, fstab syntax validation before reboot, partition alignment, and filesystem mounting.

| Command | Role & Operational Focus | Quick-Reference Invocations |
|:---|:---|:---|
| [`lsblk`](./article/linux-lsblk-tutorial.md) | Block device hierarchy, SSD TRIM discovery, partition trees | `lsblk -f -o NAME,SIZE,FSTYPE,MOUNTPOINTS,UUID` |
| [`blkid`](./article/linux-blkid-tutorial.md) | Low-level UUID and filesystem token extraction for fstab | `blkid -s UUID -o value /dev/sdX` |
| [`findmnt`](./article/linux-findmnt-tutorial.md) | Active VFS mount tree, fstab syntax verification prior to reboot | `findmnt --verify` |
| [`mount`](./article/linux-mount-tutorial.md) | VFS filesystem attachment, read-only remounts, bind mounts | `mount -o remount,ro /data` |
| [`umount`](./article/linux-umount-tutorial.md) | Safe filesystem detachment, lazy and force unmounting | `umount -l /mnt` |
| [`fdisk`](./article/linux-fdisk-tutorial.md) | Sector-aligned GPT/MBR partition table creation and manipulation | `fdisk -l /dev/nvme0n1` |

### Playbook 3: Network Diagnostics & Traffic Control

> **Scenario**: Layer 2/3 network configuration, open socket auditing, bufferbloat mitigation, and bridge VLAN isolation.

| Command | Role & Operational Focus | Quick-Reference Invocations |
|:---|:---|:---|
| [`ip`](./article/linux-ip-tutorial.md) | Interface state, CIDR addressing, routing tables, network namespaces | `ip -br addr show` |
| [`ss`](./article/linux-ss-tutorial.md) | High-performance Netlink socket statistics, port audits, state filters | `ss -tulpn` |
| [`tc`](./article/linux-tc-tutorial.md) | Kernel traffic shaping, bufferbloat mitigation (FQ-CoDel), WAN latency simulation | `tc qdisc replace dev eth0 root fq_codel` |
| [`bridge`](./article/linux-bridge-tutorial.md) | Ethernet bridge links, Forwarding Database (FDB), 802.1Q VLAN filtering | `bridge vlan show` |

### Playbook 4: Remote Access & Cryptographic Identity

> **Scenario**: Hardened remote terminal administration, modern key generation, agent caching, and encrypted file transfers.

| Command | Role & Operational Focus | Quick-Reference Invocations |
|:---|:---|:---|
| [`ssh`](./article/linux-ssh-tutorial.md) | Encrypted interactive remote shell, bastion ProxyJump, port forwarding | `ssh -J jump.host user@target` |
| [`ssh-keygen`](./article/linux-ssh-keygen-tutorial.md) | Modern Ed25519 keypair generation and fingerprint auditing | `ssh-keygen -t ed25519 -C "admin"` |
| [`ssh-agent`](./article/linux-ssh-agent-tutorial.md) | Background authentication agent daemon lifecycle management | `eval "$(ssh-agent -s)"` |
| [`ssh-add`](./article/linux-ssh-add-tutorial.md) | Private key registration and time-limited agent caching | `ssh-add -t 1h ~/.ssh/id_ed25519` |
| [`ssh-keyscan`](./article/linux-ssh-keyscan-tutorial.md) | Automated remote host key gathering for known_hosts | `ssh-keyscan -H -t ed25519 host >> ~/.ssh/known_hosts` |
| [`scp`](./article/linux-scp-tutorial.md) | SFTP-backed secure remote file copying | `scp -P 2222 file.tar.gz remote:/tmp/` |
| [`sftp`](./article/linux-sftp-tutorial.md) | Interactive secure file transfer protocol client | `sftp user@remote` |

### Playbook 5: Data Pipelines, Stream Filtering & Log Slicing

> **Scenario**: Parsing multi-gigabyte log streams, transforming structured data, regex filtering, and parallel command execution.

| Command | Role & Operational Focus | Quick-Reference Invocations |
|:---|:---|:---|
| [`grep`](./article/linux-grep-tutorial.md) | High-speed regular expression pattern matching, PCRE searching | `grep -P '(?<=error: )\w+' app.log` |
| [`sed`](./article/linux-sed-tutorial.md) | Non-interactive stream editing, safe in-place file replacement | `sed -i.bak 's/old/new/g' config.ini` |
| [`awk`](./article/linux-awk-tutorial.md) | Pattern-directed scanning, column arithmetic, structured report generation | `awk '{sum += $5} END {print sum}' data.tsv` |
| [`cut`](./article/linux-cut-tutorial.md) | Field and byte slicing by delimiter or position | `cut -d: -f1,7 /etc/passwd` |
| [`sort`](./article/linux-sort-tutorial.md) | Stable multi-key sorting, numeric collation, human-readable sizes | `sort -hr -k5 disk_usage.txt` |
| [`uniq`](./article/linux-uniq-tutorial.md) | Adjacent line deduplication and frequency counting | `sort access.log | uniq -c | sort -nr` |
| [`tr`](./article/linux-tr-tutorial.md) | Character translation, case conversion, squeezing repeated characters | `tr -s ' ' '\t'` |
| [`find`](./article/linux-find-tutorial.md) | Filesystem traversal with predicate filtering and null-delimited output | `find /var/log -type f -mtime +30 -print0` |
| [`xargs`](./article/linux-xargs-tutorial.md) | Null-delimited batch argument execution, parallel worker execution | `find ... -print0 | xargs -0 -P 4 rm -f` |
| [`cat`](./article/linux-cat-tutorial.md) | Sequential file streaming, line numbering, non-printing characters | `cat -n script.sh` |
| [`head`](./article/linux-head-tutorial.md) | Leading record and byte extraction | `head -n 20 data.csv` |
| [`tail`](./article/linux-tail-tutorial.md) | Descriptor-based live log following (-F), trailing record extraction | `tail -F -n 50 /var/log/syslog` |
| [`locate`](./article/linux-locate-tutorial.md) | Rapid database index file search | `locate -i "*.conf"` |

### Playbook 6: Transfer, Archiving & Compression

> **Scenario**: REST API interactions, delta-transfer synchronization, incremental backups, and high-ratio multi-threaded compression.

| Command | Role & Operational Focus | Quick-Reference Invocations |
|:---|:---|:---|
| [`curl`](./article/linux-curl-tutorial.md) | REST API interaction, data transfers, TLS validation, latency benchmarks | `curl -sSfL -w "%{time_total}\n" https://api.example.com` |
| [`rsync`](./article/linux-rsync-tutorial.md) | Delta-transfer sync, archive mode, snapshot hardlinks (--link-dest) | `rsync -avzP --delete /src/ remote:/dest/` |
| [`tar`](./article/linux-tar-tutorial.md) | Tape archive creation, compression filter chaining, incremental backups | `tar -caf backup.tar.xz -C /dir .` |
| [`gzip`](./article/linux-gzip-tutorial.md) | DEFLATE stream compression with file retention (-k), integrity testing | `gzip -kv -9 database.dump` |
| [`xz`](./article/linux-xz-tutorial.md) | Multi-threaded LZMA2 high-ratio compression (-T0), memory limit constraints | `xz -k -T0 -9e release.tar` |

---

## 🛡️ Execution Safety Tiers

To prevent operational accidents on production infrastructure, every command is classified by its execution safety tier in the upstream inventory:

| Safety Tier | Operational Impact | Privilege Scope | Example Utilities |
|:---|:---|:---|:---|
| `Safe (Read-Only)` | Strictly non-destructive; performs queries without altering system state. | Unprivileged User | `ps`, `top`, `free`, `findmnt`, `lsblk`, `ss`, `journalctl`, `locate` |
| `Unprivileged Write` | Alters files or streams in user-space without system-wide side effects. | Unprivileged User | `cat`, `sed`, `awk`, `curl`, `rsync`, `tar`, `gzip`, `xz` |
| `Privileged Network` | Alters kernel networking tables, socket filters, or Layer 2 bridging. | `CAP_NET_ADMIN` / Root | `ip`, `tc`, `bridge` |
| `Privileged Destructive` | Modifies disk partitions, filesystems, or system runlevel states. | `CAP_SYS_ADMIN` / Root | `fdisk`, `mount`, `umount`, `systemctl` |

---

## 📦 Upstream Command Catalog

The master reference matrix lists all 53 utilities grouped by official upstream suite, displaying researched target versions, POSIX compliance, safety tiers, and verified article links.

### OpenSSH Utilities

| Command | Article | Upstream Version | POSIX.1-2024 | Safety Tier | Status |
|:---|:---|:---|:---:|:---|:---:|
| `scp` | [scp](./article/linux-scp-tutorial.md) | OpenSSH 10.5 | No | `Unprivileged Write` | **Available** |
| `sftp` | [sftp](./article/linux-sftp-tutorial.md) | OpenSSH 10.5 | No | `Unprivileged Write` | **Available** |
| `ssh` | [ssh](./article/linux-ssh-tutorial.md) | OpenSSH 10.5 | No | `Safe (Read-Only)` | **Available** |
| `ssh-add` | [ssh-add](./article/linux-ssh-add-tutorial.md) | OpenSSH 10.5 | No | `Safe (Read-Only)` | **Available** |
| `ssh-agent` | [ssh-agent](./article/linux-ssh-agent-tutorial.md) | OpenSSH 10.5 | No | `Safe (Read-Only)` | **Available** |
| `ssh-keygen` | [ssh-keygen](./article/linux-ssh-keygen-tutorial.md) | OpenSSH 10.5 | No | `Unprivileged Write` | **Available** |
| `ssh-keyscan` | [ssh-keyscan](./article/linux-ssh-keyscan-tutorial.md) | OpenSSH 10.5 | No | `Safe (Read-Only)` | **Available** |

### GNU Coreutils

| Command | Article | Upstream Version | POSIX.1-2024 | Safety Tier | Status |
|:---|:---|:---|:---:|:---|:---:|
| `cat` | [cat](./article/linux-cat-tutorial.md) | GNU Coreutils 9.11 | Yes | `Safe (Read-Only)` | **Available** |
| `cp` | [cp](./article/linux-cp-tutorial.md) | GNU Coreutils 9.11 | Yes | `Unprivileged Write` | **Available** |
| `cut` | [cut](./article/linux-cut-tutorial.md) | GNU Coreutils 9.11 | Yes | `Safe (Read-Only)` | **Available** |
| `head` | [head](./article/linux-head-tutorial.md) | GNU Coreutils 9.11 | Yes | `Safe (Read-Only)` | **Available** |
| `ln` | [ln](./article/linux-ln-tutorial.md) | GNU Coreutils 9.11 | Yes | `Unprivileged Write` | **Available** |
| `ls` | [ls](./article/linux-ls-tutorial.md) | GNU Coreutils 9.11 | Yes | `Safe (Read-Only)` | **Available** |
| `mkdir` | [mkdir](./article/linux-mkdir-tutorial.md) | GNU Coreutils 9.11 | Yes | `Unprivileged Write` | **Available** |
| `mv` | [mv](./article/linux-mv-tutorial.md) | GNU Coreutils 9.11 | Yes | `Unprivileged Write` | **Available** |
| `rm` | [rm](./article/linux-rm-tutorial.md) | GNU Coreutils 9.11 | Yes | `Privileged Destructive` | **Available** |
| `rmdir` | [rmdir](./article/linux-rmdir-tutorial.md) | GNU Coreutils 9.11 | Yes | `Unprivileged Write` | **Available** |
| `sort` | [sort](./article/linux-sort-tutorial.md) | GNU Coreutils 9.11 | Yes | `Safe (Read-Only)` | **Available** |
| `tail` | [tail](./article/linux-tail-tutorial.md) | GNU Coreutils 9.11 | Yes | `Safe (Read-Only)` | **Available** |
| `touch` | [touch](./article/linux-touch-tutorial.md) | GNU Coreutils 9.11 | Yes | `Unprivileged Write` | **Available** |
| `tr` | [tr](./article/linux-tr-tutorial.md) | GNU Coreutils 9.11 | Yes | `Safe (Read-Only)` | **Available** |
| `uniq` | [uniq](./article/linux-uniq-tutorial.md) | GNU Coreutils 9.11 | Yes | `Safe (Read-Only)` | **Available** |

### GNU Findutils

| Command | Article | Upstream Version | POSIX.1-2024 | Safety Tier | Status |
|:---|:---|:---|:---:|:---|:---:|
| `find` | [find](./article/linux-find-tutorial.md) | GNU Findutils 4.10 | Yes | `Safe (Read-Only)` | **Available** |
| `locate` | [locate](./article/linux-locate-tutorial.md) | GNU Findutils 4.10 | No | `Safe (Read-Only)` | **Available** |
| `xargs` | [xargs](./article/linux-xargs-tutorial.md) | GNU Findutils 4.10 | Yes | `Unprivileged Write` | **Available** |

### GNU Grep

| Command | Article | Upstream Version | POSIX.1-2024 | Safety Tier | Status |
|:---|:---|:---|:---:|:---|:---:|
| `grep` | [grep](./article/linux-grep-tutorial.md) | GNU Grep 3.11 | Yes | `Safe (Read-Only)` | **Available** |

### GNU Sed

| Command | Article | Upstream Version | POSIX.1-2024 | Safety Tier | Status |
|:---|:---|:---|:---:|:---|:---:|
| `sed` | [sed](./article/linux-sed-tutorial.md) | GNU Sed 4.9 | Yes | `Unprivileged Write` | **Available** |

### GNU GAWK

| Command | Article | Upstream Version | POSIX.1-2024 | Safety Tier | Status |
|:---|:---|:---|:---:|:---|:---:|
| `awk` | [awk](./article/linux-awk-tutorial.md) | GNU GAWK 5.3.0 | Yes | `Safe (Read-Only)` | **Available** |

### procps-ng (Process & System Inspection)

| Command | Article | Upstream Version | POSIX.1-2024 | Safety Tier | Status |
|:---|:---|:---|:---:|:---|:---:|
| `free` | [free](./article/linux-free-tutorial.md) | procps-ng 4.0.4 | No | `Safe (Read-Only)` | **Available** |
| `pgrep` | [pgrep](./article/linux-pgrep-tutorial.md) | procps-ng 4.0.4 | No | `Safe (Read-Only)` | **Available** |
| `pkill` | [pkill](./article/linux-pkill-tutorial.md) | procps-ng 4.0.4 | No | `Privileged Destructive` | **Available** |
| `ps` | [ps](./article/linux-ps-tutorial.md) | procps-ng 4.0.4 | Yes | `Safe (Read-Only)` | **Available** |
| `top` | [top](./article/linux-top-tutorial.md) | procps-ng 4.0.4 | No | `Safe (Read-Only)` | **Available** |
| `uptime` | [uptime](./article/linux-uptime-tutorial.md) | procps-ng 4.0.4 | No | `Safe (Read-Only)` | **Available** |
| `vmstat` | [vmstat](./article/linux-vmstat-tutorial.md) | procps-ng 4.0.4 | No | `Safe (Read-Only)` | **Available** |
| `w` | [w](./article/linux-w-tutorial.md) | procps-ng 4.0.4 | No | `Safe (Read-Only)` | **Available** |

### util-linux (Storage & Core System Administration)

| Command | Article | Upstream Version | POSIX.1-2024 | Safety Tier | Status |
|:---|:---|:---|:---:|:---|:---:|
| `blkid` | [blkid](./article/linux-blkid-tutorial.md) | util-linux 2.40 | No | `Safe (Read-Only)` | **Available** |
| `fdisk` | [fdisk](./article/linux-fdisk-tutorial.md) | util-linux 2.40 | No | `Privileged Destructive` | **Available** |
| `findmnt` | [findmnt](./article/linux-findmnt-tutorial.md) | util-linux 2.40 | No | `Safe (Read-Only)` | **Available** |
| `kill` | [kill](./article/linux-kill-tutorial.md) | 2.40 | Yes | `Privileged Destructive` | **Available** |
| `lsblk` | [lsblk](./article/linux-lsblk-tutorial.md) | util-linux 2.40 | No | `Safe (Read-Only)` | **Available** |
| `mount` | [mount](./article/linux-mount-tutorial.md) | util-linux 2.40 | No | `Privileged Destructive` | **Available** |
| `su` | [su](./article/linux-su-tutorial.md) | 2.40 | No | `Privileged Destructive` | **Available** |
| `umount` | [umount](./article/linux-umount-tutorial.md) | util-linux 2.40 | No | `Privileged Destructive` | **Available** |

### iproute2 (Linux Networking Suite)

| Command | Article | Upstream Version | POSIX.1-2024 | Safety Tier | Status |
|:---|:---|:---|:---:|:---|:---:|
| `bridge` | [bridge](./article/linux-bridge-tutorial.md) | iproute2 6.13 | No | `Privileged Network` | **Available** |
| `ip` | [ip](./article/linux-ip-tutorial.md) | iproute2 6.13 | No | `Privileged Network` | **Available** |
| `ss` | [ss](./article/linux-ss-tutorial.md) | iproute2 6.13 | No | `Safe (Read-Only)` | **Available** |
| `tc` | [tc](./article/linux-tc-tutorial.md) | iproute2 6.13 | No | `Privileged Network` | **Available** |

### systemd (Services & System Journal)

| Command | Article | Upstream Version | POSIX.1-2024 | Safety Tier | Status |
|:---|:---|:---|:---:|:---|:---:|
| `journalctl` | [journalctl](./article/linux-journalctl-tutorial.md) | systemd 256 | No | `Safe (Read-Only)` | **Available** |
| `systemctl` | [systemctl](./article/linux-systemctl-tutorial.md) | systemd 256 | No | `Privileged Destructive` | **Available** |

### curl (Network Transfer)

| Command | Article | Upstream Version | POSIX.1-2024 | Safety Tier | Status |
|:---|:---|:---|:---:|:---|:---:|
| `curl` | [curl](./article/linux-curl-tutorial.md) | curl 8.12.0 | No | `Unprivileged Write` | **Available** |

### rsync (Remote Sync)

| Command | Article | Upstream Version | POSIX.1-2024 | Safety Tier | Status |
|:---|:---|:---|:---:|:---|:---:|
| `rsync` | [rsync](./article/linux-rsync-tutorial.md) | rsync 3.5.0 | No | `Unprivileged Write` | **Available** |

### GNU tar (Archiving)

| Command | Article | Upstream Version | POSIX.1-2024 | Safety Tier | Status |
|:---|:---|:---|:---:|:---|:---:|
| `tar` | [tar](./article/linux-tar-tutorial.md) | GNU tar 1.35 | No | `Unprivileged Write` | **Available** |

### GNU gzip (Compression)

| Command | Article | Upstream Version | POSIX.1-2024 | Safety Tier | Status |
|:---|:---|:---|:---:|:---|:---:|
| `gzip` | [gzip](./article/linux-gzip-tutorial.md) | GNU gzip 1.13 | No | `Unprivileged Write` | **Available** |

### XZ Utils (Compression)

| Command | Article | Upstream Version | POSIX.1-2024 | Safety Tier | Status |
|:---|:---|:---|:---:|:---|:---:|
| `xz` | [xz](./article/linux-xz-tutorial.md) | XZ Utils 5.6.2 | No | `Unprivileged Write` | **Available** |

---

## 📐 Project Standards & Verification

This repository enforces rigorous architectural and quality contracts through automated CI-ready test scripts:

1. **Article Quality Specification**: Defined in [`docs/article-contract.md`](./docs/article-contract.md), requiring 9 mandatory top-level headings, ISO front matter, verified code fences, and zero hallucinated options.
2. **Upstream Inventory Schema**: Defined in [`schemas/upstream-inventory.schema.json`](./schemas/upstream-inventory.schema.json), enforcing strict metadata contracts across all suite manifests.
3. **Automated Verification Suite**:
   ```bash
   # Validate all 53 articles against the 20-point contract
   python scripts/validate_articles.py --all

   # Validate all upstream inventory files against schema
   python scripts/validate_inventory.py

   # Regenerate this README deterministically
   python scripts/generate_readme.py
   ```

**Catalog Summary:** 55/64 articles available and verified.
