<script setup>
import { ref } from 'vue'
import Breadcrumbs from './Breadcrumbs.vue'
import ArticleCard from './ArticleCard.vue'
import HorizontalArticleItem from './HorizontalArticleItem.vue'
import Pagination from './Pagination.vue'

const breadcrumbs = [
  { text: 'HOME', link: '/LinuxHandbook/' },
  { text: 'TAGS', link: '#' },
  { text: 'LINUX COMMANDS' }
]

const featured = [
  {
    title: 'Understanding the /etc/fstab File in Linux',
    date: 'SEP 13, 2026',
    readTime: '12 MIN READ',
    badge: 'SERIES',
    description: 'The /etc/fstab file defines how filesystems and storage devices are mounted at boot. This guide explains the fstab format, field syntax, and recovery.',
    url: '/LinuxHandbook/article/linux-mount-tutorial',
    gradientClass: 'gradient-teal',
    thumbText: 'fstab'
  },
  {
    title: 'How to Create Users in Linux (useradd Command)',
    date: 'SEP 11, 2026',
    readTime: '13 MIN READ',
    badge: 'SERIES',
    description: 'Create user accounts in Linux with useradd: home directories, passwords, groups, shells, UIDs, and expiry dates, plus how useradd works.',
    url: '/LinuxHandbook/article/linux-useradd-tutorial',
    gradientClass: 'gradient-purple',
    thumbText: 'useradd'
  },
  {
    title: 'Package Management in Modern Linux (APT & DNF)',
    date: 'SEP 11, 2026',
    readTime: '9 MIN READ',
    description: 'Comprehensive guide covering package installations, repositories, locks, dependency management, and unattended upgrades.',
    url: '/LinuxHandbook/article/linux-apt-tutorial',
    gradientClass: 'gradient-blue',
    thumbText: 'apt'
  }
]

const articles = [
  {
    title: 'vmstat Command in Linux: Memory, CPU, and I/O Statistics',
    date: 'SEP 7, 2026',
    readTime: '9 MIN READ',
    badge: 'NEW',
    description: 'Use vmstat to monitor Linux CPU, memory, swap, processes, and disk I/O. This guide explains each column, live sampling, timestamps, and disk statistics.',
    url: '/LinuxHandbook/article/linux-vmstat-tutorial',
    gradientClass: 'gradient-cyan',
    thumbText: 'vmstat'
  },
  {
    title: 'rm Command in Linux: Remove Files and Directories',
    date: 'SEP 7, 2026',
    readTime: '7 MIN READ',
    description: 'Use the rm command in Linux to delete files and directories, with examples for recursive removal, force mode, safety prompts, glob patterns, and safer alternatives.',
    url: '/LinuxHandbook/article/linux-rm-tutorial',
    gradientClass: 'gradient-rose',
    thumbText: 'rm'
  },
  {
    title: 'ls Command in Linux: List Files and Directories',
    date: 'SEP 6, 2026',
    readTime: '13 MIN READ',
    description: 'The ls command lists files and directories in Linux. Learn how to use ls -l, ls -al, hidden-file options, sorting, and practical combinations.',
    url: '/LinuxHandbook/article/linux-ls-tutorial',
    gradientClass: 'gradient-yellow',
    thumbText: 'ls'
  },
  {
    title: 'Listing Linux Services with systemctl',
    date: 'SEP 5, 2026',
    readTime: '8 MIN READ',
    description: 'Use the systemctl command to list running, failed, and enabled Linux services. Includes filtering by state, checking status, and listing unit files.',
    url: '/LinuxHandbook/article/linux-systemctl-tutorial',
    gradientClass: 'gradient-purple',
    thumbText: 'systemctl'
  },
  {
    title: 'ps Command in Linux: ps aux and Common Options',
    date: 'SEP 3, 2026',
    readTime: '11 MIN READ',
    description: 'Use ps aux and related ps command options in Linux to list running processes, read output columns, sort by CPU or memory, and filter by PID or user.',
    url: '/LinuxHandbook/article/linux-ps-tutorial',
    gradientClass: 'gradient-blue',
    thumbText: 'ps aux'
  },
  {
    title: 'ss Command in Linux: Display Socket Statistics',
    date: 'SEP 2, 2026',
    readTime: '12 MIN READ',
    description: 'Use the ss command to list TCP, UDP, and Unix sockets, filter by port and state, read queue columns, inspect timers, and replace legacy netstat.',
    url: '/LinuxHandbook/article/linux-ss-tutorial',
    gradientClass: 'gradient-emerald',
    thumbText: 'ss -tulpn'
  },
  {
    title: 'dnf Command in Linux: Install, Update, and Manage Packages',
    date: 'SEP 1, 2026',
    readTime: '12 MIN READ',
    description: 'Common dnf commands for installing, updating, removing, searching, and managing packages on Fedora, RHEL, Rocky Linux, AlmaLinux, and other RPM systems.',
    url: '/LinuxHandbook/article/linux-dnf-tutorial',
    gradientClass: 'gradient-amber',
    thumbText: 'dnf'
  },
  {
    title: 'Linux Kill Process: Stop Processes by PID or Name',
    date: 'AUG 28, 2026',
    readTime: '12 MIN READ',
    description: 'Stop stuck programs in Linux with kill, killall, pkill, and xkill. Find the PID, send SIGTERM first, and use SIGKILL only when the process refuses to exit.',
    url: '/LinuxHandbook/article/linux-kill-tutorial',
    gradientClass: 'gradient-purple',
    thumbText: 'kill -9'
  },
  {
    title: 'find Command in Linux: Search Files and Directories',
    date: 'AUG 25, 2026',
    readTime: '14 MIN READ',
    description: 'Real-time filesystem search with the find utility. Filter by name, type, size, modification time, and execute batch commands with exec and xargs.',
    url: '/LinuxHandbook/article/linux-find-tutorial',
    gradientClass: 'gradient-teal',
    thumbText: 'find'
  },
  {
    title: 'grep Command: Search Text Using Regular Expressions',
    date: 'AUG 22, 2026',
    readTime: '15 MIN READ',
    description: 'Fast pattern scanning across files and pipelines. Covers recursive search, line numbers, inverted matches, context lines, and extended regex.',
    url: '/LinuxHandbook/article/linux-grep-tutorial',
    gradientClass: 'gradient-blue',
    thumbText: 'grep -rn'
  },
  {
    title: 'SSH Protocol & Remote Server Administration',
    date: 'AUG 20, 2026',
    readTime: '16 MIN READ',
    badge: 'SERIES',
    description: 'Connect securely to remote Linux servers using OpenSSH. Config files, key authentication, port forwarding, and agent forwarding best practices.',
    url: '/LinuxHandbook/article/linux-ssh-tutorial',
    gradientClass: 'gradient-slate',
    thumbText: 'ssh'
  },
  {
    title: 'rsync Command: Delta File Synchronization & Remote Backups',
    date: 'AUG 18, 2026',
    readTime: '13 MIN READ',
    description: 'Fast, flexible file-copying tool for local and remote transfers. Bandwidth limiting, archive mode, permissions preservation, and SSH tunnels.',
    url: '/LinuxHandbook/article/linux-rsync-tutorial',
    gradientClass: 'gradient-rose',
    thumbText: 'rsync -avz'
  }
]
</script>

<template>
  <div class="linuxize-page-container">
    <!-- Breadcrumbs -->
    <Breadcrumbs :items="breadcrumbs" />

    <!-- Page Header -->
    <header class="category-header">
      <h1 class="category-title">Linux Commands</h1>
      <p class="category-subtitle">
        Command references for core Linux tools, syntax, examples, and practical one-liners.
      </p>
    </header>

    <!-- Top Featured Row (3 Cards) -->
    <section class="featured-cards-grid">
      <ArticleCard
        v-for="(item, idx) in featured"
        :key="idx"
        v-bind="item"
      />
    </section>

    <!-- Article List (Horizontal Items) -->
    <section class="articles-list-section">
      <HorizontalArticleItem
        v-for="(article, idx) in articles"
        :key="idx"
        v-bind="article"
      />
    </section>

    <!-- Pagination -->
    <Pagination :current-page="1" :pages="[1, 2, 3, '...', 11]" />
  </div>
</template>

<style scoped>
.linuxize-page-container {
  max-width: 1100px;
  margin: 0 auto;
  padding: 2.5rem 1.5rem 4rem;
}

.category-header {
  margin-bottom: 2.5rem;
}

.category-title {
  font-size: 2.75rem;
  font-weight: 800;
  letter-spacing: -0.02em;
  color: #0f172a;
  margin: 0 0 0.75rem 0;
  line-height: 1.2;
}

.category-subtitle {
  font-size: 1.15rem;
  color: #475569;
  max-width: 800px;
  margin: 0;
  line-height: 1.6;
}

.featured-cards-grid {
  display: grid;
  grid-template-columns: repeat(1, minmax(0, 1fr));
  gap: 1.5rem;
  margin-bottom: 3.5rem;
}

@media (min-width: 768px) {
  .featured-cards-grid {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
}

.articles-list-section {
  border-top: 1px solid #f1f5f9;
  padding-top: 1rem;
}

/* Dark mode */
.dark .category-title {
  color: #f8fafc;
}

.dark .category-subtitle {
  color: #94a3b8;
}

.dark .articles-list-section {
  border-top-color: #1e293b;
}
</style>
