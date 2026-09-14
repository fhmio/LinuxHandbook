<script setup>
defineProps({
  title: {
    type: String,
    required: true
  },
  date: {
    type: String,
    required: true
  },
  description: {
    type: String,
    required: true
  },
  url: {
    type: String,
    required: true
  },
  tag: {
    type: String,
    default: ''
  }
})
</script>

<template>
  <a :href="url" class="cheatsheet-card">
    <div class="card-meta">
      <span class="card-date">🕒 {{ date }}</span>
      <span v-if="tag" class="card-tag">{{ tag }}</span>
    </div>
    <h3 class="card-title">{{ title }}</h3>
    <p class="card-desc">{{ description }}</p>
  </a>
</template>

<style scoped>
.cheatsheet-card {
  display: block;
  background: white;
  border-radius: 10px;
  padding: 1.5rem;
  border: 1px solid #f1f5f9;
  box-shadow: 0 1px 3px rgba(0,0,0,0.04);
  transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
  text-decoration: none !important;
  color: inherit !important;
  height: 100%;
}

.cheatsheet-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 14px rgba(0,0,0,0.06);
  border-color: #cbd5e1;
}

.card-meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 0.725rem;
  color: #6b7280;
  margin-bottom: 0.5rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  font-weight: 600;
}

.card-tag {
  background: #f1f5f9;
  color: #475569;
  padding: 1px 6px;
  border-radius: 4px;
  font-size: 0.65rem;
  font-weight: 700;
}

.card-title {
  font-size: 1.15rem;
  font-weight: 700;
  line-height: 1.35;
  margin: 0 0 0.5rem 0;
  color: #0f172a;
}

.card-desc {
  font-size: 0.875rem;
  color: #475569;
  margin: 0;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Dark mode */
.dark .cheatsheet-card {
  background: #1e293b;
  border-color: #334155;
  box-shadow: 0 1px 3px rgba(0,0,0,0.3);
}

.dark .cheatsheet-card:hover {
  border-color: #475569;
  box-shadow: 0 6px 14px rgba(0,0,0,0.4);
}

.dark .card-meta {
  color: #94a3b8;
}

.dark .card-tag {
  background: #334155;
  color: #cbd5e1;
}

.dark .card-title {
  color: #f8fafc;
}

.dark .card-desc {
  color: #94a3b8;
}
</style>
