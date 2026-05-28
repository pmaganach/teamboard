<template>
  <div class="agenda-wrap">
    <table class="agenda-table">
      <thead>
        <tr>
          <th class="col-nombre">Persona</th>
          <th v-for="d in dias" :key="d.iso" class="col-dia" :class="{ hoy: d.esHoy }">
            <div class="dia-nombre">{{ d.nombre }}</div>
            <div class="dia-num" :class="{ hoy: d.esHoy }">{{ d.num }}</div>
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="persona in personas" :key="persona.id">
          <td class="cell-nombre">
            <div class="persona-row">
              <div class="av" :style="{ background: persona.color + '22', color: persona.color }">
                {{ persona.iniciales }}
              </div>
              <span class="persona-name">{{ persona.nombre.split(' ')[0] }}</span>
            </div>
          </td>
          <td v-for="d in dias" :key="d.iso" class="cell-dia" :class="{ hoy: d.esHoy }">
            <div
              v-for="t in trabajosEnDia(persona.id, d.iso)"
              :key="t.id"
              class="bloque"
              :style="{ background: persona.color + '28', borderColor: persona.color, color: persona.color }"
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
  personas: { type: Array, default: () => [] },
  trabajos: { type: Array, default: () => [] },
})
defineEmits(['editar'])

const ESTADOS = {
  por_comenzar: 'Por comenzar',
  en_gestion:   'En gestión',
  en_revision:  'En revisión',
  pendiente:    'Pendiente',
  completado:   'Completado',
}
const estadoLabel = (e) => ESTADOS[e] || e

function esResponsable(t, uid) {
  if (t.responsable_id === uid) return true
  if (t.responsables_ids) {
    try { return JSON.parse(t.responsables_ids).includes(uid) } catch { /* ignore */ }
  }
  return false
}

function trabajosEnDia(uid, isoDay) {
  return props.trabajos.filter(t => {
    if (!esResponsable(t, uid)) return false
    if (!t.fecha_inicio) return false
    const inicio = t.fecha_inicio
    const fin    = t.fecha_sla || t.fecha_inicio
    return isoDay >= inicio && isoDay <= fin
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
.col-nombre { width: 140px; text-align: left; padding-left: 14px; }
.col-dia    { text-align: center; }
.col-dia.hoy { background: var(--accent-dim); }

.dia-nombre { font-size: 10px; color: var(--text-sub); }
.dia-num    {
  font-size: 15px; font-weight: 800; color: var(--text); margin-top: 2px;
  width: 28px; height: 28px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center; margin: 2px auto 0;
}
.dia-num.hoy { background: var(--accent); color: #fff; }

tr { border-bottom: 1px solid var(--border); }
tr:last-child { border-bottom: none; }

.cell-nombre {
  padding: 8px 8px 8px 14px;
  background: var(--surface);
  border-right: 1px solid var(--border);
  vertical-align: middle;
}
.persona-row { display: flex; align-items: center; gap: 7px; }
.av {
  width: 26px; height: 26px; border-radius: 50%;
  font-size: 9px; font-weight: 800; flex-shrink: 0;
  display: flex; align-items: center; justify-content: center;
}
.persona-name { font-size: 11px; font-weight: 600; color: var(--text); }

.cell-dia {
  padding: 5px 4px; vertical-align: top;
  min-width: 100px; min-height: 48px;
  transition: background 0.15s;
}
.cell-dia.hoy { background: var(--accent-dim); }

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
