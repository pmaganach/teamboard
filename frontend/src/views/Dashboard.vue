<template>
  <div class="view-wrapper">
    <TopBar titulo="Dashboard" sub="Visibilidad del equipo" @nuevo="abrirModal(null)" />
    <TrabajoModal v-if="modalAbierto" :trabajo="trabajoSeleccionado" @cerrar="modalAbierto = false" @actualizado="recargar" />

    <div class="view-content">
      <!-- KPI Cards -->
      <KpiCards :trabajos="trabajos" />

      <!-- Analistas -->
      <section class="section">
        <h2 class="section-title">Equipo</h2>
        <div class="members-grid">
          <MemberCard
            v-for="u in analistas"
            :key="u.id"
            :usuario="u"
            :trabajos="trabajosPorUsuario(u.id)"
            @editar="abrirModal"
          />
        </div>
      </section>

      <!-- Áreas -->
      <section class="section">
        <h2 class="section-title">Trabajos por área</h2>
        <div class="areas-grid">
          <AreaCard
            v-for="a in areas"
            :key="a.id"
            :area="a"
            :trabajos="trabajosPorArea(a.nombre)"
            @editar="abrirModal"
          />
        </div>
      </section>

      <!-- Desglose -->
      <section class="section">
        <Desglose :trabajos="trabajos" :usuarios="usuarios" @editar="abrirModal" />
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { getUsuarios } from '../api/usuarios'
import { getAreas }    from '../api/areas'
import { getTrabaj }   from '../api/trabajos'
import { useFiltros }  from '../composables/useFiltros'
import TopBar       from '../components/TopBar.vue'
import KpiCards      from '../components/KpiCards.vue'
import MemberCard    from '../components/MemberCard.vue'
import AreaCard      from '../components/AreaCard.vue'
import Desglose      from '../components/Desglose.vue'
import TrabajoModal  from '../components/TrabajoModal.vue'

const usuarios = ref([])
const areas    = ref([])
const trabajos = ref([])
const modalAbierto        = ref(false)
const trabajoSeleccionado = ref(null)
const { filtros }         = useFiltros()

const analistas = computed(() => usuarios.value.filter(u => u.rol === 'analista'))

async function recargar() {
  [usuarios.value, areas.value, trabajos.value] = await Promise.all([
    getUsuarios(), getAreas(), getTrabaj(filtros())
  ])
}

onMounted(recargar)
watch(filtros, recargar)

const trabajosPorUsuario = (uid) =>
  trabajos.value.filter(t => t.responsable_id === uid)

const trabajosPorArea = (nombre) =>
  trabajos.value.filter(t => !t.responsable_id && t.area_equipo === nombre)

function abrirModal(trabajo) {
  trabajoSeleccionado.value = trabajo || null
  modalAbierto.value = true
}
</script>

<style scoped>
.view-wrapper  { display: flex; flex-direction: column; flex: 1; overflow: hidden; }
.view-content  { flex: 1; overflow-y: auto; padding: 24px; background: var(--bg); }

.section       { margin-bottom: 32px; }
.section-title {
  font-size: 12px; font-weight: 700; text-transform: uppercase;
  letter-spacing: 0.6px; color: var(--text-sub);
  margin-bottom: 14px;
}

.members-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 14px;
}

.areas-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 12px;
}
</style>
