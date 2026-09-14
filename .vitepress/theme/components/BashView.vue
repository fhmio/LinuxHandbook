<script setup>
import Breadcrumbs from './Breadcrumbs.vue'
import ArticleCard from './ArticleCard.vue'
import HorizontalArticleItem from './HorizontalArticleItem.vue'
import Pagination from './Pagination.vue'

const breadcrumbs = [
  { text: 'HOME', link: '/LinuxHandbook/' },
  { text: 'TAGS', link: '#' },
  { text: 'BASH' }
]

const featured = [
  {
    title: 'Bash For Loop: Syntax and Examples',
    date: 'SEP 9, 2026',
    readTime: '10 MIN READ',
    badge: 'SERIES',
    description: 'A complete guide to the Bash for loop: standard syntax, C-style loops, arrays, ranges, break and continue, and real-world scripting patterns.',
    url: '/LinuxHandbook/article/linux-jobs-tutorial',
    gradientClass: 'gradient-yellow',
    thumbText: 'for loop'
  },
  {
    title: 'Bash source Command: Load Scripts and Variables',
    date: 'SEP 5, 2026',
    readTime: '8 MIN READ',
    badge: 'SERIES',
    description: 'Use source (or its dot shorthand) to run a file in your current shell, reload .bashrc, share functions between scripts, and load environment variables.',
    url: '/LinuxHandbook/article/linux-cat-tutorial',
    gradientClass: 'gradient-teal',
    thumbText: 'source'
  },
  {
    title: 'What Is .bashrc? When It Runs and What to Put in It',
    date: 'AUG 31, 2026',
    readTime: '10 MIN READ',
    description: '~/.bashrc controls aliases, functions, prompts, and other interactive Bash settings. See when it runs, what belongs inside, and how to debug it.',
    url: '/LinuxHandbook/article/linux-touch-tutorial',
    gradientClass: 'gradient-purple',
    thumbText: '.bashrc'
  }
]

const articles = [
  {
    title: 'How to Create Bash Aliases',
    date: 'AUG 30, 2026',
    readTime: '7 MIN READ',
    badge: 'SERIES',
    description: 'Bash aliases let you shorten long commands into short, memorable shortcuts. This guide covers alias syntax, persistent aliases in .bashrc, and functions.',
    url: '/LinuxHandbook/article/linux-ls-tutorial',
    gradientClass: 'gradient-cyan',
    thumbText: 'alias'
  },
  {
    title: 'How to Add a Directory to PATH in Linux',
    date: 'AUG 28, 2026',
    readTime: '9 MIN READ',
    badge: 'SERIES',
    description: 'Add a directory to the PATH variable in Linux, temporarily or permanently, covering ~/.local/bin, custom binaries, and system-wide changes for all users.',
    url: '/LinuxHandbook/article/linux-w-tutorial',
    gradientClass: 'gradient-emerald',
    thumbText: 'export PATH'
  },
  {
    title: '.bashrc vs .bash_profile: What is the Difference?',
    date: 'AUG 28, 2026',
    readTime: '7 MIN READ',
    badge: 'SERIES',
    description: 'Understand the difference between .bashrc and .bash_profile, when each file is loaded, and where to put aliases, PATH changes, and environment variables.',
    url: '/LinuxHandbook/article/linux-useradd-tutorial',
    gradientClass: 'gradient-purple',
    thumbText: 'bash profiles'
  },
  {
    title: 'Bash Append to File: >>, tee, and Heredoc Examples',
    date: 'AUG 23, 2026',
    readTime: '8 MIN READ',
    badge: 'SERIES',
    description: 'Append text to a file in Bash without erasing existing content. Covers >>, echo, printf, tee -a for protected files, and combining multi-line heredocs.',
    url: '/LinuxHandbook/article/linux-cat-tutorial',
    gradientClass: 'gradient-amber',
    thumbText: '>> append'
  },
  {
    title: 'Bash Best Practices: Writing Safer, Cleaner Scripts',
    date: 'AUG 20, 2026',
    readTime: '9 MIN READ',
    badge: 'SERIES',
    description: 'Practical Bash best practices for writing safer and more predictable scripts, covering strict mode (set -euo pipefail), quoting, error handling, and everyday patterns.',
    url: '/LinuxHandbook/article/linux-jobs-tutorial',
    gradientClass: 'gradient-slate',
    thumbText: 'set -euo'
  },
  {
    title: 'How to Redirect stderr to stdout in Bash',
    date: 'AUG 19, 2026',
    readTime: '11 MIN READ',
    badge: 'SERIES',
    description: 'Redirecting stderr to stdout in Bash using 2>&1, &>, and other operators. Covers file descriptors, appending, piping errors, and discarding output with /dev/null.',
    url: '/LinuxHandbook/article/linux-grep-tutorial',
    gradientClass: 'gradient-purple',
    thumbText: '2>&1'
  },
  {
    title: 'echo Command in Linux: Print Text and Variables',
    date: 'AUG 16, 2026',
    readTime: '9 MIN READ',
    badge: 'SERIES',
    description: 'Print text, variables, script arguments, and exit codes with echo in Linux, plus escape sequences, colored output, and quoting pitfalls to avoid.',
    url: '/LinuxHandbook/article/linux-cat-tutorial',
    gradientClass: 'gradient-blue',
    thumbText: 'echo'
  },
  {
    title: 'Bash Shebang: What #!/bin/bash Means in Shell Scripts',
    date: 'AUG 14, 2026',
    readTime: '7 MIN READ',
    badge: 'SERIES',
    description: 'A Bash shebang tells Linux which interpreter runs a script. See what #!/bin/bash means, how /usr/bin/env bash differs, and what happens without #!.',
    url: '/LinuxHandbook/article/linux-touch-tutorial',
    gradientClass: 'gradient-teal',
    thumbText: '#!/bin/bash'
  },
  {
    title: 'Bash Positional Arguments: How to Use $1, $2, $@, and shift',
    date: 'JUL 28, 2026',
    readTime: '6 MIN READ',
    badge: 'SERIES',
    description: 'Learn how Bash positional arguments work, including $0, $1, $#, "$@", "$*", shift, default values, and function arguments in shell scripts.',
    url: '/LinuxHandbook/article/linux-xargs-tutorial',
    gradientClass: 'gradient-rose',
    thumbText: '$1 $2 $@'
  }
]
</script>

<template>
  <div class="linuxize-page-container">
    <Breadcrumbs :items="breadcrumbs" />

    <header class="category-header">
      <h1 class="category-title">Bash</h1>
      <p class="category-subtitle">
        Bash scripting, shell fundamentals, automation patterns, and common pitfalls.
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
