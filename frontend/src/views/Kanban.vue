<template>
  <div class="view-wrapper">
    <TopBar titulo="Kanban" sub="Tablero por estado" @nuevo="abrirModal" />
    <div class="view-content">
      <KanbanBoard
        :trabajos="trabajos"
        :usuarios="usuarios"
        @editar="abrirModal"
        @actualizado="cargarDatos"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getUsuarios } from '../api/usuarios'
import { getTrabaj }   from '../api/trabajos'
import TopBar      from '../components/TopBar.vue'
import KanbanBoard from '../components/KanbanBoard.vue'

const usuarios = ref([])
const trabajos = ref([])

async function cargarDatos() {
  [usuarios.value, trabajos.value] = await Promise.all([
    getUsuarios(), getTrabaj()
  ])
}

onMounted(cargarDatos)

function abrirModal(trabajo) {
  console.log('Abrir modal:', trabajo)
}
</script>

<style scoped>
.view-wrapper { display: flex; flex-direction: column; flex: 1; overflow: hidden; }
.view-content { flex: 1; overflow-y: auto; padding: 24px; background: var(--bg); }
</style>
