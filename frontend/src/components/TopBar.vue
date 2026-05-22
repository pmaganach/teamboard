<template>
  <header class="topbar">
    <div class="topbar-left">
      <h1 class="topbar-title">{{ titulo }}</h1>
      <span class="topbar-sub">{{ sub }}</span>
    </div>
    <div class="topbar-right">
      <slot name="filtros" />

      <!-- Filtros de fecha globales -->
      <div class="filtros-fecha">
        <label class="filtro-label">Desde</label>
        <input type="date" v-model="desde" class="date-input" />
        <label class="filtro-label">Hasta</label>
        <input type="date" v-model="hasta" class="date-input" />
        <button v-if="desde || hasta" class="btn-limpiar" @click="limpiar" title="Limpiar filtros">
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
import { useFiltros } from '../composables/useFiltros'

defineProps({
  titulo: { type: String, default: 'TeamBoard' },
  sub:    { type: String, default: '' },
})
defineEmits(['nuevo'])

const { desde, hasta, limpiar } = useFiltros()
</script>

<style scoped>
.topbar {
  display: flex; align-items: center; justify-content: space-between;
  padding: 14px 24px;
  background: var(--topbar-bg);
  border-bottom: 1px solid var(--border);
  gap: 16px; flex-wrap: wrap;
}
.topbar-left { display: flex; align-items: baseline; gap: 10px; }
.topbar-title { font-size: 16px; font-weight: 700; color: var(--text); }
.topbar-sub   { font-size: 11px; color: var(--text-sub); }

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
