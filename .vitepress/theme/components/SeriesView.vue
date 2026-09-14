<script setup>
import SeriesCard from './SeriesCard.vue'

const featuredSeries = [
  {
    title: 'Linux Storage Fundamentals',
    date: 'AUG 15, 2026',
    articleCount: 13,
    description: 'From block devices to filesystems, swap, and recovery. This series covers lsblk, df, du, fdisk, blkid, mount, and persistent storage management.',
    url: '/LinuxHandbook/article/linux-lsblk-tutorial',
    gradientClass: 'gradient-teal'
  },
  {
    title: 'Bash Scripting Fundamentals',
    date: 'JUL 1, 2026',
    articleCount: 50,
    description: 'Learn Bash scripting from the ground up. This series covers everything from basic syntax, loops, and conditions to advanced functions and error trapping.',
    url: '/LinuxHandbook/bash',
    gradientClass: 'gradient-purple'
  },
  {
    title: 'Modern Linux Networking Suite',
    date: 'MAY 8, 2026',
    articleCount: 14,
    description: 'Master enterprise networking with iproute2, Netlink sockets, bridge devices, and traffic control QoS policies using ip, ss, bridge, and tc.',
    url: '/LinuxHandbook/article/linux-ip-tutorial',
    gradientClass: 'gradient-blue'
  }
]

const listSeries = [
  {
    title: 'Linux Users and Permissions',
    date: 'FEB 3, 2026',
    articleCount: 20,
    description: 'Learn how to manage Linux users, groups, and file permissions. This series covers useradd, usermod, passwd, su, sudo, chmod, chown, and umask.',
    url: '/LinuxHandbook/article/linux-useradd-tutorial',
    gradientClass: 'gradient-purple',
    horizontal: true
  },
  {
    title: 'SSH Essentials & Key Infrastructure',
    date: 'JAN 30, 2026',
    articleCount: 28,
    description: 'Learn how to use SSH to securely connect to remote servers, transfer files with scp/sftp, set up key-based authentication, and manage ssh-agent daemons.',
    url: '/LinuxHandbook/article/linux-ssh-tutorial',
    gradientClass: 'gradient-amber',
    horizontal: true
  },
  {
    title: 'Systemd Services, Daemons, and Journal Logging',
    date: 'JUL 28, 2026',
    articleCount: 15,
    description: 'Master service lifecycle management, custom unit file design, automatic restarts, dependencies, and binary journal triage with systemctl and journalctl.',
    url: '/LinuxHandbook/article/linux-systemctl-tutorial',
    gradientClass: 'gradient-indigo',
    horizontal: true
  },
  {
    title: 'GNU Stream Editing and Text Wrangling (Awk & Sed)',
    date: 'APR 15, 2026',
    articleCount: 18,
    description: 'Automate data extraction, text parsing, log analysis, and formatting with the power of awk, sed, grep, cut, sort, and regular expressions.',
    url: '/LinuxHandbook/article/linux-awk-tutorial',
    gradientClass: 'gradient-rose',
    horizontal: true
  },
  {
    title: 'Linux Package Management Across Distributions',
    date: 'MAR 6, 2026',
    articleCount: 10,
    description: 'Manage packages, repositories, and dependencies consistently across Debian/Ubuntu (APT), Fedora/RHEL (DNF & YUM), and open-source distributions.',
    url: '/LinuxHandbook/article/linux-apt-tutorial',
    gradientClass: 'gradient-teal',
    horizontal: true
  },
  {
    title: 'High-Load Process Control and Incident Response',
    date: 'MAR 1, 2026',
    articleCount: 12,
    description: 'Diagnose runaway threads, identify zombie processes, investigate memory leaks, and signal processes safely with ps, top, kill, killall, pgrep, and pkill.',
    url: '/LinuxHandbook/article/linux-kill-tutorial',
    gradientClass: 'gradient-slate',
    horizontal: true
  }
]
</script>

<template>
  <div class="linuxize-page-container">
    <header class="series-page-header">
      <h1 class="series-page-title">Series</h1>
      <p class="series-page-subtitle">
        Collections of related guides and tutorials so you can follow a topic from start to finish.
      </p>
    </header>

    <!-- Top Featured 3 Series Cards -->
    <section class="featured-series-grid">
      <SeriesCard
        v-for="(s, idx) in featuredSeries"
        :key="idx"
        v-bind="s"
      />
    </section>

    <!-- Horizontal Series List -->
    <section class="series-list-section">
      <SeriesCard
        v-for="(s, idx) in listSeries"
        :key="idx"
        v-bind="s"
      />
    </section>
  </div>
</template>

<style scoped>
.linuxize-page-container {
  max-width: 1100px;
  margin: 0 auto;
  padding: 2.5rem 1.5rem 4rem;
}

.series-page-header {
  margin-bottom: 2.5rem;
}

.series-page-title {
  font-size: 2.75rem;
  font-weight: 800;
  letter-spacing: -0.02em;
  color: #0f172a;
  margin: 0 0 0.75rem 0;
}

.series-page-subtitle {
  font-size: 1.15rem;
  color: #475569;
  max-width: 800px;
  margin: 0;
  line-height: 1.6;
}

.featured-series-grid {
  display: grid;
  grid-template-columns: repeat(1, minmax(0, 1fr));
  gap: 1.5rem;
  margin-bottom: 3.5rem;
}

@media (min-width: 768px) {
  .featured-series-grid {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
}

.series-list-section {
  border-top: 1px solid #f1f5f9;
  padding-top: 1rem;
}

.dark .series-page-title {
  color: #f8fafc;
}

.dark .series-page-subtitle {
  color: #94a3b8;
}

.dark .series-list-section {
  border-top-color: #1e293b;
}
</style>
