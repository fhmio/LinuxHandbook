---
title: "Linux Command Tutorial: ssh-keyscan"
date: 2026-09-12T00:00:00+00:00
categories: ['Technology']
tags:
  - 'Linux'
  - 'OpenSSH'
  - 'ssh-keyscan'
  - 'Linux Command Tutorial'
draft: false
slug: "linux-ssh-keyscan-tutorial"
description: "Authoritative reference tutorial for ssh-keyscan (OpenSSH), detailing host key gathering, known_hosts bootstrapping, security considerations, and automation."
upstream_suite: "openssh"
upstream_version: "OpenSSH 10.5"
posix_standard: "None"
research_date: "2026-09-12"
---

The **Linux Command Tutorial** series provides rigorous, upstream-verified references for essential system commands across Linux distributions and UNIX-like environments. Each article focuses on a single executable, combining exhaustive option documentation, verified real-world examples, security boundaries, and best practices directly derived from official source documentation and POSIX standards.

---

## 1. Introduction

> **Upstream**: `OpenSSH 10.5` | **POSIX**: `None (OpenSSH standard)` | **Safety Tier**: `safe-read-only` | **Scope**: `Non-interactive host key gathering & known_hosts provisioning`

`ssh-keyscan` is a diagnostic and provisioning utility in the **OpenSSH** suite that gathers the public SSH host keys of a number of hosts. It is designed to aid in building and auditing `known_hosts` files and bootstrapping fleet configuration across modern infrastructure.

- **Upstream Project & Provenance**: Maintained within OpenSSH (`openssh-clients`).
- **Portability & Standards Baseline**: Proprietary OpenSSH utility; not defined in POSIX.1-2024.
- **Target Research Implementation**: Audited against **OpenSSH 10.5** (`ssh-keyscan(1)`).
- **Applicability & Lifecycle**: The standard utility for pre-populating `/etc/ssh/ssh_known_hosts` or `~/.ssh/known_hosts` in automation scripts, CI/CD runners, and configuration management tools (Ansible, Terraform).

---

## 2. Syntax and Command Model

### 2.1 Canonical Synopsis

```bash
ssh-keyscan [-46cDHqv] [-f file] [-p port] [-T timeout]
            [-t type] [host | addrlist namelist] ...
```

### 2.2 Execution Model

- `ssh-keyscan` connects concurrently to the specified target hosts on the designated TCP port.
- It performs an initial SSH protocol handshake to extract the server's public host key without completing authentication.
- **Standard Output**: Outputs host keys formatted in standard `known_hosts` line format directly to `stdout`. Diagnostic information is sent to `stderr`.

---

## 3. Options

### 3.1 Gathering and Filtering Flags

| Flag | Description | Default | Upstream Note |
|:---|:---|:---|:---|
| `-t type` | Comma-separated list of key types to fetch (`ed25519`, `ecdsa`, `rsa`). | All supported types | Recommended to restrict to `ed25519` |
| `-p port` | Remote TCP port to connect to on the target host. | `22` | Standard |
| `-4` / `-6` | Force IPv4 or IPv6 lookup. | Dual-stack | Standard |
| `-H` | Hash all hostnames and addresses in the output. | Plaintext | Privacy protection |
| `-f file` | Read hosts to scan from `file` (one per line, `-` for stdin). | CLI arguments | Batch operations |
| `-T timeout` | Connection attempt timeout in seconds. | `5` | Tuning for WAN |
| `-q` | Quiet mode: suppress diagnostic messages and comments. | Normal | Scripting friendly |
| `-v` | Verbose mode: prints detailed connection progress to stderr. | Normal | Debugging |

---

## 4. Basic Usage

### 4.1 Quick Reference & Common Invocations

| Task / Scenario | Command | Key Flags / Behavior |
|:---|:---|:---|
| Gather Ed25519 host key | `ssh-keyscan -t ed25519 192.168.1.100` | Gathers Ed25519 public host key |
| Append key to known_hosts | `ssh-keyscan -t ed25519 host.example.com >> ~/.ssh/known_hosts` | Bootstraps personal trusted hosts file |
| Scan with hashed hostname | `ssh-keyscan -H -t ed25519 host.example.com` | `-H` hashes host/IP for reconnaissance defense |
| Scan non-standard SSH port | `ssh-keyscan -p 2222 -t ed25519 host.example.com` | `-p` sets remote target port |
| Scan hosts from file list | `ssh-keyscan -f host_list.txt` | `-f` reads targets line-by-line |
| Fast scan with short timeout | `ssh-keyscan -T 2 -t ed25519 -f hosts.txt` | `-T` reduces timeout to 2 seconds |
| Quiet scripted scan | `ssh-keyscan -q -t ed25519 host.example.com` | `-q` suppresses comments and diagnostic stderr |

### 4.2 Gathering Ed25519 Host Key for a Single Host

```bash
ssh-keyscan -t ed25519 192.168.1.100
```

*Sample terminal output:*

```text
# 192.168.1.100:22 SSH-2.0-OpenSSH_10.5
192.168.1.100 ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIOrX...admin@web-node-01
```

### 4.3 Appending Directly to User known_hosts

```bash
ssh-keyscan -t ed25519 gitlab.corp.example.com >> ~/.ssh/known_hosts
```

---

## 5. Practical Operations

### 5.1 Bootstrapping a Cluster Known Hosts File

Scanning a list of 50 cluster nodes from a file and generating a hashed known hosts file:

```bash
ssh-keyscan -t ed25519 -H -f cluster_nodes.txt > /etc/ssh/ssh_known_hosts
```

- **Technical Analysis**: `-H` hashes each hostname and IP address using SHA1 HMAC with a random salt per line, preventing unauthorized users on the system from enumerating cluster hosts by inspecting `/etc/ssh/ssh_known_hosts`.

### 5.2 Scanning Non-Standard SSH Ports

Gathering keys from servers running SSH on port `2222`:

```bash
ssh-keyscan -p 2222 -t ed25519 bastion.corp.example.com
```

*Sample terminal output:*

```text
# bastion.corp.example.com:2222 SSH-2.0-OpenSSH_10.5
[bastion.corp.example.com]:2222 ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIPq...
```

- Notice that non-standard ports automatically enclose the host in square brackets (`[host]:port`), conforming to OpenSSH `known_hosts` syntax.

### 5.3 CI/CD Runner Known Hosts Initialization

Injecting a target server's host key during automated GitLab CI or GitHub Actions runner setup:

```bash
mkdir -p ~/.ssh && chmod 700 ~/.ssh
ssh-keyscan -H -t ed25519 deploy.internal.lan >> ~/.ssh/known_hosts
chmod 644 ~/.ssh/known_hosts
```

---

## 6. Advanced Usage

### 6.1 Fast Multi-Threaded Scanning with Custom Timeouts

When scanning large subnets, default timeouts may cause long delays on unreachable nodes. Reducing timeout to 2 seconds:

```bash
ssh-keyscan -T 2 -t ed25519 -f subnet_ips.txt 2> scan_errors.log > valid_hosts.txt
```

- Separates valid `known_hosts` records on `stdout` from connection failures logged on `stderr`.

---

## 7. Exit Status, Environment, and Configuration

### 7.1 Exit Status Codes

| Exit Code | Condition | Upstream Note |
|:---:|:---|:---|
| `0` | Clean execution. | Returns `0` even if some or all target hosts failed to respond. |
| `1` | Command-line argument error or invalid file input. | Bad arguments or unreadable files. |

> [!WARNING]
> **Silent Exit Code Trap**: `ssh-keyscan` returns exit status `0` even if network connections fail and zero keys are retrieved. Automation scripts must test that captured output is non-empty before appending to configuration:
>
> ```bash
> keys=$(ssh-keyscan -t ed25519 host.example.com)
> [ -n "$keys" ] || { echo "Error: Failed to obtain host key"; exit 1; }
> ```

---

## 8. Safety, Security, and Portability

### 8.1 Man-in-the-Middle (MITM) Vulnerability Warning

> [!WARNING]
> **MITM Injection Vulnerability**: `ssh-keyscan` does **not** verify the cryptographic authenticity of the host keys it gathers. If a network adversary conducts a Man-in-the-Middle (MITM) attack or DNS spoofing while `ssh-keyscan` executes, the utility will capture the adversary's key and inject it into your trusted `known_hosts`.
>
> In high-security environments, always verify the fingerprint of keys gathered via `ssh-keyscan` through an out-of-band channel (such as server console or cloud metadata API) before trusting them in production.

---

## 9. Best Practices

1. **Explicitly Restrict Key Types with `-t ed25519`**:
   > [!TIP]
   > *Guidance*: Always specify `-t ed25519` or `-t ed25519,ecdsa`.
   > *Authoritative Justification*: Prevents collecting deprecated RSA or DSA host keys.

2. **Always Hash Output in Shared Environments with `-H`**:
   > [!TIP]
   > *Guidance*: Use `-H` when writing to system-wide `/etc/ssh/ssh_known_hosts`.
   > *Authoritative Justification*: OpenSSH manual states that hashed hostnames prevent exposure of network topology to local unprivileged users.

3. **Never Blindly Trust Scanned Keys on Public Networks**:
   > [!WARNING]
   > *Guidance*: Verify fingerprints out-of-band (`ssh-keygen -lf -`) after scanning.
   > *Authoritative Justification*: OpenSSH upstream explicitly notes that keyscan does not validate certificates or authenticate remote servers.

4. **Enforce Connection Timeouts (`-T`) in Automated Scripts**:
   > [!TIP]
   > *Guidance*: Set `-T 3` or `-T 5` in automated orchestration scripts.
   > *Authoritative Justification*: Prevents hung pipelines when target hosts are offline or firewalled.

---

## References

1. **OpenSSH ssh-keyscan(1) Manual**: OpenBSD Manual Pages. [https://man.openbsd.org/ssh-keyscan](https://man.openbsd.org/ssh-keyscan)
2. **OpenSSH sshd(8) Manual**: Host key configuration specifications. [https://man.openbsd.org/sshd](https://man.openbsd.org/sshd)
3. **OpenSSH 10.5 Release Notes**: Official Project Portal. [https://www.openssh.com/releasenotes.html](https://www.openssh.com/releasenotes.html)
