# LinuxHandbook v1.0.0

🚀 **Welcome to the initial production release of LinuxHandbook: The Authoritative Linux Reference & Operational Systems Playbook!**

LinuxHandbook transforms standard command documentation into an enterprise-grade, field-tested reference suite designed for systems engineers, DevOps professionals, site reliability engineers, and software developers.

---

## 🌟 What's New in v1.0.0

### 📚 64 Authoritative Linux Command References
Authored and published 64 in-depth, production-ready command tutorials adhering strictly to our **20-point quality contract** (`docs/article-contract.md`):

* **Package Management**: `apt`, `dnf`, `yum`
* **User & Group Administration**: `passwd`, `su`, `sudo`, `useradd`, `usermod`
* **Process & Job Control**: `kill`, `killall`, `jobs`
* **Core File Utilities**: `cat`, `cp`, `mv`, `rm`, `mkdir`, `rmdir`, `touch`, `ln`, `ls`
* **Text Processing & Streams**: `awk`, `sed`, `grep`, `cut`, `sort`, `uniq`, `tr`, `head`, `tail`
* **Modern Networking**: `ip`, `ss`, `bridge`, `tc`
* **OpenSSH Infrastructure**: `ssh`, `scp`, `sftp`, `ssh-keygen`, `ssh-agent`, `ssh-add`, `ssh-keyscan`
* **Storage, Disks & Filesystems**: `lsblk`, `blkid`, `fdisk`, `mount`, `umount`, `findmnt`
* **System & Kernel Monitoring**: `ps`, `top`, `free`, `uptime`, `vmstat`, `w`, `pgrep`, `pkill`
* **Systemd & Logging**: `systemctl`, `journalctl`
* **Search & Traversal**: `find`, `xargs`, `locate`
* **Compression & Transfers**: `tar`, `gzip`, `xz`, `rsync`, `curl`

---

### ⚡ Every Article Features
- **Quick-Reference Cards**: Instant flag tables and high-frequency syntax at the top of every guide.
- **Copyable Terminal One-Liners**: Copy-ready commands tested for immediate production triage.
- **Visual ASCII Architecture & Flowcharts**: Mental models for complex flag combinations, pipelines, network packets, and system daemons.
- **Safety Callouts & Blast Radius Advisories**: Standardized GitHub alerts (`[!CAUTION]`, `[!WARNING]`, `[!TIP]`) preventing downtime and accidental data destruction.
- **Real-World Triage Scenarios**: Concrete operational recipes for incident response, memory exhaustion, hung processes, disk leaks, and network diagnostics.

---

### 🎨 Modern VitePress Documentation Portal
- **Linuxize-Inspired Custom Theme**: Tailored layout with modern typography, responsive cards, category grids, and dark/light mode toggle.
- **Instant Search**: Client-side full-text search across all 64 commands and options.
- **Interactive UI**: Reading progress bar, category browse pills, and copyable snippets.

---

### 🛠️ Rigorous Automated Quality Tooling
- **13 Upstream Inventories**: Standardized JSON data mapping commands to their respective upstream maintainers and packages.
- **Automated Article Linter** (`scripts/validate_articles.py`): Verifies article structure, headers, code blocks, and safety tiers.
- **Upstream Schema Validator** (`scripts/validate_inventory.py`): Validates all JSON inventories against formal JSON schemas.
- **Catalog & Playbook Generator** (`scripts/generate_readme.py`): Automatically rebuilds the master table of contents and emergency runbooks.
- **GitHub Actions CI/CD**:
  - Full automated validation pipeline on every push and pull request.
  - Automated deployment workflow to GitHub Pages.

---

## 🚀 Quick Start

### Browse the Documentation Locally
```bash
git clone https://github.com/fhmio/LinuxHandbook.git
cd LinuxHandbook
npm install
npm run docs:dev
```

### Validate Articles & Inventories
```bash
python scripts/validate_inventory.py
python scripts/validate_articles.py --all
npm run docs:build
```

---

## 🤝 Contributing
Contributions, issue reports, and suggestions are welcome! Check out our [Article Contract](docs/article-contract.md) to learn more about our writing standards.
