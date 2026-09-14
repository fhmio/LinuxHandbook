<script setup>
import CheatsheetCard from './CheatsheetCard.vue'
import Pagination from './Pagination.vue'

const cheatsheets = [
  {
    title: 'SSH Cheatsheet',
    date: 'SEP 14, 2026',
    tag: 'OPENSSH',
    description: 'Quick reference for SSH keys, config host shortcuts, port forwarding tunnels, and agent management.',
    url: '/LinuxHandbook/article/linux-ssh-tutorial'
  },
  {
    title: 'Systemctl Cheatsheet',
    date: 'SEP 14, 2026',
    tag: 'SYSTEMD',
    description: 'Service unit operations, lifecycle controls, failed units inspection, and masked daemon overrides.',
    url: '/LinuxHandbook/article/linux-systemctl-tutorial'
  },
  {
    title: 'Journalctl Cheatsheet',
    date: 'SEP 13, 2026',
    tag: 'SYSTEMD',
    description: 'Binary system logs query syntax: boot-scoped filtering, priority levels, live tails, and kernel logs.',
    url: '/LinuxHandbook/article/linux-journalctl-tutorial'
  },
  {
    title: 'Grep Cheatsheet',
    date: 'SEP 12, 2026',
    tag: 'COREUTILS',
    description: 'Fast regex search syntax, recursive directory trees, line context flags, and PCRE expressions.',
    url: '/LinuxHandbook/article/linux-grep-tutorial'
  },
  {
    title: 'Awk Cheatsheet',
    date: 'SEP 11, 2026',
    tag: 'TEXT',
    description: 'Column delimiter parsing, field arithmetic, BEGIN/END patterns, and one-liner stream formatting.',
    url: '/LinuxHandbook/article/linux-awk-tutorial'
  },
  {
    title: 'Sed Cheatsheet',
    date: 'SEP 10, 2026',
    tag: 'TEXT',
    description: 'Stream search-and-replace, in-place file backups, regex delimiters, and line deletion commands.',
    url: '/LinuxHandbook/article/linux-sed-tutorial'
  },
  {
    title: 'Find Cheatsheet',
    date: 'SEP 9, 2026',
    tag: 'FINDUTILS',
    description: 'Find files by modification time, size, ownership, permissions, and batch processing with xargs.',
    url: '/LinuxHandbook/article/linux-find-tutorial'
  },
  {
    title: 'IP (iproute2) Cheatsheet',
    date: 'SEP 8, 2026',
    tag: 'NETWORKING',
    description: 'Interface state management, CIDR IP assignment, routing tables, and network namespace isolation.',
    url: '/LinuxHandbook/article/linux-ip-tutorial'
  },
  {
    title: 'SS (Sockets) Cheatsheet',
    date: 'SEP 7, 2026',
    tag: 'NETWORKING',
    description: 'Listening TCP/UDP ports, process associations, established connection states, and Netlink timers.',
    url: '/LinuxHandbook/article/linux-ss-tutorial'
  },
  {
    title: 'Rsync Cheatsheet',
    date: 'SEP 6, 2026',
    tag: 'TRANSFER',
    description: 'Delta synchronization, archive mode flags, delete synchronization, and SSH port specifications.',
    url: '/LinuxHandbook/article/linux-rsync-tutorial'
  },
  {
    title: 'Tar & Compression Cheatsheet',
    date: 'SEP 5, 2026',
    tag: 'ARCHIVE',
    description: 'Archive creation, gzip/xz stream compression, safe extraction, and preserving directory permissions.',
    url: '/LinuxHandbook/article/linux-tar-tutorial'
  },
  {
    title: 'Lsblk & Storage Cheatsheet',
    date: 'SEP 4, 2026',
    tag: 'STORAGE',
    description: 'Block device hierarchy, filesystem types, UUID discovery, mountpoints, and partition tables.',
    url: '/LinuxHandbook/article/linux-lsblk-tutorial'
  },
  {
    title: 'Fdisk Cheatsheet',
    date: 'SEP 3, 2026',
    tag: 'STORAGE',
    description: 'GPT/MBR disk partition tables, partition type codes, sector alignment, and non-destructive inspection.',
    url: '/LinuxHandbook/article/linux-fdisk-tutorial'
  },
  {
    title: 'Mount & Umount Cheatsheet',
    date: 'SEP 2, 2026',
    tag: 'STORAGE',
    description: 'Filesystem mounting flags (noexec, ro), loop devices, bind mounts, and safe lazy unmounting.',
    url: '/LinuxHandbook/article/linux-mount-tutorial'
  },
  {
    title: 'Ps & Process Triage Cheatsheet',
    date: 'SEP 1, 2026',
    tag: 'PROCPS',
    description: 'Process tree hierarchy, thread inspection, custom output columns, and CPU/memory sorting.',
    url: '/LinuxHandbook/article/linux-ps-tutorial'
  },
  {
    title: 'Kill & Signals Cheatsheet',
    date: 'AUG 30, 2026',
    tag: 'PROCPS',
    description: 'Standard Linux POSIX signals: SIGHUP (1), SIGINT (2), SIGKILL (9), SIGTERM (15), and safety rules.',
    url: '/LinuxHandbook/article/linux-kill-tutorial'
  },
  {
    title: 'Apt & Debian Cheatsheet',
    date: 'AUG 28, 2026',
    tag: 'PACKAGE',
    description: 'Package repository updates, version pinning, build dependencies, and autoremove orphan cleanup.',
    url: '/LinuxHandbook/article/linux-apt-tutorial'
  },
  {
    title: 'Dnf & RHEL Cheatsheet',
    date: 'AUG 26, 2026',
    tag: 'PACKAGE',
    description: 'RPM transaction history, rollback commands, repository enabling, and group software installations.',
    url: '/LinuxHandbook/article/linux-dnf-tutorial'
  }
]
</script>

<template>
  <div class="linuxize-page-container">
    <header class="cheatsheet-header">
      <h1 class="cheatsheet-title">Cheatsheets</h1>
      <p class="cheatsheet-subtitle">
        Cheatsheets are compact, copy-paste friendly references for common Linux commands and tools, so you can find syntax, options, and examples quickly.
      </p>
    </header>

    <!-- 3-Column Card Grid -->
    <section class="cheatsheet-grid">
      <CheatsheetCard
        v-for="(item, idx) in cheatsheets"
        :key="idx"
        v-bind="item"
      />
    </section>

    <!-- Pagination -->
    <Pagination :current-page="1" :pages="[1, 2, '...', 4]" />
  </div>
</template>

<style scoped>
.linuxize-page-container {
  max-width: 1100px;
  margin: 0 auto;
  padding: 2.5rem 1.5rem 4rem;
}

.cheatsheet-header {
  margin-bottom: 2.5rem;
}

.cheatsheet-title {
  font-size: 2.75rem;
  font-weight: 800;
  letter-spacing: -0.02em;
  color: #0f172a;
  margin: 0 0 0.75rem 0;
}

.cheatsheet-subtitle {
  font-size: 1.15rem;
  color: #475569;
  max-width: 800px;
  margin: 0;
  line-height: 1.6;
}

.cheatsheet-grid {
  display: grid;
  grid-template-columns: repeat(1, minmax(0, 1fr));
  gap: 1.25rem;
}

@media (min-width: 768px) {
  .cheatsheet-grid {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
}

.dark .cheatsheet-title {
  color: #f8fafc;
}

.dark .cheatsheet-subtitle {
  color: #94a3b8;
}
</style>
