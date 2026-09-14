<script setup>
defineProps({
  currentPage: {
    type: Number,
    default: 1
  },
  totalPages: {
    type: Number,
    default: 5
  },
  pages: {
    type: Array,
    default: () => [1, 2, '...', 11]
  }
})

const emit = defineEmits(['page-change'])

function selectPage(p) {
  if (typeof p === 'number') {
    emit('page-change', p)
  }
}
</script>

<template>
  <div class="linuxize-pagination">
    <button
      v-for="(p, i) in pages"
      :key="i"
      class="page-btn"
      :class="{ active: p === currentPage, ellipsis: p === '...' }"
      :disabled="p === '...'"
      @click="selectPage(p)"
    >
      {{ p }}
    </button>
    <button class="page-btn next-btn" aria-label="Next page">
      &rarr;
    </button>
  </div>
</template>

<style scoped>
.linuxize-pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  margin: 3.5rem 0 2rem;
}

.page-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 38px;
  height: 38px;
  padding: 0 0.5rem;
  border-radius: 6px;
  font-size: 0.875rem;
  font-weight: 600;
  background: white;
  border: 1px solid #e5e7eb;
  color: #374151;
  cursor: pointer;
  transition: all 0.15s ease;
}

.page-btn:hover:not(:disabled):not(.active) {
  background: #f9fafb;
  border-color: #d1d5db;
  color: #111827;
}

.page-btn.active {
  background: #111827;
  color: #ffffff;
  border-color: #111827;
}

.page-btn.ellipsis {
  cursor: default;
  border: none;
  background: transparent;
  color: #9ca3af;
}

.next-btn {
  font-size: 1.1rem;
}

.dark .page-btn {
  background: #1e293b;
  border-color: #334155;
  color: #cbd5e1;
}

.dark .page-btn:hover:not(:disabled):not(.active) {
  background: #334155;
  color: #f8fafc;
}

.dark .page-btn.active {
  background: #f8fafc;
  color: #0f172a;
  border-color: #f8fafc;
}
</style>
