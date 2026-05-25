<template>
  <div class="view-wrapper">
    <TopBar titulo="Inicio" :sub="fechaHoy" @nuevo="abrirModal(null)" />
    <TrabajoModal v-if="modalAbierto" :trabajo="trabajoSeleccionado" @cerrar="modalAbierto = false" @actualizado="recargar" />

    <div class="view-content">
      <!-- KPI Cards -->
      <section class="section">
        <h2 class="section-title">General</h2>
        <KpiCards :trabajos="trabajos" />
      </section>

      <!-- Analistas -->
      <section class="section">
        <div class="section-header">
          <h2 class="section-title">Equipo</h2>
          <div class="vista-toggle">
            <button :class="{ active: vistaEquipo === 'cards' }"   @click="setVista('cards')"   title="Cards">⊞</button>
            <button :class="{ active: vistaEquipo === 'heatmap' }" @click="setVista('heatmap')" title="Heatmap">⊟</button>
            <button :class="{ active: vistaEquipo === 'strips' }"  @click="setVista('strips')"  title="Strips">≡</button>
          </div>
        </div>

        <div v-if="vistaEquipo === 'cards'" class="members-grid">
          <MemberCard
            v-for="u in analistas"
            :key="u.id"
            :usuario="u"
            :trabajos="trabajosPorUsuario(u.id)"
            @editar="abrirModal"
          />
        </div>
        <EquipoHeatmap
          v-else-if="vistaEquipo === 'heatmap'"
          :usuarios="analistas"
          :trabajos="trabajos"
        />
        <EquipoStrips
          v-else-if="vistaEquipo === 'strips'"
          :usuarios="analistas"
          :trabajos="trabajos"
          @editar="abrirModal"
        />
      </section>

      <!-- Áreas -->
      <section class="section">
        <div class="section-header">
          <h2 class="section-title">Trabajos por área</h2>
          <div class="vista-toggle">
            <button :class="{ active: vistaArea === 'cards' }"   @click="setVistaArea('cards')"   title="Cards">⊞</button>
            <button :class="{ active: vistaArea === 'heatmap' }" @click="setVistaArea('heatmap')" title="Heatmap">⊟</button>
            <button :class="{ active: vistaArea === 'strips' }"  @click="setVistaArea('strips')"  title="Strips">≡</button>
          </div>
        </div>

        <div v-if="vistaArea === 'cards'" class="areas-grid">
          <AreaCard
            v-for="a in areas"
            :key="a.id"
            :area="a"
            :trabajos="trabajosPorArea(a.nombre)"
            @editar="abrirModal"
          />
        </div>
        <AreaHeatmap
          v-else-if="vistaArea === 'heatmap'"
          :areas="areas"
          :trabajos="trabajos"
        />
        <AreaStrips
          v-else-if="vistaArea === 'strips'"
          :areas="areas"
          :trabajos="trabajos"
          @editar="abrirModal"
        />
      </section>

      <!-- Desglose -->
      <section class="section">
        <h2 class="section-title">Detalle</h2>
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
import TopBar         from '../components/TopBar.vue'
import KpiCards        from '../components/KpiCards.vue'
import MemberCard      from '../components/MemberCard.vue'
import AreaCard        from '../components/AreaCard.vue'
import Desglose        from '../components/Desglose.vue'
import TrabajoModal    from '../components/TrabajoModal.vue'
import EquipoHeatmap   from '../components/EquipoHeatmap.vue'
import EquipoStrips    from '../components/EquipoStrips.vue'
import AreaHeatmap     from '../components/AreaHeatmap.vue'
import AreaStrips      from '../components/AreaStrips.vue'

const usuarios = ref([])
const areas    = ref([])
const trabajos = ref([])
const modalAbierto        = ref(false)
const trabajoSeleccionado = ref(null)
const { filtros }         = useFiltros()

const analistas = computed(() => usuarios.value.filter(u => u.rol === 'analista'))

const fechaHoy = new Date().toLocaleDateString('es-CL', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' })

const vistaEquipo = ref(localStorage.getItem('equipo_vista') || 'cards')
function setVista(v) {
  vistaEquipo.value = v
  localStorage.setItem('equipo_vista', v)
}

const vistaArea = ref(localStorage.getItem('area_vista') || 'cards')
function setVistaArea(v) {
  vistaArea.value = v
  localStorage.setItem('area_vista', v)
}

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
  trabajos.value.filter(t => t.area_cliente === nombre)

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
  margin-bottom: 14px; margin-top: 0;
}

.section-header {
  display: flex; align-items: center; justify-content: space-between;
  margin-bottom: 14px;
}
.section-header .section-title { margin-bottom: 0; }

.vista-toggle {
  display: flex; gap: 2px;
  background: var(--surface); border: 1px solid var(--border);
  border-radius: 8px; padding: 3px;
}
.vista-toggle button {
  padding: 4px 10px; border-radius: 6px;
  font-size: 14px; color: var(--text-sub);
  transition: background 0.15s, color 0.15s;
}
.vista-toggle button:hover  { color: var(--text); }
.vista-toggle button.active { background: var(--accent); color: #fff; }

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
