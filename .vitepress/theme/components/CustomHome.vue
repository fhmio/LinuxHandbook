<script setup>
import ArticleCard from './ArticleCard.vue'
import CheatsheetCard from './CheatsheetCard.vue'
</script>

<template>
  <div class="linuxize-container">
    <header class="linuxize-header">
      <h1>Start Here</h1>
      <p>New to Linux? Start here for curated learning paths, essential command guides, and quick references to help you get the most out of Linux.</p>
    </header>

    <!-- Top Tutorials -->
    <section class="linuxize-section">
      <h2 class="linuxize-section-title">TOP TUTORIALS</h2>
      <div class="linuxize-grid grid-cols-3">
        <ArticleCard title="Basic Linux Commands Every User Should Know" date="AUG 26, 2026" url="/article/linux-ls-tutorial" gradientClass="gradient-1" />
        <ArticleCard title="pwd Command in Linux: Print the Current Working Directory" date="AUG 24, 2026" url="/article/linux-pwd-tutorial" gradientClass="gradient-2" />
        <ArticleCard title="cd Command in Linux: Change Directories" date="AUG 23, 2026" url="/article/linux-cd-tutorial" gradientClass="gradient-3" />
        <ArticleCard title="ls Command in Linux: List Files and Directories" date="AUG 20, 2026" url="/article/linux-ls-tutorial" gradientClass="gradient-4" />
        <ArticleCard title="How to Create a File in Linux" date="AUG 18, 2026" url="/article/linux-touch-tutorial" gradientClass="gradient-5" />
        <ArticleCard title="How to Create a Directory in Linux: mkdir Command Examples" date="AUG 15, 2026" url="/article/linux-mkdir-tutorial" gradientClass="gradient-6" />
      </div>
    </section>

    <!-- 3 Column Lists -->
    <section class="linuxize-section" style="padding-top: 0;">
      <div class="linuxize-grid grid-cols-3">
        <div>
          <h2 class="linuxize-section-title">FILE PERMISSIONS</h2>
          <CheatsheetCard title="cp" description="Copy files and directories." date="JUN 15, 2026" url="/article/linux-cp-tutorial" style="margin-bottom: 1rem;" />
          <CheatsheetCard title="rm" description="Remove files and directories." date="JUN 14, 2026" url="/article/linux-rm-tutorial" style="margin-bottom: 1rem;" />
          <CheatsheetCard title="mv" description="Move or rename files and directories." date="JUN 13, 2026" url="/article/linux-mv-tutorial" />
        </div>
        <div>
          <h2 class="linuxize-section-title">SEARCH AND PROCESS</h2>
          <CheatsheetCard title="grep" description="Search text using patterns." date="MAY 10, 2026" url="/article/linux-grep-tutorial" style="margin-bottom: 1rem;" />
          <CheatsheetCard title="find" description="Search for files in a directory hierarchy." date="MAY 9, 2026" url="/article/linux-find-tutorial" style="margin-bottom: 1rem;" />
          <CheatsheetCard title="ps" description="Report a snapshot of the current processes." date="MAY 8, 2026" url="/article/linux-ps-tutorial" />
        </div>
        <div>
          <h2 class="linuxize-section-title">NETWORKING AND SYSTEM</h2>
          <CheatsheetCard title="ip" description="Show / manipulate routing, network devices." date="APR 20, 2026" url="/article/linux-ip-tutorial" style="margin-bottom: 1rem;" />
          <CheatsheetCard title="ss" description="Investigate sockets." date="APR 19, 2026" url="/article/linux-ss-tutorial" style="margin-bottom: 1rem;" />
          <CheatsheetCard title="systemctl" description="Control the systemd system and service manager." date="APR 18, 2026" url="/article/linux-systemctl-tutorial" />
        </div>
      </div>
    </section>

    <!-- Latest Posts -->
    <section class="linuxize-section" style="border-top: 1px solid #e5e7eb;">
      <h2 class="linuxize-section-title">LATEST POSTS</h2>
      <div class="linuxize-grid grid-cols-3">
        <ArticleCard title="Linux Users and Permissions" date="SEP 10, 2026" url="/article/linux-su-tutorial" gradientClass="gradient-2" />
        <ArticleCard title="Bash Scripting Fundamentals" date="SEP 9, 2026" url="/bash" gradientClass="gradient-4" />
        <ArticleCard title="SSH Essentials" date="SEP 8, 2026" url="/article/linux-ssh-tutorial" gradientClass="gradient-6" />
      </div>
    </section>
  </div>
</template>
