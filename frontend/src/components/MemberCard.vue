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
      <!-- Nube de pensamientos -->
      <button class="btn-nube" @click.stop="abrirNotas" title="Notas">
        💭
        <span v-if="tieneNoNLeidas" class="badge-nuevo"></span>
      </button>
    </div>

    <div v-if="trabajos.length" class="trabajos-list">
      <div v-for="t in trabajos" :key="t.id" class="trabajo-chip" :style="{ '--ec': estadoColor(t.estado) }" @click.stop="$emit('editar', t)">
        <span class="chip-dot"></span>
        <span class="chip-nombre">{{ t.nombre }}</span>
        <span class="chip-estado">{{ estadoLabel(t.estado) }}</span>
      </div>
    </div>
    <div v-else class="empty">Sin trabajos activos</div>

    <NotaPostit
      v-if="postitAbierto"
      :usuario="usuario"
      :usuarios="usuarios"
      @cerrar="postitAbierto = false"
      @actualizado="cargarConteo"
    />

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import NotaPostit from './NotaPostit.vue'
import { getNotas } from '../api/usuarios'
import { useAuth } from '../composables/useAuth'

const props = defineProps({
  usuario:  { type: Object, required: true },
  trabajos: { type: Array,  default: () => [] },
  usuarios: { type: Array,  default: () => [] },
})
defineEmits(['editar'])

const { user } = useAuth()

const postitAbierto    = ref(false)
const hayNoLeidas      = ref(false)

// Gerentes ven notif en todas las cards; analistas solo en la suya
const tieneNoNLeidas = computed(() => {
  if (!hayNoLeidas.value) return false
  if (user.value?.rol === 'gerente') return true
  return props.usuario.id === user.value?.usuario_id ||
         props.usuario.nombre === user.value?.nombre
})

async function cargarConteo() {
  const r = await getNotas(props.usuario.id)
  hayNoLeidas.value = r.data.some(n => !n.leida)
}

function abrirNotas() {
  postitAbierto.value = true
}

onMounted(cargarConteo)

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

.card-header { display: flex; align-items: center; gap: 10px; position: relative; }

.btn-nube {
  margin-left: auto; border: none;
  font-size: 18px; cursor: pointer; position: relative;
  padding: 5px 7px; line-height: 1;
  background: var(--accent-dim);
  border-radius: 10px;
  box-shadow: 0 1px 3px #0001, inset 0 1px 0 #ffffff18;
  transition: background 0.18s, transform 0.18s, box-shadow 0.18s;
}
.btn-nube:hover {
  background: var(--accent);
  transform: scale(1.13);
  box-shadow: 0 2px 8px #0002;
}
.badge-nuevo {
  position: absolute; top: 0; right: 0;
  width: 8px; height: 8px; border-radius: 50%;
  background: #ef4444;
  animation: pulso 1.5s ease-in-out infinite;
}
@keyframes pulso {
  0%, 100% { transform: scale(1);   opacity: 1; }
  50%       { transform: scale(1.4); opacity: 0.6; }
}
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
