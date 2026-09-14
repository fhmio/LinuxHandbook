<script setup>
import { useData } from 'vitepress'
const { frontmatter, page } = useData()

// We can extract date from frontmatter or page update time.
// For now, we will use a static placeholder if not available.
const date = 'SEP 14, 2026'
const author = 'Linuxize'
</script>

<template>
  <div v-if="frontmatter.layout !== 'custom-home'" class="article-meta">
    <div class="meta-author-date">
      <span class="meta-icon">👤</span> By <span class="meta-author">{{ author }}</span> 
      <span class="meta-separator">•</span> 
      <span class="meta-date">🕒 {{ date }}</span>
    </div>
  </div>
</template>

<style scoped>
.article-meta {
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #e5e7eb;
}

.dark .article-meta {
  border-bottom-color: #334155;
}

.meta-author-date {
  display: flex;
  align-items: center;
  font-size: 0.875rem;
  color: #6b7280;
}

.dark .meta-author-date {
  color: #94a3b8;
}

.meta-author {
  font-weight: 600;
  color: #111827;
  margin-left: 0.25rem;
}

.dark .meta-author {
  color: #f3f4f6;
}

.meta-separator {
  margin: 0 0.75rem;
  color: #d1d5db;
}

.dark .meta-separator {
  color: #475569;
}
</style>
