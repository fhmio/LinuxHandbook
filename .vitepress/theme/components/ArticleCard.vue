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
    default: '10 MIN READ'
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
  <a :href="url" class="article-card">
    <div class="card-image" :class="gradientClass">
      <div class="card-illustration">
        <div class="mini-terminal">
          <div class="terminal-bar">
            <span class="dot red"></span>
            <span class="dot yellow"></span>
            <span class="dot green"></span>
          </div>
          <div class="terminal-text">
            <span>$ {{ thumbText || title.split(' ')[0] }}</span>
          </div>
        </div>
      </div>
    </div>
    <div class="card-content">
      <div class="card-meta">
        <span class="card-date">🕒 {{ date }}</span>
        <span class="meta-dot">•</span>
        <span class="card-readtime">{{ readTime }}</span>
        <span v-if="badge" class="card-badge" :class="'badge-' + badge.toLowerCase()">
          {{ badge }}
        </span>
      </div>
      <h3 class="card-title">{{ title }}</h3>
      <p v-if="description" class="card-desc">{{ description }}</p>
    </div>
  </a>
</template>

<style scoped>
.article-card {
  display: flex;
  flex-direction: column;
  background: white;
  border-radius: 12px;
  overflow: hidden;
  border: 1px solid #f1f5f9;
  box-shadow: 0 1px 3px rgba(0,0,0,0.04);
  transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
  text-decoration: none !important;
  color: inherit !important;
  height: 100%;
}

.article-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 16px rgba(0,0,0,0.08);
  border-color: #e2e8f0;
}

.card-image {
  height: 160px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
}

.card-illustration {
  width: 75%;
  height: 70%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.mini-terminal {
  width: 100%;
  height: 100%;
  background: rgba(15, 23, 42, 0.88);
  border-radius: 8px;
  backdrop-filter: blur(4px);
  padding: 10px 12px;
  display: flex;
  flex-direction: column;
  box-shadow: 0 8px 16px rgba(0,0,0,0.15);
}

.terminal-bar {
  display: flex;
  gap: 5px;
  margin-bottom: 8px;
}

.dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
}

.dot.red { background: #ef4444; }
.dot.yellow { background: #eab308; }
.dot.green { background: #22c55e; }

.terminal-text {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  font-size: 0.85rem;
  font-weight: 700;
  color: #38bdf8;
  letter-spacing: 0.05em;
  text-align: center;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.card-content {
  padding: 1.25rem 1.5rem 1.5rem;
  display: flex;
  flex-direction: column;
  flex: 1;
}

.card-meta {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
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

.card-badge {
  display: inline-flex;
  align-items: center;
  padding: 1px 7px;
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

.card-title {
  font-size: 1.15rem;
  font-weight: 700;
  line-height: 1.35;
  margin: 0 0 0.5rem 0;
  color: #111827;
}

.card-desc {
  font-size: 0.875rem;
  color: #4b5563;
  line-height: 1.5;
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Gradients */
.gradient-blue { background: linear-gradient(135deg, #bfdbfe 0%, #60a5fa 100%); }
.gradient-teal { background: linear-gradient(135deg, #99f6e4 0%, #2dd4bf 100%); }
.gradient-purple { background: linear-gradient(135deg, #e9d5ff 0%, #c084fc 100%); }
.gradient-yellow { background: linear-gradient(135deg, #fef08a 0%, #facc15 100%); }
.gradient-pink { background: linear-gradient(135deg, #fbcfe8 0%, #f472b6 100%); }
.gradient-cyan { background: linear-gradient(135deg, #a5f3fc 0%, #38bdf8 100%); }
.gradient-emerald { background: linear-gradient(135deg, #a7f3d0 0%, #34d399 100%); }
.gradient-rose { background: linear-gradient(135deg, #fecdd3 0%, #fb7185 100%); }

/* Dark mode */
.dark .article-card {
  background: #1e293b;
  border-color: #334155;
  box-shadow: 0 1px 3px rgba(0,0,0,0.3);
}

.dark .article-card:hover {
  border-color: #475569;
  box-shadow: 0 8px 16px rgba(0,0,0,0.4);
}

.dark .card-meta {
  color: #94a3b8;
}

.dark .card-title {
  color: #f1f5f9;
}

.dark .card-desc {
  color: #94a3b8;
}
</style>
