<template>
  <Teleport to="body">
    <div class="overlay" @click.self="cerrar">
      <div class="modal">
        <div class="modal-header">
          <h2 class="modal-title">{{ form.id ? 'Editar trabajo' : 'Nuevo trabajo' }}</h2>
          <button class="btn-cerrar" @click="cerrar">&#x2715;</button>
        </div>

        <div class="modal-body">
          <!-- Nombre -->
          <div class="campo">
            <label>Nombre del trabajo *</label>
            <input v-model="form.nombre" placeholder="Ej: Dashboard Comercial Q2" />
          </div>

          <!-- Área cliente -->
          <div class="campo">
            <label>Área cliente *</label>
            <select v-model="form.area_cliente">
              <option value="">Seleccionar área...</option>
              <option v-for="a in areas" :key="a.id" :value="a.nombre">{{ a.icono }} {{ a.nombre }}</option>
            </select>
          </div>

          <!-- Responsable -->
          <div class="campo">
            <label>Responsable</label>
            <select v-model="form.responsable_id" @change="onResponsableChange">
              <option :value="null">Sin asignar (tarea de área)</option>
              <option v-for="u in analistas" :key="u.id" :value="u.id">{{ u.nombre }}</option>
            </select>
          </div>

          <!-- Área equipo (solo si sin responsable) -->
          <div class="campo" v-if="!form.responsable_id">
            <label>Área del equipo</label>
            <input v-model="form.area_equipo" placeholder="Ej: Análisis · Reportería" />
          </div>

          <!-- Fila: Estado + Prioridad -->
          <div class="campo-fila">
            <div class="campo">
              <label>Estado</label>
              <select v-model="form.estado">
                <option value="por_comenzar">Por comenzar</option>
                <option value="en_gestion">En gestión</option>
                <option value="en_revision">En revisión</option>
                <option value="pendiente">Pendiente</option>
                <option value="completado">Completado</option>
              </select>
            </div>
            <div class="campo">
              <label>Prioridad</label>
              <select v-model="form.prioridad">
                <option value="alta">Alta</option>
                <option value="media">Media</option>
                <option value="baja">Baja</option>
              </select>
            </div>
          </div>

          <!-- Progreso -->
          <div class="campo">
            <label>Progreso — <strong>{{ form.progreso }}%</strong></label>
            <input type="range" min="0" max="100" v-model.number="form.progreso" class="slider" />
            <div class="prog-preview">
              <div class="prog-bar">
                <div class="prog-fill" :style="{ width: form.progreso + '%' }"></div>
              </div>
            </div>
          </div>

          <!-- Fecha SLA -->
          <div class="campo">
            <label>Fecha SLA estimada</label>
            <input type="date" v-model="form.fecha_sla" />
          </div>
        </div>

        <div class="modal-footer">
          <button class="btn-secundario" @click="cerrar">Cancelar</button>
          <button v-if="form.id" class="btn-danger" @click="eliminar">Eliminar</button>
          <button class="btn-primario" @click="guardar" :disabled="!form.nombre || !form.area_cliente">
            {{ form.id ? 'Guardar cambios' : 'Crear trabajo' }}
          </button>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { reactive, onMounted } from 'vue'
import { getAreas }    from '../api/areas'
import { getUsuarios } from '../api/usuarios'
import { createTrabaj, updateTrabaj, deleteTrabaj } from '../api/trabajos'

const props = defineProps({
  trabajo: { type: Object, default: null },
})
const emit = defineEmits(['cerrar', 'actualizado'])

const areas    = reactive([])
const analistas = reactive([])

const form = reactive({
  id:             null,
  nombre:         '',
  area_cliente:   '',
  responsable_id: null,
  area_equipo:    null,
  estado:         'por_comenzar',
  prioridad:      'media',
  progreso:       0,
  fecha_sla:      null,
})

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
      fecha_sla:      props.trabajo.fecha_sla,
    })
  }
})

function onResponsableChange() {
  if (form.responsable_id) form.area_equipo = null
}

async function guardar() {
  const datos = {
    nombre:         form.nombre,
    area_cliente:   form.area_cliente,
    responsable_id: form.responsable_id,
    area_equipo:    form.area_equipo,
    estado:         form.estado,
    prioridad:      form.prioridad,
    progreso:       form.progreso,
    fecha_sla:      form.fecha_sla || null,
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

.modal-header {
  display: flex; align-items: center; justify-content: space-between;
  padding: 18px 20px; border-bottom: 1px solid var(--border);
}
.modal-title { font-size: 15px; font-weight: 700; color: var(--text); }
.btn-cerrar {
  color: var(--text-sub); font-size: 16px; padding: 4px 8px;
  border-radius: 6px; transition: background 0.15s;
}
.btn-cerrar:hover { background: var(--surface2); color: var(--text); }

.modal-body { padding: 20px; display: flex; flex-direction: column; gap: 14px; }

.campo { display: flex; flex-direction: column; gap: 5px; }
.campo label { font-size: 11px; font-weight: 700; color: var(--text-sub); text-transform: uppercase; letter-spacing: 0.4px; }
.campo input, .campo select {
  background: var(--surface2); border: 1px solid var(--border);
  border-radius: 8px; padding: 9px 12px;
  color: var(--text); font-size: 13px; font-family: inherit;
  transition: border-color 0.15s;
  width: 100%;
}
.campo input:focus, .campo select:focus {
  outline: none; border-color: var(--accent);
}
.campo select option { background: var(--surface2); }

.campo-fila { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }

.slider { width: 100%; accent-color: var(--accent); cursor: pointer; }
.prog-preview { margin-top: 4px; }
.prog-bar  { height: 6px; background: var(--border); border-radius: 3px; }
.prog-fill { height: 100%; background: var(--accent); border-radius: 3px; transition: width 0.2s; }

.modal-footer {
  display: flex; align-items: center; justify-content: flex-end; gap: 8px;
  padding: 14px 20px; border-top: 1px solid var(--border);
}

.btn-primario {
  background: var(--accent); color: #fff;
  padding: 8px 18px; border-radius: 8px;
  font-size: 13px; font-weight: 700;
  transition: opacity 0.15s;
}
.btn-primario:hover:not(:disabled) { opacity: 0.88; }
.btn-primario:disabled { opacity: 0.4; cursor: not-allowed; }

.btn-secundario {
  background: var(--surface2); border: 1px solid var(--border);
  color: var(--text-sub); padding: 8px 14px; border-radius: 8px;
  font-size: 13px; font-weight: 600;
  transition: background 0.15s;
}
.btn-secundario:hover { background: var(--border); }

.btn-danger {
  background: #ED002F18; border: 1px solid #ED002F44;
  color: #ED002F; padding: 8px 14px; border-radius: 8px;
  font-size: 13px; font-weight: 700; margin-right: auto;
  transition: background 0.15s;
}
.btn-danger:hover { background: #ED002F28; }
</style>
