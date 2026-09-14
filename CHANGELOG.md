# Changelog

All notable changes to the **LinuxHandbook** project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2026-09-14

### Initial Production Release: The Authoritative Linux Reference & Operational Systems Playbook

This milestone release establishes **LinuxHandbook** as an authoritative, upstream-aligned systems reference and documentation portal for Linux system engineers, DevOps practitioners, and developers.

---

### Added

#### 1. 64 Authoritative Linux Command Tutorials
Authored and published 64 comprehensive, production-grade Linux command references adhering strictly to the [20-Point Article Contract](docs/article-contract.md):
- **Core File Operations (GNU Coreutils)**: `cat`, `cp`, `mv`, `rm`, `mkdir`, `rmdir`, `touch`, `ln`, `ls`
- **Text Processing & Pattern Matching**: `awk`, `sed`, `grep`, `cut`, `sort`, `uniq`, `tr`, `head`, `tail`
- **Modern Networking (iproute2 & Sockets)**: `ip`, `ss`, `bridge`, `tc`
- **OpenSSH Secure Communications Suite**: `ssh`, `scp`, `sftp`, `ssh-keygen`, `ssh-agent`, `ssh-add`, `ssh-keyscan`
- **Storage, Partitions & Filesystems (util-linux)**: `lsblk`, `blkid`, `fdisk`, `mount`, `umount`, `findmnt`
- **Process & System Monitoring (procps-ng)**: `ps`, `top`, `free`, `uptime`, `vmstat`, `w`, `pgrep`, `pkill`
- **Package Management Systems**: `apt` (Debian/Ubuntu), `dnf` (Fedora/RHEL/CentOS), `yum` (Legacy Enterprise Linux)
- **User & Privilege Management (shadow-utils & sudo)**: `useradd`, `usermod`, `passwd`, `su`, `sudo`
- **Process & Job Control**: `kill`, `killall`, `jobs`
- **System Initialization & Logging (systemd)**: `systemctl`, `journalctl`
- **Search & Traversal (Findutils & mlocate)**: `find`, `xargs`, `locate`
- **Archiving, Compression & Transfers**: `tar`, `gzip`, `xz`, `rsync`, `curl`

#### 2. Enhanced Visual Learning & Safe Operations
Every tutorial includes:
- **Quick-Reference Cards**: Instant flag tables and high-frequency syntax at the top of every guide.
- **Copyable One-Liner Commands**: Copy-ready snippets formatted for rapid execution in production terminals.
- **Visual ASCII Diagrams & Flowcharts**: Architectural visuals illustrating command flags, data pipelines, packet filters, and process lifecycles.
- **Blast Radius & Safety Callouts**: Standardized GitHub-style callouts (`[!CAUTION]`, `[!WARNING]`, `[!TIP]`) preventing accidental service disruption or data loss.
- **Real-World Troubleshooting Scenarios**: Field-tested diagnostic procedures for high-load systems, memory leaks, zombie processes, disk saturation, and connection drops.

#### 3. Upstream Metadata Inventories (JSON)
Created 13 validated, machine-readable JSON inventories in `data/inventory/` aligned with upstream tool maintainers:
- `coreutils-files.json`
- `text-processing.json`
- `findutils.json`
- `networking.json`
- `storage-admin.json`
- `process-monitoring.json`
- `openssh.json`
- `systemd.json`
- `network-transfer.json`
- `compression.json`
- `package-management.json`
- `user-management.json`
- `process-control.json`

#### 4. Automated Testing & Verification Tooling
Implemented custom Python automated verification tools in `scripts/`:
- `validate_inventory.py`: Validates all JSON files against `schemas/upstream-inventory.schema.json`.
- `validate_articles.py`: Enforces the 20-point article contract across all Markdown documents (frontmatter, structure, headings, callouts, safety advisories).
- `generate_readme.py`: Automatically compiles the central `README.md` catalog, category tables, and operational safety playbooks.

#### 5. VitePress Documentation Portal & Custom Linuxize UI Theme
- Deployed a static documentation engine powered by VitePress (`v1.6.4`).
- Custom Linuxize-inspired responsive layout with high-readability typography, dark mode support, category browse cards, quick search, reading progress, and terminal-aesthetic code blocks.
- Optimized static site build with zero dead links and sub-second page loads.

#### 6. Continuous Integration & Deployment Workflows
- Added `.github/workflows/ci.yml`: Automated quality gate executing article linting, inventory validation, and documentation build on every commit and PR.
- Added `.github/workflows/deploy.yml`: Automated deployment workflow building and hosting the VitePress site on GitHub Pages.

---

### Changed
- **Rebranding**: Transitioned repository identity from generic tutorial repository to **LinuxHandbook**: *The Authoritative Linux Reference & Operational Systems Playbook*.
- **Catalog Navigation**: Unified table of contents with tier badges (Tier 1 Core, Tier 2 Operational, Tier 3 Advanced).
