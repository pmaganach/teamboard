<template>
  <div class="view-wrapper">
    <TrabajoModal v-if="modalAbierto" :trabajo="trabajoSeleccionado" @cerrar="modalAbierto = false" @actualizado="recargar" />
    <TopBar titulo="Agenda" subtitulo="Vista semanal del equipo" @nuevo="abrirModal(null)">
      <template #filtros>
        <div class="week-nav">
          <button class="nav-btn" @click="cambiarSemana(-1)">&#8249;</button>
          <span class="semana-label">{{ semanaLabel }}</span>
          <button class="nav-btn" @click="cambiarSemana(1)">&#8250;</button>
          <button class="nav-btn hoy-btn" @click="irAHoy">Hoy</button>
        </div>
        <div class="vista-toggle">
          <button :class="{ active: vistaAgenda === 'equipo' }" @click="vistaAgenda = 'equipo'">Equipo</button>
          <button :class="{ active: vistaAgenda === 'areas' }"  @click="vistaAgenda = 'areas'">Áreas</button>
        </div>
      </template>
    </TopBar>

    <div class="view-content">
      <AgendaGrid
        v-if="vistaAgenda === 'equipo'"
        :dias="dias"
        :personas="analistas"
        :trabajos="trabajos"
        @editar="abrirModal"
      />
      <AgendaGridAreas
        v-else
        :dias="dias"
        :areas="areas"
        :trabajos="trabajos"
        @editar="abrirModal"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { getUsuarios } from '../api/usuarios'
import { getAreas }    from '../api/areas'
import { getTrabaj }   from '../api/trabajos'
import TopBar           from '../components/TopBar.vue'
import AgendaGrid       from '../components/AgendaGrid.vue'
import AgendaGridAreas  from '../components/AgendaGridAreas.vue'
import TrabajoModal     from '../components/TrabajoModal.vue'

const usuarios = ref([])
const areas    = ref([])
const trabajos = ref([])
const analistas    = computed(() => usuarios.value.filter(u => u.rol === 'analista'))
const vistaAgenda  = ref('equipo')
const modalAbierto        = ref(false)
const trabajoSeleccionado = ref(null)

// ── Semana activa ──────────────────────────────────────
const lunesActivo = ref(lunesDeHoy())

function lunesDeHoy() {
  const hoy = new Date()
  const dia = hoy.getDay()           // 0=dom, 1=lun … 6=sab
  const diff = dia === 0 ? -6 : 1 - dia
  const lunes = new Date(hoy)
  lunes.setDate(hoy.getDate() + diff)
  lunes.setHours(0, 0, 0, 0)
  return lunes
}

function cambiarSemana(delta) {
  const d = new Date(lunesActivo.value)
  d.setDate(d.getDate() + delta * 7)
  lunesActivo.value = d
}

function irAHoy() {
  lunesActivo.value = lunesDeHoy()
}

// ── Días de la semana ──────────────────────────────────
const DIAS_NOMBRE = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom']

const dias = computed(() => {
  const hoyISO = new Date().toISOString().slice(0, 10)
  return Array.from({ length: 7 }, (_, i) => {
    const d = new Date(lunesActivo.value)
    d.setDate(d.getDate() + i)
    const iso = d.toISOString().slice(0, 10)
    return {
      iso,
      nombre:  DIAS_NOMBRE[i],
      num:     d.getDate(),
      esHoy:   iso === hoyISO,
      esFinde: i >= 5,
    }
  })
})

const semanaLabel = computed(() => {
  const inicio = dias.value[0]
  const fin    = dias.value[6]
  return `${inicio.num} — ${fin.num} ${lunesActivo.value.toLocaleString('es', { month: 'long', year: 'numeric' })}`
})

// ── Carga de datos ────────────────────────────────────
async function recargar() {
  [usuarios.value, areas.value, trabajos.value] = await Promise.all([
    getUsuarios(), getAreas(), getTrabaj()
  ])
}
onMounted(recargar)

function abrirModal(trabajo) {
  trabajoSeleccionado.value = trabajo || null
  modalAbierto.value = true
}
</script>

<style scoped>
.view-wrapper { display: flex; flex-direction: column; flex: 1; overflow: hidden; }
.view-content { flex: 1; overflow-y: auto; padding: 24px; background: var(--bg); }

.week-nav { display: flex; align-items: center; gap: 6px; }
.nav-btn {
  background: var(--surface2); border: 1px solid var(--border);
  color: var(--text); border-radius: 7px;
  padding: 5px 10px; font-size: 13px; cursor: pointer;
  transition: background 0.15s;
}
.nav-btn:hover { background: var(--border); }
.hoy-btn { font-size: 11px; font-weight: 700; padding: 5px 10px; }
.semana-label {
  font-size: 12px; font-weight: 700; color: var(--text);
  min-width: 160px; text-align: center; text-transform: capitalize;
}

.vista-toggle {
  display: flex; gap: 2px;
  background: var(--surface); border: 1px solid var(--border);
  border-radius: 8px; padding: 3px;
}
.vista-toggle button {
  padding: 5px 12px; border-radius: 6px;
  font-size: 11px; font-weight: 600; color: var(--text-sub);
  transition: background 0.15s, color 0.15s;
}
.vista-toggle button:hover  { color: var(--text); }
.vista-toggle button.active { background: var(--accent); color: #fff; }
</style>
