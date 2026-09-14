<script setup>
import { ref, computed } from 'vue'
import ToolCard from './ToolCard.vue'

const activeTool = ref(null)

const tools = [
  {
    id: 'systemd',
    title: 'systemd Service File Generator',
    description: 'Build a systemd service file online, choose common service and restart settings, then download the unit and copy the commands needed to install and test it.',
    icon: 'terminal'
  },
  {
    id: 'find',
    title: 'find Command Builder',
    description: 'Interactive find command builder. Set a name pattern, type, size, modification time, or permissions, and copy a working command with every argument explained.',
    icon: 'wrench'
  },
  {
    id: 'rsync',
    title: 'rsync Command Builder',
    description: 'Interactive rsync command builder. Pick the flags you need, add excludes, an SSH port, or a bandwidth limit, and copy the exact rsync command with an explanation of every option.',
    icon: 'wrench'
  },
  {
    id: 'cron',
    title: 'Cron Generator and Crontab Expression Explainer',
    description: 'Build cron expressions with presets and field controls, or paste a crontab schedule to see its plain-English meaning and next five run times.',
    icon: 'wrench'
  },
  {
    id: 'subnet',
    title: 'Subnet Calculator',
    description: 'Interactive IPv4 subnet and CIDR calculator. Enter a network in CIDR notation to get the network and broadcast address, usable host range, netmask, wildcard mask, and a binary bit view.',
    icon: 'wrench'
  },
  {
    id: 'chmod',
    title: 'chmod Calculator',
    description: 'Interactive chmod permission calculator. Toggle read, write, and execute bits to get the octal and symbolic notation, plus the exact chmod command to run.',
    icon: 'wrench'
  }
]

// Interactive Chmod Calculator State
const permissions = ref({
  user: { r: true, w: true, x: false },
  group: { r: true, w: false, x: false },
  others: { r: true, w: false, x: false }
})

const octalValue = computed(() => {
  const calc = (p) => (p.r ? 4 : 0) + (p.w ? 2 : 0) + (p.x ? 1 : 0)
  return `${calc(permissions.value.user)}${calc(permissions.value.group)}${calc(permissions.value.others)}`
})

const symbolicValue = computed(() => {
  const p = permissions.value
  return (
    (p.user.r ? 'r' : '-') + (p.user.w ? 'w' : '-') + (p.user.x ? 'x' : '-') +
    (p.group.r ? 'r' : '-') + (p.group.w ? 'w' : '-') + (p.group.x ? 'x' : '-') +
    (p.others.r ? 'r' : '-') + (p.others.w ? 'w' : '-') + (p.others.x ? 'x' : '-')
  )
})

const copied = ref(false)
function copyCommand(text) {
  navigator.clipboard.writeText(text)
  copied.value = true
  setTimeout(() => { copied.value = false }, 2000)
}

function openTool(id) {
  activeTool.value = activeTool.value === id ? null : id
}
</script>

<template>
  <div class="linuxize-page-container">
    <header class="tools-header">
      <h1 class="tools-title">Linux Tools</h1>
      <p class="tools-subtitle">
        Interactive, client-side tools for Linux and DevOps work: permission calculators, subnet planners, cron expression builders, and more. Calculations run locally in your browser.
      </p>
    </header>

    <!-- 3x2 Tool Cards Grid -->
    <section class="tools-grid">
      <ToolCard
        v-for="tool in tools"
        :key="tool.id"
        :title="tool.title"
        :description="tool.description"
        :icon="tool.icon"
        @click="openTool(tool.id)"
      />
    </section>

    <!-- Interactive Workspace (Expands when clicked) -->
    <transition name="fade">
      <section v-if="activeTool === 'chmod'" class="interactive-tool-box">
        <div class="box-header">
          <h3>Interactive chmod Calculator</h3>
          <button class="close-btn" @click="activeTool = null">&times;</button>
        </div>
        
        <div class="chmod-columns">
          <div class="perm-col">
            <h4>Owner (User)</h4>
            <label><input type="checkbox" v-model="permissions.user.r" /> Read (4)</label>
            <label><input type="checkbox" v-model="permissions.user.w" /> Write (2)</label>
            <label><input type="checkbox" v-model="permissions.user.x" /> Execute (1)</label>
          </div>

          <div class="perm-col">
            <h4>Group</h4>
            <label><input type="checkbox" v-model="permissions.group.r" /> Read (4)</label>
            <label><input type="checkbox" v-model="permissions.group.w" /> Write (2)</label>
            <label><input type="checkbox" v-model="permissions.group.x" /> Execute (1)</label>
          </div>

          <div class="perm-col">
            <h4>Others (Public)</h4>
            <label><input type="checkbox" v-model="permissions.others.r" /> Read (4)</label>
            <label><input type="checkbox" v-model="permissions.others.w" /> Write (2)</label>
            <label><input type="checkbox" v-model="permissions.others.x" /> Execute (1)</label>
          </div>
        </div>

        <div class="calc-results">
          <div class="result-pill">
            <span class="pill-label">Octal:</span>
            <span class="pill-value font-mono">{{ octalValue }}</span>
          </div>
          <div class="result-pill">
            <span class="pill-label">Symbolic:</span>
            <span class="pill-value font-mono">{{ symbolicValue }}</span>
          </div>
          <div class="result-command font-mono">
            <code>chmod {{ octalValue }} filename</code>
            <button class="copy-btn" @click="copyCommand(`chmod ${octalValue} filename`)">
              {{ copied ? 'Copied!' : 'Copy' }}
            </button>
          </div>
        </div>
      </section>
    </transition>
  </div>
</template>

<style scoped>
.linuxize-page-container {
  max-width: 1100px;
  margin: 0 auto;
  padding: 2.5rem 1.5rem 4rem;
}

.tools-header {
  margin-bottom: 2.5rem;
}

.tools-title {
  font-size: 2.75rem;
  font-weight: 800;
  letter-spacing: -0.02em;
  color: #0f172a;
  margin: 0 0 0.75rem 0;
}

.tools-subtitle {
  font-size: 1.15rem;
  color: #475569;
  max-width: 800px;
  margin: 0;
  line-height: 1.6;
}

.tools-grid {
  display: grid;
  grid-template-columns: repeat(1, minmax(0, 1fr));
  gap: 1.5rem;
}

@media (min-width: 768px) {
  .tools-grid {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
}

/* Interactive Calculator Box */
.interactive-tool-box {
  margin-top: 2.5rem;
  background: white;
  border-radius: 12px;
  border: 1px solid #cbd5e1;
  padding: 2rem;
  box-shadow: 0 10px 25px rgba(0,0,0,0.08);
}

.box-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid #e2e8f0;
}

.box-header h3 {
  margin: 0;
  font-size: 1.35rem;
  font-weight: 700;
  color: #0f172a;
}

.close-btn {
  background: transparent;
  border: none;
  font-size: 1.75rem;
  cursor: pointer;
  color: #64748b;
}

.chmod-columns {
  display: grid;
  grid-template-columns: repeat(1, minmax(0, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

@media (min-width: 640px) {
  .chmod-columns {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
}

.perm-col {
  background: #f8fafc;
  padding: 1.25rem;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
}

.perm-col h4 {
  margin: 0 0 1rem 0;
  font-size: 1rem;
  font-weight: 700;
  color: #1e293b;
}

.perm-col label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
  color: #334155;
  cursor: pointer;
}

.calc-results {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 1rem;
  padding-top: 1.5rem;
  border-top: 1px solid #e2e8f0;
}

.result-pill {
  background: #eff6ff;
  border: 1px solid #bfdbfe;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  display: flex;
  gap: 0.5rem;
  font-size: 0.95rem;
}

.pill-label {
  color: #1d4ed8;
  font-weight: 600;
}

.pill-value {
  color: #0f172a;
  font-weight: 700;
}

.result-command {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #0f172a;
  color: #38bdf8;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  min-width: 250px;
}

.copy-btn {
  background: #2563eb;
  color: white;
  border: none;
  padding: 0.25rem 0.75rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.15s;
}

.copy-btn:hover {
  background: #1d4ed8;
}

.font-mono {
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
}

/* Dark mode */
.dark .tools-title {
  color: #f8fafc;
}

.dark .tools-subtitle {
  color: #94a3b8;
}

.dark .interactive-tool-box {
  background: #1e293b;
  border-color: #334155;
}

.dark .box-header {
  border-bottom-color: #334155;
}

.dark .box-header h3 {
  color: #f8fafc;
}

.dark .perm-col {
  background: #0f172a;
  border-color: #334155;
}

.dark .perm-col h4 {
  color: #f1f5f9;
}

.dark .perm-col label {
  color: #cbd5e1;
}

.dark .calc-results {
  border-top-color: #334155;
}

.dark .result-pill {
  background: rgba(37, 99, 235, 0.2);
  border-color: rgba(37, 99, 235, 0.3);
}

.dark .pill-value {
  color: #f8fafc;
}
</style>
