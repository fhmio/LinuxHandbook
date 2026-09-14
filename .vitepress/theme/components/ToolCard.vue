<script setup>
defineProps({
  title: {
    type: String,
    required: true
  },
  description: {
    type: String,
    required: true
  },
  url: {
    type: String,
    default: '#'
  },
  icon: {
    type: String,
    default: 'wrench'
  }
})

const emit = defineEmits(['click'])
</script>

<template>
  <div class="tool-card" @click="emit('click')">
    <div class="tool-icon-wrapper">
      <svg v-if="icon === 'wrench'" class="tool-svg" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 4a2 2 0 114 0v1a1 1 0 001 1h3a1 1 0 011 1v3a1 1 0 01-1 1h-1a2 2 0 100 4h1a1 1 0 011 1v3a1 1 0 01-1 1h-3a1 1 0 01-1-1v-1a2 2 0 10-4 0v1a1 1 0 01-1 1H7a1 1 0 01-1-1v-3a1 1 0 00-1-1H4a2 2 0 110-4h1a1 1 0 001-1V7a1 1 0 011-1h3a1 1 0 001-1V4z" />
      </svg>
      <svg v-else-if="icon === 'terminal'" class="tool-svg" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 9l3 3-3 3m5 0h3M5 20h14a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
      </svg>
      <svg v-else class="tool-svg" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
      </svg>
    </div>
    <div class="tool-content">
      <h3 class="tool-title">{{ title }}</h3>
      <p class="tool-desc">{{ description }}</p>
    </div>
  </div>
</template>

<style scoped>
.tool-card {
  background: #f8fafc;
  border: 1px solid #f1f5f9;
  border-radius: 12px;
  padding: 1.75rem;
  display: flex;
  gap: 1.25rem;
  align-items: flex-start;
  transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease, background-color 0.2s ease;
  cursor: pointer;
}

.tool-card:hover {
  transform: translateY(-2px);
  background: #ffffff;
  border-color: #cbd5e1;
  box-shadow: 0 6px 16px rgba(0,0,0,0.06);
}

.tool-icon-wrapper {
  width: 44px;
  height: 44px;
  border-radius: 10px;
  background: #eff6ff;
  color: #2563eb;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  border: 1px solid #dbeafe;
}

.tool-svg {
  width: 22px;
  height: 22px;
}

.tool-content {
  flex: 1;
}

.tool-title {
  font-size: 1.125rem;
  font-weight: 700;
  color: #0f172a;
  margin: 0 0 0.5rem 0;
  line-height: 1.35;
}

.tool-desc {
  font-size: 0.875rem;
  color: #475569;
  line-height: 1.55;
  margin: 0;
}

/* Dark mode */
.dark .tool-card {
  background: #1e293b;
  border-color: #334155;
}

.dark .tool-card:hover {
  background: #1e293b;
  border-color: #64748b;
  box-shadow: 0 6px 16px rgba(0,0,0,0.3);
}

.dark .tool-icon-wrapper {
  background: rgba(37, 99, 235, 0.2);
  color: #60a5fa;
  border-color: rgba(37, 99, 235, 0.3);
}

.dark .tool-title {
  color: #f8fafc;
}

.dark .tool-desc {
  color: #94a3b8;
}
</style>
