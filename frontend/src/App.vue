<template>
  <div class="layout">
    <Sidebar />
    <div class="main">
      <router-view />
    </div>
  </div>
</template>

<script setup>
import Sidebar from './components/Sidebar.vue'
</script>

<style>
@import './styles/themes.css';
@import './styles/base.css';

.layout { display: flex; min-height: 100vh; }
.main   { flex: 1; display: flex; flex-direction: column; overflow: hidden; }
</style>
