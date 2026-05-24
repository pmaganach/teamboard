<template>
  <div class="heatmap-wrap">
    <table class="hm-table">
      <thead>
        <tr>
          <th class="th-name">Área</th>
          <th v-for="e in estados" :key="e.id">
            <div class="th-col">
              <div class="th-dot" :style="{ background: e.color }"></div>
              <span>{{ e.label }}</span>
            </div>
          </th>
          <th>Total</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="a in areas" :key="a.id" class="hm-row">
          <td>
            <div class="hm-area">
              <span class="hm-icono">{{ a.icono }}</span>
              <div>
                <div class="hm-nombre">{{ a.nombre }}</div>
                <div class="hm-encargado" v-if="a.encargado">{{ a.encargado }}</div>
              </div>
            </div>
          </td>
          <td v-for="e in estados" :key="e.id" class="hm-cell">
            <div class="hm-bubble" :class="bubbleClass(countPor(a.nombre, e.id), e.id)">
              {{ countPor(a.nombre, e.id) || '—' }}
            </div>
          </td>
          <td class="hm-total">{{ trabajosPorArea(a.nombre).length }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
const props = defineProps({
  areas:    { type: Array, default: () => [] },
  trabajos: { type: Array, default: () => [] },
})

const estados = [
  { id: 'por_comenzar', label: 'Por comenzar', color: '#636466' },
  { id: 'en_gestion',   label: 'En gestión',   color: '#3b82f6' },
  { id: 'en_revision',  label: 'En revisión',  color: '#f59e0b' },
  { id: 'pendiente',    label: 'Pendiente',    color: '#f97316' },
  { id: 'completado',   label: 'Completado',   color: '#10b981' },
]

const trabajosPorArea = (nombre) => props.trabajos.filter(t => t.area_cliente === nombre)
const countPor = (nombre, estado) => props.trabajos.filter(t => t.area_cliente === nombre && t.estado === estado).length

function bubbleClass(count, estado) {
  if (!count) return 'b-empty'
  if (estado === 'completado') return 'b-done'
  if (estado === 'pendiente' && count >= 2) return 'b-warn'
  if (count >= 3) return 'b-high'
  if (count >= 1) return 'b-low'
  return 'b-empty'
}
</script>

<style scoped>
.heatmap-wrap { overflow-x: auto; }
.hm-table { width: 100%; border-collapse: collapse; }

th {
  padding: 8px 12px; text-align: center;
  font-size: 10px; font-weight: 700; text-transform: uppercase;
  letter-spacing: 0.5px; color: var(--text-sub);
  border-bottom: 1px solid var(--border); white-space: nowrap;
}
th.th-name { text-align: left; min-width: 200px; }
.th-col { display: flex; flex-direction: column; align-items: center; gap: 4px; }
.th-dot { width: 7px; height: 7px; border-radius: 50%; }

.hm-row { transition: background 0.15s; }
.hm-row:hover td { background: var(--surface2); }
td { padding: 8px 10px; border-bottom: 1px solid var(--border); }
.hm-row:last-child td { border-bottom: none; }

.hm-area { display: flex; align-items: center; gap: 10px; }
.hm-icono   { font-size: 18px; flex-shrink: 0; }
.hm-nombre  { font-size: 12px; font-weight: 600; color: var(--text); }
.hm-encargado { font-size: 10px; color: var(--text-sub); }

.hm-cell { text-align: center; }
.hm-bubble {
  display: inline-flex; align-items: center; justify-content: center;
  width: 32px; height: 32px; border-radius: 8px;
  font-size: 13px; font-weight: 800;
}
.b-empty { background: transparent; color: var(--border); }
.b-low   { background: var(--accent-dim); color: var(--accent); }
.b-high  { background: #3b82f630; color: #3b82f6; }
.b-warn  { background: #f9731620; color: #f97316; }
.b-done  { background: #10b98118; color: #10b981; }

.hm-total { text-align: center; font-size: 12px; font-weight: 800; color: var(--text-sub); }
</style>
