---
title: "Linux Command Tutorial: scp"
date: 2026-09-12T00:00:00+00:00
categories: ['Technology']
tags:
  - 'Linux'
  - 'OpenSSH'
  - 'scp'
  - 'Linux Command Tutorial'
draft: false
slug: "linux-scp-tutorial"
description: "Authoritative reference tutorial for scp (OpenSSH), covering SFTP-protocol transport mode, legacy rcp mode, option syntax, and security boundaries."
upstream_suite: "openssh"
upstream_version: "OpenSSH 10.5"
posix_standard: "None"
research_date: "2026-09-12"
---

The **Linux Command Tutorial** series provides rigorous, upstream-verified references for essential system commands across Linux distributions and UNIX-like environments. Each article focuses on a single executable, combining exhaustive option documentation, verified real-world examples, security boundaries, and best practices directly derived from official source documentation and POSIX standards.

---

## 1. Introduction

`scp` (Secure Copy protocol) is a file copying utility that transfers files across an encrypted network link using the **OpenSSH** client infrastructure. Historically, `scp` implemented the legacy BSD `rcp` protocol over an SSH channel; in modern releases, `scp` uses the **SFTP protocol by default** for improved security and predictability.

- **Upstream Project & Provenance**: Maintained within OpenSSH (`openssh-clients`).
- **Portability & Standards Baseline**: `scp` is an industry standard OpenSSH tool, not defined by POSIX.1-2024.
- **Target Research Implementation**: Audited against **OpenSSH 10.5** (`scp(1)`).
- **Applicability & Lifecycle**: Intended for quick, one-off file transfers between local and remote filesystems. For complex synchronization or delta-transfers, `rsync` or `sftp` is recommended.

---

## 2. Syntax and Command Model

### 2.1 Canonical Synopsis

```bash
scp [-346ABCOpqRrsTv] [-c cipher] [-D sftp_server_path] [-F ssh_config]
    [-i identity_file] [-J destination] [-l limit] [-o ssh_option]
    [-P port] [-S program] [-X sftp_option] source ... target
```

### 2.2 Source and Target Operands

Files may be specified as a local path or a remote destination:
```bash
[[user@]host:]path
```
or via URI:
```bash
scp://[user@]host[:port][/path]
```

### 2.3 Execution Model (SFTP vs Legacy Mode)

- **Default SFTP Protocol**: OpenSSH 9.0 and later default to using the SFTP subsystem protocol on the remote end. This prevents server-side globbing vulnerabilities present in legacy `rcp`.
- **Legacy Mode (`-O`)**: Forces the legacy `scp/rcp` protocol. Retained strictly for backwards compatibility with legacy servers that do not run `sftp-server`.
- **Third-Party Transfers (`-3`)**: When copying between two remote hosts (`scp host1:file host2:file`), `-3` directs all traffic through the local host instead of attempting direct server-to-server connection.

---

## 3. Options

### 3.1 Transfer and Protocol Controls

| Flag | Description | Default | Upstream Note |
|:---|:---|:---|:---|
| `-r` | Recursively copy entire directories. | Disabled | Follows symlinks encountered on command line |
| `-p` | Preserves modification times, access times, and file modes. | Disabled | Recommended for backups |
| `-O` | Use legacy SCP protocol instead of default SFTP. | SFTP default | OpenSSH 9.0+ deprecation |
| `-s` | Passes SFTP subsystem program path to `ssh`. | Standard | OpenSSH baseline |
| `-3` | Copies between two remote hosts through local client. | Direct | Required when hosts cannot route to each other |
| `-C` | Enables transport compression. | Disabled | Useful over slow WAN |
| `-l limit` | Limits bandwidth specified in Kbit/s. | Unlimited | Rate limiting |

### 3.2 Network and Connection Options

| Flag | Description | Default |
|:---|:---|:---|
| `-P port` | Specifies the remote host TCP port (note capital `-P`). | `22` |
| `-i identity_file` | Path to public key identity file. | `~/.ssh/id_*` |
| `-J destination` | Connect via proxy jump host. | Direct |
| `-F ssh_config` | Alternative SSH configuration file. | `~/.ssh/config` |
| `-q` | Quiet mode: disables progress meters and diagnostics. | Verbose meters |
| `-v` | Verbose debug logging. | Normal |

---

## 4. Basic Usage

### 4.1 Copying a Local File to a Remote Host

```bash
scp ./deploy.tar.gz admin@192.168.1.100:/var/www/
```
```text
deploy.tar.gz                         100%   24MB  12.5MB/s   00:01
```

### 4.2 Downloading a Remote File to Local Working Directory

```bash
scp admin@192.168.1.100:/var/log/syslog.1.gz ./
```
```text
syslog.1.gz                           100%  512KB   8.2MB/s   00:00
```

---

## 5. Practical Operations

### 5.1 Recursive Directory Transfer Preserving Attributes

Copying an application release directory while retaining timestamps and permissions:

```bash
scp -p -r ./build_v2 admin@192.168.1.100:/opt/apps/
```
- **Technical Analysis**: `-r` traverses the local tree; `-p` ensures mtime/atime and permission bits match the source on the remote destination.

### 5.2 Transferring Files Across a Bastion Host

Transferring configuration files to an internal server unreachable directly from your network:

```bash
scp -J bastion.corp.example.com:2222 ./nginx.conf admin@10.0.5.20:/etc/nginx/
```

### 5.3 Transferring Directly Between Two Remote Servers

Transferring a tarball from `serverA` to `serverB` via your workstation:

```bash
scp -3 -C user@serverA.internal:/backups/db.sql user@serverB.internal:/backups/
```
- **Technical Analysis**: `-3` streams data through the local machine's memory, avoiding the need for `serverA` to have network routing or SSH credentials to `serverB`.

### 5.4 Bandwidth-Limited File Push

Limiting transfer speed to 10,000 Kbit/s (approx 1.25 MB/s) to prevent impacting co-located services:

```bash
scp -l 10000 ./iso_image.iso admin@remote-office:/storage/
```

---

## 6. Advanced Usage

### 6.1 Port Specification Discrepancies

A critical syntax trap: `ssh` uses lowercase `-p`, whereas `scp` uses uppercase `-P` for port designation:

```bash
# Correct for scp:
scp -P 2222 app.tar.gz admin@target.host:/tmp/

# Alternatively, URI syntax allows natural port notation:
scp app.tar.gz scp://admin@target.host:2222//tmp/
```

### 6.2 Passing Advanced SSH Configuration Inline

Applying arbitrary SSH configuration options without editing `~/.ssh/config`:

```bash
scp -o "StrictHostKeyChecking=accept-new" -o "ConnectTimeout=10" package.deb admin@192.168.1.100:/tmp/
```

---

## 7. Exit Status, Environment, and Configuration

### 7.1 Exit Status Codes

| Exit Code | Condition |
|:---:|:---|
| `0` | All files copied successfully. |
| `1` | General file access error, destination write error, or remote command failure. |
| `255` | SSH connection or authentication failure. |

### 7.2 Configuration Inheritance

`scp` reads `~/.ssh/config` and `/etc/ssh/ssh_config`. Settings configured under `Host` blocks (such as `User`, `Port`, `IdentityFile`, `ProxyJump`) apply automatically without command-line repetition.

---

## 8. Safety, Security, and Portability

### 8.1 Legacy SCP Protocol Vulnerabilities (CVE-2019-6111)

- In the legacy `rcp` protocol (`-O`), the client sends a command to the remote server, and the remote server decides which filenames to stream back. Malicious or compromised servers could send arbitrary filenames outside the requested path (e.g., overwriting `~/.ssh/authorized_keys`).
- **OpenSSH Default**: Modern `scp` utilizes the SFTP protocol engine where file names and targets are explicitly controlled by the client, neutralizing this class of attack.
- Avoid passing `-O` unless explicitly necessary for interoperability with ancient embedded devices.

### 8.2 Overwrite Traps

`scp` will overwrite existing destination files without prompting unless write permissions are restricted on the target filesystem.

---

## 9. Best Practices

1. **Retain the Default SFTP Protocol Mode**:
   - *Guidance*: Never add `-O` to scripts unless connecting to legacy appliances that lack SFTP server subsystems.
   - *Authoritative Justification*: OpenSSH release documentation confirms that the default SFTP mode protects clients against malicious remote file name injection.
2. **Use `-p` When Archiving or Deploying Builds**:
   - *Guidance*: Pass `-p` for configuration and build artifact distribution.
   - *Authoritative Justification*: Preserves original file modification timestamps, preventing cache invalidation issues on the target host.
3. **Use `-3` for Remote-to-Remote Copies**:
   - *Guidance*: Always specify `-3` when copying between two remote hosts.
   - *Authoritative Justification*: Prevents insecure direct authentication requirements between two remote servers.
4. **Throttle Batch Transfers on Shared Uplinks**:
   - *Guidance*: Use `-l <kbit/s>` in automated crontab scripts.
   - *Authoritative Justification*: Prevents TCP link saturation on corporate VPNs or shared gateway interfaces.
5. **Prefer `rsync` for Large or Resumable Transfers**:
   - *Guidance*: For large directory synchronization, use `rsync -avP` instead of `scp -r`.
   - *Authoritative Justification*: `scp` lacks delta-transfer algorithms and cannot resume partial files without re-transmitting the entire payload.

---

## References

1. **OpenSSH scp(1) Manual**: OpenBSD Manual Pages. [https://man.openbsd.org/scp](https://man.openbsd.org/scp)
2. **OpenSSH 9.0 Release Notes (SFTP by default)**: OpenSSH Project. [https://www.openssh.com/txt/release-9.0](https://www.openssh.com/txt/release-9.0)
3. **OpenSSH 10.5 Release Notes**: Current Release Portal. [https://www.openssh.com/releasenotes.html](https://www.openssh.com/releasenotes.html)
