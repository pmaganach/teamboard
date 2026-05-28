<template>
  <div class="kanban">
    <div
      v-for="col in columnas"
      :key="col.id"
      class="columna"
      :class="{ 'drag-over': dragSobre === col.id }"
      @dragover.prevent="dragSobre = col.id"
      @dragleave="dragSobre = null"
      @drop="soltar(col.id)"
    >
      <!-- Header columna -->
      <div class="col-header" :style="{ '--cc': col.color }">
        <span class="col-titulo">{{ col.label }}</span>
        <span class="col-count">{{ tarjetasPor(col.id).length }}</span>
      </div>

      <!-- Tarjetas -->
      <div class="tarjetas">
        <div
          v-for="t in tarjetasPor(col.id)"
          :key="t.id"
          class="tarjeta"
          draggable="true"
          @dragstart="arrastrar(t)"
          @dragend="dragSobre = null"
          @click="$emit('editar', t)"
        >
          <div class="tarjeta-nombre">{{ t.nombre }}</div>

          <div class="tarjeta-meta">
            <span class="tarjeta-area">{{ t.area_cliente }}</span>
            <span class="prio" :class="t.prioridad">{{ t.prioridad }}</span>
          </div>

          <div class="tarjeta-footer">
            <div class="resp" v-if="usuario(t.responsable_id)" :style="{ background: usuario(t.responsable_id).color + '22', color: usuario(t.responsable_id).color }">
              {{ usuario(t.responsable_id).iniciales }}
            </div>
            <div class="resp area-resp" v-else>{{ (t.area_equipo || '?').slice(0, 2).toUpperCase() }}</div>

            <div class="prog-mini" v-if="t.progreso">
              <div class="prog-track">
                <div class="prog-fill" :style="{ width: t.progreso + '%' }"></div>
              </div>
              <span>{{ t.progreso }}%</span>
            </div>

            <span class="sla" v-if="t.fecha_sla">{{ fmtFecha(t.fecha_sla) }}</span>
          </div>
        </div>

        <!-- Zona vacía -->
        <div v-if="!tarjetasPor(col.id).length" class="col-vacia">
          Sin trabajos
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { cambiarEstado } from '../api/trabajos'

const props = defineProps({
  trabajos: { type: Array, default: () => [] },
  usuarios: { type: Array, default: () => [] },
})
const emit = defineEmits(['editar', 'actualizado'])

const columnas = [
  { id: 'por_comenzar', label: 'Por comenzar', color: '#a78bfa' },
  { id: 'en_gestion',   label: 'En gestión',   color: '#3b82f6' },
  { id: 'en_revision',  label: 'En revisión',  color: '#f59e0b' },
  { id: 'pendiente',    label: 'Pendiente',    color: '#f97316' },
  { id: 'completado',   label: 'Completado',   color: '#10b981' },
]

const tarjetaArrastrada = ref(null)
const dragSobre         = ref(null)

const tarjetasPor = (estado) => props.trabajos.filter(t => t.estado === estado)
const usuario     = (id)     => props.usuarios.find(u => u.id === id)
const fmtFecha    = (f)      => f ? f.split('-').reverse().join('-') : '—'

function arrastrar(t) {
  tarjetaArrastrada.value = t
}

async function soltar(nuevoEstado) {
  dragSobre.value = null
  if (!tarjetaArrastrada.value) return
  if (tarjetaArrastrada.value.estado === nuevoEstado) return
  await cambiarEstado(tarjetaArrastrada.value.id, nuevoEstado)
  emit('actualizado')
  tarjetaArrastrada.value = null
}
</script>

<style scoped>
.kanban {
  display: flex;
  gap: 14px;
  align-items: flex-start;
  overflow-x: auto;
  padding-bottom: 12px;
  min-height: 60vh;
}

.columna {
  flex: 0 0 240px;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 12px;
  overflow: hidden;
  transition: border-color 0.15s, box-shadow 0.15s;
}
.columna.drag-over {
  border-color: var(--accent);
  box-shadow: 0 0 0 2px var(--accent-dim);
}

.col-header {
  display: flex; align-items: center; justify-content: space-between;
  padding: 12px 14px;
  border-bottom: 2px solid var(--cc);
  background: var(--surface2);
}
.col-titulo { font-size: 12px; font-weight: 700; color: var(--text); }
.col-count  {
  font-size: 11px; font-weight: 800;
  background: var(--cc); color: #fff;
  padding: 1px 7px; border-radius: 10px;
}

.tarjetas { display: flex; flex-direction: column; gap: 8px; padding: 10px; min-height: 80px; }

.tarjeta {
  background: var(--card-bg);
  border: 1px solid var(--border);
  border-radius: 9px;
  padding: 11px 12px;
  cursor: grab;
  display: flex; flex-direction: column; gap: 8px;
  transition: box-shadow 0.15s, transform 0.1s;
  user-select: none;
}
.tarjeta:hover { box-shadow: 0 2px 12px #0004; transform: translateY(-1px); }
.tarjeta:active { cursor: grabbing; }

.tarjeta-nombre { font-size: 12px; font-weight: 700; color: var(--text); line-height: 1.3; }

.tarjeta-meta { display: flex; align-items: center; justify-content: space-between; gap: 6px; }
.tarjeta-area { font-size: 10px; color: var(--text-sub); flex: 1; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

.prio {
  font-size: 9px; font-weight: 800; padding: 1px 6px; border-radius: 4px;
  text-transform: uppercase; flex-shrink: 0;
}
.prio.alta  { background: #ED002F18; color: #ED002F; }
.prio.media { background: #eab30818; color: #eab308; }
.prio.baja  { background: #38bdf818; color: #38bdf8; }

.tarjeta-footer { display: flex; align-items: center; gap: 8px; }
.resp {
  width: 22px; height: 22px; border-radius: 50%; font-size: 8px; font-weight: 800;
  display: flex; align-items: center; justify-content: center; flex-shrink: 0;
}
.area-resp { background: var(--surface2); color: var(--text-sub); }

.prog-mini { display: flex; align-items: center; gap: 4px; flex: 1; }
.prog-track { flex: 1; height: 4px; background: var(--border); border-radius: 2px; }
.prog-fill  { height: 100%; background: var(--accent); border-radius: 2px; }
.prog-mini span { font-size: 9px; color: var(--text-sub); }

.sla { font-size: 9px; color: var(--text-sub); margin-left: auto; white-space: nowrap; }

.col-vacia {
  text-align: center; font-size: 11px; color: var(--text-sub);
  padding: 20px 0; opacity: 0.6;
}
</style>
