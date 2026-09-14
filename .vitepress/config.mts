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
      { text: 'Start Here', link: '/' },
      { text: 'Linux Commands', link: '/linux-commands' },
      { text: 'Bash', link: '/bash' },
      { text: 'Ubuntu', link: '/ubuntu' },
      { text: 'Series', link: '/series' },
      { text: 'Cheatsheets', link: '/cheatsheets' },
      { text: 'Tools', link: '/tools' },
      { text: 'About', link: '/about' }
    ],
    sidebar: false,
    socialLinks: [
      { icon: 'github', link: 'https://github.com/fhmio/LinuxHandbook' }
    ],
    footer: {
      message: 'Released under the MIT License.',
      copyright: 'Copyright © 2026 LinuxHandbook Contributors'
    }
  }
})
