---
title: "Linux Command Tutorial: sudo"
date: 2026-09-14T00:00:00+00:00
categories: ['Technology']
tags:
  - 'Linux'
  - 'Sudo Project'
  - 'sudo'
  - 'Linux Command Tutorial'
draft: false
slug: "linux-sudo-tutorial"
description: "Authoritative reference tutorial for sudo (Superuser Do), detailing privilege escalation, security policies, sudoers syntax, and interactive session simulation."
upstream_suite: "sudo"
upstream_version: "sudo 1.9.15"
posix_standard: "None"
research_date: "2026-09-14"
---

The **Linux Command Tutorial** series provides rigorous, upstream-verified references for essential system commands across Linux distributions and UNIX-like environments. Each article focuses on a single executable, combining exhaustive option documentation, verified real-world examples, security boundaries, and best practices directly derived from official source documentation and POSIX standards.

---

## 1. Introduction

> **Upstream**: Sudo Project | **POSIX**: None | **Safety Tier**: privileged-system-destructive | **Scope**: user-management

`sudo` (Superuser Do) allows a permitted user to execute a command as the superuser or another user, as specified by the security policy. 

- **Upstream Project & Provenance**: Developed and maintained by Todd C. Miller and the Sudo Project.
- **Portability & Standards Baseline**: Not defined in POSIX. It is a widely adopted standard across BSD, Linux, and macOS systems.
- **Target Research Implementation**: Audited against **sudo 1.9.15**.
- **Applicability & Lifecycle**: The definitive standard for privilege escalation in modern UNIX-like operating systems. It replaces the practice of logging in as `root` or sharing the `root` password via `su`, ensuring individual accountability and fine-grained access control.

---

## 2. Syntax and Command Model

### 2.1 Canonical Synopsis

```bash
sudo [options] [-u user] command [args]
```

### 2.2 Execution Model & Adjacency Requirement

- Unlike `su`, which requires the target user's password, `sudo` authenticates the **invoking user** using their own password.
- Successful authentication grants a cached ticket (usually valid for 15 minutes), allowing subsequent `sudo` commands without re-entering the password.
- Execution rights are determined by a security policy plugin, defaulting to the `sudoers` file (`/etc/sudoers`).
- `sudo` actively sanitizes the environment before executing the target command to prevent privilege escalation vulnerabilities (e.g., stripping `LD_PRELOAD`).

---

## 3. Options

### 3.1 Primary Flags

| Short Flag | Long Flag | Description | POSIX Defined |
|:---|:---|:---|:---:|
| `-i` | `--login` | Run the login shell as the target user. Reads `.profile`, `.bash_profile`. | No |
| `-s` | `--shell` | Run the shell specified by the `SHELL` environment variable. | No |
| `-u` | `--user=USER` | Run the command as a user other than the default target user (root). | No |
| `-l` | `--list` | List the invoking user's allowed (and forbidden) commands on the current host. | No |
| `-n` | `--non-interactive` | Avoid prompting for a password. Fails if a password is required. | No |
| `-S` | `--stdin` | Read the password from the standard input instead of the terminal device. | No |
| `-E` | `--preserve-env` | Preserve the user's existing environment variables (requires permission in `sudoers`). | No |
| `-k` | `--reset-timestamp` | Invalidate the cached credentials, forcing the user to authenticate again. | No |

---

## 4. Basic Usage

### 4.1 Quick-Reference Cheatsheet Card

| Operation | Command | Notes |
|:---|:---|:---|
| Run as root | `sudo ls /root` | Executes a single command as root. |
| Run as specific user | `sudo -u postgres psql` | Executes a command as the postgres user. |
| Open a root shell | `sudo -s` | Opens a shell, retaining current environment variables. |
| Open a root login shell | `sudo -i` | Opens a login shell, loading root's full environment. |
| List permissions | `sudo -l` | Shows which commands the current user can run. |
| Clear auth cache | `sudo -k` | Forces a password prompt on the next `sudo`. |

### 4.2 Executing a Command as Root

```console
$ cat /etc/shadow
cat: /etc/shadow: Permission denied

$ sudo cat /etc/shadow
[sudo] password for alice:
root:!:19318:0:99999:7:::
```

### 4.3 Listing Granted Permissions

```console
$ sudo -l
Matching Defaults entries for alice on server1:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User alice may run the following commands on server1:
    (ALL : ALL) ALL
    (postgres) NOPASSWD: /usr/bin/psql
```

---

## 5. Practical Operations

### 5.1 Simulating a Root Login

To fully assume the root identity, including changing to `/root` and applying root's profile configurations:

```console
$ sudo -i
# pwd
/root
# echo $PATH
/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
```

### 5.2 Editing Restricted Files (`sudoedit`)

Instead of running `sudo vim /etc/fstab`, it is safer to use `sudoedit` (or `sudo -e`). This securely copies the file to a temporary location, opens it as the *invoking user*, and then overwrites the original file as root upon saving.

```console
$ sudoedit /etc/fstab
```
*(Prevents vulnerabilities where an editor spawned as root allows shell escapes.)*

### 5.3 Working Around Output Redirection Limitations

A common mistake is attempting to redirect standard output to a protected file:
```bash
# This FAILS because the shell performs the redirection as the normal user:
sudo echo "127.0.0.1 db" >> /etc/hosts
```
**Solution 1**: Use `tee` with `sudo`:
```bash
echo "127.0.0.1 db" | sudo tee -a /etc/hosts > /dev/null
```
**Solution 2**: Spawn a root shell for the entire pipeline:
```bash
sudo sh -c 'echo "127.0.0.1 db" >> /etc/hosts'
```

---

## 6. Advanced Usage

### 6.1 Unattended Automation in Scripts

When writing scripts intended for cron or CI/CD pipelines, prompts for passwords will break execution. Ensure the script operates under a user with a `NOPASSWD` entry in `/etc/sudoers`, and pass the `-n` flag to guarantee `sudo` fails instantly rather than hanging on a prompt:

```bash
sudo -n /usr/bin/systemctl restart nginx
```

### 6.2 Passing Passwords via Stdin (`-S`)

> [!WARNING]
> Piping passwords in plaintext is extremely insecure and should be avoided. Use `NOPASSWD` configurations in `sudoers` instead.

If absolutely necessary for legacy integration:
```bash
echo "MySecretPass" | sudo -S systemctl restart sshd
```

---

## 7. Exit Status, Environment, and Configuration

### 7.1 Exit Status Codes

| Exit Code | Meaning |
|:---:|:---|
| `0` | Success (or the exit status of the executed command). |
| `1` | Configuration/permission error, or authentication failed. |
| `130` | The command was interrupted (SIGINT). |
| `137` | The command was killed (SIGKILL). |

### 7.2 Configuration Files

| Path | Purpose |
|:---|:---|
| `/etc/sudoers` | The master security policy file. **Must only be edited with `visudo`.** |
| `/etc/sudoers.d/` | Directory for drop-in policy files, commonly used for package configurations. |
| `/var/run/sudo/ts/` | Directory where timestamp (credential caching) files are stored per user. |

---

## 8. Safety, Security, and Portability

### 8.1 Safe Editing via `visudo`

> [!CAUTION]
> Never edit `/etc/sudoers` directly with `vim` or `nano`. Always use the `visudo` command. `visudo` locks the file against concurrent edits and performs strict syntax validation upon saving. If you introduce a syntax error with a normal editor, `sudo` will completely break, locking you out of administrative access.

### 8.2 Environment Sanitization

By design, `sudo` strips out potentially dangerous environment variables (`LD_PRELOAD`, `LD_LIBRARY_PATH`) before executing the target command. This prevents an attacker from hooking libraries into root-executed binaries. Do not broadly use the `-E` (preserve environment) flag without careful consideration.

---

## 9. Best Practices

1. **Use Drop-in Files for Custom Policies**:
   - *Guidance*: Place custom access rules in `/etc/sudoers.d/custom-rules` rather than modifying the main `/etc/sudoers` file.
   - *Authoritative Justification*: Prevents package upgrades from creating merge conflicts with the primary `sudoers` file.
2. **Never Grant NOPASSWD to ALL**:
   - *Guidance*: Limit `NOPASSWD` directives to specific, non-exploitable scripts (e.g., `NOPASSWD: /bin/systemctl restart nginx`).
   - *Authoritative Justification*: `NOPASSWD: ALL` entirely defeats the purpose of the password challenge and provides a trivial escalation path for malware.
3. **Use `sudo -i` Over `su`**:
   - *Guidance*: Always configure `sudo` access for administrators rather than sharing the root password via `su`.

---

## References

1. **Sudo Project Documentation**: [https://www.sudo.ws/docs/](https://www.sudo.ws/docs/)
2. **Sudo Manual Page**: `man 8 sudo`
3. **Sudoers Policy Manual**: `man 5 sudoers`
