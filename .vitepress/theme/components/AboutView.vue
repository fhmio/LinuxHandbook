<script setup>
</script>

<template>
  <div class="linuxize-page-container">
    <header class="about-header">
      <h1 class="about-title">About LinuxHandbook</h1>
      <p class="about-subtitle">
        The Authoritative Linux Reference & Operational Systems Playbook.
      </p>
    </header>

    <section class="about-content">
      <div class="about-card">
        <h2>🎯 Our Mission</h2>
        <p>
          <strong>LinuxHandbook</strong> was created to bridge the gap between fragmented man pages and superficial online tutorials.
          We publish practical, strictly validated, and production-tested guides on Linux, Bash scripting, system architecture, DevOps, and cloud administration.
        </p>
        <p>
          Every command, flag, and configuration snippet is tested against real enterprise environments across Ubuntu, Debian, RHEL, Fedora, Arch, and Alpine Linux.
        </p>
      </div>

      <div class="about-card">
        <h2>📜 The 20-Point Article Quality Contract</h2>
        <p>
          Every article published on LinuxHandbook must pass automated linting enforcing our strict 20-point quality contract, including:
        </p>
        <ul class="contract-list">
          <li><strong>Quick-Reference Cards:</strong> High-frequency syntax and flag tables at the top of every guide.</li>
          <li><strong>Copyable One-Liners:</strong> Immediate terminal snippets ready for triage during active outages.</li>
          <li><strong>ASCII Architecture Diagrams:</strong> Visual mental models illustrating packet flows, memory pools, and process trees.</li>
          <li><strong>Blast Radius & Safety Callouts:</strong> Standardized alerts (<code>[!CAUTION]</code>, <code>[!WARNING]</code>, <code>[!TIP]</code>) to prevent accidental data loss.</li>
          <li><strong>Root Cause & Edge Cases:</strong> Pitfalls, compatibility nuances across distributions, and exit code meanings.</li>
        </ul>
      </div>

      <div class="about-card">
        <h2>🛠️ Upstream-Driven Inventories</h2>
        <p>
          We track 64 core commands across 13 machine-readable JSON inventories directly synced with upstream maintainers, including GNU Coreutils, util-linux, procps-ng, OpenSSH, iproute2, and systemd.
        </p>
      </div>

      <div class="about-card">
        <h2>📬 Contact & Feedback</h2>
        <p>
          LinuxHandbook is completely open source under the MIT license.
          Have a suggestion, spot a typo, or want to contribute? Visit our GitHub repository at
          <a href="https://github.com/fhmio/LinuxHandbook" target="_blank" rel="noopener">github.com/fhmio/LinuxHandbook</a>.
        </p>
      </div>
    </section>
  </div>
</template>

<style scoped>
.linuxize-page-container {
  max-width: 900px;
  margin: 0 auto;
  padding: 2.5rem 1.5rem 4rem;
}

.about-header {
  margin-bottom: 2.5rem;
  text-align: center;
}

.about-title {
  font-size: 2.75rem;
  font-weight: 800;
  letter-spacing: -0.02em;
  color: #0f172a;
  margin: 0 0 0.75rem 0;
}

.about-subtitle {
  font-size: 1.2rem;
  color: #475569;
  max-width: 650px;
  margin: 0 auto;
  line-height: 1.6;
}

.about-content {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.about-card {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 1px 3px rgba(0,0,0,0.03);
}

.about-card h2 {
  font-size: 1.4rem;
  font-weight: 700;
  color: #0f172a;
  margin: 0 0 1rem 0;
}

.about-card p {
  font-size: 1rem;
  line-height: 1.7;
  color: #334155;
  margin: 0 0 1rem 0;
}

.about-card p:last-child {
  margin-bottom: 0;
}

.contract-list {
  padding-left: 1.5rem;
  color: #334155;
  line-height: 1.8;
  font-size: 0.95rem;
}

.contract-list li {
  margin-bottom: 0.5rem;
}

.about-card a {
  color: #2563eb !important;
  font-weight: 600;
  text-decoration: underline;
}

/* Dark mode */
.dark .about-title {
  color: #f8fafc;
}

.dark .about-subtitle {
  color: #94a3b8;
}

.dark .about-card {
  background: #1e293b;
  border-color: #334155;
}

.dark .about-card h2 {
  color: #f8fafc;
}

.dark .about-card p,
.dark .contract-list {
  color: #cbd5e1;
}

.dark .about-card a {
  color: #60a5fa !important;
}
</style>
