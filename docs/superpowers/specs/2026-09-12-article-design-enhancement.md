# Design Specification: Article Visual Enhancement & Easy-Copy Commands

## 1. Objective and Scope

Transform all 53 command reference guides in `article/` from plain text/console-mixed documentation into modern, visually structured, and friction-free operational guides. Each article will feature:
1. **Metadata Badges**: Upstream suite, researched version, POSIX compliance, and execution safety tier at the top of Section 1.
2. **Quick-Reference Cheatsheet Card**: Fast-lookup table at the beginning of Section 4 (`## 4. Basic Usage`) with the top 5–8 common real-world invocations.
3. **Friction-Free 1-Click Copy Commands**: Separation of executable commands into pure, un-prefixed ```` ```bash ```` blocks followed by clearly labeled sample output blocks in ```` ```text ```` or ```` ```console ````.
4. **Admonition Callouts**: Structured GitHub-style callouts (`> [!WARNING]`, `> [!IMPORTANT]`, `> [!TIP]`, `> [!NOTE]`) for destructive actions, kernel prerequisites, performance optimizations, and upstream caveats in Sections 8 and 9.

---

## 2. Component Design Standard

### 2.1 Metadata Badge Bar (Section 1)
Directly beneath `## 1. Introduction`, an executive badge line is inserted:
```markdown
## 1. Introduction

> **Upstream**: `<Suite> <Version>` | **POSIX**: `<Standard>` | **Safety Tier**: `<Badge>` | **Scope**: `<Operational Scope>`
```

### 2.2 Quick-Reference Cheatsheet Table (Section 4)
Immediately beneath `## 4. Basic Usage`:
```markdown
## 4. Basic Usage

### 4.1 Quick Reference & Common Invocations

| Task / Scenario | Command | Key Flags |
|:---|:---|:---|
| Primary operation | `command -flag <arg>` | Short description |
| Secondary operation | `command --long-flag <arg>` | Short description |
```

### 2.3 1-Click Copy Command vs Sample Output Pattern
All terminal workflows in Sections 4, 5, and 6 will follow this exact structure:
```markdown
### 5.X Workflow Title

Context and explanation paragraph explaining the purpose and mechanics of the command.

```bash
command --flag argument
```

*Sample terminal output:*

```text
Expected output line 1
Expected output line 2
```

- **Technical Analysis**: Bullet points dissecting flags, kernel system calls, and edge cases.
```

### 2.4 Visual Callout Taxonomy (Sections 8 & 9)
- `> [!WARNING]`: Used exclusively for destructive commands (`rm -rf`, `--delete`, `fdisk`, filesystem formatting, signal kills).
- `> [!IMPORTANT]`: Used for mandatory prerequisites, required privileges (`CAP_NET_ADMIN`), and syntax rules (trailing slashes).
- `> [!TIP]`: Used for performance boosts (`-T0` multithreading, `--link-dest` snapshotting, active queue management).
- `> [!NOTE]`: Used for upstream version differences, POSIX vs GNU distinctions, and distribution quirks.

---

## 3. Batch Delivery Roadmap

| Batch | Upstream Suite | Article Count | Utility Executables |
|:---:|:---|:---:|:---|
| **1** | OpenSSH | 7 | `sftp`, `ssh`, `scp`, `ssh-keygen`, `ssh-agent`, `ssh-add`, `ssh-keyscan` |
| **2** | GNU Coreutils File Ops | 8 | `ls`, `cp`, `mv`, `rm`, `mkdir`, `rmdir`, `touch`, `ln` |
| **3** | Text Processing & Filtering | 10 | `cat`, `head`, `tail`, `grep`, `sed`, `awk`, `sort`, `uniq`, `cut`, `tr` |
| **4** | GNU Findutils | 3 | `find`, `xargs`, `locate` |
| **5** | procps-ng | 8 | `ps`, `top`, `free`, `vmstat`, `pgrep`, `pkill`, `w`, `uptime` |
| **6** | util-linux Storage | 6 | `mount`, `umount`, `findmnt`, `lsblk`, `fdisk`, `blkid` |
| **7** | iproute2 Networking | 4 | `ip`, `ss`, `tc`, `bridge` |
| **8** | systemd Services & Logs | 2 | `systemctl`, `journalctl` |
| **9** | Transfer & Compression | 5 | `curl`, `rsync`, `tar`, `gzip`, `xz` |

---

## 4. Verification & Quality Gates

1. Every article must strictly preserve the 9 required top-level numbered headings and front matter contract defined in `docs/article-contract.md`.
2. After editing each batch, run:
   ```bash
   python scripts/validate_articles.py --suite <suite>
   ```
3. Commit each enhanced article file individually with a semantic commit message.
4. Conclude with full library verification:
   ```bash
   python scripts/validate_articles.py --all
   python scripts/validate_inventory.py
   python scripts/generate_readme.py
   ```
