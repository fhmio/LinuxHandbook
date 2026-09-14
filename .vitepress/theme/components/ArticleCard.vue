<script setup>
defineProps({
  title: String,
  date: String,
  url: String,
  gradientClass: {
    type: String,
    default: 'gradient-1'
  }
})
</script>

<template>
  <a :href="url" class="article-card">
    <div class="card-image" :class="gradientClass">
      <span class="card-icon">💻</span>
    </div>
    <div class="card-content">
      <div class="card-meta">
        <span class="card-date">🕒 {{ date }}</span>
      </div>
      <h3 class="card-title">{{ title }}</h3>
    </div>
  </a>
</template>

<style scoped>
.article-card {
  display: flex;
  flex-direction: column;
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  transition: transform 0.2s, box-shadow 0.2s;
  text-decoration: none !important;
  color: inherit !important;
}

.article-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

.dark .article-card {
  background: #1e293b;
  box-shadow: 0 1px 3px rgba(0,0,0,0.3);
}

.card-image {
  height: 160px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.card-icon {
  font-size: 3rem;
}

.gradient-1 { background: linear-gradient(135deg, #a8c0ff 0%, #3f2b96 100%); }
.gradient-2 { background: linear-gradient(135deg, #fbc2eb 0%, #a6c1ee 100%); }
.gradient-3 { background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%); }
.gradient-4 { background: linear-gradient(135deg, #fccb90 0%, #d57eeb 100%); }
.gradient-5 { background: linear-gradient(135deg, #e0c3fc 0%, #8ec5fc 100%); }
.gradient-6 { background: linear-gradient(135deg, #f6d365 0%, #fda085 100%); }

.card-content {
  padding: 1.5rem;
}

.card-meta {
  font-size: 0.75rem;
  color: #6b7280;
  margin-bottom: 0.5rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.dark .card-meta {
  color: #94a3b8;
}

.card-title {
  font-size: 1.125rem;
  font-weight: 600;
  line-height: 1.4;
  margin: 0;
  color: #111827;
}

.dark .card-title {
  color: #f3f4f6;
}
</style>
