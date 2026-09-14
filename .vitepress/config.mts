import { defineConfig } from 'vitepress'

export default defineConfig({
  title: 'LinuxHandbook',
  description: 'The Authoritative Linux Reference & Operational Systems Playbook',
  base: '/LinuxHandbook/',
  cleanUrls: true,
  lastUpdated: true,
  themeConfig: {
    logo: { text: '🐧 LinuxHandbook' },
    siteTitle: 'LinuxHandbook',
    search: {
      provider: 'local',
      options: {
        detailedView: true
      }
    },
    nav: [
      { text: 'Home', link: '/' },
      { text: 'Command Catalog', link: '/#upstream-command-catalog' },
      { text: 'Playbooks', link: '/#operational-playbooks' },
      {
        text: 'Suites',
        items: [
          { text: 'GNU Coreutils', link: '/article/linux-ls-tutorial' },
          { text: 'Text Processing', link: '/article/linux-grep-tutorial' },
          { text: 'procps-ng (Process)', link: '/article/linux-ps-tutorial' },
          { text: 'util-linux (Storage)', link: '/article/linux-mount-tutorial' },
          { text: 'iproute2 (Network)', link: '/article/linux-ip-tutorial' },
          { text: 'OpenSSH Suite', link: '/article/linux-ssh-tutorial' },
          { text: 'Transfer & Archives', link: '/article/linux-curl-tutorial' },
          { text: 'systemd Services', link: '/article/linux-systemctl-tutorial' },
          { text: 'Package Management', link: '/article/linux-apt-tutorial' },
          { text: 'User & Group Management', link: '/article/linux-su-tutorial' },
          { text: 'Process & Job Control', link: '/article/linux-kill-tutorial' }
        ]
      }
    ],
    sidebar: [
      {
        text: '📁 Core File Operations (Coreutils)',
        collapsed: false,
        items: [
          { text: 'ls — Directory Listing', link: '/article/linux-ls-tutorial' },
          { text: 'cp — Copy Files & Trees', link: '/article/linux-cp-tutorial' },
          { text: 'mv — Move & Rename', link: '/article/linux-mv-tutorial' },
          { text: 'rm — Unlink & Remove', link: '/article/linux-rm-tutorial' },
          { text: 'mkdir — Create Directories', link: '/article/linux-mkdir-tutorial' },
          { text: 'rmdir — Remove Empty Directories', link: '/article/linux-rmdir-tutorial' },
          { text: 'touch — Update Timestamps', link: '/article/linux-touch-tutorial' },
          { text: 'ln — Hard & Symbolic Links', link: '/article/linux-ln-tutorial' }
        ]
      },
      {
        text: '📝 Text & Stream Processing',
        collapsed: false,
        items: [
          { text: 'cat — Stream & Concatenate', link: '/article/linux-cat-tutorial' },
          { text: 'head — Output File Beginning', link: '/article/linux-head-tutorial' },
          { text: 'tail — Output File End & Follow', link: '/article/linux-tail-tutorial' },
          { text: 'grep — Regular Expression Match', link: '/article/linux-grep-tutorial' },
          { text: 'sed — Stream Editor', link: '/article/linux-sed-tutorial' },
          { text: 'awk — Pattern Scanning & Processing', link: '/article/linux-awk-tutorial' },
          { text: 'sort — Sort Lines of Text', link: '/article/linux-sort-tutorial' },
          { text: 'uniq — Report / Filter Repeated Lines', link: '/article/linux-uniq-tutorial' },
          { text: 'cut — Extract Fields & Columns', link: '/article/linux-cut-tutorial' },
          { text: 'tr — Translate & Squeeze Characters', link: '/article/linux-tr-tutorial' }
        ]
      },
      {
        text: '🔎 Find & Batch Execution (Findutils)',
        collapsed: false,
        items: [
          { text: 'find — Real-Time Filesystem Search', link: '/article/linux-find-tutorial' },
          { text: 'xargs — Build & Execute Arguments', link: '/article/linux-xargs-tutorial' },
          { text: 'locate — Fast Database Index Search', link: '/article/linux-locate-tutorial' }
        ]
      },
      {
        text: '⚡ Process & System Triage (procps-ng)',
        collapsed: false,
        items: [
          { text: 'ps — Process Snapshot & Hierarchy', link: '/article/linux-ps-tutorial' },
          { text: 'top — Dynamic Real-Time Resource Monitor', link: '/article/linux-top-tutorial' },
          { text: 'free — Memory & Swap Utilization', link: '/article/linux-free-tutorial' },
          { text: 'vmstat — Virtual Memory Statistics', link: '/article/linux-vmstat-tutorial' },
          { text: 'pgrep — Process Lookup by Attribute', link: '/article/linux-pgrep-tutorial' },
          { text: 'pkill — Signal Process Groups', link: '/article/linux-pkill-tutorial' },
          { text: 'w — Logged-in Users & Activity', link: '/article/linux-w-tutorial' },
          { text: 'uptime — System Runtime & Load Averages', link: '/article/linux-uptime-tutorial' }
        ]
      },
      {
        text: '⚙️ Process & Job Control',
        collapsed: false,
        items: [
          { text: 'kill — Signal Processes', link: '/article/linux-kill-tutorial' },
          { text: 'killall — Signal by Name', link: '/article/linux-killall-tutorial' },
          { text: 'jobs — Shell Job Control', link: '/article/linux-jobs-tutorial' }
        ]
      },
      {
        text: '💾 Storage & Partitions (util-linux)',
        collapsed: false,
        items: [
          { text: 'mount — Attach Filesystems', link: '/article/linux-mount-tutorial' },
          { text: 'umount — Detach Filesystems', link: '/article/linux-umount-tutorial' },
          { text: 'findmnt — Mount Hierarchy Inspection', link: '/article/linux-findmnt-tutorial' },
          { text: 'lsblk — Block Device Tree Topology', link: '/article/linux-lsblk-tutorial' },
          { text: 'fdisk — GPT/MBR Partition Manager', link: '/article/linux-fdisk-tutorial' },
          { text: 'blkid — Block Device Superblock & UUIDs', link: '/article/linux-blkid-tutorial' }
        ]
      },
      {
        text: '🌐 Networking Suite (iproute2)',
        collapsed: false,
        items: [
          { text: 'ip — Interface, Routing & Namespaces', link: '/article/linux-ip-tutorial' },
          { text: 'ss — Netlink Socket Statistics', link: '/article/linux-ss-tutorial' },
          { text: 'tc — Traffic Control & Queuing', link: '/article/linux-tc-tutorial' },
          { text: 'bridge — Ethernet Bridge & Forwarding', link: '/article/linux-bridge-tutorial' }
        ]
      },
      {
        text: '🔑 Remote Access & Keys (OpenSSH)',
        collapsed: false,
        items: [
          { text: 'ssh — Secure Shell Remote Client', link: '/article/linux-ssh-tutorial' },
          { text: 'sftp — Interactive Secure File Transfer', link: '/article/linux-sftp-tutorial' },
          { text: 'scp — Secure Remote Copy', link: '/article/linux-scp-tutorial' },
          { text: 'ssh-keygen — Key Generation & Fingerprinting', link: '/article/linux-ssh-keygen-tutorial' },
          { text: 'ssh-agent — Authentication Agent Daemon', link: '/article/linux-ssh-agent-tutorial' },
          { text: 'ssh-add — Private Key Registration', link: '/article/linux-ssh-add-tutorial' },
          { text: 'ssh-keyscan — Host Key Discovery', link: '/article/linux-ssh-keyscan-tutorial' }
        ]
      },
      {
        text: '👥 User & Group Management',
        collapsed: false,
        items: [
          { text: 'su — Substitute User', link: '/article/linux-su-tutorial' },
          { text: 'sudo — Superuser Do', link: '/article/linux-sudo-tutorial' },
          { text: 'useradd — Create New Users', link: '/article/linux-useradd-tutorial' },
          { text: 'usermod — Modify Users', link: '/article/linux-usermod-tutorial' },
          { text: 'passwd — Update Passwords', link: '/article/linux-passwd-tutorial' }
        ]
      },
      {
        text: '📦 Package Management',
        collapsed: false,
        items: [
          { text: 'apt — Debian Package Manager', link: '/article/linux-apt-tutorial' },
          { text: 'yum — RPM Package Manager (Legacy)', link: '/article/linux-yum-tutorial' },
          { text: 'dnf — Dandified YUM', link: '/article/linux-dnf-tutorial' }
        ]
      },
      {
        text: '📦 Transfer & Compression',
        collapsed: false,
        items: [
          { text: 'curl — HTTP/HTTPS Transfer Client', link: '/article/linux-curl-tutorial' },
          { text: 'rsync — Delta File Synchronization', link: '/article/linux-rsync-tutorial' },
          { text: 'tar — Archiving & Compression Streams', link: '/article/linux-tar-tutorial' },
          { text: 'gzip — DEFLATE Stream Compression', link: '/article/linux-gzip-tutorial' },
          { text: 'xz — High-Ratio LZMA2 Compression', link: '/article/linux-xz-tutorial' }
        ]
      },
      {
        text: '⚙️ Service Lifecycle (systemd)',
        collapsed: false,
        items: [
          { text: 'systemctl — Service & Unit Manager', link: '/article/linux-systemctl-tutorial' },
          { text: 'journalctl — Query Systemd Binary Journal', link: '/article/linux-journalctl-tutorial' }
        ]
      }
    ],
    socialLinks: [
      { icon: 'github', link: 'https://github.com/fhmio/LinuxHandbook' }
    ],
    footer: {
      message: 'Released under the MIT License.',
      copyright: 'Copyright © 2026 LinuxHandbook Contributors'
    }
  }
})
