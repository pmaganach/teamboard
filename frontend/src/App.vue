<template>
  <div v-if="isLoginPage" class="login-layout">
    <router-view />
  </div>
  <div v-else class="layout">
    <Sidebar />
    <div class="main">
      <router-view />
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import Sidebar from './components/Sidebar.vue'

const route       = useRoute()
const isLoginPage = computed(() => route.path === '/login')
</script>

<style>
@import './styles/themes.css';
@import './styles/base.css';

.login-layout { min-height: 100vh; background: var(--bg); }
.layout { display: flex; min-height: 100vh; }
.main   { flex: 1; display: flex; flex-direction: column; overflow: hidden; }
</style>
