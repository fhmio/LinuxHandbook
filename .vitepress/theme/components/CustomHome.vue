<script setup>
import ArticleCard from './ArticleCard.vue'
import CheatsheetCard from './CheatsheetCard.vue'
import ToolCard from './ToolCard.vue'
import SeriesCard from './SeriesCard.vue'

// Top 6 Basics
const basics = [
  {
    title: 'Basic Linux Commands Every User Should Know',
    date: 'APR 20, 2026',
    readTime: '18 MIN READ',
    description: 'The basic Linux commands you need for file management, navigation, permissions, networking, and package management.',
    url: '/LinuxHandbook/article/linux-ls-tutorial',
    gradientClass: 'gradient-blue',
    thumbText: 'Linux Commands'
  },
  {
    title: 'pwd Command in Linux: Print the Current Working Directory',
    date: 'MAR 2, 2026',
    readTime: '4 MIN READ',
    description: 'The pwd command prints the current working directory in Linux. This guide covers pwd syntax, physical and logical paths, and variables.',
    url: '/LinuxHandbook/article/linux-ls-tutorial',
    gradientClass: 'gradient-teal',
    thumbText: 'YOU ARE HERE'
  },
  {
    title: 'cd Command in Linux: Change Directories',
    date: 'AUG 5, 2026',
    readTime: '9 MIN READ',
    description: 'Change directories in Linux with cd, covering absolute and relative paths, home and parent shortcuts, and symbolic links.',
    url: '/LinuxHandbook/article/linux-ls-tutorial',
    gradientClass: 'gradient-purple',
    thumbText: 'cd ~'
  },
  {
    title: 'ls Command in Linux: List Files and Directories',
    date: 'SEP 6, 2026',
    readTime: '13 MIN READ',
    description: 'The ls command lists files and directories in Linux. See how to use ls -l, ls -al, hidden-file options, sorting, and practical combinations.',
    url: '/LinuxHandbook/article/linux-ls-tutorial',
    gradientClass: 'gradient-yellow',
    thumbText: 'ls -la'
  },
  {
    title: 'How to Create a File in Linux',
    date: 'AUG 25, 2026',
    readTime: '7 MIN READ',
    description: 'Create a file in Linux from the command line with touch, redirection, cat, echo, printf, or a heredoc, and build large test files.',
    url: '/LinuxHandbook/article/linux-touch-tutorial',
    gradientClass: 'gradient-pink',
    thumbText: 'touch file.txt'
  },
  {
    title: 'How to Create a Directory in Linux: mkdir Command Examples',
    date: 'JUL 6, 2026',
    readTime: '5 MIN READ',
    description: 'Create single, multiple, and nested directories in Linux with mkdir, set permissions with -m, and fix Permission denied errors.',
    url: '/LinuxHandbook/article/linux-mkdir-tutorial',
    gradientClass: 'gradient-cyan',
    thumbText: 'mkdir -p'
  }
]

// Learning Paths (3 Cards)
const learningPaths = [
  {
    title: 'Linux Users and Permissions',
    date: 'FEB 3, 2026',
    readTime: '20 ARTICLES',
    description: 'Learn how to manage Linux users, groups, and file permissions. This series covers useradd, chmod, chown, sudo, and security best practices.',
    url: '/LinuxHandbook/article/linux-useradd-tutorial',
    gradientClass: 'gradient-purple',
    thumbText: 'Users & Perms'
  },
  {
    title: 'Bash Scripting Fundamentals',
    date: 'JUL 1, 2026',
    readTime: '50 ARTICLES',
    description: 'Learn Bash scripting from the ground up. This series covers everything from basic syntax to advanced techniques for writing robust scripts.',
    url: '/LinuxHandbook/bash',
    gradientClass: 'gradient-indigo',
    thumbText: 'Bash Scripting'
  },
  {
    title: 'SSH Essentials & Secure Shell',
    date: 'JAN 30, 2026',
    readTime: '28 ARTICLES',
    description: 'Learn how to use SSH to securely connect to remote servers, transfer files, set up key-based authentication, and create encrypted tunnels.',
    url: '/LinuxHandbook/article/linux-ssh-tutorial',
    gradientClass: 'gradient-amber',
    thumbText: 'SSH Keys'
  }
]

// Quick References
const quickReferences = [
  {
    title: 'Linux Commands Cheatsheet',
    date: 'JAN 12, 2026',
    description: 'The most-used Linux commands at a glance.',
    url: '/LinuxHandbook/cheatsheets'
  },
  {
    title: 'Bash Cheatsheet',
    date: 'AUG 17, 2026',
    description: 'Variables, loops, conditionals, strings, and parameter expansion.',
    url: '/LinuxHandbook/bash'
  },
  {
    title: 'SSH Cheatsheet',
    date: 'JAN 26, 2026',
    description: 'Connection options, key management, and port tunneling.',
    url: '/LinuxHandbook/article/linux-ssh-tutorial'
  },
  {
    title: 'Systemctl Cheatsheet',
    date: 'AUG 2, 2026',
    description: 'Service commands, daemon lifecycle, and journal logging.',
    url: '/LinuxHandbook/article/linux-systemctl-tutorial'
  },
  {
    title: 'Networking (IP & SS) Cheatsheet',
    date: 'JAN 12, 2026',
    description: 'Interface routing, Netlink socket inspection, and listening ports.',
    url: '/LinuxHandbook/article/linux-ss-tutorial'
  },
  {
    title: 'Storage & Fdisk Cheatsheet',
    date: 'AUG 25, 2026',
    description: 'Essential shortcuts for disk partitions, block devices, and filesystems.',
    url: '/LinuxHandbook/article/linux-lsblk-tutorial'
  }
]
</script>

<template>
  <div class="linuxize-home-container">
    <!-- Header -->
    <header class="home-main-header">
      <h1 class="home-main-title">Start Here</h1>
      <p class="home-main-subtitle">
        New to Linux? Start here for curated learning paths, essential command guides, and quick references to help you get the most out of Linux.
      </p>
    </header>

    <!-- Welcome Intro Callout -->
    <div class="welcome-callout-box">
      <p>
        Welcome to <strong>LinuxHandbook</strong>. We publish practical, tested tutorials on Linux, Bash, DevOps, and server administration. With our comprehensive command references, finding where to begin is simple. This page gives you a guided starting point, whether you are a complete beginner or looking to level up specific operational skills. Each guide includes verified commands, examples, and troubleshooting when it matters.
      </p>
    </div>

    <!-- NEW TO LINUX? -->
    <section class="home-section">
      <div class="section-title-group">
        <h2 class="section-label">NEW TO LINUX?</h2>
        <p class="section-subtext">Start with these basics if you are new to the command line.</p>
      </div>

      <div class="cards-grid-3">
        <ArticleCard
          v-for="(item, idx) in basics"
          :key="idx"
          v-bind="item"
        />
      </div>
    </section>

    <!-- 3-Column Category Lists -->
    <section class="home-section">
      <div class="lists-grid-3">
        <!-- Col 1 -->
        <div class="list-col">
          <h2 class="col-title">FILE OPERATIONS</h2>
          <div class="mini-cards-stack">
            <CheatsheetCard title="cp" date="AUG 21, 2026 • 16 MIN READ" description="Copy files and directories." url="/LinuxHandbook/article/linux-cp-tutorial" />
            <CheatsheetCard title="mv" date="AUG 5, 2026 • 11 MIN READ" description="Move and rename files." url="/LinuxHandbook/article/linux-mv-tutorial" />
            <CheatsheetCard title="rm" date="AUG 11, 2026 • 11 MIN READ" description="Remove files and directories safely." url="/LinuxHandbook/article/linux-rm-tutorial" />
            <CheatsheetCard title="mkdir" date="JUL 6, 2026 • 5 MIN READ" description="Create directories and parent hierarchies." url="/LinuxHandbook/article/linux-mkdir-tutorial" />
          </div>
        </div>

        <!-- Col 2 -->
        <div class="list-col">
          <h2 class="col-title">TEXT PROCESSING AND SEARCH</h2>
          <div class="mini-cards-stack">
            <CheatsheetCard title="grep" date="AUG 15, 2026 • 18 MIN READ" description="Search text using regular expression patterns." url="/LinuxHandbook/article/linux-grep-tutorial" />
            <CheatsheetCard title="find" date="JUL 8, 2026 • 10 MIN READ" description="Locate files across the filesystem hierarchy." url="/LinuxHandbook/article/linux-find-tutorial" />
            <CheatsheetCard title="cat" date="JUL 30, 2026 • 7 MIN READ" description="View, stream, and concatenate files." url="/LinuxHandbook/article/linux-cat-tutorial" />
            <CheatsheetCard title="awk" date="AUG 16, 2026 • 9 MIN READ" tag="SERIES" description="Scan and process column-delimited data." url="/LinuxHandbook/article/linux-awk-tutorial" />
          </div>
        </div>

        <!-- Col 3 -->
        <div class="list-col">
          <h2 class="col-title">PERMISSIONS AND SYSTEM</h2>
          <div class="mini-cards-stack">
            <CheatsheetCard title="sudo" date="AUG 22, 2026 • 13 MIN READ" tag="SERIES" description="Run commands with elevated root privileges." url="/LinuxHandbook/article/linux-sudo-tutorial" />
            <CheatsheetCard title="useradd" date="SEP 11, 2026 • 13 MIN READ" tag="SERIES" description="Create user accounts, shells, and home dirs." url="/LinuxHandbook/article/linux-useradd-tutorial" />
            <CheatsheetCard title="passwd" date="SEP 12, 2026 • 8 MIN READ" description="Update and manage authentication tokens." url="/LinuxHandbook/article/linux-passwd-tutorial" />
            <CheatsheetCard title="systemctl" date="AUG 6, 2026 • 16 MIN READ" tag="SERIES" description="Manage systemd units, services, and boots." url="/LinuxHandbook/article/linux-systemctl-tutorial" />
          </div>
        </div>
      </div>
    </section>

    <!-- LEARNING PATHS -->
    <section class="home-section">
      <div class="section-title-group">
        <h2 class="section-label">LEARNING PATHS</h2>
      </div>

      <div class="cards-grid-3">
        <ArticleCard
          v-for="(path, idx) in learningPaths"
          :key="idx"
          v-bind="path"
        />
      </div>
    </section>

    <!-- QUICK REFERENCES -->
    <section class="home-section">
      <div class="section-title-group">
        <h2 class="section-label">QUICK REFERENCES</h2>
      </div>

      <div class="cards-grid-3">
        <CheatsheetCard
          v-for="(ref, idx) in quickReferences"
          :key="idx"
          v-bind="ref"
        />
      </div>
    </section>

    <!-- 3-Column Topics: DEVOPS, WEB SERVERS, NETWORKING -->
    <section class="home-section">
      <div class="lists-grid-3">
        <div class="list-col">
          <h2 class="col-title">STORAGE & DISKS</h2>
          <div class="mini-cards-stack">
            <CheatsheetCard title="lsblk" date="JUL 27, 2026 • 6 MIN READ" description="Inspect block device trees and partitions." url="/LinuxHandbook/article/linux-lsblk-tutorial" />
            <CheatsheetCard title="fdisk" date="JUN 24, 2026 • 5 MIN READ" description="Partition GPT/MBR storage drives." url="/LinuxHandbook/article/linux-fdisk-tutorial" />
          </div>
        </div>

        <div class="list-col">
          <h2 class="col-title">TRANSFER & SYNC</h2>
          <div class="mini-cards-stack">
            <CheatsheetCard title="rsync" date="APR 25, 2026 • 8 MIN READ" description="Delta synchronization over SSH." url="/LinuxHandbook/article/linux-rsync-tutorial" />
            <CheatsheetCard title="curl" date="APR 26, 2026 • 6 MIN READ" description="Data transfer with HTTP/HTTPS." url="/LinuxHandbook/article/linux-curl-tutorial" />
          </div>
        </div>

        <div class="list-col">
          <h2 class="col-title">NETWORKING & SECURITY</h2>
          <div class="mini-cards-stack">
            <CheatsheetCard title="ss" date="JUL 27, 2026 • 12 MIN READ" tag="SERIES" description="Socket statistics and active ports." url="/LinuxHandbook/article/linux-ss-tutorial" />
            <CheatsheetCard title="ip" date="MAR 25, 2026 • 9 MIN READ" description="Interfaces, routes, and address assignment." url="/LinuxHandbook/article/linux-ip-tutorial" />
          </div>
        </div>
      </div>
    </section>

    <!-- INTERACTIVE TOOLS -->
    <section class="home-section">
      <div class="section-title-group">
        <h2 class="section-label">INTERACTIVE TOOLS</h2>
      </div>

      <div class="tools-grid-3">
        <ToolCard title="chmod Calculator" description="Toggle permission bits and read off octal and symbolic values." url="/LinuxHandbook/tools" />
        <ToolCard title="Cron Generator" description="Build and explain crontab expressions in plain English." url="/LinuxHandbook/tools" />
        <ToolCard title="Subnet Calculator" description="Split IPv4 CIDR blocks and calculate netmasks and broadcasts." url="/LinuxHandbook/tools" />
        <ToolCard title="rsync Command Builder" description="Pick options, excludes, and build an explained command." url="/LinuxHandbook/tools" />
        <ToolCard title="find Command Builder" description="Filter by date, size, pattern, and generate find syntax." url="/LinuxHandbook/tools" />
        <ToolCard title="systemd Service Generator" description="Create clean unit files with restart and security policies." url="/LinuxHandbook/tools" />
      </div>
    </section>

    <!-- EXPLORE MORE -->
    <section class="explore-more-section">
      <h2 class="explore-label">EXPLORE MORE</h2>
      <div class="explore-pills">
        <a href="/LinuxHandbook/linux-commands" class="explore-pill">All Articles</a>
        <a href="/LinuxHandbook/series" class="explore-pill">All Series</a>
        <a href="/LinuxHandbook/cheatsheets" class="explore-pill">All Cheatsheets</a>
        <a href="/LinuxHandbook/tools" class="explore-pill">All Tools</a>
        <a href="/LinuxHandbook/about" class="explore-pill">About</a>
      </div>
      <p class="explore-footer-text">
        If you have any questions or suggestions, feel free to visit our
        <a href="/LinuxHandbook/about">About page</a> or contribute on GitHub.
      </p>
    </section>
  </div>
</template>

<style scoped>
.linuxize-home-container {
  max-width: 1100px;
  margin: 0 auto;
  padding: 2.5rem 1.5rem 5rem;
}

.home-main-header {
  margin-bottom: 2rem;
}

.home-main-title {
  font-size: 3rem;
  font-weight: 800;
  letter-spacing: -0.02em;
  color: #0f172a;
  margin: 0 0 0.75rem 0;
}

.home-main-subtitle {
  font-size: 1.15rem;
  color: #475569;
  max-width: 820px;
  margin: 0;
  line-height: 1.6;
}

.welcome-callout-box {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 1.75rem;
  margin-bottom: 3.5rem;
}

.welcome-callout-box p {
  margin: 0;
  font-size: 1rem;
  line-height: 1.7;
  color: #334155;
}

.home-section {
  margin-bottom: 4rem;
}

.section-title-group {
  margin-bottom: 1.75rem;
}

.section-label {
  font-size: 0.85rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #64748b;
  margin: 0 0 0.35rem 0;
}

.section-subtext {
  font-size: 1rem;
  color: #475569;
  margin: 0;
}

.cards-grid-3 {
  display: grid;
  grid-template-columns: repeat(1, minmax(0, 1fr));
  gap: 1.5rem;
}

@media (min-width: 768px) {
  .cards-grid-3 {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
}

.lists-grid-3 {
  display: grid;
  grid-template-columns: repeat(1, minmax(0, 1fr));
  gap: 2rem;
}

@media (min-width: 768px) {
  .lists-grid-3 {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
}

.col-title {
  font-size: 0.825rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #64748b;
  margin: 0 0 1.25rem 0;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid #f1f5f9;
}

.mini-cards-stack {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.tools-grid-3 {
  display: grid;
  grid-template-columns: repeat(1, minmax(0, 1fr));
  gap: 1.5rem;
}

@media (min-width: 768px) {
  .tools-grid-3 {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
}

.explore-more-section {
  border-top: 1px solid #e2e8f0;
  padding-top: 3.5rem;
  margin-top: 2rem;
}

.explore-label {
  font-size: 0.85rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #64748b;
  margin: 0 0 1.25rem 0;
}

.explore-pills {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  margin-bottom: 2rem;
}

.explore-pill {
  background: #2563eb;
  color: white !important;
  font-size: 0.875rem;
  font-weight: 600;
  padding: 0.5rem 1.25rem;
  border-radius: 9999px;
  text-decoration: none !important;
  transition: background 0.15s ease, transform 0.15s ease;
}

.explore-pill:hover {
  background: #1d4ed8;
  transform: translateY(-1px);
}

.explore-footer-text {
  font-size: 0.95rem;
  color: #64748b;
  margin: 0;
}

.explore-footer-text a {
  color: #2563eb !important;
  text-decoration: underline;
}

/* Dark mode */
.dark .home-main-title {
  color: #f8fafc;
}

.dark .home-main-subtitle,
.dark .section-subtext {
  color: #94a3b8;
}

.dark .welcome-callout-box {
  background: #1e293b;
  border-color: #334155;
}

.dark .welcome-callout-box p {
  color: #cbd5e1;
}

.dark .col-title {
  color: #94a3b8;
  border-bottom-color: #334155;
}

.dark .explore-more-section {
  border-top-color: #334155;
}

.dark .explore-footer-text {
  color: #94a3b8;
}

.dark .explore-footer-text a {
  color: #60a5fa !important;
}
</style>
