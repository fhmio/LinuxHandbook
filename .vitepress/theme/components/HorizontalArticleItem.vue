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
  readTime: {
    type: String,
    default: '8 MIN READ'
  },
  badge: {
    type: String,
    default: ''
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
    default: 'gradient-blue'
  },
  thumbText: {
    type: String,
    default: ''
  }
})
</script>

<template>
  <article class="horizontal-article-item">
    <div class="article-info">
      <div class="article-meta">
        <span class="meta-date">🕒 {{ date }}</span>
        <span class="meta-dot">•</span>
        <span class="meta-readtime">{{ readTime }}</span>
        <span v-if="badge" class="meta-badge" :class="'badge-' + badge.toLowerCase()">
          {{ badge }}
        </span>
      </div>
      <h2 class="article-title">
        <a :href="url">{{ title }}</a>
      </h2>
      <p class="article-desc">{{ description }}</p>
    </div>

    <a :href="url" class="article-thumb" :class="gradientClass" :aria-label="title">
      <div class="thumb-inner">
        <div class="thumb-mini-window">
          <div class="window-dots"><span></span><span></span><span></span></div>
          <div class="window-content">
            <span class="thumb-cmd">{{ thumbText || title.split(' ')[0] }}</span>
          </div>
        </div>
      </div>
    </a>
  </article>
</template>

<style scoped>
.horizontal-article-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 2rem;
  padding: 1.75rem 0;
  border-bottom: 1px solid #f1f5f9;
  transition: all 0.2s ease;
}

.horizontal-article-item:last-child {
  border-bottom: none;
}

.article-info {
  flex: 1;
  min-width: 0;
}

.article-meta {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 0.5rem;
  font-size: 0.75rem;
  font-weight: 600;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 0.5rem;
}

.meta-dot {
  color: #cbd5e1;
}

.meta-badge {
  display: inline-flex;
  align-items: center;
  padding: 2px 8px;
  border-radius: 9999px;
  font-size: 0.65rem;
  font-weight: 700;
  letter-spacing: 0.06em;
}

.badge-new {
  background: #f3e8ff;
  color: #7e22ce;
}

.badge-series {
  background: #dcfce7;
  color: #15803d;
}

.dark .badge-new {
  background: rgba(126, 34, 206, 0.25);
  color: #d8b4fe;
}

.dark .badge-series {
  background: rgba(21, 128, 61, 0.25);
  color: #86efac;
}

.article-title {
  font-size: 1.25rem;
  font-weight: 700;
  line-height: 1.4;
  margin: 0 0 0.5rem 0;
  color: #111827;
}

.article-title a {
  color: inherit !important;
  text-decoration: none !important;
  transition: color 0.15s ease;
}

.article-title a:hover {
  color: #2563eb !important;
}

.article-desc {
  font-size: 0.925rem;
  color: #4b5563;
  line-height: 1.55;
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Right Thumbnail */
.article-thumb {
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
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  position: relative;
}

.article-thumb:hover {
  transform: scale(1.03);
  box-shadow: 0 6px 12px rgba(0,0,0,0.1);
}

.thumb-inner {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 12px;
}

.thumb-mini-window {
  width: 100%;
  height: 100%;
  background: rgba(15, 23, 42, 0.85);
  border-radius: 6px;
  backdrop-filter: blur(4px);
  padding: 8px 10px;
  display: flex;
  flex-direction: column;
  box-shadow: 0 4px 6px rgba(0,0,0,0.2);
}

.window-dots {
  display: flex;
  gap: 4px;
  margin-bottom: 6px;
}

.window-dots span {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.3);
}

.window-dots span:nth-child(1) { background: #ef4444; }
.window-dots span:nth-child(2) { background: #eab308; }
.window-dots span:nth-child(3) { background: #22c55e; }

.window-content {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.thumb-cmd {
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  font-size: 0.75rem;
  font-weight: 700;
  color: #38bdf8;
  letter-spacing: 0.05em;
  text-shadow: 0 1px 2px rgba(0,0,0,0.5);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* Gradients */
.gradient-blue { background: linear-gradient(135deg, #dbeafe 0%, #93c5fd 100%); }
.gradient-purple { background: linear-gradient(135deg, #f3e8ff 0%, #d8b4fe 100%); }
.gradient-emerald { background: linear-gradient(135deg, #d1fae5 0%, #6ee7b7 100%); }
.gradient-amber { background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); }
.gradient-rose { background: linear-gradient(135deg, #ffe4e6 0%, #fca5a5 100%); }
.gradient-slate { background: linear-gradient(135deg, #f1f5f9 0%, #cbd5e1 100%); }
.gradient-cyan { background: linear-gradient(135deg, #cffafe 0%, #67e8f9 100%); }
.gradient-indigo { background: linear-gradient(135deg, #e0e7ff 0%, #a5b4fc 100%); }

/* Dark mode */
.dark .horizontal-article-item {
  border-bottom-color: #1e293b;
}

.dark .article-meta {
  color: #94a3b8;
}

.dark .article-title {
  color: #f1f5f9;
}

.dark .article-title a:hover {
  color: #60a5fa !important;
}

.dark .article-desc {
  color: #94a3b8;
}

@media (max-width: 640px) {
  .horizontal-article-item {
    flex-direction: column-reverse;
    align-items: flex-start;
    gap: 1rem;
  }
  .article-thumb {
    width: 100%;
    height: 120px;
  }
}
</style>
