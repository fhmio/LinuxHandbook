---
title: "Linux Command Tutorial: su"
date: 2026-09-14T00:00:00+00:00
categories: ['Technology']
tags:
  - 'Linux'
  - 'util-linux'
  - 'su'
  - 'Linux Command Tutorial'
draft: false
slug: "linux-su-tutorial"
description: "Authoritative reference tutorial for su (Substitute User), detailing identity switching, login shell simulation, PAM integration, and security boundaries."
upstream_suite: "util-linux"
upstream_version: "util-linux 2.40"
posix_standard: "None"
research_date: "2026-09-14"
---

The **Linux Command Tutorial** series provides rigorous, upstream-verified references for essential system commands across Linux distributions and UNIX-like environments. Each article focuses on a single executable, combining exhaustive option documentation, verified real-world examples, security boundaries, and best practices directly derived from official source documentation and POSIX standards.

---

## 1. Introduction

> **Upstream**: util-linux | **POSIX**: None | **Safety Tier**: privileged-system-destructive | **Scope**: user-management

`su` allows you to run commands with a substitute user and group ID. When called without arguments, `su` defaults to running an interactive shell as the `root` user.

- **Upstream Project & Provenance**: Originally part of AT&T UNIX. On modern Linux, `su` is typically provided by the **util-linux** suite (formerly part of GNU Coreutils or shadow-utils).
- **Portability & Standards Baseline**: `su` is a classic UNIX command but is strictly **not** defined in POSIX.1-2024, as user identity switching mechanisms are considered implementation-defined.
- **Target Research Implementation**: Audited against **util-linux 2.40**.
- **Applicability & Lifecycle**: A fundamental tool for identity switching. While often superseded by `sudo` for administrative workflows, `su` remains essential for directly assuming service accounts and full root login environments.

---

## 2. Syntax and Command Model

### 2.1 Canonical Synopsis

```bash
su [options] [-] [user [argument...]]
```

### 2.2 Execution Model & Adjacency Requirement

- `su` requests the password of the **target user**, unlike `sudo` which requests the password of the **invoking user**.
- By default, `su` spawns a new shell but retains the environment variables of the invoking user.
- To simulate a full login (reading `.bash_profile`, resetting `$HOME`, `$PATH`, etc.), the `-` (or `--login`) flag must be used.
- Authentication and session management are completely delegated to PAM (Pluggable Authentication Modules).

---

## 3. Options

### 3.1 Primary Flags

| Short Flag | Long Flag | Description | POSIX Defined |
|:---|:---|:---|:---:|
| `-` / `-l` | `--login` | Start the shell as a login shell with an environment similar to a real login. | No |
| `-c` | `--command=COMMAND` | Pass a single command to the invoked shell using `-c`. | No |
| `-s` | `--shell=SHELL` | Specify the shell to run instead of the user's default shell in `/etc/passwd`. | No |
| `-m` / `-p` | `--preserve-environment`| Do not reset environment variables (e.g., `$HOME`, `$USER`). | No |
| `-g` | `--group=GROUP` | Specify the primary group. Available only if invoked by root. | No |
| `-G` | `--supp-group=GROUP` | Specify a supplementary group. Available only if invoked by root. | No |

---

## 4. Basic Usage

### 4.1 Quick-Reference Cheatsheet Card

| Operation | Command | Notes |
|:---|:---|:---|
| Switch to root (keep env) | `su` | Prompts for root password. Retains current directory and variables. |
| Switch to root (full login) | `su -` | Simulates a fresh root login, changing to `/root` and resetting `$PATH`. |
| Switch to a specific user | `su - alice` | Prompts for Alice's password and simulates her login. |
| Run a command as user | `su -c 'ls -l' alice` | Executes one command as Alice and returns. |
| Override default shell | `su -s /bin/bash postgres`| Useful when target user has `/sbin/nologin`. |

### 4.2 Switching to Root (Interactive)

```console
$ su
Password:
# pwd
/home/alice
# echo $HOME
/home/alice
```
*(Notice that without `-`, the `$HOME` and working directory remain the invoking user's.)*

### 4.3 Switching to Root (Login Shell)

```console
$ su -
Password:
# pwd
/root
# echo $HOME
/root
```

---

## 5. Practical Operations

### 5.1 Assuming a Service Account

System administrators frequently need to run commands as unprivileged service accounts (like `postgres` or `nginx`). Since these accounts often have `/sbin/nologin` or `/bin/false` as their shell, standard `su` fails. Use `-s` to override the shell (must be run as root):

```console
# su -s /bin/bash postgres
bash-5.1$ psql
```

### 5.2 Executing a Single Command as Another User

To execute a command pipeline as another user without opening an interactive session:

```console
# su -c "pg_dump database > backup.sql" postgres
```

### 5.3 Preserving the Environment

If you need to switch to root but require an environment variable exported in your normal user session (e.g., `DISPLAY` for X11 applications, though not recommended for security):

```console
$ su -p
```

---

## 6. Advanced Usage

### 6.1 Using `su` in Shell Scripts

Using `su` within a script can be problematic because it inherently expects a TTY for password input. However, if the script is running as root, `su` does not prompt for a password.

```bash
#!/bin/bash
# Backup script running as root

echo "Starting backup as postgres user..."
su -c "/usr/bin/pg_dumpall > /backups/all.sql" postgres
echo "Backup complete."
```

### 6.2 Bypassing PAM Limits

In highly restricted environments, administrators can use `su` to bypass certain login restrictions. For instance, if a user is restricted from SSH access via PAM, an administrator can SSH as root and `su` into the user.

---

## 7. Exit Status, Environment, and Configuration

### 7.1 Exit Status Codes

| Exit Code | Meaning |
|:---:|:---|
| `0` | Success (if invoked with `-c`, returns the exit code of the executed command). |
| `1` | General failure (e.g., incorrect password, PAM failure). |
| `126` | Command found but not executable. |
| `127` | Command not found. |

### 7.2 Configuration Files

| Path | Purpose |
|:---|:---|
| `/etc/pam.d/su` | PAM configuration file governing authentication rules for `su`. |
| `/etc/pam.d/su-l` | PAM configuration specifically for `su --login`. |
| `/etc/login.defs` | Contains global parameters (like `SU_WHEEL_ONLY`) that influence `su` behavior. |
| `/etc/passwd` | Read to determine the target user's home directory and default shell. |

---

## 8. Safety, Security, and Portability

### 8.1 The Risk of Preserving Environment

> [!WARNING]
> Running `su` without `-` (or `--login`) is dangerous. It preserves the invoking user's environment, including `$PATH` and `$LD_LIBRARY_PATH`. A malicious user could set `$PATH` to point to a compromised binary, tricking the root user into executing it. Always use `su -` for administrative tasks.

### 8.2 The `wheel` Group Restriction

On many enterprise systems (e.g., RHEL), `su` to root is restricted via PAM to users who belong to the `wheel` group. If a user is not in the `wheel` group, `su` will fail immediately, even if the user knows the root password.

### 8.3 `su` vs `sudo`

`su` requires sharing the root password, which violates the principle of individual accountability. `sudo` is widely preferred because it authenticates the invoking user, allows granular command restrictions, and logs execution to `/var/log/auth.log`.

---

## 9. Best Practices

1. **Always Use Login Shells for Root**:
   - *Guidance*: Always invoke as `su -` rather than `su`.
   - *Authoritative Justification*: The util-linux manual explicitly notes that avoiding `--login` can cause unpredictable behavior due to environment pollution.
2. **Prefer `sudo` Over `su` for Routine Admin Tasks**:
   - *Guidance*: Use `sudo -i` or `sudo command` instead of sharing the root password via `su`.
   - *Authoritative Justification*: Centralizes audit logging and adheres to least-privilege principles.
3. **Use `-s` and `-c` for Service Contexts**:
   - *Guidance*: Use `su -s /bin/bash -c "cmd" user` to invoke actions as service accounts without changing their secure `/sbin/nologin` default.

---

## References

1. **util-linux su Manual Page**: `man 1 su`
2. **Debian Wiki - su**: [https://wiki.debian.org/su](https://wiki.debian.org/su)
3. **Linux PAM System Administrator's Guide**: [https://www.linux-pam.org/Linux-PAM-html/Linux-PAM_SAG.html](https://www.linux-pam.org/Linux-PAM-html/Linux-PAM_SAG.html)
