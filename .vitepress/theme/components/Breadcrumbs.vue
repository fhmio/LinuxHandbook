<script setup>
defineProps({
  items: {
    type: Array,
    required: true
    // e.g. [{ text: 'HOME', link: '/' }, { text: 'TAGS', link: '#' }, { text: 'LINUX COMMANDS' }]
  }
})
</script>

<template>
  <nav class="linuxize-breadcrumbs" aria-label="Breadcrumb">
    <template v-for="(item, idx) in items" :key="idx">
      <span v-if="idx > 0" class="breadcrumb-separator">/</span>
      <a v-if="item.link" :href="item.link" class="breadcrumb-link">{{ item.text }}</a>
      <span v-else class="breadcrumb-current">{{ item.text }}</span>
    </template>
  </nav>
</template>

<style scoped>
.linuxize-breadcrumbs {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 0.5rem;
  font-size: 0.75rem;
  font-weight: 600;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #6b7280;
  margin-bottom: 1.25rem;
}

.breadcrumb-link {
  color: #6b7280 !important;
  text-decoration: none !important;
  transition: color 0.15s;
}

.breadcrumb-link:hover {
  color: #111827 !important;
}

.breadcrumb-separator {
  color: #9ca3af;
  font-size: 0.7rem;
}

.breadcrumb-current {
  color: #111827;
  font-weight: 700;
}

.dark .breadcrumb-link {
  color: #94a3b8 !important;
}

.dark .breadcrumb-link:hover {
  color: #f1f5f9 !important;
}

.dark .breadcrumb-separator {
  color: #64748b;
}

.dark .breadcrumb-current {
  color: #f8fafc;
}
</style>
