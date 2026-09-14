---
title: "Linux Command Tutorial: passwd"
date: 2026-09-14T00:00:00+00:00
categories: ['Technology']
tags:
  - 'Linux'
  - 'shadow-utils'
  - 'passwd'
  - 'Linux Command Tutorial'
draft: false
slug: "linux-passwd-tutorial"
description: "Authoritative reference tutorial for passwd, detailing user password changes, account locking, password aging, and PAM integration."
upstream_suite: "shadow-utils"
upstream_version: "shadow-utils 4.14"
posix_standard: "None"
research_date: "2026-09-14"
---

The **Linux Command Tutorial** series provides rigorous, upstream-verified references for essential system commands across Linux distributions and UNIX-like environments. Each article focuses on a single executable, combining exhaustive option documentation, verified real-world examples, security boundaries, and best practices directly derived from official source documentation and POSIX standards.

---

## 1. Introduction

> **Upstream**: shadow-utils | **POSIX**: None | **Safety Tier**: privileged-system-destructive | **Scope**: user-management

`passwd` changes passwords for user accounts. A normal user may only change the password for their own account, whereas the superuser (`root`) may change the password for any account. It also allows administrators to manage account locking and password aging parameters.

- **Upstream Project & Provenance**: Core component of the `shadow-utils` suite.
- **Portability & Standards Baseline**: Not strictly defined in POSIX.1-2024 (though historically present in various UNIX specifications). Implementation and password hashing mechanisms vary wildly across UNIX-like systems.
- **Target Research Implementation**: Audited against **shadow-utils 4.14**.
- **Applicability & Lifecycle**: The fundamental tool for credential management on Linux.

---

## 2. Syntax and Command Model

### 2.1 Canonical Synopsis

```bash
passwd [options] [LOGIN]
```

### 2.2 Execution Model & Adjacency Requirement

- `passwd` updates the `/etc/shadow` file, where the actual encrypted password hashes are stored.
- The binary is typically installed with **setuid root** permissions (`-rwsr-xr-x`), allowing an unprivileged user to temporarily execute as root in order to write to `/etc/shadow`.
- Password complexity, strength checking, and hashing algorithms (e.g., SHA-512, yescrypt) are entirely delegated to **PAM** (Pluggable Authentication Modules), not the `passwd` binary itself.
- Normal users are prompted for their current password before providing a new one. Root is not prompted for the current password of the target user.

---

## 3. Options

### 3.1 Primary Flags

| Short Flag | Long Flag | Description | POSIX Defined |
|:---|:---|:---|:---:|
| `-d` | `--delete` | Delete a user's password (makes it empty). **Highly dangerous.** | No |
| `-e` | `--expire` | Immediately expire an account's password, forcing a change on next login. | No |
| `-l` | `--lock` | Lock the password of the named account (prefixes `!` to the hash). | No |
| `-u` | `--unlock` | Unlock the password of the named account (removes the `!`). | No |
| `-S` | `--status` | Report password status on the named account. | No |
| `-n` | `--mindays MIN_DAYS` | Set the minimum number of days before a password can be changed. | No |
| `-x` | `--maxdays MAX_DAYS` | Set the maximum number of days a password remains valid. | No |
| `-w` | `--warndays WARN_DAYS`| Set the number of days of warning before a password expires. | No |
| `-i` | `--inactive INACTIVE`| Set the number of days after a password expires until the account is disabled. | No |

---

## 4. Basic Usage

### 4.1 Quick-Reference Cheatsheet Card

| Operation | Command | Notes |
|:---|:---|:---|
| Change your own password | `passwd` | Prompts for current, then new password. |
| Change another's password| `sudo passwd alice` | Root does not need Alice's current password. |
| Force password change | `sudo passwd -e bob` | Bob must pick a new password on next login. |
| Lock an account | `sudo passwd -l charlie` | Disables password-based login for Charlie. |
| View account status | `sudo passwd -S alice` | Shows if account is locked or active. |

### 4.2 Changing Your Own Password

```console
$ passwd
Changing password for alice.
Current password: 
New password: 
Retype new password: 
passwd: password updated successfully
```
*(Note: PAM modules will reject passwords that are too short, based on dictionary words, or previously used, depending on the system's `/etc/security/pwquality.conf` settings).*

### 4.3 Viewing Password Status (`-S`)

You can query the current aging and lock status of an account (requires root):

```console
$ sudo passwd -S alice
alice P 09/14/2026 0 99999 7 -1
```
The output format is: `Username | Status (P=Usable, L=Locked, NP=No Password) | Date of last change | Min Age | Max Age | Warning Period | Inactivity Period`.

---

## 5. Practical Operations

### 5.1 Forcing a Password Change on Next Login

When creating a new user account, it is standard practice to set a temporary password and immediately expire it. This forces the user to choose their own secure password immediately upon logging in via SSH or the console:

```console
$ sudo useradd -m bob
$ echo "TemporaryPass123" | sudo passwd --stdin bob
$ sudo passwd -e bob
```

### 5.2 Locking a Compromised Account

If an account is compromised, you can lock it immediately. This behaves identically to `usermod -L`:

```console
$ sudo passwd -l charlie
passwd: password expiry information changed.
```
*(Reminder: This only locks password authentication. If Charlie has SSH keys installed, they must be removed manually).*

### 5.3 Enforcing Password Rotation Policies

To enforce a policy where a user must change their password every 90 days, with a 14-day warning period:

```console
$ sudo passwd -x 90 -w 14 david
```

---

## 6. Advanced Usage

### 6.1 Scripting and Automation

> [!WARNING]
> The `passwd` command is designed strictly for interactive use. Older versions (and some Red Hat systems) support `--stdin`, but this is highly insecure and deprecated.

Do **not** use `passwd` in scripts. If you need to set passwords non-interactively (e.g., in Ansible or bash scripts), use `chpasswd`:

```bash
# Securely batch-update passwords
echo "alice:NewSecurePass!@#" | sudo chpasswd
```

---

## 7. Exit Status, Environment, and Configuration

### 7.1 Exit Status Codes

| Exit Code | Meaning |
|:---:|:---|
| `0` | Success. |
| `1` | Permission denied. |
| `2` | Invalid command syntax. |
| `3` | Unexpected failure (cannot lock file, PAM error). |
| `4` | Unexpected failure, passwd file is missing. |
| `5` | Password file is busy (try again later). |
| `6` | Invalid argument to option. |

### 7.2 Configuration Files

| Path | Purpose |
|:---|:---|
| `/etc/passwd` | Contains user account metadata (does not contain the password hash). |
| `/etc/shadow` | Contains the actual encrypted password hashes and aging information. |
| `/etc/pam.d/passwd` | PAM configuration file dictating complexity requirements and hashing algorithms (e.g., `pam_pwquality.so`). |
| `/etc/login.defs` | Global default settings for password aging (e.g., `PASS_MAX_DAYS`). |

---

## 8. Safety, Security, and Portability

### 8.1 The Danger of `-d` (Delete Password)

The `-d` (`--delete`) flag removes the password for an account. This does not mean the account cannot be logged into; it means the account **has no password and can be logged into by anyone who knows the username** (depending on PAM configurations, which usually forbid empty passwords via `nullok`, but it is a massive security risk).

```bash
# DANGEROUS: Do not do this.
sudo passwd -d charlie
```
If you want to disable an account, use `passwd -l` (lock).

### 8.2 Setuid Root Binary Risk

Because `passwd` must write to `/etc/shadow` (which is owned by root and has `000` or `040` permissions), the binary has the setuid bit set. Any vulnerability in the `passwd` executable could yield local privilege escalation to root. Always ensure the `shadow-utils` package is up to date with security patches.

---

## 9. Best Practices

1. **Expire Temporary Passwords Immediately**:
   - *Guidance*: Always run `sudo passwd -e <user>` immediately after assigning an initial password.
   - *Authoritative Justification*: Ensures the administrator does not know the user's permanent password, maintaining cryptographic accountability.
2. **Use `chpasswd` for Automation**:
   - *Guidance*: Never attempt to pipe input into `passwd` using `echo` or `expect`. Use `chpasswd` for all automated provisioning.
   - *Authoritative Justification*: `chpasswd` is specifically designed for secure batch processing and avoids interactive TTY limitations.
3. **Lock Accounts, Don't Delete Passwords**:
   - *Guidance*: Use `-l` to restrict access. Never use `-d`.

---

## References

1. **shadow-utils passwd Manual Page**: `man 1 passwd`
2. **Linux PAM System Administrator's Guide**: [https://www.linux-pam.org/Linux-PAM-html/Linux-PAM_SAG.html](https://www.linux-pam.org/Linux-PAM-html/Linux-PAM_SAG.html)
