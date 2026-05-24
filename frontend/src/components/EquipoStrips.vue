<template>
  <div class="strips-wrap">
    <div v-for="u in usuarios" :key="u.id" class="strip-row">
      <div class="strip-person">
        <div class="strip-av" :style="{ background: u.color + '22', color: u.color }">{{ u.iniciales }}</div>
        <div>
          <div class="strip-nombre">{{ u.nombre }}</div>
          <div class="strip-count">{{ trabajosPorUsuario(u.id).length }} trabajos</div>
        </div>
      </div>

      <div class="strip-bar">
        <div
          v-for="t in trabajosPorUsuario(u.id)"
          :key="t.id"
          class="strip-block"
          :style="{ background: estadoColor(t.estado) + '28', color: estadoColor(t.estado), borderColor: estadoColor(t.estado) + '44' }"
          :title="t.nombre + ' · ' + estadoLabel(t.estado)"
          @click="$emit('editar', t)"
        >
          {{ t.nombre }}
        </div>
        <div v-if="!trabajosPorUsuario(u.id).length" class="strip-empty">Sin trabajos</div>
      </div>

      <div class="strip-pct" :style="{ color: pctColor(progProm(u.id)) }">
        {{ progProm(u.id) }}%
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  usuarios: { type: Array, default: () => [] },
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
const estadoLabel = (e) => ESTADOS[e]?.label || e
const estadoColor = (e) => ESTADOS[e]?.color || '#636466'

const trabajosPorUsuario = (uid) => props.trabajos.filter(t => t.responsable_id === uid)

function progProm(uid) {
  const ts = trabajosPorUsuario(uid)
  if (!ts.length) return 0
  return Math.round(ts.reduce((s, t) => s + t.progreso, 0) / ts.length)
}

const pctColor = (p) => p >= 75 ? '#10b981' : p >= 40 ? '#f59e0b' : '#636466'
</script>

<style scoped>
.strips-wrap { display: flex; flex-direction: column; gap: 2px; }

.strip-row {
  display: flex; align-items: center; gap: 14px;
  padding: 10px 14px; border-radius: 10px;
  transition: background 0.15s;
}
.strip-row:hover { background: var(--surface2); }

.strip-person { display: flex; align-items: center; gap: 8px; width: 160px; flex-shrink: 0; }
.strip-av {
  width: 30px; height: 30px; border-radius: 50%;
  font-size: 9px; font-weight: 800; flex-shrink: 0;
  display: flex; align-items: center; justify-content: center;
}
.strip-nombre { font-size: 12px; font-weight: 600; color: var(--text); line-height: 1.2; }
.strip-count  { font-size: 10px; color: var(--text-sub); }

.strip-bar {
  flex: 1; display: flex; gap: 4px; flex-wrap: wrap; align-items: center; min-height: 32px;
}
.strip-block {
  height: 28px; border-radius: 6px; border: 1px solid;
  display: flex; align-items: center;
  font-size: 10px; font-weight: 600;
  padding: 0 8px; white-space: nowrap;
  cursor: pointer; transition: filter 0.15s;
  max-width: 160px; overflow: hidden; text-overflow: ellipsis;
}
.strip-block:hover { filter: brightness(1.15); }
.strip-empty { font-size: 11px; color: var(--text-sub); }

.strip-pct { width: 36px; text-align: right; font-size: 12px; font-weight: 800; flex-shrink: 0; }
</style>
