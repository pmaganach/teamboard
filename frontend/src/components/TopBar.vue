<template>
  <header class="topbar">
    <div class="topbar-left">
      <h1 class="topbar-title">{{ titulo }}</h1>
      <span v-if="subtitulo" class="topbar-subtitulo">{{ subtitulo }}</span>
    </div>
    <div class="topbar-right" v-if="!hideControls">
      <slot name="filtros" />

      <span v-if="sub" class="topbar-fecha">{{ sub }}</span>

      <!-- Filtros rápidos -->
      <div class="filtros-rapidos">
        <button :class="['btn-rapido', { active: periodoActivo === '7d' }]" @click="setPeriodo('7d')">7 días</button>
        <button :class="['btn-rapido', { active: periodoActivo === '1m' }]" @click="setPeriodo('1m')">1 mes</button>
        <button v-if="periodoActivo" class="btn-rapido btn-clear" @click="setPeriodo(null)">&#x2715;</button>
      </div>

      <!-- Filtros de fecha globales -->
      <div class="filtros-fecha">
        <label class="filtro-label">Desde</label>
        <input type="date" v-model="desde" class="date-input" />
        <label class="filtro-label">Hasta</label>
        <input type="date" v-model="hasta" class="date-input" />
        <button v-if="(desde || hasta) && !periodoActivo" class="btn-limpiar" @click="limpiar" title="Limpiar filtros">
          &#x2715;
        </button>
      </div>

      <button class="btn-nuevo" @click="$emit('nuevo')">
        + Nuevo trabajo
      </button>
    </div>
  </header>
</template>

<script setup>
import { ref } from 'vue'
import { useFiltros } from '../composables/useFiltros'

defineProps({
  titulo:       { type: String,  default: 'TeamBoard' },
  subtitulo:    { type: String,  default: '' },
  sub:          { type: String,  default: '' },
  hideControls: { type: Boolean, default: false },
})
defineEmits(['nuevo'])

const { desde, hasta, limpiar } = useFiltros()

const periodoActivo = ref(null)

function toISO(date) {
  return date.toISOString().split('T')[0]
}

function setPeriodo(periodo) {
  periodoActivo.value = periodo
  if (!periodo) {
    limpiar()
    return
  }
  const hoy = new Date()
  hasta.value = toISO(hoy)
  if (periodo === '7d') {
    const d = new Date(hoy); d.setDate(d.getDate() - 7)
    desde.value = toISO(d)
  } else if (periodo === '1m') {
    const d = new Date(hoy); d.setMonth(d.getMonth() - 1)
    desde.value = toISO(d)
  }
}
</script>

<style scoped>
.topbar {
  display: flex; align-items: center; justify-content: space-between;
  padding: 21px 24px 17px;
  background: var(--topbar-bg);
  border-bottom: 1px solid var(--border);
  gap: 16px; flex-wrap: wrap;
}
.topbar-left { display: flex; align-items: baseline; gap: 10px; }
.topbar-title     { font-size: 16px; font-weight: 700; color: var(--text); }
.topbar-subtitulo { font-size: 11px; color: var(--text-sub); font-weight: 500; }
.topbar-fecha     { font-size: 11px; color: var(--text-sub); white-space: nowrap; }

.topbar-right { display: flex; align-items: center; gap: 10px; flex-wrap: wrap; }

.filtros-fecha {
  display: flex; align-items: center; gap: 6px;
  background: var(--surface2); border: 1px solid var(--border);
  border-radius: 9px; padding: 5px 10px;
}
.filtro-label { font-size: 10px; font-weight: 700; color: var(--text-sub); white-space: nowrap; }
.date-input {
  background: transparent; border: none;
  color: var(--text); font-size: 11px; font-family: inherit;
  cursor: pointer;
}
.date-input:focus { outline: none; }

.filtros-rapidos {
  display: flex; align-items: center; gap: 4px;
}
.btn-rapido {
  padding: 5px 10px; border-radius: 7px;
  font-size: 11px; font-weight: 700;
  background: var(--surface2); border: 1px solid var(--border);
  color: var(--text-sub); cursor: pointer;
  transition: background 0.15s, color 0.15s, border-color 0.15s;
}
.btn-rapido:hover { color: var(--text); border-color: var(--accent); }
.btn-rapido.active { background: var(--accent); color: #fff; border-color: var(--accent); }
.btn-rapido.btn-clear { padding: 5px 8px; }

.btn-limpiar {
  color: var(--text-sub); font-size: 12px; padding: 2px 5px;
  border-radius: 4px; transition: color 0.15s;
}
.btn-limpiar:hover { color: var(--accent); }

.btn-nuevo {
  background: var(--accent); color: #fff;
  padding: 7px 14px; border-radius: 8px;
  font-size: 12px; font-weight: 700;
  transition: opacity 0.15s; white-space: nowrap;
}
.btn-nuevo:hover { opacity: 0.88; }
</style>
