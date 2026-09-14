---
title: "Linux Command Tutorial: dnf"
date: 2026-09-14T00:00:00+00:00
categories: ['Technology']
tags:
  - 'Linux'
  - 'Package Management'
  - 'dnf'
  - 'Linux Command Tutorial'
draft: false
slug: "linux-dnf-tutorial"
description: "Authoritative reference tutorial for dnf (Dandified YUM), detailing advanced package resolution, modules, repository management, and Fedora/RHEL workflows."
upstream_suite: "dnf"
upstream_version: "DNF 4.14"
posix_standard: "None"
research_date: "2026-09-14"
---

The **Linux Command Tutorial** series provides rigorous, upstream-verified references for essential system commands across Linux distributions and UNIX-like environments. Each article focuses on a single executable, combining exhaustive option documentation, verified real-world examples, security boundaries, and best practices directly derived from official source documentation and POSIX standards.

---

## 1. Introduction

> **Upstream**: DNF Project | **POSIX**: None | **Safety Tier**: privileged-destructive | **Scope**: package-management

`dnf` (Dandified YUM) is the next-generation version of the Yellowdog Updater, Modified (YUM), serving as the primary package manager for RPM-based Linux distributions like Fedora, RHEL 8+, and CentOS 8+. It resolves the performance bottlenecks, excessive memory usage, and slow dependency resolution of legacy `yum` by utilizing `libsolv` under the hood.

- **Upstream Project & Provenance**: Maintained by the DNF development team (primarily at Red Hat).
- **Portability & Standards Baseline**: Specific to modern RPM-based distributions. Not defined in POSIX.
- **Target Research Implementation**: Audited against **DNF 4.14**.
- **Applicability & Lifecycle**: The definitive standard for interactive package management on modern Fedora and Enterprise Linux. Maintains strict CLI compatibility with `yum` for most basic operations.

---

## 2. Syntax and Command Model

### 2.1 Canonical Synopsis

```bash
dnf [options] [command] [package ...]
```

### 2.2 Execution Model & Adjacency Requirement

- `dnf` uses a localized metadata cache, which it periodically synchronizes with configured repositories.
- It utilizes an advanced boolean satisfiability solver (`libsolv`) to compute dependency trees instantly, preventing the "dependency hell" seen in older managers.
- State-altering commands (install, upgrade, remove) require superuser privileges. Read-only commands (search, repoquery) can run as an unprivileged user.

---

## 3. Options

### 3.1 Primary Commands

| Command | Description |
|:---|:---|
| `install` | Installs the specified packages along with required dependencies. |
| `upgrade` | Upgrades installed packages to the newest available versions. |
| `remove` / `erase` | Removes the specified packages. |
| `autoremove` | Removes packages installed as dependencies that are no longer required. |
| `search` | Searches package metadata for keywords. |
| `info` | Displays detailed summaries for packages. |
| `list` | Lists installed and available packages. |
| `module` | Interacts with AppStream modules (enable, disable, install streams). |
| `repoquery` | Searches for packages matching complex criteria (e.g., querying dependencies). |
| `history` | Views, reverts, or repeats past transactions. |

### 3.2 Primary Flags

| Short Flag | Long Flag | Description | POSIX Defined |
|:---|:---|:---|:---:|
| `-y` | `--assumeyes` | Automatically answer yes for all questions. | No |
| `-q` | `--quiet` | Run quietly, suppressing normal output. | No |
| `-v` | `--verbose` | Output verbose debugging information. | No |
| N/A | `--enablerepo=REPO`| Enable additional repositories. | No |
| N/A | `--disablerepo=REPO`| Disable specific repositories. | No |
| N/A | `--refresh` | Force synchronization of repository metadata before running. | No |

---

## 4. Basic Usage

### 4.1 Quick-Reference Cheatsheet Card

| Operation | Command | Notes |
|:---|:---|:---|
| Install software | `sudo dnf install <pkg>` | Computes dependencies using `libsolv`. |
| Upgrade system | `sudo dnf upgrade` | Recommended method to apply all updates. |
| Search repositories | `dnf search <term>` | Checks descriptions, summaries, and names. |
| List installed software | `dnf list --installed` | Dumps all currently installed packages. |
| Force metadata refresh | `sudo dnf makecache --refresh`| Refreshes all configured repository caches. |

### 4.2 Searching for a Package

```console
$ dnf search podman
Last metadata expiration check: 0:45:12 ago on Mon Sep 14 09:00:00 2026.
======================= Name Exactly Matched: podman =======================
podman.x86_64 : Manage Pods, Containers and Container Images
====================== Name & Summary Matched: podman ======================
cockpit-podman.noarch : Cockpit UI for podman containers
podman-docker.noarch : Emulate Docker CLI using podman
podman-plugins.x86_64 : Plugins for podman
```

### 4.3 Showing Package Information

```console
$ dnf info nginx
Last metadata expiration check: 1:12:05 ago on Mon Sep 14 09:00:00 2026.
Installed Packages
Name         : nginx
Version      : 1.24.0
Release      : 1.el9
Architecture : x86_64
Size         : 1.4 M
Source       : nginx-1.24.0-1.el9.src.rpm
Repository   : @System
From repo    : appstream
Summary      : A high performance web server and reverse proxy server
```

---

## 5. Practical Operations

### 5.1 Installing a Package with Confirmation

Installing `tmux`:

```console
$ sudo dnf install tmux
Dependencies resolved.
================================================================================
 Package        Architecture     Version               Repository          Size
================================================================================
Installing:
 tmux           x86_64           3.2a-4.el9            baseos             364 k

Transaction Summary
================================================================================
Install  1 Package

Total download size: 364 k
Installed size: 915 k
Is this ok [y/N]: y
Downloading Packages:
tmux-3.2a-4.el9.x86_64.rpm                      1.5 MB/s | 364 kB     00:00    
--------------------------------------------------------------------------------
Total                                           820 kB/s | 364 kB     00:00     
Running transaction check
Transaction check succeeded.
Running transaction test
Transaction test succeeded.
Running transaction
  Preparing        :                                                        1/1 
  Installing       : tmux-3.2a-4.el9.x86_64                                 1/1 
  Running scriptlet: tmux-3.2a-4.el9.x86_64                                 1/1 
  Verifying        : tmux-3.2a-4.el9.x86_64                                 1/1 

Installed:
  tmux-3.2a-4.el9.x86_64

Complete!
```

### 5.2 Managing AppStream Modules

Modern RHEL/Fedora introduces Modularity, where multiple major versions of software (e.g., PostgreSQL 13, 14, 15) are available in the same repository as "Streams".

To list available streams for Node.js:
```console
$ dnf module list nodejs
```
To enable and install a specific stream (e.g., Node.js 18):
```bash
sudo dnf module enable nodejs:18
sudo dnf install nodejs
```

### 5.3 Undoing Transactions with DNF History

Like `yum`, `dnf` tracks all state changes. You can view the history:
```console
$ sudo dnf history
ID     | Command line             | Date and time    | Action(s)      | Altered
-------------------------------------------------------------------------------
    12 | install tmux             | 2026-09-14 09:30 | Install        |    1
    11 | upgrade                  | 2026-09-13 18:45 | Upgrade        |   42
```
To rollback the installation of `tmux` (ID 12):
```bash
sudo dnf history undo 12
```

---

## 6. Advanced Usage

### 6.1 Querying Repositories (`repoquery`)

`repoquery` is built directly into DNF, allowing you to interrogate the package database without installing packages.

To find which package provides a specific missing binary or file (e.g., `semanage`):
```console
$ dnf repoquery --provides *bin/semanage
policycoreutils-python-utils-0:3.5-1.el9.noarch
```

To view the dependency tree of a package before installing it:
```console
$ dnf repoquery --requires --resolve docker
```

---

## 7. Exit Status, Environment, and Configuration

### 7.1 Exit Status Codes

| Exit Code | Meaning |
|:---:|:---|
| `0` | Success (operation completed normally). |
| `1` | General error (e.g., network failure, dependency conflict). |
| `100` | Updates available (returned specifically by `dnf check-update`). |

### 7.2 Configuration Files

| Path | Purpose |
|:---|:---|
| `/etc/dnf/dnf.conf` | Global DNF configuration file. |
| `/etc/yum.repos.d/` | Directory defining repository configurations (`.repo` files). Retained for `yum` compatibility. |
| `/var/cache/dnf/` | Local metadata and package cache. |
| `/var/log/dnf.log` | Detailed log of DNF operations. |

---

## 8. Safety, Security, and Portability

### 8.1 GPG Signature Verification

DNF enforces `gpgcheck=1` strictly by default, ensuring all downloaded packages are cryptographically signed by the repository maintainer. If a signature fails, DNF aborts the installation.

### 8.2 Autoremoval Safeguards

When running `dnf autoremove`, DNF identifies orphaned dependencies. However, it explicitly protects core packages (defined in `/etc/dnf/protected.d/`, e.g., `systemd`, `dnf`, `kernel`) from ever being removed, preventing catastrophic system destruction.

---

## 9. Best Practices

1. **Prefer `dnf upgrade` over `dnf update`**:
   - *Guidance*: Always use `dnf upgrade` for applying patches.
   - *Authoritative Justification*: While `update` is accepted as an alias for backwards compatibility with `yum`, `upgrade` is the canonical DNF command to update packages and safely handle obsoletes (replacing deprecated packages).
2. **Do Not Manually Delete the Cache Directory**:
   - *Guidance*: Never `rm -rf /var/cache/dnf/`. Always use `sudo dnf clean all`.
   - *Authoritative Justification*: Manual deletion can corrupt local SQLite databases that DNF relies upon for tracking repository states.
3. **Use AppStream Modules for Language Runtimes**:
   - *Guidance*: When installing Python, Node.js, or PostgreSQL on RHEL 8+, use `dnf module` rather than relying solely on the default stream.
   - *Authoritative Justification*: Allows deterministic pinning of major language versions, preventing breaking changes during global system upgrades.

---

## References

1. **DNF Official Documentation**: [https://dnf.readthedocs.io/en/latest/](https://dnf.readthedocs.io/en/latest/)
2. **Red Hat Enterprise Linux 9 - Managing Software**: [https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/9/html/managing_software_with_the_dnf_tool/](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/9/html/managing_software_with_the_dnf_tool/)
3. **Fedora Package Management**: [https://docs.fedoraproject.org/en-US/quick-docs/dnf/](https://docs.fedoraproject.org/en-US/quick-docs/dnf/)
