<template>
  <div class="desglose">
    <div class="desglose-header">
      <h3 class="desglose-title">Desglose completo</h3>
      <span class="desglose-count">{{ trabajos.length }} trabajos</span>
    </div>

    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Responsable</th>
            <th>Trabajo</th>
            <th>Área cliente</th>
            <th>Progreso</th>
            <th>SLA</th>
            <th>Prioridad</th>
            <th>Estado</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="t in trabajos" :key="t.id" class="data-row" @click="$emit('editar', t)">
            <td>
              <div class="resp-cell" v-if="usuario(t.responsable_id)">
                <div class="mini-av"
                  :style="{ background: usuario(t.responsable_id).color + '22', color: usuario(t.responsable_id).color }">
                  {{ usuario(t.responsable_id).iniciales }}
                </div>
                <span>{{ usuario(t.responsable_id).nombre }}</span>
              </div>
              <span v-else class="area-tag">{{ t.area_equipo || '—' }}</span>
            </td>
            <td class="nombre-cell">{{ t.nombre }}</td>
            <td class="sub-cell">{{ t.area_cliente }}</td>
            <td class="prog-cell">
              <div class="prog-wrap">
                <div class="prog-bar">
                  <div class="prog-fill" :style="{ width: t.progreso + '%', background: progColor(t.progreso) }"></div>
                </div>
                <span class="prog-pct">{{ t.progreso }}%</span>
              </div>
            </td>
            <td class="sub-cell">{{ fmtFecha(t.fecha_sla) }}</td>
            <td>
              <span class="prio-badge" :class="t.prioridad">{{ t.prioridad }}</span>
            </td>
            <td>
              <span class="estado-badge" :style="{ color: estadoColor(t.estado), background: estadoColor(t.estado) + '18' }">
                {{ estadoLabel(t.estado) }}
              </span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  trabajos: { type: Array, default: () => [] },
  usuarios: { type: Array, default: () => [] },
})
defineEmits(['editar'])

const usuario   = (id) => props.usuarios.find(u => u.id === id)
const fmtFecha  = (f) => f ? f.split('-').reverse().join('-') : '—'

const ESTADOS = {
  por_comenzar: { label: 'Por comenzar', color: '#636466' },
  en_gestion:   { label: 'En gestión',   color: '#3b82f6' },
  en_revision:  { label: 'En revisión',  color: '#f59e0b' },
  pendiente:    { label: 'Pendiente',    color: '#f97316' },
  completado:   { label: 'Completado',   color: '#10b981' },
}
const estadoLabel = (e) => ESTADOS[e]?.label || e
const estadoColor = (e) => ESTADOS[e]?.color || '#636466'
const progColor   = (p) => p >= 75 ? '#10b981' : p >= 40 ? '#f59e0b' : '#636466'
</script>

<style scoped>
.desglose {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 14px;
  overflow: hidden;
}
.desglose-header {
  display: flex; align-items: center; justify-content: space-between;
  padding: 14px 18px; border-bottom: 1px solid var(--border);
}
.desglose-title { font-size: 13px; font-weight: 700; color: var(--text); }
.desglose-count { font-size: 11px; color: var(--text-sub); }

.table-wrap { overflow-x: auto; }
table { width: 100%; border-collapse: collapse; }
th {
  padding: 10px 14px; text-align: left;
  font-size: 10px; font-weight: 700; text-transform: uppercase;
  letter-spacing: 0.5px; color: var(--text-sub);
  border-bottom: 1px solid var(--border);
  white-space: nowrap;
}
td { padding: 10px 14px; border-bottom: 1px solid var(--border); }
.data-row { cursor: pointer; transition: background 0.15s; }
.data-row:hover { background: var(--surface2); }
.data-row:last-child td { border-bottom: none; }

.resp-cell { display: flex; align-items: center; gap: 7px; }
.mini-av {
  width: 24px; height: 24px; border-radius: 50%;
  font-size: 9px; font-weight: 800; flex-shrink: 0;
  display: flex; align-items: center; justify-content: center;
}
.area-tag { font-size: 11px; color: var(--text-sub); }
.nombre-cell { font-size: 12px; font-weight: 600; color: var(--text); max-width: 200px; }
.sub-cell    { font-size: 11px; color: var(--text-sub); white-space: nowrap; }

.prog-wrap { display: flex; align-items: center; gap: 6px; }
.prog-bar  { width: 60px; height: 5px; background: var(--border); border-radius: 3px; }
.prog-fill { height: 100%; border-radius: 3px; transition: width 0.3s; }
.prog-pct  { font-size: 10px; color: var(--text-sub); }

.prio-badge {
  font-size: 10px; font-weight: 700; padding: 2px 7px; border-radius: 5px;
  text-transform: capitalize;
}
.prio-badge.alta  { background: #ED002F18; color: #ED002F; }
.prio-badge.media { background: #f59e0b18; color: #f59e0b; }
.prio-badge.baja  { background: #63646618; color: #636466; }

.estado-badge {
  font-size: 10px; font-weight: 700; padding: 2px 8px; border-radius: 5px;
  white-space: nowrap;
}
</style>
