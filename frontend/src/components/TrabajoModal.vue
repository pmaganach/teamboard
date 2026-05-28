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
            <label><span class="lbl-dot" style="background:#a78bfa"></span>Nombre del trabajo *</label>
            <input v-model="form.nombre" placeholder="Ej: Dashboard Comercial" :disabled="!esMiTrabajo" />
          </div>

          <!-- Área + Responsable en fila (responsable solo para gerente) -->
          <div :class="isGerente ? 'campo-fila' : 'campo'">
            <div class="campo">
              <label><span class="lbl-dot" style="background:#3b82f6"></span>Área *</label>
              <select v-model="form.area_cliente" :disabled="!esMiTrabajo">
                <option value="">Seleccionar área...</option>
                <option v-for="a in areas" :key="a.id" :value="a.nombre">{{ a.icono }} {{ a.nombre }}</option>
              </select>
            </div>
            <div class="campo" v-if="isGerente">
              <label><span class="lbl-dot" style="background:#f59e0b"></span>Responsable *</label>
              <div class="avatares">
                <!-- Opción equipo (visible para analistas) -->
                <div
                  v-if="!isGerente"
                  class="av av-equipo"
                  :class="{ selected: form.responsable_id === null }"
                  @click="form.responsable_id = null"
                  title="Tarea del equipo"
                >👥</div>
                <!-- Mi propio avatar (analista) -->
                <div
                  v-if="!isGerente && miUsuario"
                  class="av"
                  :class="{ selected: form.responsable_id === miUsuario.id }"
                  :style="{ background: miUsuario.color + '22', color: miUsuario.color }"
                  :title="miUsuario.nombre"
                  @click="form.responsable_id = miUsuario.id"
                >{{ miUsuario.iniciales }}</div>
                <!-- Todos los analistas (gerente, multiselección) -->
                <template v-if="isGerente">
                  <div
                    class="av av-none"
                    :class="{ selected: form.responsables_ids.length === 0 }"
                    @click="form.responsables_ids = []"
                    title="Sin asignar"
                  >—</div>
                  <div
                    class="av av-todos"
                    :class="{ selected: todosSeleccionados }"
                    @click="seleccionarTodos"
                    title="Todos"
                  >All</div>
                  <div
                    v-for="u in analistas" :key="u.id"
                    class="av"
                    :class="{ selected: form.responsables_ids.includes(u.id) }"
                    :style="{ background: u.color + '22', color: u.color }"
                    :title="u.nombre"
                    @click="toggleResponsable(u.id)"
                  >{{ u.iniciales }}</div>
                </template>
              </div>
            </div>
          </div>

          <!-- Estado pills -->
          <div class="sep-label">Estado</div>
          <div class="campo">
            <div class="pills-estado">
              <button
                v-for="(cfg, key) in ESTADOS" :key="key"
                class="pill-estado"
                :class="{ active: form.estado === key }"
                :style="form.estado === key
                  ? { background: cfg.color + '20', color: cfg.color, borderColor: cfg.color + '70', fontWeight: 600 }
                  : { background: 'transparent', color: 'var(--text-sub)', borderColor: 'var(--border)' }"
                :disabled="!esMiTrabajo"
                @click="form.estado = form.estado === key ? null : key"
              ><span class="pill-dot" :style="{ background: cfg.color }"></span>{{ cfg.label }}</button>
            </div>
          </div>

          <!-- Prioridad pills -->
          <div class="sep-label">Prioridad</div>
          <div class="campo">
            <div class="pills-prio">
              <button
                v-for="(cfg, key) in PRIORIDADES" :key="key"
                class="pill-prio"
                :class="{ active: form.prioridad === key }"
                :style="form.prioridad === key
                  ? { background: cfg.color + '20', color: cfg.color, borderColor: cfg.color + '70', fontWeight: 600 }
                  : { background: 'transparent', color: 'var(--text-sub)', borderColor: 'var(--border)' }"
                :disabled="!esMiTrabajo"
                @click="form.prioridad = form.prioridad === key ? null : key"
              ><span class="pill-dot" :style="{ background: cfg.color }"></span>{{ cfg.label }}</button>
            </div>
          </div>

          <!-- Magnitud + Tipo -->
          <div class="sep-label">Detalles</div>

          <div class="campo">
            <label><span class="lbl-dot" style="background:#10b981"></span>Magnitud</label>
            <div class="pills-generic">
              <button
                v-for="(cfg, key) in MAGNITUDES" :key="key"
                class="pill-generic"
                :class="{ active: form.magnitud === key }"
                :style="form.magnitud === key
                  ? { background: cfg.color + '20', color: cfg.color, borderColor: cfg.color + '70', fontWeight: 600 }
                  : { background: 'transparent', color: 'var(--text-sub)', borderColor: 'var(--border)' }"
                :disabled="!esMiTrabajo"
                @click="form.magnitud = form.magnitud === key ? null : key"
              ><span class="pill-dot" :style="{ background: cfg.color }"></span>{{ cfg.label }}</button>
            </div>
          </div>

          <div class="campo">
            <label><span class="lbl-dot" style="background:#6366f1"></span>Tipo</label>
            <div class="pills-generic">
              <button
                v-for="(cfg, key) in TIPOS" :key="key"
                class="pill-generic"
                :class="{ active: form.tipo === key }"
                :style="form.tipo === key
                  ? { background: cfg.color + '20', color: cfg.color, borderColor: cfg.color + '70', fontWeight: 600 }
                  : { background: 'transparent', color: 'var(--text-sub)', borderColor: 'var(--border)' }"
                :disabled="!esMiTrabajo"
                @click="form.tipo = form.tipo === key ? null : key"
              ><span class="pill-dot" :style="{ background: cfg.color }"></span>{{ cfg.label }}</button>
            </div>
          </div>

          <!-- Progreso segmentado -->
          <div class="campo">
            <label><span class="lbl-dot" style="background:#ED002F"></span>Progreso *</label>
            <div class="prog-segs">
              <button
                v-for="v in [0, 25, 50, 75, 100]" :key="v"
                class="prog-seg"
                :class="{ active: form.progreso === v }"
                :disabled="!esMiTrabajo"
                @click="form.progreso = form.progreso === v ? null : v"
              >{{ v }}%</button>
            </div>
          </div>

          <!-- Fechas -->
          <div class="campo-fila">
            <div class="campo">
              <label><span class="lbl-dot" style="background:#06b6d4"></span>Fecha inicio *</label>
              <input type="date" v-model="form.fecha_inicio" />
            </div>
            <div class="campo">
              <label><span class="lbl-dot" style="background:#f97316"></span>Fecha SLA estimada *</label>
              <input type="date" v-model="form.fecha_sla" />
            </div>
          </div>

          <!-- Comentarios -->
          <div class="campo">
            <label><span class="lbl-dot" style="background:#636466"></span>Comentarios</label>
            <textarea v-model="form.comentarios" placeholder="Notas adicionales, contexto, links..." rows="2" @input="autoResize" ref="txtComentarios"></textarea>
          </div>

        </div>

        <div class="modal-footer">
          <button class="btn-secundario" @click="cerrar">Cancelar</button>
          <button v-if="form.id && esMiTrabajo" class="btn-danger" @click="eliminar">Eliminar</button>
          <button class="btn-primario" @click="guardar" :disabled="!esMiTrabajo || !form.nombre || !form.area_cliente || form.estado === null || form.prioridad === null || form.progreso === null">
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
  por_comenzar: { label: 'Por comenzar', color: '#a78bfa' },
  en_gestion:   { label: 'En gestión',   color: '#3b82f6' },
  en_revision:  { label: 'En revisión',  color: '#f59e0b' },
  pendiente:    { label: 'Pendiente',    color: '#f97316' },
  completado:   { label: 'Completado',   color: '#10b981' },
}

const PRIORIDADES = {
  baja:  { label: 'Baja',  color: '#38bdf8' },
  media: { label: 'Media', color: '#eab308' },
  alta:  { label: 'Alta',  color: '#ED002F' },
}

const MAGNITUDES = {
  rapido:   { label: 'Rápido',   color: '#10b981' },
  moderado: { label: 'Moderado', color: '#3b82f6' },
  extenso:  { label: 'Extenso',  color: '#f59e0b' },
  complejo: { label: 'Complejo', color: '#ED002F' },
}

const TIPOS = {
  puntual:    { label: 'Puntual',    color: '#6366f1' },
  recurrente: { label: 'Recurrente', color: '#f97316' },
  iniciativa: { label: 'Iniciativa', color: '#0ea5e9' },
}

const areas     = reactive([])
const analistas = reactive([])
const miUsuario = computed(() => analistas.find(u => u.id === user.value?.usuario_id) || null)

const form = reactive({
  id:               null,
  nombre:           '',
  area_cliente:     '',
  responsable_id:   null,
  responsables_ids: [],
  area_equipo:      null,
  estado:         null,
  prioridad:      null,
  magnitud:       null,
  tipo:           null,
  progreso:       null,
  fecha_inicio:   new Date().toISOString().split('T')[0],
  fecha_sla:      null,
  comentarios:    null,
})

// Gerente: edita todo. Analista: solo sus propias tareas (por responsable_id o responsables_ids)
const esMiTrabajo = computed(() => {
  if (!form.id) return true          // tarea nueva
  if (isGerente.value) return true   // gerente siempre
  const uid = user.value?.usuario_id
  if (form.responsable_id === uid) return true
  if (form.responsables_ids?.length) {
    return form.responsables_ids.includes(uid)
  }
  return false
})

onMounted(async () => {
  const [a, u] = await Promise.all([getAreas(), getUsuarios()])
  areas.push(...a)
  analistas.push(...u.filter(x => x.rol === 'analista'))

  if (props.trabajo) {
    let responsables_ids = []
    if (props.trabajo.responsables_ids) {
      try { responsables_ids = JSON.parse(props.trabajo.responsables_ids) } catch { /* ignore */ }
    } else if (props.trabajo.responsable_id) {
      responsables_ids = [props.trabajo.responsable_id]
    }
    Object.assign(form, {
      id:               props.trabajo.id,
      nombre:           props.trabajo.nombre,
      area_cliente:     props.trabajo.area_cliente,
      responsable_id:   props.trabajo.responsable_id,
      responsables_ids: responsables_ids,
      area_equipo:      props.trabajo.area_equipo,
      estado:         props.trabajo.estado,
      prioridad:      props.trabajo.prioridad,
      magnitud:       props.trabajo.magnitud   || null,
      tipo:           props.trabajo.tipo       || null,
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

const todosSeleccionados = computed(() =>
  analistas.length > 0 && analistas.every(u => form.responsables_ids.includes(u.id))
)

function seleccionarTodos() {
  if (todosSeleccionados.value) {
    form.responsables_ids = []
  } else {
    form.responsables_ids = analistas.map(u => u.id)
  }
}

function toggleResponsable(id) {
  const idx = form.responsables_ids.indexOf(id)
  if (idx === -1) form.responsables_ids.push(id)
  else form.responsables_ids.splice(idx, 1)
}

async function guardar() {
  const datos = {
    nombre:           form.nombre,
    area_cliente:     form.area_cliente,
    responsable_id:   isGerente.value ? (form.responsables_ids[0] ?? null) : form.responsable_id,
    responsables_ids: isGerente.value ? form.responsables_ids : null,
    area_equipo:      form.area_equipo,
    estado:         form.estado,
    prioridad:      form.prioridad,
    magnitud:       form.magnitud  || null,
    tipo:           form.tipo      || null,
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
.modal-header.estado-por_comenzar::before { background: #a78bfa; }
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
.campo label { font-size: 10px; font-weight: 700; color: var(--text-sub); text-transform: uppercase; letter-spacing: 0.5px; display: flex; align-items: center; gap: 5px; }
.lbl-dot { width: 6px; height: 6px; border-radius: 50%; flex-shrink: 0; }

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

.sep-label {
  display: flex; align-items: center; gap: 10px;
  color: var(--text-sub); font-size: 9px; font-weight: 700;
  text-transform: uppercase; letter-spacing: 0.6px;
}
.sep-label::before, .sep-label::after {
  content: ''; flex: 1; height: 1px; background: var(--border);
}

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
.av-none   { background: var(--surface2); color: var(--text-sub); font-size: 15px; font-weight: 400; }
.av-equipo { background: var(--surface2); color: var(--text-sub); font-size: 14px; }
.av-todos  { background: var(--accent-dim); color: var(--accent); font-size: 9px; font-weight: 800; letter-spacing: 0.5px; }

/* ── Dot dentro de cada pill ── */
.pill-dot {
  width: 6px; height: 6px; border-radius: 50%; flex-shrink: 0;
}

/* ── Estado pills ── */
.pills-estado { display: flex; gap: 5px; flex-wrap: wrap; }
.pill-estado {
  padding: 5px 11px; border-radius: 20px;
  font-size: 11px; font-weight: 500;
  border: 1px solid; cursor: pointer; transition: all 0.15s;
  display: flex; align-items: center; gap: 6px;
}
.pill-estado:hover:not(:disabled) { color: var(--text) !important; border-color: var(--text-sub) !important; }
.pill-estado.active:hover:not(:disabled) { filter: brightness(1.15); color: inherit !important; border-color: inherit !important; }
.pill-estado:disabled { cursor: default; opacity: 0.4; }

/* ── Prioridad pills ── */
.pills-prio { display: flex; gap: 6px; }
.pill-prio {
  flex: 1; padding: 7px; border-radius: 8px;
  font-size: 11px; font-weight: 500;
  border: 1px solid; cursor: pointer; transition: all 0.15s;
  display: flex; align-items: center; justify-content: center; gap: 6px;
}
.pill-prio:hover:not(:disabled) { color: var(--text) !important; border-color: var(--text-sub) !important; }
.pill-prio.active:hover:not(:disabled) { filter: brightness(1.15); color: inherit !important; border-color: inherit !important; }
.pill-prio:disabled { cursor: default; opacity: 0.4; }

/* ── Magnitud / Tipo pills genéricos ── */
.pills-generic { display: flex; gap: 6px; flex-wrap: wrap; }
.pill-generic {
  flex: 1; padding: 7px; border-radius: 8px;
  font-size: 11px; font-weight: 500;
  border: 1px solid; cursor: pointer; transition: all 0.15s; white-space: nowrap;
  display: flex; align-items: center; justify-content: center; gap: 6px;
}
.pill-generic:hover:not(:disabled) { color: var(--text) !important; border-color: var(--text-sub) !important; }
.pill-generic.active:hover:not(:disabled) { filter: brightness(1.15); color: inherit !important; border-color: inherit !important; }
.pill-generic:disabled { cursor: default; opacity: 0.4; }

/* ── Progreso segmentado ── */
.prog-segs { display: flex; gap: 5px; }
.prog-seg {
  flex: 1; padding: 7px 4px; border-radius: 8px;
  font-size: 11px; font-weight: 700; text-align: center;
  border: 1px solid var(--border);
  background: transparent; color: var(--text-sub);
  cursor: pointer; transition: all 0.15s;
  position: relative; overflow: hidden;
}
.prog-seg::after {
  content: ''; position: absolute;
  bottom: 0; left: 0; height: 3px; border-radius: 0 0 8px 8px;
  transition: width 0.2s;
}
.prog-seg:nth-child(1)::after { width: 0%;   background: #636466; }
.prog-seg:nth-child(2)::after { width: 25%;  background: #f59e0b; }
.prog-seg:nth-child(3)::after { width: 50%;  background: #f59e0b; }
.prog-seg:nth-child(4)::after { width: 75%;  background: #10b981; }
.prog-seg:nth-child(5)::after { width: 100%; background: #10b981; }
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
