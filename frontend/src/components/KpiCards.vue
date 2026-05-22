<template>
  <div class="kpi-row">
    <div v-for="k in kpis" :key="k.label" class="kpi-card" :style="{ '--kc': k.color }">
      <div class="kpi-value">{{ k.valor }}</div>
      <div class="kpi-label">{{ k.label }}</div>
      <div class="kpi-bar"><div class="kpi-fill" :style="{ width: pct(k.valor) + '%' }"></div></div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({ trabajos: { type: Array, default: () => [] } })

const total = computed(() => props.trabajos.length)

function count(estado) {
  return props.trabajos.filter(t => t.estado === estado).length
}

const kpis = computed(() => [
  { label: 'Total trabajos',  valor: total.value,                color: '#ED002F' },
  { label: 'Por comenzar',    valor: count('por_comenzar'),      color: '#636466' },
  { label: 'En gestión',      valor: count('en_gestion'),        color: '#3b82f6' },
  { label: 'En revisión',     valor: count('en_revision'),       color: '#f59e0b' },
  { label: 'Pendientes',      valor: count('pendiente'),         color: '#f97316' },
  { label: 'Completados',     valor: count('completado'),        color: '#10b981' },
])

function pct(val) {
  return total.value ? Math.round((val / total.value) * 100) : 0
}
</script>

<style scoped>
.kpi-row {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 12px;
  margin-bottom: 28px;
}
@media (max-width: 1100px) { .kpi-row { grid-template-columns: repeat(3, 1fr); } }

.kpi-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 16px;
  display: flex; flex-direction: column; gap: 4px;
  border-top: 3px solid var(--kc);
}
.kpi-value {
  font-size: 28px; font-weight: 800;
  color: var(--kc); line-height: 1;
}
.kpi-label {
  font-size: 11px; color: var(--text-sub);
  font-weight: 600; text-transform: uppercase; letter-spacing: 0.4px;
}
.kpi-bar {
  height: 3px; background: var(--border); border-radius: 2px; margin-top: 8px;
}
.kpi-fill {
  height: 100%; background: var(--kc); border-radius: 2px;
  transition: width 0.4s ease;
}
</style>
