<template>
  <div class="member-card">
    <div class="card-header">
      <div class="avatar" :style="{ background: usuario.color + '22', color: usuario.color, borderColor: usuario.color }">
        {{ usuario.iniciales }}
      </div>
      <div class="member-info">
        <div class="member-name">{{ usuario.nombre }}</div>
        <div class="member-meta">
          <span class="badge-rol" :class="usuario.rol">{{ usuario.rol }}</span>
          <span class="count">{{ trabajos.length }} trabajo{{ trabajos.length !== 1 ? 's' : '' }}</span>
        </div>
      </div>
    </div>

    <div v-if="trabajos.length" class="trabajos-list">
      <div v-for="t in trabajos" :key="t.id" class="trabajo-chip" :style="{ '--ec': estadoColor(t.estado) }" @click="$emit('editar', t)">
        <span class="chip-dot"></span>
        <span class="chip-nombre">{{ t.nombre }}</span>
        <span class="chip-estado">{{ estadoLabel(t.estado) }}</span>
      </div>
    </div>
    <div v-else class="empty">Sin trabajos activos</div>
  </div>
</template>

<script setup>
defineProps({
  usuario:  { type: Object, required: true },
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
.member-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 16px;
  display: flex; flex-direction: column; gap: 12px;
  transition: border-color 0.2s;
}
.member-card:hover { border-color: var(--accent); }

.card-header { display: flex; align-items: center; gap: 10px; }
.avatar {
  width: 40px; height: 40px; border-radius: 50%;
  font-size: 13px; font-weight: 800;
  display: flex; align-items: center; justify-content: center;
  border: 2px solid; flex-shrink: 0;
}
.member-name { font-size: 13px; font-weight: 700; color: var(--text); }
.member-meta { display: flex; align-items: center; gap: 8px; margin-top: 2px; }

.badge-rol {
  font-size: 9px; font-weight: 700; text-transform: uppercase;
  letter-spacing: 0.5px; padding: 2px 6px; border-radius: 4px;
}
.badge-rol.analista { background: var(--accent-dim); color: var(--accent); }
.badge-rol.gerente  { background: #f59e0b22; color: #f59e0b; }

.count { font-size: 11px; color: var(--text-sub); }

.trabajos-list { display: flex; flex-direction: column; gap: 5px; }
.trabajo-chip {
  display: flex; align-items: center; gap: 7px;
  padding: 6px 10px; border-radius: 8px;
  background: var(--surface2); cursor: pointer;
  transition: background 0.15s;
}
.trabajo-chip:hover { background: var(--border); }
.chip-dot {
  width: 8px; height: 8px; border-radius: 50%;
  background: var(--ec); flex-shrink: 0;
}
.chip-nombre {
  flex: 1; font-size: 11px; font-weight: 600; color: var(--text);
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
.chip-estado {
  font-size: 10px; color: var(--ec); font-weight: 600;
  white-space: nowrap; flex-shrink: 0;
}
.empty { font-size: 11px; color: var(--text-sub); padding: 4px 0; }
</style>
