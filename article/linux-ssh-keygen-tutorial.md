---
title: "Linux Command Tutorial: ssh-keygen"
date: 2026-09-12T00:00:00+00:00
categories: ['Technology']
tags:
  - 'Linux'
  - 'OpenSSH'
  - 'ssh-keygen'
  - 'Linux Command Tutorial'
draft: false
slug: "linux-ssh-keygen-tutorial"
description: "Authoritative reference tutorial for ssh-keygen (OpenSSH), detailing key generation, certificate authorities, known_hosts management, and modern cryptosystem selection."
upstream_suite: "openssh"
upstream_version: "OpenSSH 10.5"
posix_standard: "None"
research_date: "2026-09-12"
---

The **Linux Command Tutorial** series provides rigorous, upstream-verified references for essential system commands across Linux distributions and UNIX-like environments. Each article focuses on a single executable, combining exhaustive option documentation, verified real-world examples, security boundaries, and best practices directly derived from official source documentation and POSIX standards.

---

## 1. Introduction

`ssh-keygen` is the key generation, management, and conversion utility in the **OpenSSH** suite. It generates authentication key pairs for SSH protocol versions, manages OpenSSH certificate authorities (CA), audits host key fingerprints, and modifies existing keys.

- **Upstream Project & Provenance**: Maintained as a core utility within OpenSSH (`openssh-clients`).
- **Portability & Standards Baseline**: Proprietary to OpenSSH key infrastructure; not defined in POSIX.1-2024.
- **Target Research Implementation**: Audited against **OpenSSH 10.5** (`ssh-keygen(1)`).
- **Applicability & Lifecycle**: The mandatory tool for creating user identity keys (`id_ed25519`), server host keys (`ssh_host_*_key`), and signing cryptographic user/host certificates.

---

## 2. Syntax and Command Model

### 2.1 Canonical Synopsis

```bash
# Key Generation Mode:
ssh-keygen [-q] [-a rounds] [-b bits] [-C comment] [-f output_keyfile]
           [-m format] [-N new_passphrase] [-O option] [-t dsa | ecdsa |
           ecdsa-sk | ed25519 | ed25519-sk | rsa]

# Key Management & Inspection Modes:
ssh-keygen -l [-v] [-E fingerprint_hash] [-f keyfile]
ssh-keygen -p [-f keyfile] [-P old_passphrase] [-N new_passphrase]
ssh-keygen -y [-f keyfile]
ssh-keygen -R hostname [-f known_hosts_file]
ssh-keygen -F hostname [-f known_hosts_file]
ssh-keygen -s ca_key -I cert_id [-n principals] [-V validity_interval] file ...
```

### 2.2 Execution Model

`ssh-keygen` operates in different discrete modes determined by primary action flags:
- **Generation Mode**: Default when no mode switch is specified.
- **Fingerprint Query (`-l`)**: Inspects a key or certificate and prints its cryptographic hash.
- **Passphrase Modification (`-p`)**: Re-encrypts an existing private key in place.
- **Public Key Extraction (`-y`)**: Derives a public key file from a private key.
- **Known Hosts Management (`-F`, `-R`, `-H`)**: Queries, removes, or hashes known host records.
- **Certificate Authority Signing (`-s`)**: Signs user or host public keys.

---

## 3. Options

### 3.1 Key Generation Parameters

| Flag | Description | Default | Upstream Recommendation |
|:---|:---|:---|:---|
| `-t type` | Specifies algorithm: `ed25519`, `rsa`, `ecdsa`, `ed25519-sk`. | `ed25519` | Modern default; Ed25519 recommended |
| `-b bits` | Key bit length (valid for RSA: 2048–4096; ECDSA: 256/384/521). | Type-specific | RSA min 3072, Ed25519 fixed 256 |
| `-C comment` | Text comment appended to the public key. | `user@host` | Useful for key inventory |
| `-f filename` | Output path for generated private key. | `~/.ssh/id_<type>` | Always specify in automation |
| `-N passphrase` | New passphrase encryption string (`""` for unencrypted). | Prompts TTY | Unencrypted only for automation |
| `-a rounds` | Number of KDF (Key Derivation Function) rounds using bcrypt. | `16` | Higher rounds increase brute-force cost |

### 3.2 Key Inspection and Maintenance Options

| Flag | Description | Default |
|:---|:---|:---|
| `-l` | Show fingerprint of specified public/private key. | SHA256 base64 |
| `-E hash` | Specify fingerprint hash algorithm (`sha256` or `md5`). | `sha256` |
| `-v` | Visual host key visualizer (ASCII art fingerprint). | Disabled |
| `-R host` | Remove all keys belonging to `host` from `known_hosts`. | Modifies `~/.ssh/known_hosts` |
| `-H` | Hash `known_hosts` file to obfuscate IP/host names. | In-place update |

---

## 4. Basic Usage

### 4.1 Generating an Ed25519 User Key Pair

```bash
ssh-keygen -t ed25519 -C "admin@corp.example.com" -f ~/.ssh/id_ed25519
```
```console
Generating public/private ed25519 key pair.
Enter passphrase (empty for no passphrase): 
Enter same passphrase again: 
Your identification has been saved in /home/admin/.ssh/id_ed25519
Your public key has been saved in /home/admin/.ssh/id_ed25519.pub
The key fingerprint is:
SHA256:7fK2m9W81XzpBqLa39XjN1sK21vL3p0kZqA7w9eF1m8 admin@corp.example.com
The key's randomart image is:
+--[ED25519 256]--+
|      ..o.       |
|     . +o.       |
|    . =.+ .      |
|     = O.= .     |
|    . * S.= .    |
|   . = = B .     |
|    o * * .      |
|     + B .       |
|      E.o        |
+----[SHA256]-----+
```

### 4.2 Inspecting Key Fingerprints

```bash
ssh-keygen -l -f ~/.ssh/id_ed25519.pub
```
```text
256 SHA256:7fK2m9W81XzpBqLa39XjN1sK21vL3p0kZqA7w9eF1m8 admin@corp.example.com (ED25519)
```

---

## 5. Practical Operations

### 5.1 Hardening Private Key Storage with Bcrypt Rounds

Increasing KDF work factor to 100 rounds to protect local credentials against offline dictionary cracking:

```bash
ssh-keygen -t ed25519 -a 100 -f ~/.ssh/id_production_ed25519
```
- **Technical Analysis**: `-a 100` instructs `ssh-keygen` to perform 100 rounds of bcrypt KDF during key encryption, exponentially slowing brute-force attempts on the stolen keyfile.

### 5.2 Purging Changed Server Keys from `known_hosts`

When a remote server is re-imaged and its host key changes, `ssh` refuses connection with a "Host key verification failed" alert. Purging the old entry:

```bash
ssh-keygen -R 192.168.1.100
```
```text
# Host 192.168.1.100 found: line 14
/home/admin/.ssh/known_hosts updated.
Original contents retained as /home/admin/.ssh/known_hosts.old
```

### 5.3 Deriving a Lost Public Key from Private Key

If the `.pub` file is accidentally deleted:

```bash
ssh-keygen -y -f ~/.ssh/id_ed25519 > ~/.ssh/id_ed25519.pub
```
- Re-derives the public key text directly from the encrypted private key after passphrase entry.

### 5.4 Changing the Passphrase of an Existing Key

```bash
ssh-keygen -p -f ~/.ssh/id_ed25519
```
```console
Enter old passphrase:
Key has comment 'admin@corp.example.com'
Enter new passphrase (empty for no passphrase):
Enter same passphrase again:
Your identification has been saved with the new passphrase.
```

---

## 6. Advanced Usage

### 6.1 Creating an OpenSSH Certificate Authority (CA)

OpenSSH certificates eliminate `known_hosts` prompts and `authorized_keys` file sprawl by enabling cryptographic signature verification of keys.

1. **Generate the CA Key Pair**:
   ```bash
   ssh-keygen -t ed25519 -f /etc/ssh/ca_user_key -C "Corporate User CA"
   ```

2. **Sign a User Key for a 30-Day Validity Window**:
   ```bash
   ssh-keygen -s /etc/ssh/ca_user_key -I "developer_alice" -n alice,deployer -V +30d ~/.ssh/id_ed25519.pub
   ```
   ```text
   Signed user key /home/alice/.ssh/id_ed25519-cert.pub: id "developer_alice" serial 0 for alice,deployer valid from 2026-09-12T10:00:00 to 2026-10-12T10:00:00
   ```

3. **Verify the Certificate**:
   ```bash
   ssh-keygen -L -f ~/.ssh/id_ed25519-cert.pub
   ```
   ```text
   Type: ssh-ed25519-cert-v01@openssh.com user certificate
   Public key: ED25519-CERT SHA256:...
   Signing CA: ED25519 SHA256:...
   Key ID: "developer_alice"
   Serial: 0
   Valid: from 2026-09-12T10:00:00 to 2026-10-12T10:00:00
   Principals:
           alice
           deployer
   ```

---

## 7. Exit Status, Environment, and Configuration

### 7.1 Exit Status Codes

| Exit Code | Condition |
|:---:|:---|
| `0` | Successful key generation, query, modification, or removal. |
| `1` | Command failure, invalid arguments, incorrect passphrase, or corrupt keyfile. |

### 7.2 Generated Files and Modes

`ssh-keygen` automatically sets strict file permissions upon creation:
- **Private Key (`id_ed25519`)**: Mode `0600` (`-rw-------`).
- **Public Key (`id_ed25519.pub`)**: Mode `0644` (`-rw-r--r--`).

---

## 8. Safety, Security, and Portability

### 8.1 Modern Cryptosystem Evaluation

- **Ed25519**: 256-bit Edwards-curve Digital Signature Algorithm. Upstream default and strongly recommended. Constant-time operations prevent side-channel timing attacks.
- **RSA**: Supported for legacy compatibility. Minimum acceptable key length is 3072 bits (`-b 3072`). RSA keys with SHA-1 signatures are rejected by default in modern OpenSSH.
- **FIDO2 Hardware Keys (`-sk`)**: OpenSSH supports hardware security tokens (`-t ed25519-sk`) where the private key requires physical touch on a USB/NFC authenticator.

---

## 9. Best Practices

1. **Standardize on Ed25519 Across Infrastructure**:
   - *Guidance*: Default all key creation to `ssh-keygen -t ed25519`.
   - *Authoritative Justification*: OpenSSH upstream documentation confirms Ed25519 provides compact 68-character public keys and enhanced side-channel attack resistance.
2. **Always Encrypt Private Keys with a Strong Passphrase**:
   - *Guidance*: Never generate passphrase-less keys (`-N ""`) for human interactive accounts; delegate caching to `ssh-agent`.
   - *Authoritative Justification*: Unencrypted private keys stored on disk can be exfiltrated without defense if an unprivileged vulnerability is exploited.
3. **Increase KDF Iterations for High-Value Keys**:
   - *Guidance*: Pass `-a 64` or `-a 100` when creating administrative master keys.
   - *Authoritative Justification*: The default bcrypt KDF slows down parallel GPU cracking of captured private keys.
4. **Obfuscate Known Host Records**:
   - *Guidance*: Run `ssh-keygen -H` to hash `~/.ssh/known_hosts`.
   - *Authoritative Justification*: Prevents attackers from harvesting internal hostnames and IP addresses if workstation files are read.
5. **Implement Time-Bound SSH Certificates**:
   - *Guidance*: Use `-V +1d` to `-V +30d` when signing certificates with a CA.
   - *Authoritative Justification*: Enforces key rotation and expiration without requiring manual edits to remote `authorized_keys`.

---

## References

1. **OpenSSH ssh-keygen(1) Manual**: OpenBSD Manual Pages. [https://man.openbsd.org/ssh-keygen](https://man.openbsd.org/ssh-keygen)
2. **OpenSSH Certificate Specifications**: PROTOCOL.certkeys documentation. [https://github.com/openssh/openssh-portable/blob/master/PROTOCOL.certkeys](https://github.com/openssh/openssh-portable/blob/master/PROTOCOL.certkeys)
3. **OpenSSH 10.5 Release Notes**: Official Release Portal. [https://www.openssh.com/releasenotes.html](https://www.openssh.com/releasenotes.html)
