<script setup>
import DefaultTheme from 'vitepress/theme'
import { useData } from 'vitepress'
import CustomHome from './components/CustomHome.vue'
import ArticleMeta from './components/ArticleMeta.vue'

const { Layout } = DefaultTheme
const { frontmatter } = useData()
</script>

<template>
  <Layout>
    <template #home-hero-before v-if="frontmatter.layout === 'custom-home'">
      <CustomHome />
    </template>
    <template #doc-before>
      <ArticleMeta v-if="frontmatter.layout !== 'custom-home' && frontmatter.layout !== 'page'" />
    </template>
  </Layout>
</template>
