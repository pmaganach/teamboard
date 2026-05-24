<template>
  <div class="kpi-wrap">
    <!-- Donut -->
    <div class="donut-wrap">
      <svg :width="size" :height="size" :viewBox="`0 0 ${size} ${size}`" style="transform:rotate(-90deg);flex-shrink:0">
        <circle
          :cx="cx" :cy="cy" :r="r"
          fill="none" stroke="var(--border)" :stroke-width="sw"
        />
        <circle
          v-for="(k, i) in arcos" :key="k.label"
          :cx="cx" :cy="cy" :r="r"
          fill="none"
          :stroke="k.color"
          :stroke-width="sw"
          :stroke-dasharray="circunf"
          :stroke-dashoffset="k.offset"
          stroke-linecap="butt"
        />
      </svg>
      <div class="donut-center" :style="{ width: size + 'px', height: size + 'px' }">
        <span class="donut-num">{{ total }}</span>
        <span class="donut-lbl">trabajos</span>
      </div>

      <!-- Lista -->
      <div class="kpi-list">
        <div v-for="k in estados" :key="k.label" class="kpi-row">
          <div class="kpi-dot" :style="{ background: k.color }"></div>
          <span class="kpi-label">{{ k.label }}</span>
          <div class="kpi-bar-wrap">
            <div class="kpi-bar">
              <div class="kpi-fill" :style="{ width: pct(k.valor) + '%', background: k.color }"></div>
            </div>
          </div>
          <span class="kpi-num" :style="{ color: k.color }">{{ k.valor }}</span>
          <span class="kpi-pct">{{ pct(k.valor) }}%</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({ trabajos: { type: Array, default: () => [] } })

const size = 110
const cx   = size / 2
const cy   = size / 2
const r    = 40
const sw   = 14
const circunf = computed(() => 2 * Math.PI * r)

const total = computed(() => props.trabajos.length)

function count(estado) {
  return props.trabajos.filter(t => t.estado === estado).length
}

const estados = computed(() => [
  { label: 'Por comenzar', valor: count('por_comenzar'), color: '#636466' },
  { label: 'En gestión',   valor: count('en_gestion'),   color: '#3b82f6' },
  { label: 'En revisión',  valor: count('en_revision'),  color: '#f59e0b' },
  { label: 'Pendiente',    valor: count('pendiente'),    color: '#f97316' },
  { label: 'Completado',   valor: count('completado'),   color: '#10b981' },
])

function pct(val) {
  return total.value ? Math.round((val / total.value) * 100) : 0
}

const arcos = computed(() => {
  let acum = 0
  return estados.value.map(k => {
    const dash  = (k.valor / (total.value || 1)) * circunf.value
    const offset = circunf.value - acum
    acum += dash
    return { ...k, offset }
  })
})
</script>

<style scoped>
.kpi-wrap {
  margin-bottom: 28px;
}

.donut-wrap {
  display: flex; align-items: center; gap: 24px;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 20px 24px;
  position: relative;
}

.donut-center {
  position: absolute;
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  pointer-events: none;
  left: 24px;
}
.donut-num { font-size: 22px; font-weight: 900; color: var(--text); line-height: 1; }
.donut-lbl { font-size: 9px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; color: var(--text-sub); }

.kpi-list {
  flex: 1; display: flex; flex-direction: column; gap: 9px;
}

.kpi-row {
  display: flex; align-items: center; gap: 9px;
}
.kpi-dot   { width: 7px; height: 7px; border-radius: 50%; flex-shrink: 0; }
.kpi-label { font-size: 11px; color: var(--text-sub); width: 90px; flex-shrink: 0; }
.kpi-bar-wrap { flex: 1; }
.kpi-bar   { height: 4px; background: var(--border); border-radius: 2px; }
.kpi-fill  { height: 100%; border-radius: 2px; transition: width 0.4s ease; }
.kpi-num   { font-size: 12px; font-weight: 800; width: 20px; text-align: right; flex-shrink: 0; }
.kpi-pct   { font-size: 10px; color: var(--text-sub); width: 30px; text-align: right; flex-shrink: 0; }
</style>
