<script setup>
defineProps({
  title: String,
  date: String,
  description: String,
  url: String
})
</script>

<template>
  <a :href="url" class="cheatsheet-card">
    <div class="card-meta">
      <span class="card-date">🕒 {{ date }}</span>
    </div>
    <h3 class="card-title">{{ title }}</h3>
    <p class="card-desc">{{ description }}</p>
  </a>
</template>

<style scoped>
.cheatsheet-card {
  display: block;
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 1px 2px rgba(0,0,0,0.05);
  transition: transform 0.2s, box-shadow 0.2s;
  text-decoration: none !important;
  color: inherit !important;
  border: 1px solid #f3f4f6;
}

.cheatsheet-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 6px rgba(0,0,0,0.05);
  border-color: #e5e7eb;
}

.dark .cheatsheet-card {
  background: #1e293b;
  border-color: #334155;
  box-shadow: none;
}

.dark .cheatsheet-card:hover {
  border-color: #475569;
}

.card-meta {
  font-size: 0.75rem;
  color: #9ca3af;
  margin-bottom: 0.5rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.card-title {
  font-size: 1.125rem;
  font-weight: 600;
  line-height: 1.4;
  margin: 0 0 0.5rem 0;
  color: #111827;
}

.dark .card-title {
  color: #f3f4f6;
}

.card-desc {
  font-size: 0.875rem;
  color: #6b7280;
  margin: 0;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.dark .card-desc {
  color: #94a3b8;
}
</style>
