<template>
  <div class="view-wrapper">
    <TopBar titulo="Agenda" sub="Vista semanal del equipo" @nuevo="abrirModal">
      <template #filtros>
        <div class="week-nav">
          <button class="nav-btn" @click="cambiarSemana(-1)">&#8249;</button>
          <span class="semana-label">{{ semanaLabel }}</span>
          <button class="nav-btn" @click="cambiarSemana(1)">&#8250;</button>
          <button class="nav-btn hoy-btn" @click="irAHoy">Hoy</button>
        </div>
      </template>
    </TopBar>

    <div class="view-content">
      <AgendaGrid
        :dias="dias"
        :personas="analistas"
        :trabajos="trabajos"
        @editar="abrirModal"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { getUsuarios } from '../api/usuarios'
import { getTrabaj }   from '../api/trabajos'
import TopBar     from '../components/TopBar.vue'
import AgendaGrid from '../components/AgendaGrid.vue'

const usuarios = ref([])
const trabajos = ref([])
const analistas = computed(() => usuarios.value.filter(u => u.rol === 'analista'))

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
      nombre: DIAS_NOMBRE[i],
      num:    d.getDate(),
      esHoy:  iso === hoyISO,
    }
  })
})

const semanaLabel = computed(() => {
  const inicio = dias.value[0]
  const fin    = dias.value[6]
  return `${inicio.num} — ${fin.num} ${lunesActivo.value.toLocaleString('es', { month: 'long', year: 'numeric' })}`
})

// ── Carga de datos ────────────────────────────────────
onMounted(async () => {
  [usuarios.value, trabajos.value] = await Promise.all([
    getUsuarios(), getTrabaj()
  ])
})

function abrirModal(trabajo) {
  console.log('Abrir modal:', trabajo)
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
</style>
