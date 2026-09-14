<script setup>
import Breadcrumbs from './Breadcrumbs.vue'
import ArticleCard from './ArticleCard.vue'
import HorizontalArticleItem from './HorizontalArticleItem.vue'
import Pagination from './Pagination.vue'

const breadcrumbs = [
  { text: 'HOME', link: '/LinuxHandbook/' },
  { text: 'TAGS', link: '#' },
  { text: 'UBUNTU' }
]

const featured = [
  {
    title: 'Ubuntu Initial Server Setup & Security Hardening',
    date: 'SEP 12, 2026',
    readTime: '12 MIN READ',
    badge: 'SERIES',
    description: 'Essential configuration steps for a new Ubuntu server: root login restriction, sudo user creation, SSH key authentication, and firewall rules.',
    url: '/LinuxHandbook/article/linux-sudo-tutorial',
    gradientClass: 'gradient-rose',
    thumbText: 'ubuntu setup'
  },
  {
    title: 'APT Command Guide: Managing Packages on Ubuntu',
    date: 'SEP 10, 2026',
    readTime: '11 MIN READ',
    badge: 'SERIES',
    description: 'Master apt and apt-get on Ubuntu: update repositories, upgrade installed packages, search caches, clean orphans, and troubleshoot broken dependencies.',
    url: '/LinuxHandbook/article/linux-apt-tutorial',
    gradientClass: 'gradient-blue',
    thumbText: 'apt-get'
  },
  {
    title: 'How to Set Up a Firewall with UFW on Ubuntu',
    date: 'SEP 6, 2026',
    readTime: '8 MIN READ',
    description: 'Configure Uncomplicated Firewall (UFW) on Ubuntu servers. Allow SSH, HTTP/HTTPS ports, limit brute-force attempts, and check firewall status.',
    url: '/LinuxHandbook/article/linux-ss-tutorial',
    gradientClass: 'gradient-teal',
    thumbText: 'ufw'
  }
]

const articles = [
  {
    title: 'How to Manage System Services with systemctl on Ubuntu',
    date: 'SEP 4, 2026',
    readTime: '9 MIN READ',
    badge: 'SERIES',
    description: 'Control systemd daemons on Ubuntu: start, stop, restart, reload, enable at boot, and inspect service logs with journalctl.',
    url: '/LinuxHandbook/article/linux-systemctl-tutorial',
    gradientClass: 'gradient-purple',
    thumbText: 'systemctl'
  },
  {
    title: 'How to Create and Manage Sudo Users in Ubuntu',
    date: 'SEP 1, 2026',
    readTime: '7 MIN READ',
    description: 'Add new administrative accounts, configure passwordless sudo, grant temporary privileges, and edit /etc/sudoers safely with visudo.',
    url: '/LinuxHandbook/article/linux-useradd-tutorial',
    gradientClass: 'gradient-amber',
    thumbText: 'sudo usermod'
  },
  {
    title: 'Modern Ubuntu Networking: IPRoute2 and Interfaces',
    date: 'AUG 27, 2026',
    readTime: '10 MIN READ',
    badge: 'SERIES',
    description: 'Inspect interfaces, configure static IP addresses, inspect routing tables, and test socket connections using the modern ip command suite.',
    url: '/LinuxHandbook/article/linux-ip-tutorial',
    gradientClass: 'gradient-emerald',
    thumbText: 'ip addr'
  },
  {
    title: 'Disk Space Management on Ubuntu: Lsblk, Mount, and Fdisk',
    date: 'AUG 24, 2026',
    readTime: '13 MIN READ',
    badge: 'SERIES',
    description: 'Inspect NVMe and SATA block devices, partition new storage volumes with fdisk, format with ext4, and mount persistently via /etc/fstab.',
    url: '/LinuxHandbook/article/linux-lsblk-tutorial',
    gradientClass: 'gradient-cyan',
    thumbText: 'lsblk'
  },
  {
    title: 'Troubleshooting Memory and High Load on Ubuntu',
    date: 'AUG 20, 2026',
    readTime: '12 MIN READ',
    badge: 'NEW',
    description: 'Diagnose out-of-memory errors, check swap usage with free and vmstat, inspect high-load processes with top and ps, and optimize server runtime.',
    url: '/LinuxHandbook/article/linux-free-tutorial',
    gradientClass: 'gradient-yellow',
    thumbText: 'free -m'
  }
]
</script>

<template>
  <div class="linuxize-page-container">
    <Breadcrumbs :items="breadcrumbs" />

    <header class="category-header">
      <h1 class="category-title">Ubuntu</h1>
      <p class="category-subtitle">
        Ubuntu server administration, configuration guides, APT package management, and system optimization.
      </p>
    </header>

    <section class="featured-cards-grid">
      <ArticleCard
        v-for="(item, idx) in featured"
        :key="idx"
        v-bind="item"
      />
    </section>

    <section class="articles-list-section">
      <HorizontalArticleItem
        v-for="(article, idx) in articles"
        :key="idx"
        v-bind="article"
      />
    </section>

    <Pagination :current-page="1" :pages="[1, 2, 3]" />
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
