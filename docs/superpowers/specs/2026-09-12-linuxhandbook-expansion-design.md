# Design Specification: LinuxHandbook Platform Rebranding, Modern VitePress Documentation Portal, CI/CD Automation, and Content Expansion

**Specification ID:** `2026-09-12-linuxhandbook-expansion-design`  
**Date:** 2026-09-12  
**Target Repository:** [`fhmio/LinuxHandbook`](https://github.com/fhmio/LinuxHandbook.git)  
**Status:** DRAFT (Pending User Review)

---

## 1. Executive Summary & Goals

The `LinuxHandbook` project evolves the existing 53-article reference library into an enterprise-grade open-source documentation platform and systems operational playbook. This architectural specification establishes:

1. **Official Brand & Identity Alignment**: Formal rebranding from legacy naming to **LinuxHandbook**, updating all repository badges, metadata schemas, documentation links, and README assets to reference [`https://github.com/fhmio/LinuxHandbook.git`](https://github.com/fhmio/LinuxHandbook.git).
2. **Automated CI/CD Quality Gates**: Implementation of GitHub Actions workflows ensuring automated compliance testing for article contracts, JSON inventory schemas, link validity, and build health on every commit and pull request.
3. **Interactive Documentation Web Portal (VitePress)**: A modern, ultra-fast static web portal built with VitePress, offering instant in-browser local search (Minisearch), dark/light mode, responsive navigation, 1-click command copying, and automated deployment to GitHub Pages.
4. **Structured Content Expansion**: A roadmap and technical standard for expanding beyond the core 53 POSIX/system utilities to modern CLI replacements (`ripgrep`, `fd`, `bat`, `btop`), container runtimes (`docker`, `podman`), and Linux hardening/firewalls (`ufw`, `iptables`, `nftables`).

---

## 2. Core Architectural Components

### 2.1 Rebranding & Metadata Updates

All repository metadata and user-facing documentation will be systematically updated to establish **LinuxHandbook** as the canonical project name:

- **[`README.md`](file:///c:/Users/mazen/OneDrive/Documents/linux-command-tutorials/README.md)**:
  - Title: `# LinuxHandbook — The Authoritative Linux Reference & Systems Playbook`
  - Repository Links: `https://github.com/fhmio/LinuxHandbook.git`
  - GitHub Badges: CI Status, Catalog Size (53 Guides), POSIX.1-2024 Audit, License (MIT), GitHub Pages Live Site.
- **[`schemas/upstream-inventory.schema.json`](file:///c:/Users/mazen/OneDrive/Documents/linux-command-tutorials/schemas/upstream-inventory.schema.json)**:
  - `$id` updated to `https://github.com/fhmio/LinuxHandbook/schemas/upstream-inventory.json`.
- **Generator & Validation Tooling**:
  - Update [`scripts/generate_readme.py`](file:///c:/Users/mazen/OneDrive/Documents/linux-command-tutorials/scripts/generate_readme.py) header generation and references.
- **Node.js Project Configuration (`package.json`)**:
  - Project name: `linuxhandbook`
  - Repository field: `https://github.com/fhmio/LinuxHandbook.git`
  - Scripts: `docs:dev`, `docs:build`, `docs:preview`, `lint:articles`, `lint:inventory`.

---

### 2.2 CI/CD Quality & Automation Infrastructure

A dedicated `.github/workflows/` suite will enforce architectural invariants:

1. **Continuous Integration Workflow (`.github/workflows/ci.yml`)**:
   - **Triggers**: `push` on branch `main`, `pull_request` against `main`.
   - **Environment**: `ubuntu-latest`, Python 3.12, Node.js 20.x.
   - **Steps**:
     1. Check out repository code.
     2. Set up Python and install schema validation dependencies (`jsonschema`).
     3. Run inventory validation: `python scripts/validate_inventory.py`.
     4. Run article compliance validation: `python scripts/validate_articles.py --all`.
     5. Set up Node.js and verify VitePress build: `npm ci && npm run docs:build`.

2. **Automated Documentation Deployment (`.github/workflows/deploy-docs.yml`)**:
   - **Triggers**: `push` to `main` (paths: `article/**`, `.vitepress/**`, `package.json`, `index.md`).
   - **Permissions**: `contents: read`, `pages: write`, `id-token: write`.
   - **Deployment Target**: GitHub Pages using official `@actions/deploy-pages`.

---

### 2.3 VitePress Web Portal Architecture

The documentation portal will be built with VitePress for maximum speed, clean typography, and zero overhead:

```
LinuxHandbook/
├── .github/
│   └── workflows/
│       ├── ci.yml                 # CI quality verification
│       └── deploy-docs.yml        # Automated GitHub Pages deployment
├── .vitepress/
│   ├── config.mts                 # VitePress configuration & navigation
│   └── theme/                     # Custom CSS & branding styling
├── article/                       # 53 authoritative Markdown tutorials
├── index.md                       # High-impact documentation portal landing page
├── inventory/                     # Upstream metadata JSON catalogs
├── schemas/                       # JSON schemas
├── scripts/                       # Python validation & generation scripts
└── package.json                   # Node package & VitePress scripts
```

#### VitePress Configuration Specifications:
- **Title**: `LinuxHandbook`
- **Description**: `The Authoritative Linux Reference & Operational Systems Playbook`
- **Base URL**: `/LinuxHandbook/` (configured for GitHub Pages hosting at `fhmio.github.io/LinuxHandbook/`)
- **Search Engine**: Native Minisearch local search provider (instant full-text search across all 53 articles without third-party dependencies).
- **Navigation Sidebar**: Categorized logically into:
  - 📖 **Playbooks**: Incident Triage, Storage Auditing, Network Diagnostics, Security Audits.
  - 📁 **File Operations**: GNU Coreutils (`ls`, `cp`, `mv`, `rm`, `mkdir`, `rmdir`, `touch`, `ln`).
  - 📝 **Text & Stream Processing**: `grep`, `sed`, `awk`, `cut`, `sort`, `uniq`, `tr`, `cat`, `head`, `tail`.
  - ⚡ **Process & System Triage**: procps-ng (`ps`, `top`, `free`, `vmstat`, `pgrep`, `pkill`, `w`, `uptime`).
  - 🌐 **Networking Suite**: iproute2 (`ip`, `ss`, `tc`, `bridge`).
  - 💾 **Storage & Partitions**: util-linux (`mount`, `umount`, `findmnt`, `lsblk`, `fdisk`, `blkid`).
  - 🔑 **Remote Access & Keys**: OpenSSH (`ssh`, `sftp`, `scp`, `ssh-keygen`, `ssh-agent`, `ssh-add`, `ssh-keyscan`).
  - 📦 **Transfer & Archives**: `curl`, `rsync`, `tar`, `gzip`, `xz`.
  - ⚙️ **Service Lifecycle**: systemd (`systemctl`, `journalctl`).

---

### 2.4 Content Expansion Roadmap

Following the establishment of the rebranded platform and web portal, content expansion will proceed in structured phases maintaining the 20-point Definition of Done:

1. **Phase 3.1: Modern CLI Replacements**:
   - Tools: `ripgrep` (`rg`), `fd`, `bat`, `eza`, `btop`.
   - Deliverables: `inventory/modern-cli.json` + 5 comprehensive reference guides.
2. **Phase 3.2: Containerization & Cloud Runtimes**:
   - Tools: `docker`, `podman`, `crictl`.
   - Deliverables: `inventory/containers.json` + 3 comprehensive reference guides.
3. **Phase 3.3: Linux Hardening & Firewall Administration**:
   - Tools: `ufw`, `iptables`, `nftables`.
   - Deliverables: `inventory/security.json` + 3 comprehensive reference guides.

---

## 3. Phased Implementation Plan

- **Phase 1: Brand Rebranding & CI/CD Pipelines**
  - Update `README.md`, `schemas/upstream-inventory.schema.json`, and generation scripts.
  - Create `.github/workflows/ci.yml`.
  - Validate all tests pass locally.
  - Git commit: `feat(meta): rebrand project to LinuxHandbook and establish CI pipeline`.

- **Phase 2: VitePress Web Portal Setup & Pages Deployment**
  - Initialize `package.json` with `vitepress`.
  - Configure `.vitepress/config.mts` with full sidebar and local search.
  - Create `index.md` landing page.
  - Create `.github/workflows/deploy-docs.yml`.
  - Test build locally with `npx vitepress build`.
  - Git commit: `feat(docs): initialize VitePress documentation portal and deployment workflow`.

- **Phase 3: Content Expansion (Modern CLI, Containers, Security)**
  - Incrementally research, inventory, author, and validate articles per track.

---

## 4. Verification Plan

| Verification Gate | Command | Acceptance Criteria |
|:---|:---|:---|
| **Inventory Schema Audit** | `python scripts/validate_inventory.py` | 0 schema validation errors |
| **Article Structure Audit** | `python scripts/validate_articles.py --all` | 53/53 articles pass with 0 errors |
| **VitePress Portal Build** | `npx vitepress build` | Clean production build with 0 broken links |
| **Git Repository Status** | `git status` | Clean working tree |
