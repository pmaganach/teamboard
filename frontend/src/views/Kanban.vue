<template>
  <div class="view-wrapper">
    <TopBar titulo="Kanban" sub="Tablero por estado" @nuevo="abrirModal" />
    <div class="view-content">
      <!-- Tarea 15: KanbanBoard -->
      <p style="color: var(--text-sub); padding: 24px;">Cargando Kanban...</p>
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
