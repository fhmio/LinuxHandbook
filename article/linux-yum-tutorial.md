---
title: "Linux Command Tutorial: yum"
date: 2026-09-14T00:00:00+00:00
categories: ['Technology']
tags:
  - 'Linux'
  - 'Package Management'
  - 'yum'
  - 'Linux Command Tutorial'
draft: false
slug: "linux-yum-tutorial"
description: "Authoritative reference tutorial for yum (Yellowdog Updater, Modified), detailing RPM package resolution, repository management, and legacy CentOS/RHEL workflows."
upstream_suite: "yum"
upstream_version: "YUM 3.4.3"
posix_standard: "None"
research_date: "2026-09-14"
---

The **Linux Command Tutorial** series provides rigorous, upstream-verified references for essential system commands across Linux distributions and UNIX-like environments. Each article focuses on a single executable, combining exhaustive option documentation, verified real-world examples, security boundaries, and best practices directly derived from official source documentation and POSIX standards.

---

## 1. Introduction

> **Upstream**: YUM Project | **POSIX**: None | **Safety Tier**: privileged-destructive | **Scope**: package-management

`yum` (Yellowdog Updater, Modified) is an interactive, automated update program which can be used for maintaining systems using RPM packages. It automatically calculates dependencies and figures out what things should occur to install packages. 

- **Upstream Project & Provenance**: Originally created by Yellow Dog Linux, later adopted by Red Hat for RHEL, CentOS, and Fedora.
- **Portability & Standards Baseline**: `yum` is specific to RPM-based Linux distributions. It is not defined in POSIX.
- **Target Research Implementation**: Audited against **YUM 3.4.3** (the classic version used in CentOS 7).
- **Applicability & Lifecycle**: **Deprecated** on modern systems. Replaced by `dnf` in Fedora 22, RHEL 8, and CentOS 8. However, `yum` remains heavily used in legacy environments and is often symlinked to `dnf` on newer systems.

---

## 2. Syntax and Command Model

### 2.1 Canonical Synopsis

```bash
yum [options] [command] [package ...]
```

### 2.2 Execution Model & Adjacency Requirement

- `yum` uses a local SQLite-based cache of repository metadata to resolve RPM dependencies.
- It contacts repository servers defined in `/etc/yum.repos.d/` to fetch metadata and packages.
- Installing or removing packages requires superuser privileges (`root`).
- Uses `/var/run/yum.pid` as a lock file to prevent concurrent execution of multiple `yum` instances modifying the RPM database.

---

## 3. Options

### 3.1 Primary Commands

| Command | Description |
|:---|:---|
| `install` | Installs the latest version of a package or group of packages. |
| `update` | Updates the specified packages to their latest versions. If no packages are specified, updates all installed packages. |
| `check-update` | Checks if updates are available for installed packages. |
| `remove` / `erase` | Removes the specified packages from the system. |
| `list` | Lists information about packages (installed, available, updates). |
| `info` | Displays detailed descriptions and summaries of packages. |
| `search` | Finds packages matching a keyword in their description, summary, or name. |
| `clean` | Cleans up the local `yum` cache (e.g., `yum clean all`). |
| `history` | Views or manipulates the `yum` transaction history. |

### 3.2 Primary Flags

| Short Flag | Long Flag | Description | POSIX Defined |
|:---|:---|:---|:---:|
| `-y` | `--assumeyes` | Assume "yes" to all questions prompt, running non-interactively. | No |
| `-q` | `--quiet` | Run without output (except for errors). | No |
| `-v` | `--verbose` | Run with detailed debugging and status output. | No |
| N/A | `--enablerepo=REPO` | Temporarily enable a specific repository. | No |
| N/A | `--disablerepo=REPO` | Temporarily disable a specific repository. | No |
| N/A | `--nogpgcheck` | Disable GPG signature checking for package installation. | No |

---

## 4. Basic Usage

### 4.1 Quick-Reference Cheatsheet Card

| Operation | Command | Notes |
|:---|:---|:---|
| Install a package | `sudo yum install <pkg>` | Automatically resolves and installs dependencies. |
| Update all packages | `sudo yum update` | Safely applies available updates to the system. |
| Search for a package | `yum search <term>` | Read-only search against configured repos. |
| View package info | `yum info <pkg>` | Shows architecture, size, version, and description. |
| Clean metadata cache | `sudo yum clean all` | Fixes synchronization issues if repositories change. |

### 4.2 Searching for a Package

```console
$ yum search httpd
Loaded plugins: fastestmirror
Loading mirror speeds from cached hostfile
 * base: mirror.centos.org
 * extras: mirror.centos.org
 * updates: mirror.centos.org
============================== N/S matched: httpd ==============================
httpd.x86_64 : Apache HTTP Server
httpd-devel.x86_64 : Development interfaces for the Apache HTTP server
httpd-manual.noarch : Documentation for the Apache HTTP server
httpd-tools.x86_64 : Tools for use with the Apache HTTP Server
```

### 4.3 Listing Installed Packages

```console
$ yum list installed | grep bash
bash.x86_64            4.2.46-34.el7         @base
```

---

## 5. Practical Operations

### 5.1 Installing a Package

Installing the `epel-release` repository package:

```console
$ sudo yum install epel-release
Loaded plugins: fastestmirror
Loading mirror speeds from cached hostfile
Resolving Dependencies
--> Running transaction check
---> Package epel-release.noarch 0:7-11 will be installed
--> Finished Dependency Resolution

Dependencies Resolved

================================================================================
 Package                Arch             Version         Repository        Size
================================================================================
Installing:
 epel-release           noarch           7-11            extras            15 k

Transaction Summary
================================================================================
Install  1 Package

Total download size: 15 k
Installed size: 24 k
Is this ok [y/d/N]: y
Downloading packages:
epel-release-7-11.noarch.rpm                               |  15 kB   00:00
Running transaction check
Running transaction test
Transaction test succeeded
Running transaction
  Installing : epel-release-7-11.noarch                                     1/1
  Verifying  : epel-release-7-11.noarch                                     1/1

Installed:
  epel-release.noarch 0:7-11

Complete!
```

### 5.2 Removing a Package

When removing a package, `yum` will also remove dependencies that are no longer needed by any other installed package (if configured to do so in `yum.conf` via `clean_requirements_on_remove`):

```console
$ sudo yum remove vim-enhanced
```

### 5.3 Reviewing and Undoing Transactions

`yum history` tracks all changes made to the system via `yum`. You can view past transactions and even roll them back:

```console
$ sudo yum history
ID     | Login user               | Date and time    | Action(s)      | Altered
-------------------------------------------------------------------------------
     4 | root <root>              | 2026-09-14 10:00 | Install        |    1
     3 | root <root>              | 2026-09-13 14:20 | Update         |   15
```
To undo transaction ID 4:
```bash
sudo yum history undo 4
```

---

## 6. Advanced Usage

### 6.1 Automating Installations in Scripts

In automation scripts (like bash scripts or older config management modules), use `-y` to suppress prompts. Unlike `apt`, `yum` is safer to use in scripts directly:

```bash
yum -y install wget curl
```

### 6.2 Working with Specific Repositories

If you have a repository disabled by default in `/etc/yum.repos.d/`, you can enable it for a single transaction:

```bash
sudo yum --enablerepo=epel-testing update nginx
```

---

## 7. Exit Status, Environment, and Configuration

### 7.1 Exit Status Codes

| Exit Code | Meaning |
|:---:|:---|
| `0` | Success (operation completed without errors). |
| `1` | General error (e.g., package not found or network error). |
| `100` | Packages are available for update (specifically returned by `check-update`). |

### 7.2 Configuration Files

| Path | Purpose |
|:---|:---|
| `/etc/yum.conf` | Global configuration file for `yum` (cache directories, proxy settings, logging). |
| `/etc/yum.repos.d/` | Directory containing `.repo` files defining package repositories. |
| `/var/cache/yum/` | Directory where downloaded packages and metadata are cached. |
| `/var/log/yum.log` | Log file recording all installations, updates, and removals. |

---

## 8. Safety, Security, and Portability

### 8.1 Package Signatures (GPG)

By default, `yum` enforces GPG signature checking (`gpgcheck=1` in `/etc/yum.conf`). If a package's signature does not match the configured repository keys, `yum` will refuse to install it, protecting against supply chain attacks. Using `--nogpgcheck` bypasses this protection and should be strictly avoided in production.

### 8.2 Safe Removal

Using `yum remove` on a core package (like `glibc` or `systemd`) can accidentally destroy a system, as `yum` will attempt to recursively remove all packages that depend on it. Always carefully review the "Transaction Summary" before confirming `y`.

---

## 9. Best Practices

1. **Migrate to DNF on Modern Systems**:
   - *Guidance*: If you are on RHEL 8+, CentOS 8+, or Fedora, use `dnf` instead of `yum`.
   - *Authoritative Justification*: The `yum` project is deprecated; `dnf` provides a modernized dependency resolver (libsolv), better performance, and a largely backward-compatible CLI.
2. **Clean Cache After Network Changes**:
   - *Guidance*: Run `sudo yum clean all` if you encounter unexpected 404 errors or mirror synchronization issues.
   - *Authoritative Justification*: YUM aggressively caches metadata to improve performance, which can become stale if mirror configurations change.
3. **Use `history undo` for Rollbacks**:
   - *Guidance*: Rely on `yum history undo <ID>` instead of manually attempting to downgrade or remove a batch of recently installed packages.

---

## References

1. **CentOS 7 Package Management Guide**: [https://docs.centos.org/en-US/centos/install-guide/Package_Management/](https://docs.centos.org/en-US/centos/install-guide/Package_Management/)
2. **YUM Manual Page**: `man 8 yum`
3. **Fedora Project - DNF (YUM successor)**: [https://docs.fedoraproject.org/en-US/quick-docs/dnf/](https://docs.fedoraproject.org/en-US/quick-docs/dnf/)
