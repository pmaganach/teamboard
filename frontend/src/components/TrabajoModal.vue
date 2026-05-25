<template>
  <Teleport to="body">
    <div class="overlay" @click.self="cerrar">
      <div class="modal">

        <div class="modal-header" :class="'estado-' + form.estado">
          <h2 class="modal-title">{{ form.id ? 'Editar trabajo' : 'Nuevo trabajo' }}</h2>
          <button class="btn-cerrar" @click="cerrar">&#x2715;</button>
        </div>

        <div class="modal-body">

          <!-- Nombre -->
          <div class="campo">
            <label>Nombre del trabajo *</label>
            <input v-model="form.nombre" placeholder="Ej: Dashboard Comercial" />
          </div>

          <!-- Área + Responsable (gerente) en fila -->
          <div :class="isGerente ? 'campo-fila' : ''">
            <div class="campo">
              <label>Área *</label>
              <select v-model="form.area_cliente">
                <option value="">Seleccionar área...</option>
                <option v-for="a in areas" :key="a.id" :value="a.nombre">{{ a.icono }} {{ a.nombre }}</option>
              </select>
            </div>
            <div class="campo" v-if="isGerente">
              <label>Responsable *</label>
              <div class="avatares">
                <div
                  class="av av-none"
                  :class="{ selected: form.responsable_id === null }"
                  @click="form.responsable_id = null"
                  title="Sin asignar"
                >—</div>
                <div
                  v-for="u in analistas" :key="u.id"
                  class="av"
                  :class="{ selected: form.responsable_id === u.id }"
                  :style="{ background: u.color + '22', color: u.color }"
                  :title="u.nombre"
                  @click="form.responsable_id = u.id"
                >{{ u.iniciales }}</div>
              </div>
            </div>
          </div>

          <hr class="sep" />

          <!-- Estado pills -->
          <div class="campo">
            <label>Estado *</label>
            <div class="pills-estado">
              <button
                v-for="(cfg, key) in ESTADOS" :key="key"
                class="pill-estado"
                :class="{ active: form.estado === key }"
                :style="form.estado === key ? { background: cfg.color + '18', color: cfg.color, borderColor: cfg.color + '60' } : {}"
                :disabled="!esMiTrabajo"
                @click="form.estado = key"
              >{{ cfg.label }}</button>
            </div>
          </div>

          <!-- Prioridad pills -->
          <div class="campo">
            <label>Prioridad *</label>
            <div class="pills-prio">
              <button
                v-for="(cfg, key) in PRIORIDADES" :key="key"
                class="pill-prio"
                :class="{ active: form.prioridad === key }"
                :style="form.prioridad === key ? { background: cfg.color + '18', color: cfg.color, borderColor: cfg.color + '60' } : {}"
                :disabled="!esMiTrabajo"
                @click="form.prioridad = key"
              >{{ cfg.label }}</button>
            </div>
          </div>

          <!-- Progreso segmentado -->
          <div class="campo">
            <label>Progreso *</label>
            <div class="prog-segs">
              <button
                v-for="v in [0, 25, 50, 75, 100]" :key="v"
                class="prog-seg"
                :class="{ active: form.progreso === v }"
                :disabled="!esMiTrabajo"
                @click="form.progreso = v"
              >{{ v }}%</button>
            </div>
          </div>

          <!-- Fechas -->
          <div class="campo-fila">
            <div class="campo">
              <label>Fecha inicio *</label>
              <input type="date" v-model="form.fecha_inicio" />
            </div>
            <div class="campo">
              <label>Fecha SLA estimada *</label>
              <input type="date" v-model="form.fecha_sla" />
            </div>
          </div>

          <!-- Comentarios -->
          <div class="campo">
            <label>Comentarios</label>
            <textarea v-model="form.comentarios" placeholder="Notas adicionales, contexto, links..." rows="2" @input="autoResize" ref="txtComentarios"></textarea>
          </div>

        </div>

        <div class="modal-footer">
          <button class="btn-secundario" @click="cerrar">Cancelar</button>
          <button v-if="form.id" class="btn-danger" @click="eliminar">Eliminar</button>
          <button class="btn-primario" @click="guardar" :disabled="!form.nombre || !form.area_cliente || form.estado === null || form.prioridad === null || form.progreso === null">
            {{ form.id ? 'Guardar cambios' : 'Crear trabajo' }}
          </button>
        </div>

      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { reactive, computed, onMounted, ref } from 'vue'
import { getAreas }    from '../api/areas'
import { getUsuarios } from '../api/usuarios'
import { createTrabaj, updateTrabaj, deleteTrabaj } from '../api/trabajos'
import { useAuth } from '../composables/useAuth'

const props = defineProps({
  trabajo: { type: Object, default: null },
})
const emit = defineEmits(['cerrar', 'actualizado'])

const { user, isGerente } = useAuth()

const ESTADOS = {
  por_comenzar: { label: 'Por comenzar', color: '#636466' },
  en_gestion:   { label: 'En gestión',   color: '#3b82f6' },
  en_revision:  { label: 'En revisión',  color: '#f59e0b' },
  pendiente:    { label: 'Pendiente',    color: '#f97316' },
  completado:   { label: 'Completado',   color: '#10b981' },
}

const PRIORIDADES = {
  baja:  { label: 'Baja',  color: '#636466' },
  media: { label: 'Media', color: '#f59e0b' },
  alta:  { label: 'Alta',  color: '#ED002F' },
}

const areas    = reactive([])
const analistas = reactive([])

const form = reactive({
  id:             null,
  nombre:         '',
  area_cliente:   '',
  responsable_id: null,
  area_equipo:    null,
  estado:         null,
  prioridad:      null,
  progreso:       null,
  fecha_inicio:   new Date().toISOString().split('T')[0],
  fecha_sla:      null,
  comentarios:    null,
})

// Un analista solo puede editar estado/progreso de sus propios trabajos
const esMiTrabajo = computed(() =>
  !form.id || isGerente.value || form.responsable_id === user.value?.usuario_id
)

onMounted(async () => {
  const [a, u] = await Promise.all([getAreas(), getUsuarios()])
  areas.push(...a)
  analistas.push(...u.filter(x => x.rol === 'analista'))

  if (props.trabajo) {
    Object.assign(form, {
      id:             props.trabajo.id,
      nombre:         props.trabajo.nombre,
      area_cliente:   props.trabajo.area_cliente,
      responsable_id: props.trabajo.responsable_id,
      area_equipo:    props.trabajo.area_equipo,
      estado:         props.trabajo.estado,
      prioridad:      props.trabajo.prioridad,
      progreso:       props.trabajo.progreso,
      fecha_inicio:   props.trabajo.fecha_inicio,
      fecha_sla:      props.trabajo.fecha_sla,
      comentarios:    props.trabajo.comentarios,
    })
  } else {
    // Nuevo trabajo: asignar automáticamente al usuario actual si es analista
    if (!isGerente.value) {
      form.responsable_id = user.value?.usuario_id || null
    }
  }
})

async function guardar() {
  const datos = {
    nombre:         form.nombre,
    area_cliente:   form.area_cliente,
    responsable_id: form.responsable_id,
    area_equipo:    form.area_equipo,
    estado:         form.estado,
    prioridad:      form.prioridad,
    progreso:       form.progreso,
    fecha_inicio:   form.fecha_inicio || null,
    fecha_sla:      form.fecha_sla || null,
    comentarios:    form.comentarios || null,
  }
  if (form.id) {
    await updateTrabaj(form.id, datos)
  } else {
    await createTrabaj(datos)
  }
  emit('actualizado')
  cerrar()
}

async function eliminar() {
  if (!confirm('¿Eliminar este trabajo?')) return
  await deleteTrabaj(form.id)
  emit('actualizado')
  cerrar()
}

const txtComentarios = ref(null)
function autoResize(e) {
  e.target.style.height = 'auto'
  e.target.style.height = e.target.scrollHeight + 'px'
}

function cerrar() {
  emit('cerrar')
}
</script>

<style scoped>
.overlay {
  position: fixed; inset: 0;
  background: #0008;
  display: flex; align-items: center; justify-content: center;
  z-index: 1000; padding: 20px;
}

.modal {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 16px;
  width: 100%; max-width: 520px;
  max-height: 90vh; overflow-y: auto;
  box-shadow: 0 20px 60px #0006;
}

/* ── Header con acento de estado ── */
.modal-header {
  display: flex; align-items: center; justify-content: space-between;
  padding: 16px 20px; border-bottom: 1px solid var(--border);
  position: relative;
}
.modal-header::before {
  content: ''; position: absolute;
  top: 0; left: 0; right: 0; height: 7px;
  border-radius: 16px 16px 0 0;
}
.modal-header.estado-por_comenzar::before { background: #636466; }
.modal-header.estado-en_gestion::before   { background: #3b82f6; }
.modal-header.estado-en_revision::before  { background: #f59e0b; }
.modal-header.estado-pendiente::before    { background: #f97316; }
.modal-header.estado-completado::before   { background: #10b981; }

.modal-title { font-size: 14px; font-weight: 700; color: var(--text); }
.btn-cerrar {
  color: var(--text-sub); font-size: 16px;
  width: 28px; height: 28px; border-radius: 6px;
  display: flex; align-items: center; justify-content: center;
  transition: background 0.15s;
}
.btn-cerrar:hover { background: var(--surface2); color: var(--text); }

/* ── Body ── */
.modal-body { padding: 20px; display: flex; flex-direction: column; gap: 14px; }

.campo { display: flex; flex-direction: column; gap: 6px; }
.campo label { font-size: 10px; font-weight: 700; color: var(--text-sub); text-transform: uppercase; letter-spacing: 0.5px; }

.campo input, .campo select, .campo textarea {
  background: var(--surface2); border: 1px solid var(--border);
  border-radius: 8px; padding: 9px 12px;
  color: var(--text); font-size: 13px; font-family: inherit;
  transition: border-color 0.15s; width: 100%;
}
.campo textarea { resize: none; overflow: hidden; }
.campo input:focus, .campo select:focus, .campo textarea:focus {
  outline: none; border-color: var(--accent);
}
.campo select option { background: var(--surface2); }

.campo-fila { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }

.sep { border: none; border-top: 1px solid var(--border); }

/* ── Avatares responsable ── */
.avatares { display: flex; gap: 7px; flex-wrap: wrap; padding-top: 2px; }
.av {
  width: 34px; height: 34px; border-radius: 50%;
  font-size: 10px; font-weight: 800;
  display: flex; align-items: center; justify-content: center;
  cursor: pointer; border: 2px solid transparent;
  transition: all 0.15s; opacity: 0.4;
}
.av:hover { opacity: 0.75; }
.av.selected { opacity: 1; border-color: var(--border); box-shadow: 0 0 0 3px var(--surface2); }
.av-none { background: var(--surface2); color: var(--text-sub); font-size: 15px; font-weight: 400; }

/* ── Estado pills ── */
.pills-estado { display: flex; gap: 5px; flex-wrap: wrap; }
.pill-estado {
  padding: 5px 11px; border-radius: 20px;
  font-size: 11px; font-weight: 600;
  border: 1px solid var(--border);
  background: transparent; color: var(--text-sub);
  cursor: pointer; transition: all 0.15s;
}
.pill-estado:hover:not(:disabled) { color: var(--text); border-color: var(--text-sub); }
.pill-estado:disabled { cursor: default; opacity: 0.5; }

/* ── Prioridad pills ── */
.pills-prio { display: flex; gap: 6px; }
.pill-prio {
  flex: 1; padding: 7px; border-radius: 8px;
  font-size: 11px; font-weight: 700; text-align: center;
  border: 1px solid var(--border);
  background: transparent; color: var(--text-sub);
  cursor: pointer; transition: all 0.15s;
}
.pill-prio:hover:not(:disabled) { color: var(--text); border-color: var(--text-sub); }
.pill-prio:disabled { cursor: default; opacity: 0.5; }

/* ── Progreso segmentado ── */
.prog-segs { display: flex; gap: 5px; }
.prog-seg {
  flex: 1; padding: 7px 4px; border-radius: 8px;
  font-size: 11px; font-weight: 700; text-align: center;
  border: 1px solid var(--border);
  background: transparent; color: var(--text-sub);
  cursor: pointer; transition: all 0.15s;
}
.prog-seg:hover:not(:disabled) { color: var(--text); border-color: var(--text-sub); }
.prog-seg.active { background: var(--accent); color: #fff; border-color: var(--accent); opacity: 1; }
.prog-seg:disabled { cursor: default; opacity: 0.5; }

/* ── Footer ── */
.modal-footer {
  display: flex; align-items: center; justify-content: flex-end; gap: 8px;
  padding: 14px 20px; border-top: 1px solid var(--border);
}

.btn-primario {
  background: var(--accent); color: #fff;
  padding: 8px 18px; border-radius: 8px;
  font-size: 13px; font-weight: 700; transition: opacity 0.15s;
}
.btn-primario:hover:not(:disabled) { opacity: 0.88; }
.btn-primario:disabled { opacity: 0.4; cursor: not-allowed; }

.btn-secundario {
  background: var(--surface2); border: 1px solid var(--border);
  color: var(--text-sub); padding: 8px 14px; border-radius: 8px;
  font-size: 13px; font-weight: 600; transition: background 0.15s;
}
.btn-secundario:hover { background: var(--border); }

.btn-danger {
  background: #ED002F18; border: 1px solid #ED002F44;
  color: #ED002F; padding: 8px 14px; border-radius: 8px;
  font-size: 13px; font-weight: 700; margin-right: auto; transition: background 0.15s;
}
.btn-danger:hover { background: #ED002F28; }
</style>
