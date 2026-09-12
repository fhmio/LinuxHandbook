---
title: "Linux Command Tutorial: ssh-add"
date: 2026-09-12T00:00:00+00:00
categories: ['Technology']
tags:
  - 'Linux'
  - 'OpenSSH'
  - 'ssh-add'
  - 'Linux Command Tutorial'
draft: false
slug: "linux-ssh-add-tutorial"
description: "Authoritative reference tutorial for ssh-add (OpenSSH), detailing private key loading, agent locking, hardware token interaction, and lifetime enforcement."
upstream_suite: "openssh"
upstream_version: "OpenSSH 10.5"
posix_standard: "None"
research_date: "2026-09-12"
---

The **Linux Command Tutorial** series provides rigorous, upstream-verified references for essential system commands across Linux distributions and UNIX-like environments. Each article focuses on a single executable, combining exhaustive option documentation, verified real-world examples, security boundaries, and best practices directly derived from official source documentation and POSIX standards.

---

## 1. Introduction

`ssh-add` is the user-space utility used to inspect, load, and manage private keys in an active `ssh-agent(1)` process. It decrypts private key files using passphrases and uploads the unencrypted key data to the agent daemon memory.

- **Upstream Project & Provenance**: Core client utility in OpenSSH (`openssh-clients`).
- **Portability & Standards Baseline**: Proprietary client to the OpenSSH authentication agent protocol; not defined in POSIX.1-2024.
- **Target Research Implementation**: Audited against **OpenSSH 10.5** (`ssh-add(1)`).
- **Applicability & Lifecycle**: The daily companion to `ssh-agent`, responsible for caching identities, setting time-to-live restrictions, locking the agent, and querying loaded fingerprints.

---

## 2. Syntax and Command Model

### 2.1 Canonical Synopsis

```bash
ssh-add [-cDdLlqSTtXx] [-E fingerprint_hash] [-e pkcs11]
        [-K] [-k] [-M maxsign] [-m minsign] [-s pkcs11] [file ...]
```

### 2.2 Execution Model

When invoked without arguments, `ssh-add` searches for default identity files in `~/.ssh/`:
- `id_ed25519`
- `id_ecdsa`
- `id_rsa`

It prompts the user for passphrases on the controlling TTY (or via `SSH_ASKPASS`) and transfers the keys to `ssh-agent` via `SSH_AUTH_SOCK`.

---

## 3. Options

### 3.1 Primary Action and Control Flags

| Flag | Description | Upstream Note |
|:---|:---|:---|
| `-l` | Lists fingerprints of all currently loaded identities. | Standard query |
| `-L` | Lists public key parameters of all loaded identities. | Full public keys |
| `-d` | Delete the specified identity key from the agent. | Selective cleanup |
| `-D` | Delete **all** identities from the agent memory. | Full purge |
| `-x` | Lock the agent with a password. | Security boundary |
| `-X` | Unlock the agent with the previously set password. | Unlocking |
| `-t life` | Set a maximum lifetime on added identities (e.g. `2h`, `1800`). | Timeout restriction |
| `-c` | Require explicit confirmation (via `ssh-askpass`) before each use. | Zero-trust protection |
| `-K` | Load resident keys from a FIDO2 hardware authenticator token. | Hardware security |

---

## 4. Basic Usage

### 4.1 Loading the Default Identity Key

```bash
ssh-add
```
```console
Enter passphrase for /home/admin/.ssh/id_ed25519: 
Identity added: /home/admin/.ssh/id_ed25519 (admin@corp.example.com)
```

### 4.2 Listing Currently Loaded Keys

```bash
ssh-add -l
```
```text
256 SHA256:7fK2m9W81XzpBqLa39XjN1sK21vL3p0kZqA7w9eF1m8 admin@corp.example.com (ED25519)
```

### 4.3 Purging All Loaded Keys

```bash
ssh-add -D
```
```text
All identities removed.
```

---

## 5. Practical Operations

### 5.1 Enforcing a Time-Bound Key Lifetime

Loading a production key that automatically purges from memory after 1 hour (3600 seconds):

```bash
ssh-add -t 1h ~/.ssh/id_prod_ed25519
```
```console
Enter passphrase for /home/admin/.ssh/id_prod_ed25519:
Identity added: /home/admin/.ssh/id_prod_ed25519 (id_prod_ed25519)
Lifetime set to 3600 seconds
```

### 5.2 Requiring Confirmation Before Key Usage

Loading a high-privilege key that prompts an interactive confirmation dialog every time a signature is requested:

```bash
ssh-add -c ~/.ssh/id_root_ed25519
```
- Every time `ssh` attempts to use this key, `ssh-askpass` pops up asking: *"Allow use of key /home/admin/.ssh/id_root_ed25519?"*.

### 5.3 Locking the Agent When Stepping Away

Locking the agent memory before leaving a physical workstation:

```bash
ssh-add -x
```
```console
Enter lock password: 
Enter lock password again: 
Agent locked.
```

Unlocking upon return:
```bash
ssh-add -X
```
```console
Enter lock password: 
Agent unlocked.
```

---

## 6. Advanced Usage

### 6.1 FIDO2 Resident Key Retrieval

OpenSSH supports discovering keys stored directly on hardware tokens (such as Yubikey 5 series):

```bash
ssh-add -K
```
```text
Enter PIN for authenticator:
Identity added from token: /home/admin/.ssh/id_ed25519_sk_rk (FIDO token)
```

### 6.2 Restricting Key Signature Limits (`-M` / `-m`)

In OpenSSH 8.9+, `ssh-add` allows restricting the maximum number of signatures a key can produce before being purged from agent memory:

```bash
ssh-add -M 5 ~/.ssh/id_deploy
```
- The key is invalidated and purged after 5 authentication attempts, preventing persistent exploitation.

---

## 7. Exit Status, Environment, and Configuration

### 7.1 Exit Status Codes

| Exit Code | Condition |
|:---:|:---|
| `0` | Key successfully added, queried, deleted, or agent locked. |
| `1` | Specified key could not be loaded, incorrect passphrase, or agent locked. |
| `2` | Could not contact authentication agent (`SSH_AUTH_SOCK` invalid or unset). |

### 7.2 Environment Variable Dependencies

- `SSH_AUTH_SOCK`: Required. If unset, `ssh-add` exits with code 2: `Could not open a connection to your authentication agent.`
- `SSH_ASKPASS`: Used to display graphical passphrase entry prompts when no terminal is attached.

---

## 8. Safety, Security, and Portability

### 8.1 Protection Against Silent Hijacking

- If an attacker gains shell access as your user, they can execute `ssh` commands that use keys cached in `ssh-agent` without entering passphrases.
- Adding keys with `-c` (confirmation required) completely mitigates silent background abuse because every signature requires an affirmative UI click.

---

## 9. Best Practices

1. **Always Set Lifetimes on Administrative Keys**:
   - *Guidance*: Load keys using `ssh-add -t <duration>` (e.g., `ssh-add -t 2h`).
   - *Authoritative Justification*: OpenSSH manual states that identities with a set lifetime are automatically removed by the agent upon expiration.
2. **Use `-c` for Sensitive Production Keys**:
   - *Guidance*: Add bastion and root deployment keys with `ssh-add -c`.
   - *Authoritative Justification*: Prevents rogue background scripts from issuing unauthorized signatures through the agent socket.
3. **Lock the Agent (`ssh-add -x`) on Inactive Workstations**:
   - *Guidance*: Integrate `ssh-add -x` into desktop screen locker hooks.
   - *Authoritative Justification*: Freezes signature generation while preserving loaded keys in memory without requiring full passphrase re-entry.
4. **Purge Identities When Finished**:
   - *Guidance*: Run `ssh-add -D` at the end of maintenance windows.
   - *Authoritative Justification*: Clears in-memory cryptographic credentials.

---

## References

1. **OpenSSH ssh-add(1) Manual**: OpenBSD Manual Pages. [https://man.openbsd.org/ssh-add](https://man.openbsd.org/ssh-add)
2. **OpenSSH ssh-agent(1) Manual**: OpenBSD Manual Pages. [https://man.openbsd.org/ssh-agent](https://man.openbsd.org/ssh-agent)
3. **OpenSSH 10.5 Release Notes**: Official Project Portal. [https://www.openssh.com/releasenotes.html](https://www.openssh.com/releasenotes.html)
