<template>
  <div class="view-wrapper">
    <TopBar titulo="Dashboard" sub="Visibilidad del equipo" @nuevo="abrirModal" />
    <div class="view-content">
      <!-- Tarea 13: contenido completo del Dashboard -->
      <p style="color: var(--text-sub); padding: 24px;">Cargando Dashboard...</p>
    </div>
  </div>
</template>

<script setup>
import TopBar from '../components/TopBar.vue'
function abrirModal() {}
</script>

<style scoped>
.view-wrapper { display: flex; flex-direction: column; flex: 1; }
.view-content { flex: 1; overflow-y: auto; padding: 24px; background: var(--bg); }
</style>
