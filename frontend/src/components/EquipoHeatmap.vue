<template>
  <div class="heatmap-wrap">
    <table class="hm-table">
      <thead>
        <tr>
          <th class="th-name">Persona</th>
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
        <tr v-for="u in usuarios" :key="u.id" class="hm-row" @click="$emit('verUsuario', u)">
          <td>
            <div class="hm-person">
              <div class="hm-av" :style="{ background: u.color + '22', color: u.color }">{{ u.iniciales }}</div>
              <div>
                <div class="hm-nombre">{{ u.nombre }}</div>
                <div class="hm-rol">{{ u.rol }}</div>
              </div>
            </div>
          </td>
          <td v-for="e in estados" :key="e.id" class="hm-cell">
            <div class="hm-bubble" :class="bubbleClass(countPor(u.id, e.id), e.id)">
              {{ countPor(u.id, e.id) || '—' }}
            </div>
          </td>
          <td class="hm-total">{{ trabajosPorUsuario(u.id).length }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
const props = defineProps({
  usuarios: { type: Array, default: () => [] },
  trabajos: { type: Array, default: () => [] },
})
defineEmits(['verUsuario'])

const estados = [
  { id: 'por_comenzar', label: 'Por comenzar', color: '#a78bfa' },
  { id: 'en_gestion',   label: 'En gestión',   color: '#3b82f6' },
  { id: 'en_revision',  label: 'En revisión',  color: '#f59e0b' },
  { id: 'pendiente',    label: 'Pendiente',    color: '#f97316' },
  { id: 'completado',   label: 'Completado',   color: '#10b981' },
]

const trabajosPorUsuario = (uid) => props.trabajos.filter(t => t.responsable_id === uid)
const countPor = (uid, estado) => props.trabajos.filter(t => t.responsable_id === uid && t.estado === estado).length

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
  border-bottom: 1px solid var(--border);
  white-space: nowrap;
}
th.th-name { text-align: left; min-width: 180px; }

.th-col { display: flex; flex-direction: column; align-items: center; gap: 4px; }
.th-dot { width: 7px; height: 7px; border-radius: 50%; }

.hm-row { cursor: pointer; transition: background 0.15s; }
.hm-row:hover td { background: var(--surface2); }
td { padding: 8px 10px; border-bottom: 1px solid var(--border); }
.hm-row:last-child td { border-bottom: none; }

.hm-person { display: flex; align-items: center; gap: 8px; }
.hm-av {
  width: 28px; height: 28px; border-radius: 50%;
  font-size: 9px; font-weight: 800; flex-shrink: 0;
  display: flex; align-items: center; justify-content: center;
}
.hm-nombre { font-size: 12px; font-weight: 600; color: var(--text); }
.hm-rol    { font-size: 10px; color: var(--text-sub); text-transform: capitalize; }

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
