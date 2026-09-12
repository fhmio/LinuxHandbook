# Linux Command Reference Series

An authoritative, upstream-driven, and research-verifiable Linux command reference library.

## Overview

Every article in this series adheres to a strict architectural standard: exactly one executable per article, exhaustive option tables, verified real-world operations, exit status references, security boundaries, and source-backed best practices derived directly from official upstream manuals and IEEE Std 1003.1-2024 (POSIX.1-2024).

## Command Catalog

### OpenSSH Utilities

| Command | Article | Upstream Version | POSIX.1-2024 | Status |
|:---|:---|:---|:---:|:---:|
| `scp` | [scp](./article/linux-scp-tutorial.md) | OpenSSH 10.5 | No | Available |
| `sftp` | [sftp](./article/linux-sftp-tutorial.md) | OpenSSH 10.5 | No | Available |
| `ssh` | [ssh](./article/linux-ssh-tutorial.md) | OpenSSH 10.5 | No | Available |
| `ssh-add` | [ssh-add](./article/linux-ssh-add-tutorial.md) | OpenSSH 10.5 | No | Available |
| `ssh-agent` | [ssh-agent](./article/linux-ssh-agent-tutorial.md) | OpenSSH 10.5 | No | Available |
| `ssh-keygen` | [ssh-keygen](./article/linux-ssh-keygen-tutorial.md) | OpenSSH 10.5 | No | Available |
| `ssh-keyscan` | [ssh-keyscan](./article/linux-ssh-keyscan-tutorial.md) | OpenSSH 10.5 | No | Available |

### GNU Coreutils

| Command | Article | Upstream Version | POSIX.1-2024 | Status |
|:---|:---|:---|:---:|:---:|
| `cat` | [cat](./article/linux-cat-tutorial.md) | GNU Coreutils 9.11 | Yes | Available |
| `cp` | [cp](./article/linux-cp-tutorial.md) | GNU Coreutils 9.11 | Yes | Available |
| `cut` | [cut](./article/linux-cut-tutorial.md) | GNU Coreutils 9.11 | Yes | Available |
| `head` | [head](./article/linux-head-tutorial.md) | GNU Coreutils 9.11 | Yes | Available |
| `ln` | [ln](./article/linux-ln-tutorial.md) | GNU Coreutils 9.11 | Yes | Available |
| `ls` | [ls](./article/linux-ls-tutorial.md) | GNU Coreutils 9.11 | Yes | Available |
| `mkdir` | [mkdir](./article/linux-mkdir-tutorial.md) | GNU Coreutils 9.11 | Yes | Available |
| `mv` | [mv](./article/linux-mv-tutorial.md) | GNU Coreutils 9.11 | Yes | Available |
| `rm` | [rm](./article/linux-rm-tutorial.md) | GNU Coreutils 9.11 | Yes | Available |
| `rmdir` | [rmdir](./article/linux-rmdir-tutorial.md) | GNU Coreutils 9.11 | Yes | Available |
| `sort` | [sort](./article/linux-sort-tutorial.md) | GNU Coreutils 9.11 | Yes | Available |
| `tail` | [tail](./article/linux-tail-tutorial.md) | GNU Coreutils 9.11 | Yes | Available |
| `touch` | [touch](./article/linux-touch-tutorial.md) | GNU Coreutils 9.11 | Yes | Available |
| `tr` | [tr](./article/linux-tr-tutorial.md) | GNU Coreutils 9.11 | Yes | Available |
| `uniq` | [uniq](./article/linux-uniq-tutorial.md) | GNU Coreutils 9.11 | Yes | Available |

### GNU Findutils

| Command | Article | Upstream Version | POSIX.1-2024 | Status |
|:---|:---|:---|:---:|:---:|
| `find` | [find](./article/linux-find-tutorial.md) | GNU Findutils 4.10 | Yes | Available |
| `locate` | [locate](./article/linux-locate-tutorial.md) | GNU Findutils 4.10 | No | Available |
| `xargs` | [xargs](./article/linux-xargs-tutorial.md) | GNU Findutils 4.10 | Yes | Available |

### GNU Grep

| Command | Article | Upstream Version | POSIX.1-2024 | Status |
|:---|:---|:---|:---:|:---:|
| `grep` | [grep](./article/linux-grep-tutorial.md) | GNU Grep 3.11 | Yes | Available |

### GNU Sed

| Command | Article | Upstream Version | POSIX.1-2024 | Status |
|:---|:---|:---|:---:|:---:|
| `sed` | [sed](./article/linux-sed-tutorial.md) | GNU Sed 4.9 | Yes | Available |

### GNU GAWK

| Command | Article | Upstream Version | POSIX.1-2024 | Status |
|:---|:---|:---|:---:|:---:|
| `awk` | [awk](./article/linux-awk-tutorial.md) | GNU GAWK 5.3.0 | Yes | Available |

### procps-ng (Process & System Inspection)

| Command | Article | Upstream Version | POSIX.1-2024 | Status |
|:---|:---|:---|:---:|:---:|
| `free` | [free](./article/linux-free-tutorial.md) | procps-ng 4.0.4 | No | Available |
| `pgrep` | [pgrep](./article/linux-pgrep-tutorial.md) | procps-ng 4.0.4 | No | Available |
| `pkill` | [pkill](./article/linux-pkill-tutorial.md) | procps-ng 4.0.4 | No | Available |
| `ps` | [ps](./article/linux-ps-tutorial.md) | procps-ng 4.0.4 | Yes | Available |
| `top` | [top](./article/linux-top-tutorial.md) | procps-ng 4.0.4 | No | Available |
| `uptime` | [uptime](./article/linux-uptime-tutorial.md) | procps-ng 4.0.4 | No | Available |
| `vmstat` | [vmstat](./article/linux-vmstat-tutorial.md) | procps-ng 4.0.4 | No | Available |
| `w` | [w](./article/linux-w-tutorial.md) | procps-ng 4.0.4 | No | Available |

### util-linux (Storage & Core System Administration)

| Command | Article | Upstream Version | POSIX.1-2024 | Status |
|:---|:---|:---|:---:|:---:|
| `blkid` | [blkid](./article/linux-blkid-tutorial.md) | util-linux 2.40 | No | Available |
| `fdisk` | [fdisk](./article/linux-fdisk-tutorial.md) | util-linux 2.40 | No | Available |
| `findmnt` | [findmnt](./article/linux-findmnt-tutorial.md) | util-linux 2.40 | No | Available |
| `lsblk` | [lsblk](./article/linux-lsblk-tutorial.md) | util-linux 2.40 | No | Available |
| `mount` | [mount](./article/linux-mount-tutorial.md) | util-linux 2.40 | No | Available |
| `umount` | [umount](./article/linux-umount-tutorial.md) | util-linux 2.40 | No | Available |

### iproute2 (Linux Networking Suite)

| Command | Article | Upstream Version | POSIX.1-2024 | Status |
|:---|:---|:---|:---:|:---:|
| `bridge` | [bridge](./article/linux-bridge-tutorial.md) | iproute2 6.13 | No | Available |
| `ip` | [ip](./article/linux-ip-tutorial.md) | iproute2 6.13 | No | Available |
| `ss` | [ss](./article/linux-ss-tutorial.md) | iproute2 6.13 | No | Available |
| `tc` | [tc](./article/linux-tc-tutorial.md) | iproute2 6.13 | No | Available |

### systemd (Services & System Journal)

| Command | Article | Upstream Version | POSIX.1-2024 | Status |
|:---|:---|:---|:---:|:---:|
| `journalctl` | [journalctl](./article/linux-journalctl-tutorial.md) | systemd 256 | No | Available |
| `systemctl` | [systemctl](./article/linux-systemctl-tutorial.md) | systemd 256 | No | Available |

### curl (Network Transfer)

| Command | Article | Upstream Version | POSIX.1-2024 | Status |
|:---|:---|:---|:---:|:---:|
| `curl` | [curl](./article/linux-curl-tutorial.md) | curl 8.12.0 | No | Available |

### rsync (Remote Sync)

| Command | Article | Upstream Version | POSIX.1-2024 | Status |
|:---|:---|:---|:---:|:---:|
| `rsync` | [rsync](./article/linux-rsync-tutorial.md) | rsync 3.5.0 | No | Available |

### GNU tar (Archiving)

| Command | Article | Upstream Version | POSIX.1-2024 | Status |
|:---|:---|:---|:---:|:---:|
| `tar` | [tar](./article/linux-tar-tutorial.md) | GNU tar 1.35 | No | Available |

### GNU gzip (Compression)

| Command | Article | Upstream Version | POSIX.1-2024 | Status |
|:---|:---|:---|:---:|:---:|
| `gzip` | [gzip](./article/linux-gzip-tutorial.md) | GNU gzip 1.13 | No | Available |

### XZ Utils (Compression)

| Command | Article | Upstream Version | POSIX.1-2024 | Status |
|:---|:---|:---|:---:|:---:|
| `xz` | [xz](./article/linux-xz-tutorial.md) | XZ Utils 5.6.2 | No | Available |

## Project Standards

- [Article Specification Contract](./docs/article-contract.md)

- [Upstream Inventory Schema](./schemas/upstream-inventory.schema.json)


**Catalog Summary:** 53/53 articles available.
