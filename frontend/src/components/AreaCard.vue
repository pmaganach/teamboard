<template>
  <div class="area-card" :style="{ '--ac': area.color }">
    <div class="area-header">
      <span class="area-icono">{{ area.icono }}</span>
      <div class="area-info">
        <div class="area-nombre">{{ area.nombre }}</div>
        <div class="area-encargado" v-if="area.encargado">{{ area.encargado }}</div>
      </div>
      <span class="area-count">{{ trabajos.length }}</span>
    </div>

    <div v-if="trabajos.length" class="trabajos-list">
      <div v-for="t in trabajos" :key="t.id" class="trabajo-row" @click="$emit('editar', t)">
        <span class="row-dot" :style="{ background: estadoColor(t.estado) }"></span>
        <span class="row-nombre">{{ t.nombre }}</span>
        <span class="row-estado" :style="{ color: estadoColor(t.estado) }">{{ estadoLabel(t.estado) }}</span>
      </div>
    </div>
    <div v-else class="empty">Sin trabajos de área</div>
  </div>
</template>

<script setup>
defineProps({
  area:     { type: Object, required: true },
  trabajos: { type: Array,  default: () => [] },
})
defineEmits(['editar'])

const ESTADOS = {
  por_comenzar: { label: 'Por comenzar', color: '#a78bfa' },
  en_gestion:   { label: 'En gestión',   color: '#3b82f6' },
  en_revision:  { label: 'En revisión',  color: '#f59e0b' },
  pendiente:    { label: 'Pendiente',    color: '#f97316' },
  completado:   { label: 'Completado',   color: '#10b981' },
}
const estadoLabel = (e) => ESTADOS[e]?.label || e
const estadoColor = (e) => ESTADOS[e]?.color || '#636466'
</script>

<style scoped>
.area-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-left: 4px solid var(--ac);
  border-radius: 12px;
  padding: 14px 16px;
  display: flex; flex-direction: column; gap: 10px;
}
.area-header { display: flex; align-items: center; gap: 10px; }
.area-icono  { font-size: 20px; flex-shrink: 0; }
.area-info   { flex: 1; }
.area-nombre    { font-size: 13px; font-weight: 700; color: var(--text); }
.area-encargado { font-size: 11px; color: var(--text-sub); }
.area-count {
  font-size: 18px; font-weight: 800; color: var(--ac);
  background: var(--ac); background: color-mix(in srgb, var(--ac) 15%, transparent);
  padding: 2px 8px; border-radius: 6px;
}

.trabajos-list { display: flex; flex-direction: column; gap: 4px; }
.trabajo-row {
  display: flex; align-items: center; gap: 8px;
  padding: 6px 10px; border-radius: 8px;
  background: var(--surface2);
  cursor: pointer; transition: background 0.15s;
}
.trabajo-row:hover { background: var(--border); }
.row-dot {
  width: 7px; height: 7px; border-radius: 50%; flex-shrink: 0;
}
.row-nombre {
  flex: 1; font-size: 11px; font-weight: 600; color: var(--text);
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
.row-estado { font-size: 10px; font-weight: 600; flex-shrink: 0; }
.empty { font-size: 11px; color: var(--text-sub); }
</style>
