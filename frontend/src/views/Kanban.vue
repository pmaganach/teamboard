<template>
  <div class="view-wrapper">
    <TrabajoModal v-if="modalAbierto" :trabajo="trabajoSeleccionado" @cerrar="modalAbierto = false" @actualizado="cargarDatos" />
    <TopBar titulo="Gestión" subtitulo="Tablero por estado" @nuevo="abrirModal(null)" />
    <div class="view-content">
      <KanbanBoard
        :trabajos="trabajosFiltrados"
        :usuarios="usuarios"
        @editar="abrirModal"
        @actualizado="cargarDatos"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { getUsuarios } from '../api/usuarios'
import { getTrabaj }   from '../api/trabajos'
import { useFiltros }  from '../composables/useFiltros'
import { useAuth }     from '../composables/useAuth'
import TopBar       from '../components/TopBar.vue'
import KanbanBoard  from '../components/KanbanBoard.vue'
import TrabajoModal from '../components/TrabajoModal.vue'

const usuarios = ref([])
const trabajos = ref([])
const modalAbierto        = ref(false)
const trabajoSeleccionado = ref(null)
const { filtros }         = useFiltros()
const { user, isGerente } = useAuth()

const trabajosFiltrados = computed(() => {
  if (isGerente.value) return trabajos.value
  return trabajos.value.filter(t => t.responsable_id === user.value?.usuario_id)
})

async function cargarDatos() {
  [usuarios.value, trabajos.value] = await Promise.all([
    getUsuarios(), getTrabaj(filtros())
  ])
}

onMounted(cargarDatos)
watch(filtros, cargarDatos)

function abrirModal(trabajo) {
  trabajoSeleccionado.value = trabajo || null
  modalAbierto.value = true
}
</script>

<style scoped>
.view-wrapper { display: flex; flex-direction: column; flex: 1; overflow: hidden; }
.view-content { flex: 1; overflow-y: auto; padding: 24px; background: var(--bg); }
</style>
