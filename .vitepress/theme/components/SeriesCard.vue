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
  articleCount: {
    type: [Number, String],
    required: true
  },
  description: {
    type: String,
    default: ''
  },
  url: {
    type: String,
    required: true
  },
  gradientClass: {
    type: String,
    default: 'gradient-teal'
  },
  horizontal: {
    type: Boolean,
    default: false
  }
})
</script>

<template>
  <!-- Horizontal View -->
  <article v-if="horizontal" class="series-horizontal-item">
    <div class="series-info">
      <div class="series-meta">
        <span class="series-date">🕒 {{ date }}</span>
        <span class="meta-dot">•</span>
        <span class="series-count">{{ articleCount }} ARTICLES</span>
      </div>
      <h2 class="series-title">
        <a :href="url">{{ title }}</a>
      </h2>
      <p v-if="description" class="series-desc">{{ description }}</p>
    </div>

    <a :href="url" class="series-thumb" :class="gradientClass" :aria-label="title">
      <div class="series-thumb-content">
        <span class="series-badge-icon">📚</span>
        <span class="series-thumb-title">{{ title }}</span>
      </div>
    </a>
  </article>

  <!-- Card Grid View -->
  <a v-else :href="url" class="series-card">
    <div class="series-image" :class="gradientClass">
      <div class="series-illustration">
        <span class="series-illustration-icon">📁</span>
        <span class="series-illustration-title">{{ title }}</span>
      </div>
    </div>
    <div class="series-content">
      <div class="series-meta">
        <span class="series-date">🕒 {{ date }}</span>
        <span class="meta-dot">•</span>
        <span class="series-count">{{ articleCount }} ARTICLES</span>
      </div>
      <h3 class="series-card-title">{{ title }}</h3>
      <p v-if="description" class="series-card-desc">{{ description }}</p>
    </div>
  </a>
</template>

<style scoped>
/* Card Grid Style */
.series-card {
  display: flex;
  flex-direction: column;
  background: white;
  border-radius: 12px;
  overflow: hidden;
  border: 1px solid #f1f5f9;
  box-shadow: 0 1px 3px rgba(0,0,0,0.04);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  text-decoration: none !important;
  color: inherit !important;
  height: 100%;
}

.series-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 16px rgba(0,0,0,0.08);
}

.series-image {
  height: 160px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1.5rem;
}

.series-illustration {
  background: rgba(15, 23, 42, 0.85);
  border-radius: 8px;
  padding: 12px 16px;
  display: flex;
  align-items: center;
  gap: 8px;
  box-shadow: 0 4px 10px rgba(0,0,0,0.15);
  max-width: 90%;
}

.series-illustration-icon {
  font-size: 1.25rem;
}

.series-illustration-title {
  font-size: 0.8rem;
  font-weight: 700;
  color: #f8fafc;
  letter-spacing: 0.04em;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.series-content {
  padding: 1.25rem 1.5rem 1.5rem;
  display: flex;
  flex-direction: column;
  flex: 1;
}

.series-card-title {
  font-size: 1.15rem;
  font-weight: 700;
  line-height: 1.35;
  margin: 0 0 0.5rem 0;
  color: #111827;
}

.series-card-desc {
  font-size: 0.875rem;
  color: #4b5563;
  line-height: 1.5;
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Horizontal Style */
.series-horizontal-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 2rem;
  padding: 1.75rem 0;
  border-bottom: 1px solid #f1f5f9;
}

.series-horizontal-item:last-child {
  border-bottom: none;
}

.series-info {
  flex: 1;
  min-width: 0;
}

.series-meta {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  font-size: 0.725rem;
  color: #6b7280;
  margin-bottom: 0.6rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  font-weight: 600;
}

.meta-dot {
  color: #cbd5e1;
}

.series-count {
  color: #2563eb;
  font-weight: 700;
}

.series-title {
  font-size: 1.25rem;
  font-weight: 700;
  line-height: 1.4;
  margin: 0 0 0.5rem 0;
  color: #111827;
}

.series-title a {
  color: inherit !important;
  text-decoration: none !important;
  transition: color 0.15s ease;
}

.series-title a:hover {
  color: #2563eb !important;
}

.series-desc {
  font-size: 0.925rem;
  color: #4b5563;
  line-height: 1.5;
  margin: 0;
}

.series-thumb {
  width: 175px;
  height: 105px;
  border-radius: 10px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  text-decoration: none !important;
  box-shadow: 0 2px 5px rgba(0,0,0,0.06);
  transition: transform 0.2s ease;
  padding: 12px;
}

.series-thumb:hover {
  transform: scale(1.03);
}

.series-thumb-content {
  background: rgba(15, 23, 42, 0.85);
  border-radius: 6px;
  padding: 8px 10px;
  display: flex;
  align-items: center;
  gap: 6px;
  max-width: 100%;
}

.series-badge-icon {
  font-size: 1rem;
}

.series-thumb-title {
  font-size: 0.75rem;
  font-weight: 700;
  color: #f8fafc;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* Gradients */
.gradient-teal { background: linear-gradient(135deg, #99f6e4 0%, #2dd4bf 100%); }
.gradient-purple { background: linear-gradient(135deg, #e9d5ff 0%, #a855f7 100%); }
.gradient-blue { background: linear-gradient(135deg, #dbeafe 0%, #3b82f6 100%); }
.gradient-indigo { background: linear-gradient(135deg, #e0e7ff 0%, #6366f1 100%); }
.gradient-amber { background: linear-gradient(135deg, #fef3c7 0%, #f59e0b 100%); }
.gradient-rose { background: linear-gradient(135deg, #ffe4e6 0%, #f43f5e 100%); }
.gradient-emerald { background: linear-gradient(135deg, #d1fae5 0%, #10b981 100%); }

/* Dark mode */
.dark .series-card {
  background: #1e293b;
  border-color: #334155;
}

.dark .series-horizontal-item {
  border-bottom-color: #1e293b;
}

.dark .series-card-title,
.dark .series-title {
  color: #f1f5f9;
}

.dark .series-card-desc,
.dark .series-desc {
  color: #94a3b8;
}

.dark .series-meta {
  color: #94a3b8;
}

.dark .series-count {
  color: #60a5fa;
}

@media (max-width: 640px) {
  .series-horizontal-item {
    flex-direction: column-reverse;
    align-items: flex-start;
    gap: 1rem;
  }
  .series-thumb {
    width: 100%;
    height: 110px;
  }
}
</style>
