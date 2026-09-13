# LinuxHandbook Platform Expansion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Transform the repository into the official **LinuxHandbook** platform by executing full rebranding, implementing GitHub Actions CI/CD pipelines, and establishing an interactive VitePress documentation web portal with instant local search and automated GitHub Pages deployment.

**Architecture:** Update repository identity and schemas to match `fhmio/LinuxHandbook`. Configure `.github/workflows/` for automated schema and article contract verification on PRs/pushes. Scaffold a VitePress web application utilizing the 53 existing Markdown tutorials with categorized navigation and client-side Minisearch, paired with an automated GitHub Pages deployment workflow.

**Tech Stack:** Node.js (v22), VitePress 1.x, Python 3, GitHub Actions, Markdown.

**Spec:** [`docs/superpowers/specs/2026-09-12-linuxhandbook-expansion-design.md`](file:///c:/Users/mazen/OneDrive/Documents/linux-command-tutorials/docs/superpowers/specs/2026-09-12-linuxhandbook-expansion-design.md)

## Global Constraints

- Repository target remote: `https://github.com/fhmio/LinuxHandbook.git`
- Base URL for GitHub Pages: `/LinuxHandbook/`
- All 53 tutorials in `article/` must remain valid and pass `python scripts/validate_articles.py --all`
- All 10 inventory files must pass `python scripts/validate_inventory.py`
- VitePress must build cleanly via `npm run docs:build` with zero broken link warnings
- Every task must end with an atomic, conventional git commit

---

### Task 1: Core Project Rebranding & Metadata Updates

**Files:**
- Create: `package.json`
- Modify: `README.md`
- Modify: `schemas/upstream-inventory.schema.json`
- Modify: `scripts/generate_readme.py`

**Interfaces:**
- Consumes: Existing 53 articles in `article/` and 10 JSON files in `inventory/`
- Produces: Official `LinuxHandbook` naming, updated `$id` schema URI, `package.json` manifest with build scripts

- [ ] **Step 1: Create `package.json` manifest**

Write `package.json` in the project root:
```json
{
  "name": "linuxhandbook",
  "version": "1.0.0",
  "description": "The Authoritative Linux Reference & Operational Systems Playbook",
  "homepage": "https://github.com/fhmio/LinuxHandbook#readme",
  "repository": {
    "type": "git",
    "url": "git+https://github.com/fhmio/LinuxHandbook.git"
  },
  "license": "MIT",
  "type": "module",
  "scripts": {
    "docs:dev": "vitepress dev",
    "docs:build": "vitepress build",
    "docs:preview": "vitepress preview",
    "lint:articles": "python scripts/validate_articles.py --all",
    "lint:inventory": "python scripts/validate_inventory.py"
  },
  "devDependencies": {
    "vitepress": "^1.6.3"
  }
}
```

- [ ] **Step 2: Update `schemas/upstream-inventory.schema.json`**

Update the `$id` field to:
```json
  "$id": "https://github.com/fhmio/LinuxHandbook/schemas/upstream-inventory.json",
```

- [ ] **Step 3: Update `scripts/generate_readme.py`**

Update title, repository links, and badge URLs in `scripts/generate_readme.py` to point to `fhmio/LinuxHandbook` and `# LinuxHandbook — The Authoritative Linux Reference & Systems Playbook`.

- [ ] **Step 4: Update `README.md`**

Update `README.md` header, badges, and links to reflect `# LinuxHandbook — The Authoritative Linux Reference & Systems Playbook` and repository `https://github.com/fhmio/LinuxHandbook.git`.

- [ ] **Step 5: Verify schema validation and article validation**

Run:
```bash
python scripts/validate_inventory.py
python scripts/validate_articles.py --all
```
Expected: Both commands output success with 0 errors.

- [ ] **Step 6: Commit changes**

```bash
git add package.json README.md schemas/upstream-inventory.schema.json scripts/generate_readme.py
git commit -m "feat(meta): rebrand project to LinuxHandbook across README, schemas, and package.json"
```

---

### Task 2: Continuous Integration Quality Pipeline

**Files:**
- Create: `.github/workflows/ci.yml`

**Interfaces:**
- Consumes: Python validation scripts (`scripts/validate_articles.py`, `scripts/validate_inventory.py`) and npm scripts (`npm run docs:build`)
- Produces: GitHub Actions CI workflow enforcing quality gates on all pushes and PRs

- [ ] **Step 1: Create `.github/workflows/ci.yml`**

Create `.github/workflows/ci.yml` with two parallel jobs:
```yaml
name: CI Quality Gate

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  validate-content:
    name: Validate Articles & Inventory
    runs-on: ubuntu-latest
    steps:
      - name: Check out repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install validation dependencies
        run: pip install jsonschema pyyaml

      - name: Validate Upstream Inventory
        run: python scripts/validate_inventory.py

      - name: Validate Article Contracts
        run: python scripts/validate_articles.py --all

  validate-docs-build:
    name: Validate Documentation Build
    runs-on: ubuntu-latest
    steps:
      - name: Check out repository
        uses: actions/checkout@v4

      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: 22
          cache: 'npm'

      - name: Install dependencies
        run: npm ci || npm install

      - name: Test Build Documentation
        run: npm run docs:build
```

- [ ] **Step 2: Verify YAML syntax**

Run:
```bash
python -c "import yaml; yaml.safe_load(open('.github/workflows/ci.yml', encoding='utf-8'))"
```
Expected: Exits with code 0.

- [ ] **Step 3: Commit changes**

```bash
git add .github/workflows/ci.yml
git commit -m "ci: add GitHub Actions continuous integration quality pipeline"
```

---

### Task 3: VitePress Web Portal Architecture & Navigation

**Files:**
- Create: `.vitepress/config.mts`
- Create: `index.md`
- Modify: `package-lock.json` (via `npm install`)

**Interfaces:**
- Consumes: 53 articles in `article/`
- Produces: VitePress configuration with full categorized sidebar, client-side Minisearch, and high-impact landing page

- [ ] **Step 1: Install `vitepress` dependency**

Run:
```bash
npm install -D vitepress
```
Expected: `node_modules/` and `package-lock.json` updated.

- [ ] **Step 2: Create `.vitepress/config.mts`**

Configure VitePress with:
- Title: `LinuxHandbook`
- Description: `The Authoritative Linux Reference & Operational Systems Playbook`
- Base: `/LinuxHandbook/`
- Local search enabled via `provider: 'local'`
- Categorized sidebar organizing all 53 tutorials:
  - 📁 Core File Operations (ls, cp, mv, rm, mkdir, rmdir, touch, ln)
  - 📝 Text & Stream Processing (cat, head, tail, grep, sed, awk, sort, uniq, cut, tr)
  - ⚡ Process & System Triage (ps, top, free, vmstat, pgrep, pkill, w, uptime)
  - 💾 Storage & Administration (mount, umount, findmnt, lsblk, fdisk, blkid)
  - 🌐 iproute2 Networking (ip, ss, tc, bridge)
  - 🔑 OpenSSH Suite (ssh, sftp, scp, ssh-keygen, ssh-agent, ssh-add, ssh-keyscan)
  - 📦 Transfer & Archives (curl, rsync, tar, gzip, xz)
  - ⚙️ systemd Services (systemctl, journalctl)
  - ⚡ Operational Playbooks

- [ ] **Step 3: Create landing page `index.md`**

Create `index.md` in root with VitePress home layout hero banner, features grid (Upstream Verified, 1-Click Copy, POSIX Audited, Interactive Playbooks), and quick-start links.

- [ ] **Step 4: Verify local dev/build**

Run:
```bash
npx vitepress build
```
Expected: Clean build into `.vitepress/dist` with 0 missing link errors.

- [ ] **Step 5: Commit changes**

```bash
git add package-lock.json .vitepress/config.mts index.md .gitignore
git commit -m "feat(docs): configure VitePress documentation portal with categorized sidebar and local search"
```

---

### Task 4: Automated GitHub Pages Deployment Workflow

**Files:**
- Create: `.github/workflows/deploy-docs.yml`

**Interfaces:**
- Consumes: VitePress build output
- Produces: Automated deployment to GitHub Pages on every push to `main`

- [ ] **Step 1: Create `.github/workflows/deploy-docs.yml`**

Create `.github/workflows/deploy-docs.yml`:
```yaml
name: Deploy Documentation to GitHub Pages

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: 'pages'
  cancel-in-progress: true

jobs:
  build:
    name: Build VitePress Site
    runs-on: ubuntu-latest
    steps:
      - name: Check out repository
        uses: actions/checkout@v4

      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: 22
          cache: 'npm'

      - name: Install dependencies
        run: npm ci || npm install

      - name: Build site
        run: npm run docs:build

      - name: Upload Pages artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: .vitepress/dist

  deploy:
    name: Deploy to GitHub Pages
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    needs: build
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

- [ ] **Step 2: Verify YAML syntax**

Run:
```bash
python -c "import yaml; yaml.safe_load(open('.github/workflows/deploy-docs.yml', encoding='utf-8'))"
```
Expected: Exits with code 0.

- [ ] **Step 3: Commit changes**

```bash
git add .github/workflows/deploy-docs.yml
git commit -m "ci: add GitHub Pages automated deployment workflow"
```

---

### Task 5: End-to-End Build & Validation Audit

**Files:**
- Test all: `article/*.md`, `inventory/*.json`, `.vitepress/dist`

- [ ] **Step 1: Run complete inventory validation**

Run: `python scripts/validate_inventory.py`  
Expected: `SUCCESS: Validated 53 commands across 10 inventory files with 0 errors.`

- [ ] **Step 2: Run complete article validation**

Run: `python scripts/validate_articles.py --all`  
Expected: `All 53 article(s) validated successfully with 0 errors.`

- [ ] **Step 3: Run production documentation build**

Run: `npm run docs:build`  
Expected: Builds all 53 articles + index page into `.vitepress/dist` without errors.

- [ ] **Step 4: Check git status**

Run: `git status`  
Expected: Clean working tree.
