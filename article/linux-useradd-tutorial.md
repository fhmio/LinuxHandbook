---
title: "Linux Command Tutorial: useradd"
date: 2026-09-14T00:00:00+00:00
categories: ['Technology']
tags:
  - 'Linux'
  - 'shadow-utils'
  - 'useradd'
  - 'Linux Command Tutorial'
draft: false
slug: "linux-useradd-tutorial"
description: "Authoritative reference tutorial for useradd, detailing low-level user account creation, default configurations, skeletal directories, and system integrations."
upstream_suite: "shadow-utils"
upstream_version: "shadow-utils 4.14"
posix_standard: "None"
research_date: "2026-09-14"
---

The **Linux Command Tutorial** series provides rigorous, upstream-verified references for essential system commands across Linux distributions and UNIX-like environments. Each article focuses on a single executable, combining exhaustive option documentation, verified real-world examples, security boundaries, and best practices directly derived from official source documentation and POSIX standards.

---

## 1. Introduction

> **Upstream**: shadow-utils | **POSIX**: None | **Safety Tier**: privileged-system-destructive | **Scope**: user-management

`useradd` is a low-level utility for creating new user accounts and configuring their initial environments on Linux systems. 

- **Upstream Project & Provenance**: Part of the `shadow-utils` package, which maintains the core authentication and account management utilities on Linux.
- **Portability & Standards Baseline**: Account management is intentionally left undefined by POSIX.1-2024. `useradd` is specific to Linux (and some UNIX variants like Solaris), while BSD systems use `pw useradd` or `adduser`.
- **Target Research Implementation**: Audited against **shadow-utils 4.14**.
- **Applicability & Lifecycle**: The definitive standard for programmatic and script-based user creation on Linux. (Note: Many distributions offer an interactive Perl script called `adduser` which acts as a friendly wrapper around `useradd`).

---

## 2. Syntax and Command Model

### 2.1 Canonical Synopsis

```bash
useradd [options] LOGIN
useradd -D
useradd -D [options]
```

### 2.2 Execution Model & Adjacency Requirement

- `useradd` creates a new user account using the values specified on the command line plus the default values from the system.
- It locks and modifies the vital system identity files (`/etc/passwd`, `/etc/shadow`, `/etc/group`, and `/etc/gshadow`).
- Executing `useradd` requires superuser privileges (`root`).
- By default, `useradd` on many distributions (like CentOS/RHEL) automatically creates a home directory, but on Debian/Ubuntu, the `-m` flag is strictly required to generate one.

---

## 3. Options

### 3.1 Primary Flags

| Short Flag | Long Flag | Description | POSIX Defined |
|:---|:---|:---|:---:|
| `-m` | `--create-home` | Create the user's home directory if it does not exist. | No |
| `-M` | `--no-create-home` | Do not create the user's home directory. | No |
| `-d` | `--home-dir HOME_DIR`| Specify a custom path for the new user's home directory. | No |
| `-s` | `--shell SHELL` | Specify the path to the user's default login shell. | No |
| `-c` | `--comment COMMENT` | Add a comment field (GECOS), typically the user's full name. | No |
| `-g` | `--gid GROUP` | The group name or number of the user's initial login group. | No |
| `-G` | `--groups GROUPS` | A comma-separated list of supplementary groups. | No |
| `-u` | `--uid UID` | Force a specific numerical value for the user's ID. | No |
| `-r` | `--system` | Create a system account (UID < 1000) that typically has no password aging and does not create a home directory by default. | No |
| `-D` | `--defaults` | Print or update the default configuration values used by `useradd`. | No |

---

## 4. Basic Usage

### 4.1 Quick-Reference Cheatsheet Card

| Operation | Command | Notes |
|:---|:---|:---|
| Create a standard user | `sudo useradd -m alice` | Creates `alice` and populates `/home/alice`. |
| Create a service account | `sudo useradd -r -s /bin/false nginx` | System account, no home dir, no login shell. |
| View default settings | `useradd -D` | Read-only; shows default shell, home base, etc. |
| Add user to extra groups | `sudo useradd -m -G wheel,docker bob` | Creates `bob` and adds him to `wheel` & `docker`. |
| Set full name (GECOS) | `sudo useradd -c "Alice Smith" -m alice`| Adds descriptive comment in `/etc/passwd`. |

### 4.2 Viewing Default Configuration (`-D`)

Before creating users, you can inspect the default behavior of `useradd` on your specific distribution:

```console
$ useradd -D
GROUP=100
HOME=/home
INACTIVE=-1
EXPIRE=
SHELL=/bin/bash
SKEL=/etc/skel
CREATE_MAIL_SPOOL=yes
```

### 4.3 Creating a Basic Account

To create a new user named `alice` and generate her home directory:

```console
$ sudo useradd -m alice
```
*(Note: `useradd` does **not** prompt for a password. The account is locked until `passwd alice` is run.)*

---

## 5. Practical Operations

### 5.1 Creating a Fully Featured Human Account

Creating a user with a specific shell, a full name, and supplementary groups:

```console
$ sudo useradd -m -s /bin/zsh -c "Bob Developer" -G developers,docker bob
$ tail -n 1 /etc/passwd
bob:x:1001:1001:Bob Developer:/home/bob:/bin/zsh
```

### 5.2 Creating a System/Service Account

When installing software (like a database or web server), you should create a dedicated, unprivileged system account. Use `-r` (system account) and `-s /sbin/nologin` (disable shell access):

```console
$ sudo useradd -r -s /sbin/nologin postgres
$ grep postgres /etc/passwd
postgres:x:998:996::/home/postgres:/sbin/nologin
```

### 5.3 Copying the Skeleton Directory (`/etc/skel`)

When `-m` is used, `useradd` creates the home directory and populates it with default files (like `.bashrc` and `.profile`) copied from the skeleton directory `/etc/skel`. 
Administrators can place organization-wide default configurations inside `/etc/skel` before running `useradd`.

---

## 6. Advanced Usage

### 6.1 Creating Users in Automation Scripts

Because `useradd` is strictly non-interactive, it is perfectly suited for bash scripts and configuration management tools (Ansible, Puppet). However, setting the initial password securely in a script requires `chpasswd`:

```bash
#!/bin/bash
# Create user without prompting
useradd -m -s /bin/bash deployer

# Securely set the password from a variable
echo "deployer:SuperSecretPass123" | chpasswd
```

### 6.2 Modifying the Defaults (`-D`)

You can permanently change the `useradd` defaults by running `useradd -D` with options. For example, to change the default shell for all future users to `/bin/zsh`:

```console
$ sudo useradd -D -s /bin/zsh
```
This updates `/etc/default/useradd`.

---

## 7. Exit Status, Environment, and Configuration

### 7.1 Exit Status Codes

| Exit Code | Meaning |
|:---:|:---|
| `0` | Success. |
| `1` | Cannot update password file. |
| `2` | Invalid command syntax. |
| `3` | Invalid argument to an option. |
| `4` | UID already in use (and no `-o`). |
| `9` | Username already in use. |
| `10` | Cannot update group file. |
| `12` | Cannot create home directory. |

### 7.2 Configuration Files

| Path | Purpose |
|:---|:---|
| `/etc/default/useradd` | Contains default values (HOME, SHELL, SKEL) read and modified by `useradd -D`. |
| `/etc/login.defs` | Shadow password suite configuration, defining global constraints like `UID_MIN` and password aging. |
| `/etc/skel/` | The skeleton directory containing files to be copied to the new user's home directory. |

---

## 8. Safety, Security, and Portability

### 8.1 UID and GID Allocation

`useradd` dynamically finds the next available UID. For standard users, it checks `UID_MIN` and `UID_MAX` in `/etc/login.defs` (typically 1000 to 60000). For system accounts (`-r`), it checks `SYS_UID_MIN` and `SYS_UID_MAX` (typically 201 to 999). Never hardcode UIDs (`-u`) across fleet deployments unless explicitly managing a synchronized central directory.

### 8.2 File Locking

`useradd` uses `/etc/.pwd.lock` to prevent race conditions when modifying `/etc/passwd`. If the lockfile is orphaned due to a hard crash, `useradd` will fail to run until the lock is manually cleared.

---

## 9. Best Practices

1. **Explicitly Use `-m` on Debian/Ubuntu**:
   - *Guidance*: Never assume `useradd` will create a home directory. Always supply `-m` if one is needed.
   - *Authoritative Justification*: While RHEL's `useradd` defaults to `CREATE_HOME=yes`, Debian's `useradd` defaults to `CREATE_HOME=no`. Explicit flags guarantee portability.
2. **Never Give Service Accounts Valid Shells**:
   - *Guidance*: Always specify `-s /sbin/nologin` or `-s /bin/false` for daemons and services.
   - *Authoritative Justification*: Prevents an attacker who exploits the service from gaining an interactive shell environment.
3. **Prefer `useradd` over `adduser` in Scripts**:
   - *Guidance*: Use the POSIX-compliant syntax of `useradd` in scripts, not the interactive `adduser` Perl script.
   - *Authoritative Justification*: `adduser` prompts for passwords and GECOS information via stdin, which breaks non-interactive automation pipelines.

---

## References

1. **shadow-utils useradd Manual Page**: `man 8 useradd`
2. **Linux From Scratch - Shadow**: [https://www.linuxfromscratch.org/lfs/view/development/chapter08/shadow.html](https://www.linuxfromscratch.org/lfs/view/development/chapter08/shadow.html)
3. **Debian Administrator's Handbook - Account Management**: [https://debian-handbook.info/browse/stable/sect.user-management.html](https://debian-handbook.info/browse/stable/sect.user-management.html)
