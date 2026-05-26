<template>
  <div class="agenda-wrap">
    <table class="agenda-table">
      <thead>
        <tr>
          <th class="col-nombre">Área</th>
          <th v-for="d in dias" :key="d.iso" class="col-dia" :class="{ hoy: d.esHoy, finde: d.esFinde }">
            <div class="dia-nombre">{{ d.nombre }}</div>
            <div class="dia-num" :class="{ hoy: d.esHoy, finde: d.esFinde }">{{ d.num }}</div>
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="area in areas" :key="area.id">
          <td class="cell-nombre">
            <div class="area-row">
              <span class="area-icono">{{ area.icono }}</span>
              <span class="area-name">{{ area.nombre }}</span>
            </div>
          </td>
          <td v-for="d in dias" :key="d.iso" class="cell-dia" :class="{ hoy: d.esHoy, finde: d.esFinde }">
            <div
              v-for="t in trabajosEnDia(area.nombre, d.iso)"
              :key="t.id"
              class="bloque"
              :style="{ background: colorEstado(t.estado) + '18', borderColor: colorEstado(t.estado), color: colorEstado(t.estado) }"
              :title="t.nombre + ' · ' + estadoLabel(t.estado)"
              @click="$emit('editar', t)"
            >
              <span class="bloque-texto">{{ t.nombre }}</span>
              <span class="bloque-estado">{{ estadoLabel(t.estado) }}</span>
            </div>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
const props = defineProps({
  dias:     { type: Array, required: true },
  areas:    { type: Array, default: () => [] },
  trabajos: { type: Array, default: () => [] },
})
defineEmits(['editar'])

const ESTADOS = {
  por_comenzar: { label: 'Por comenzar', color: '#636466' },
  en_gestion:   { label: 'En gestión',   color: '#3b82f6' },
  en_revision:  { label: 'En revisión',  color: '#f59e0b' },
  pendiente:    { label: 'Pendiente',    color: '#f97316' },
  completado:   { label: 'Completado',   color: '#10b981' },
}
const estadoLabel  = (e) => ESTADOS[e]?.label || e
const colorEstado  = (e) => ESTADOS[e]?.color || '#636466'

function trabajosEnDia(areaNombre, isoDay) {
  return props.trabajos.filter(t => {
    if (t.area_cliente !== areaNombre) return false
    if (!t.fecha_inicio) return false
    const fin = t.fecha_sla || t.fecha_inicio
    return isoDay >= t.fecha_inicio && isoDay <= fin
  })
}
</script>

<style scoped>
.agenda-wrap { overflow-x: auto; border-radius: 12px; border: 1px solid var(--border); }

.agenda-table { width: 100%; border-collapse: collapse; min-width: 800px; }

th {
  background: var(--surface);
  border-bottom: 1px solid var(--border);
  padding: 10px 8px;
  font-size: 10px; font-weight: 700; text-transform: uppercase;
  letter-spacing: 0.5px; color: var(--text-sub);
  white-space: nowrap;
}
.col-nombre { width: 160px; text-align: left; padding-left: 14px; }
.col-dia    { text-align: center; }
.col-dia.hoy   { background: var(--accent-dim); }
.col-dia.finde { background: var(--surface2); opacity: 0.6; }

.dia-nombre { font-size: 10px; color: var(--text-sub); }
.dia-num {
  font-size: 15px; font-weight: 800; color: var(--text); margin-top: 2px;
  width: 28px; height: 28px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center; margin: 2px auto 0;
}
.dia-num.hoy   { background: var(--accent); color: #fff; }
.dia-num.finde { color: var(--text-sub); }

tr { border-bottom: 1px solid var(--border); }
tr:last-child { border-bottom: none; }

.cell-nombre {
  padding: 8px 8px 8px 14px;
  background: var(--surface);
  border-right: 1px solid var(--border);
  vertical-align: middle;
}
.area-row  { display: flex; align-items: center; gap: 7px; }
.area-icono { font-size: 14px; flex-shrink: 0; }
.area-name  { font-size: 11px; font-weight: 600; color: var(--text); line-height: 1.3; }

.cell-dia {
  padding: 5px 4px; vertical-align: top;
  min-width: 100px; min-height: 48px;
}
.cell-dia.hoy   { background: var(--accent-dim); }
.cell-dia.finde { background: var(--surface2); opacity: 0.7; }

.bloque {
  border-left: 3px solid;
  border-radius: 5px;
  padding: 3px 6px;
  margin-bottom: 3px;
  cursor: pointer;
  transition: filter 0.15s;
}
.bloque:hover { filter: brightness(1.2); }
.bloque-texto {
  display: block; font-size: 10px; font-weight: 700;
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 120px;
}
.bloque-estado { font-size: 9px; opacity: 0.8; }
</style>
