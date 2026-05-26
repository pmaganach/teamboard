<template>
  <div class="view-wrapper">
    <TrabajoModal v-if="modalAbierto" :trabajo="null" @cerrar="modalAbierto = false" @actualizado="recargar" />
    <TopBar titulo="Analítica" subtitulo="Seguimiento y control" @nuevo="modalAbierto = true" />

    <div class="view-content" v-if="cargado">

      <!-- ── SLA RIESGO + ESTANCADOS ─────────────────── -->
      <div class="grid-32">

        <div class="card">
          <div class="card-title">
            <span class="ct-left">
              🚨 SLA en riesgo
              <span class="info-tip tip-down" data-tip="Trabajos activos cuya fecha SLA vence en los próximos 7 días o ya está vencida. Ordenados de más urgente a menos urgente.">i</span>
            </span>
            <span v-if="slaRiesgo.length" class="badge" style="background:#ED002F20;color:#ED002F">{{ slaRiesgo.length }} críticos</span>
          </div>
          <table class="data-table" v-if="slaRiesgo.length">
            <thead>
              <tr>
                <th>Trabajo</th>
                <th>Analista</th>
                <th>Área</th>
                <th>Vence</th>
                <th>Estado</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="t in slaRiesgo" :key="t.id">
                <td class="td-titulo">{{ t.titulo }}</td>
                <td>
                  <div class="av-row" v-if="usuariosMap[t.responsable_id]">
                    <div class="av-sm" :style="avStyle(usuariosMap[t.responsable_id])">{{ usuariosMap[t.responsable_id].iniciales }}</div>
                    <span class="av-nombre">{{ primerNombre(usuariosMap[t.responsable_id].nombre) }}</span>
                  </div>
                </td>
                <td class="td-area">{{ t.area_cliente }}</td>
                <td><span class="dias-chip" :class="diasClass(t.diasRestantes)">{{ diasLabel(t.diasRestantes) }}</span></td>
                <td><span class="estado-chip" :class="'e-' + t.estado">{{ estadoLabel(t.estado) }}</span></td>
              </tr>
            </tbody>
          </table>
          <div class="empty-msg" v-else>✅ Sin trabajos en riesgo SLA</div>
        </div>

        <div class="card">
          <div class="card-title">
            <span class="ct-left">
              ⏸ Estancados
              <span class="info-tip tip-down" data-tip="Trabajos activos con más de 14 días desde su fecha de inicio y un progreso igual o menor al 25%. Indica trabajos que no están avanzando.">i</span>
            </span>
            <span v-if="estancados.length" class="badge" style="background:#f59e0b20;color:#f59e0b">+14d sin avance</span>
          </div>
          <div v-if="estancados.length">
            <div class="stall-row" v-for="t in estancados" :key="t.id">
              <div class="stall-dias" :style="{ color: t.diasAbierto >= 28 ? '#ED002F' : t.diasAbierto >= 21 ? '#f97316' : '#f59e0b' }">
                {{ t.diasAbierto }}<span>días</span>
              </div>
              <div class="stall-info">
                <div class="stall-titulo">{{ t.titulo }}</div>
                <div class="stall-meta">{{ t.area_cliente }}</div>
              </div>
              <div class="av-sm" v-if="usuariosMap[t.responsable_id]" :style="avStyle(usuariosMap[t.responsable_id])">
                {{ usuariosMap[t.responsable_id].iniciales }}
              </div>
            </div>
          </div>
          <div class="empty-msg" v-else>✅ Sin trabajos estancados</div>
        </div>

      </div>

      <!-- ── AGING + PRIORIDADES ─────────────────────── -->
      <div class="grid-2">

        <div class="card">
          <div class="card-title">
            <span class="ct-left">
              ⏱ Antigüedad de trabajos activos
              <span class="info-tip" data-tip="Cuántos trabajos activos tiene cada analista según los días transcurridos desde su fecha de inicio. Detecta acumulación de trabajos muy antiguos.">i</span>
            </span>
          </div>
          <div class="aging-wrap" v-if="agingData.some(d => d.total > 0)">
            <table class="aging-table">
              <thead>
                <tr>
                  <th class="th-left">Analista</th>
                  <th v-for="r in RANGOS" :key="r">{{ r }}</th>
                  <th>Total</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="d in agingData" :key="d.usuario.id" v-show="d.total > 0">
                  <td class="td-analista">
                    <div class="av-row">
                      <div class="av-sm" :style="avStyle(d.usuario)">{{ d.usuario.iniciales }}</div>
                      <span>{{ primerNombre(d.usuario.nombre) }}</span>
                    </div>
                  </td>
                  <td v-for="(v, ci) in d.buckets" :key="ci">
                    <div class="age-cell" :style="ageCellStyle(v, ci)">
                      <span class="age-n">{{ v || '—' }}</span>
                      <span class="age-lbl" v-if="v > 0">trab.</span>
                    </div>
                  </td>
                  <td class="td-total">{{ d.total }}</td>
                </tr>
              </tbody>
            </table>
          </div>
          <div class="empty-msg" v-else>Sin trabajos activos</div>
        </div>

        <div class="card">
          <div class="card-title">
            <span class="ct-left">
              ⚖ Balance de prioridades
              <span class="info-tip" data-tip="Proporción de trabajos activos por nivel de prioridad (Baja / Media / Alta) para cada analista. Permite detectar si alguien concentra toda la carga crítica.">i</span>
            </span>
          </div>
          <div v-if="prioData.length">
            <div class="prio-row" v-for="d in prioData" :key="d.usuario.id">
              <div class="av-sm" :style="avStyle(d.usuario)">{{ d.usuario.iniciales }}</div>
              <div class="prio-name">{{ primerNombre(d.usuario.nombre) }}</div>
              <div class="prio-track">
                <div v-if="d.baja"  class="prio-seg" style="background:#10b981" :style="{ width: pct(d.baja,  maxPrio) + '%' }" :title="`Baja: ${d.baja}`">{{ d.baja > 1 ? 'B'+d.baja : '' }}</div>
                <div v-if="d.media" class="prio-seg" style="background:#f59e0b" :style="{ width: pct(d.media, maxPrio) + '%' }" :title="`Media: ${d.media}`">{{ d.media > 1 ? 'M'+d.media : '' }}</div>
                <div v-if="d.alta"  class="prio-seg" style="background:#ED002F" :style="{ width: pct(d.alta,  maxPrio) + '%' }" :title="`Alta: ${d.alta}`">{{ d.alta > 1 ? 'A'+d.alta : '' }}</div>
              </div>
              <div class="prio-total">{{ d.total }}</div>
            </div>
            <div class="prio-legend">
              <span class="leg-item"><span class="ld" style="background:#10b981"></span>Baja</span>
              <span class="leg-item"><span class="ld" style="background:#f59e0b"></span>Media</span>
              <span class="leg-item"><span class="ld" style="background:#ED002F"></span>Alta</span>
            </div>
          </div>
          <div class="empty-msg" v-else>Sin datos de prioridad</div>
        </div>

      </div>

      <!-- ── PROGRESO + TOP ÁREAS ────────────────────── -->
      <div class="grid-2">

        <div class="card">
          <div class="card-title">
            <span class="ct-left">
              📦 Progreso promedio por analista
              <span class="info-tip" data-tip="Promedio del campo Progreso (0–100%) de los trabajos activos asignados a cada analista. Un valor bajo puede indicar trabajos recién iniciados o estancados.">i</span>
            </span>
          </div>
          <div v-if="progresoData.length">
            <div class="prog-row" v-for="d in progresoData" :key="d.usuario.id">
              <div class="av-sm" :style="avStyle(d.usuario)">{{ d.usuario.iniciales }}</div>
              <div class="prog-name">{{ primerNombre(d.usuario.nombre) }}</div>
              <div class="prog-bar-wrap">
                <div class="prog-bar" :style="{ width: d.avg + '%', background: progresoColor(d.avg) }"></div>
              </div>
              <div class="prog-pct" :style="{ color: progresoColor(d.avg) }">{{ d.avg }}%</div>
            </div>
          </div>
          <div class="empty-msg" v-else>Sin datos de progreso</div>
        </div>

        <div class="card">
          <div class="card-title">
            <span class="ct-left">
              📊 Top áreas · trabajos activos
              <span class="info-tip" data-tip="Ranking de áreas cliente por cantidad de trabajos activos. El badge de color muestra el % de SLA vigente: verde ≥80%, amarillo ≥60%, rojo <60%.">i</span>
            </span>
          </div>
          <div v-if="topAreas.length">
            <div class="area-row" v-for="(a, idx) in topAreas" :key="a.nombre">
              <div class="area-rank">{{ idx + 1 }}</div>
              <div class="area-nombre">{{ a.nombre }}</div>
              <div class="area-bar-wrap">
                <div class="area-bar" :style="{ width: pct(a.total, topAreas[0]?.total) + '%', background: AREA_COLORS[idx % AREA_COLORS.length] }">
                  <span v-if="a.total > 3">{{ a.total }}</span>
                </div>
              </div>
              <div class="area-count">{{ a.total }}</div>
              <div v-if="a.sla !== null" class="area-sla" :style="slaBadgeStyle(a.sla)">{{ a.sla }}%</div>
            </div>
          </div>
          <div class="empty-msg" v-else>Sin trabajos activos</div>
        </div>

      </div>

      <!-- ── VOLUMEN SEMANAL ─────────────────────────── -->
      <div class="card">
        <div class="card-title">
          <span class="ct-left">
            📅 Volumen semanal · trabajos por semana de inicio
            <span class="info-tip" data-tip="Cantidad de trabajos agrupados por semana según su fecha de inicio. Azul = activos, verde = completados. Permite ver semanas de alta carga y la tendencia de cierre.">i</span>
          </span>
        </div>
        <div class="empty-msg" v-if="!svgVolumen.items.length">Sin datos de fecha en los trabajos</div>
        <svg v-else :viewBox="`0 0 ${svgVolumen.W} ${svgVolumen.H}`" width="100%" style="display:block">
          <!-- Grid horizontal -->
          <template v-for="g in svgVolumen.gridY" :key="g.v">
            <line :x1="svgVolumen.PL" :y1="g.y" :x2="svgVolumen.W - 16" :y2="g.y"
              stroke="var(--border)" stroke-width="1" stroke-dasharray="4,4"/>
            <text :x="svgVolumen.PL - 4" :y="g.y + 4" text-anchor="end" font-size="9" fill="var(--text-sub)">{{ g.v }}</text>
          </template>
          <!-- Área rellena activos -->
          <polygon v-if="svgVolumen.polyActivos" :points="svgVolumen.polyActivos" fill="#3b82f6" opacity="0.08"/>
          <!-- Área rellena completados -->
          <polygon v-if="svgVolumen.polyCompletados" :points="svgVolumen.polyCompletados" fill="#10b981" opacity="0.08"/>
          <!-- Línea activos -->
          <polyline v-if="svgVolumen.lineActivos" :points="svgVolumen.lineActivos"
            fill="none" stroke="#3b82f6" stroke-width="2.5" stroke-linejoin="round" stroke-linecap="round"/>
          <!-- Línea completados -->
          <polyline v-if="svgVolumen.lineCompletados" :points="svgVolumen.lineCompletados"
            fill="none" stroke="#10b981" stroke-width="2.5" stroke-linejoin="round" stroke-linecap="round"/>
          <!-- Dots y labels -->
          <template v-for="b in svgVolumen.items" :key="b.label">
            <circle :cx="b.cx" :cy="b.yAct"  r="3.5" fill="#3b82f6" stroke="var(--surface)" stroke-width="2"/>
            <circle :cx="b.cx" :cy="b.yComp" r="3.5" fill="#10b981" stroke="var(--surface)" stroke-width="2"/>
            <text :x="b.cx" :y="svgVolumen.H - 5" text-anchor="middle" font-size="9" fill="var(--text-sub)">{{ b.label }}</text>
          </template>
          <!-- Etiquetas último punto -->
          <text v-if="svgVolumen.items.length" :x="svgVolumen.items[svgVolumen.items.length-1].cx + 8" :y="svgVolumen.items[svgVolumen.items.length-1].yAct + 4" font-size="10" font-weight="700" fill="#3b82f6">{{ svgVolumen.items[svgVolumen.items.length-1].activos }}</text>
          <text v-if="svgVolumen.items.length" :x="svgVolumen.items[svgVolumen.items.length-1].cx + 8" :y="svgVolumen.items[svgVolumen.items.length-1].yComp + 4" font-size="10" font-weight="700" fill="#10b981">{{ svgVolumen.items[svgVolumen.items.length-1].completados }}</text>
        </svg>
        <div class="svol-legend">
          <span class="leg-item"><span class="ld" style="background:#3b82f6"></span>Activos</span>
          <span class="leg-item"><span class="ld" style="background:#10b981"></span>Completados</span>
        </div>
      </div>

    </div>
    <div v-else class="loading">Cargando analítica...</div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { getUsuarios } from '../api/usuarios'
import { getTrabaj }   from '../api/trabajos'
import { useFiltros }  from '../composables/useFiltros'
import TopBar          from '../components/TopBar.vue'
import TrabajoModal    from '../components/TrabajoModal.vue'

const trabajos    = ref([])
const usuarios    = ref([])
const cargado     = ref(false)
const modalAbierto = ref(false)
const { filtros } = useFiltros()

const RANGOS      = ['0–7d', '8–14d', '15–30d', '31+d']
const AREA_COLORS = ['#ec4899','#f97316','#f59e0b','#10b981','#a78bfa','#ED002F','#06b6d4','#3b82f6']
const ESTADO_LABELS = {
  por_comenzar: 'Por comenzar',
  en_gestion:   'En gestión',
  en_revision:  'En revisión',
  completado:   'Completado',
  cancelado:    'Cancelado',
}

async function recargar() {
  ;[usuarios.value, trabajos.value] = await Promise.all([getUsuarios(), getTrabaj(filtros())])
  cargado.value = true
}
onMounted(recargar)
watch(filtros, recargar)

// ── Maps ──────────────────────────────────────────────────────────
const usuariosMap = computed(() =>
  Object.fromEntries(usuarios.value.map(u => [u.id, u]))
)
const analistas = computed(() => usuarios.value.filter(u => u.rol === 'analista'))

// ── Sets base ────────────────────────────────────────────────────
const activos     = computed(() => trabajos.value.filter(t => !['completado','cancelado'].includes(t.estado)))
const completados = computed(() => trabajos.value.filter(t => t.estado === 'completado'))

// ── KPIs ─────────────────────────────────────────────────────────
const tasaCierre = computed(() => {
  const total = trabajos.value.length
  return total ? Math.round(completados.value.length / total * 100) : 0
})

const slaOnTrack = computed(() => {
  const hoy = new Date(); hoy.setHours(0,0,0,0)
  const conSla = activos.value.filter(t => t.fecha_sla)
  if (!conSla.length) return 0
  const ok = conSla.filter(t => new Date(t.fecha_sla) >= hoy).length
  return Math.round(ok / conSla.length * 100)
})

// ── SLA en riesgo ────────────────────────────────────────────────
const slaRiesgo = computed(() => {
  const hoy = new Date(); hoy.setHours(0,0,0,0)
  const limite = new Date(hoy); limite.setDate(limite.getDate() + 7)
  return activos.value
    .filter(t => t.fecha_sla && new Date(t.fecha_sla) <= limite)
    .map(t => ({ ...t, diasRestantes: Math.ceil((new Date(t.fecha_sla) - hoy) / 86400000) }))
    .sort((a, b) => a.diasRestantes - b.diasRestantes)
})

// ── Estancados ───────────────────────────────────────────────────
const estancados = computed(() => {
  const hoy = new Date(); hoy.setHours(0,0,0,0)
  return activos.value
    .filter(t => {
      if (!t.fecha_inicio) return false
      const dias = Math.floor((hoy - new Date(t.fecha_inicio)) / 86400000)
      return dias > 14 && (t.progreso ?? 0) <= 25
    })
    .map(t => ({ ...t, diasAbierto: Math.floor((hoy - new Date(t.fecha_inicio)) / 86400000) }))
    .sort((a, b) => b.diasAbierto - a.diasAbierto)
    .slice(0, 5)
})

// ── Aging ────────────────────────────────────────────────────────
const agingData = computed(() => {
  const hoy = new Date(); hoy.setHours(0,0,0,0)
  return analistas.value.map(u => {
    const mis = activos.value.filter(t => t.responsable_id === u.id)
    const buckets = [0, 0, 0, 0]
    mis.forEach(t => {
      const dias = t.fecha_inicio ? Math.floor((hoy - new Date(t.fecha_inicio)) / 86400000) : 0
      if (dias <= 7)       buckets[0]++
      else if (dias <= 14) buckets[1]++
      else if (dias <= 30) buckets[2]++
      else                 buckets[3]++
    })
    return { usuario: u, buckets, total: mis.length }
  })
})

// ── Prioridades ──────────────────────────────────────────────────
const prioData = computed(() =>
  analistas.value.map(u => {
    const mis = activos.value.filter(t => t.responsable_id === u.id)
    return {
      usuario: u,
      baja:  mis.filter(t => t.prioridad === 'baja').length,
      media: mis.filter(t => t.prioridad === 'media').length,
      alta:  mis.filter(t => t.prioridad === 'alta').length,
      total: mis.length,
    }
  }).filter(d => d.total > 0)
)
const maxPrio = computed(() => Math.max(1, ...prioData.value.map(d => d.total)))

// ── Progreso ─────────────────────────────────────────────────────
const progresoData = computed(() =>
  analistas.value.map(u => {
    const mis = activos.value.filter(t => t.responsable_id === u.id && t.progreso != null)
    if (!mis.length) return null
    const avg = Math.round(mis.reduce((s, t) => s + (t.progreso ?? 0), 0) / mis.length)
    return { usuario: u, avg }
  })
  .filter(Boolean)
  .sort((a, b) => b.avg - a.avg)
)

// ── Top áreas ────────────────────────────────────────────────────
const topAreas = computed(() => {
  const hoy = new Date(); hoy.setHours(0,0,0,0)
  const map = {}
  activos.value.forEach(t => {
    const key = t.area_cliente || 'Sin área'
    if (!map[key]) map[key] = { nombre: key, total: 0, slaOk: 0, conSla: 0 }
    map[key].total++
    if (t.fecha_sla) {
      map[key].conSla++
      if (new Date(t.fecha_sla) >= hoy) map[key].slaOk++
    }
  })
  return Object.values(map)
    .map(a => ({ ...a, sla: a.conSla ? Math.round(a.slaOk / a.conSla * 100) : null }))
    .sort((a, b) => b.total - a.total)
})

// ── Volumen semanal ───────────────────────────────────────────────
const volumenSemanal = computed(() => {
  const map = {}
  trabajos.value.forEach(t => {
    const fechaRef = t.fecha_inicio || t.fecha_sla
    if (!fechaRef) return
    const d = new Date(fechaRef)
    const jan1 = new Date(d.getFullYear(), 0, 1)
    const week = Math.ceil(((d - jan1) / 86400000 + jan1.getDay() + 1) / 7)
    const key = `${d.getFullYear()}-${String(week).padStart(2,'0')}`
    if (!map[key]) map[key] = { key, label: `S${String(week).padStart(2,'0')}`, total: 0, completados: 0, activos: 0 }
    map[key].total++
    if (['completado','cancelado'].includes(t.estado)) map[key].completados++
    else map[key].activos++
  })
  return Object.values(map).sort((a,b) => a.key.localeCompare(b.key)).slice(-10)
})

const svgVolumen = computed(() => {
  const data = volumenSemanal.value
  if (!data.length) return { items: [], gridY: [], W: 860, H: 180, PL: 36 }
  const W=860, H=180, PT=16, PR=40, PB=32, PL=36
  const iW = W-PL-PR, iH = H-PT-PB
  const maxV = Math.max(...data.map(d => d.total), 1)
  const slotW = iW / (data.length - 1 || 1)

  const items = data.map((d, i) => {
    const cx = data.length === 1 ? PL + iW/2 : PL + i * slotW
    return {
      label: d.label, total: d.total,
      activos: d.activos, completados: d.completados,
      cx,
      yAct:  PT + iH - (d.activos / maxV) * iH,
      yComp: PT + iH - (d.completados / maxV) * iH,
    }
  })

  const lineActivos     = items.map(b => `${b.cx},${b.yAct}`).join(' ')
  const lineCompletados = items.map(b => `${b.cx},${b.yComp}`).join(' ')
  const base = `${items[items.length-1].cx},${PT+iH} ${items[0].cx},${PT+iH}`
  const polyActivos     = lineActivos + ' ' + base
  const polyCompletados = lineCompletados + ' ' + base

  const step = Math.max(1, Math.ceil(maxV / 4))
  const gridY = []
  for (let v = 0; v <= maxV; v += step) gridY.push({ v, y: PT + iH - (v/maxV)*iH })

  return { items, gridY, W, H, PL, lineActivos, lineCompletados, polyActivos, polyCompletados }
})

// ── Helpers ───────────────────────────────────────────────────────
function pct(v, max)     { return max ? ((v / max) * 100).toFixed(1) : 0 }
function primerNombre(n) { return n?.split(' ')[0] ?? n }
function avStyle(u)      { return { background: u.color + '22', color: u.color } }
function estadoLabel(e)  { return ESTADO_LABELS[e] ?? e }

function diasLabel(d) {
  if (d < 0)  return `Vencido ${Math.abs(d)}d`
  if (d === 0) return 'Vence hoy'
  return `en ${d}d`
}
function diasClass(d) {
  if (d <= 0) return 'chip-red'
  if (d <= 3) return 'chip-amber'
  return 'chip-green'
}
function ageCellStyle(v, ci) {
  if (!v) return { background: 'transparent', color: 'var(--text-sub)' }
  const colors = [
    { bg:'#10b98118', color:'#10b981' },
    { bg:'#f59e0b18', color:'#f59e0b' },
    { bg:'#f9731620', color:'#f97316' },
    { bg:'#ED002F22', color:'#ED002F' },
  ]
  return { background: colors[ci].bg, color: colors[ci].color }
}
function progresoColor(p) {
  return p >= 70 ? '#10b981' : p >= 40 ? '#f59e0b' : '#ED002F'
}
function slaBadgeStyle(sla) {
  const color = sla >= 80 ? '#10b981' : sla >= 60 ? '#f59e0b' : '#ED002F'
  return { background: color + '20', color }
}
</script>

<style scoped>
.view-wrapper  { display: flex; flex-direction: column; flex: 1; overflow: hidden; }
.view-content  { flex: 1; overflow-y: auto; padding: 22px 24px; background: var(--bg); display: flex; flex-direction: column; gap: 16px; }
.loading       { padding: 40px; text-align: center; color: var(--text-sub); }

/* Grids */
.grid-2  { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
.grid-32 { display: grid; grid-template-columns: 3fr 2fr; gap: 14px; }

/* Cards */
.card       { background: var(--surface); border: 1px solid var(--border); border-radius: 12px; padding: 16px 18px; }
.card-title { font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: .6px; color: var(--text-sub); margin-bottom: 14px; display: flex; align-items: center; justify-content: space-between; }
.ct-left    { display: flex; align-items: center; gap: 6px; }
.badge      { font-size: 9px; font-weight: 700; padding: 2px 7px; border-radius: 8px; letter-spacing: 0; }
.empty-msg  { font-size: 12px; color: var(--text-sub); padding: 12px 0; }

/* Info tooltip */
.info-tip {
  position: relative;
  display: inline-flex; align-items: center; justify-content: center;
  width: 14px; height: 14px; border-radius: 50%;
  background: var(--surface2); color: var(--text-sub);
  font-size: 8px; font-weight: 700; font-style: normal;
  cursor: default; flex-shrink: 0;
  text-transform: none; letter-spacing: 0;
}
.info-tip::after {
  content: attr(data-tip);
  position: absolute;
  bottom: calc(100% + 8px);
  left: 50%; transform: translateX(-50%);
  background: var(--surface); border: 1px solid var(--border);
  color: var(--text);
  font-size: 11px; font-weight: 400;
  text-transform: none; letter-spacing: 0;
  padding: 8px 12px; border-radius: 8px;
  width: 230px; white-space: normal; line-height: 1.5;
  opacity: 0; pointer-events: none;
  transition: opacity 0.15s; z-index: 100;
  box-shadow: 0 4px 16px rgba(0,0,0,.3);
}
.info-tip:hover::after { opacity: 1; }
.info-tip.tip-down::after { bottom: auto; top: calc(100% + 8px); }

/* Data table */
.data-table { width: 100%; border-collapse: collapse; }
.data-table th { font-size: 9px; font-weight: 700; text-transform: uppercase; letter-spacing: .4px; color: var(--text-sub); padding: 0 8px 10px; text-align: left; }
.data-table td { padding: 7px 8px; border-top: 1px solid var(--border); font-size: 11px; vertical-align: middle; }
.td-titulo { font-weight: 600; max-width: 160px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.td-area   { font-size: 10px; color: var(--text-sub); }

/* Chips */
.dias-chip  { font-size: 10px; font-weight: 700; padding: 3px 8px; border-radius: 6px; white-space: nowrap; }
.chip-red   { background: #ED002F22; color: #ED002F; }
.chip-amber { background: #f59e0b20; color: #f59e0b; }
.chip-green { background: #10b98118; color: #10b981; }
.estado-chip    { font-size: 9px; font-weight: 700; padding: 2px 6px; border-radius: 5px; white-space: nowrap; background: var(--surface2); color: var(--text-sub); }
.e-en_gestion   { background: #3b82f618; color: #3b82f6; }
.e-en_revision  { background: #f59e0b18; color: #f59e0b; }
.e-completado   { background: #10b98118; color: #10b981; }

/* Avatar */
.av-row    { display: flex; align-items: center; gap: 6px; }
.av-sm     { width: 24px; height: 24px; border-radius: 50%; font-size: 8px; font-weight: 800; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.av-nombre { font-size: 11px; font-weight: 600; }

/* Estancados */
.stall-row   { display: flex; align-items: center; gap: 10px; padding: 9px 0; border-top: 1px solid var(--border); }
.stall-row:first-child { border-top: none; }
.stall-dias  { font-size: 20px; font-weight: 800; width: 36px; text-align: center; flex-shrink: 0; line-height: 1; }
.stall-dias span { display: block; font-size: 8px; font-weight: 600; color: var(--text-sub); }
.stall-info  { flex: 1; min-width: 0; }
.stall-titulo { font-size: 12px; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.stall-meta   { font-size: 10px; color: var(--text-sub); margin-top: 2px; }

/* Aging */
.aging-wrap  { overflow-x: auto; }
.aging-table { border-collapse: collapse; width: 100%; }
.aging-table th { font-size: 9px; font-weight: 700; text-transform: uppercase; letter-spacing: .4px; color: var(--text-sub); padding: 6px 10px; text-align: center; }
.aging-table th.th-left { text-align: left; }
.aging-table td { padding: 4px 6px; text-align: center; }
.td-analista { text-align: left; padding: 4px 10px 4px 0; }
.td-total    { font-size: 12px; font-weight: 800; color: var(--text); text-align: center; }
.age-cell { width: 52px; height: 36px; border-radius: 7px; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 1px; margin: 0 auto; }
.age-n    { font-size: 15px; font-weight: 800; line-height: 1; }
.age-lbl  { font-size: 7px; opacity: .75; }

/* Prioridades */
.prio-row   { display: flex; align-items: center; gap: 8px; margin-bottom: 8px; }
.prio-name  { font-size: 11px; font-weight: 600; width: 74px; flex-shrink: 0; white-space: nowrap; }
.prio-track { flex: 1; height: 20px; background: var(--surface2); border-radius: 5px; overflow: hidden; display: flex; }
.prio-seg   { height: 100%; display: flex; align-items: center; justify-content: center; font-size: 8px; font-weight: 700; color: rgba(255,255,255,.9); min-width: 14px; cursor: default; }
.prio-seg:hover { opacity: .75; }
.prio-total { font-size: 11px; font-weight: 800; color: var(--text); width: 20px; text-align: right; flex-shrink: 0; }
.prio-legend { display: flex; gap: 14px; margin-top: 14px; flex-wrap: wrap; }

/* Progreso */
.prog-row      { display: flex; align-items: center; gap: 8px; margin-bottom: 10px; }
.prog-name     { font-size: 11px; font-weight: 600; width: 74px; flex-shrink: 0; white-space: nowrap; }
.prog-bar-wrap { flex: 1; height: 12px; background: var(--surface2); border-radius: 4px; overflow: hidden; }
.prog-bar      { height: 100%; border-radius: 4px; transition: width .4s; }
.prog-pct      { font-size: 11px; font-weight: 700; width: 34px; text-align: right; flex-shrink: 0; }

/* Top áreas */
.area-row      { display: flex; align-items: center; gap: 8px; margin-bottom: 10px; }
.area-rank     { font-size: 11px; font-weight: 800; color: var(--text-sub); width: 14px; text-align: right; flex-shrink: 0; }
.area-nombre   { font-size: 11px; font-weight: 600; width: 180px; flex-shrink: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.area-bar-wrap { flex: 1; height: 22px; background: var(--surface2); border-radius: 5px; overflow: hidden; }
.area-bar      { height: 100%; border-radius: 5px; display: flex; align-items: center; padding-left: 7px; font-size: 9px; font-weight: 700; color: rgba(255,255,255,.9); }
.area-count    { font-size: 12px; font-weight: 800; color: var(--text); width: 22px; text-align: right; flex-shrink: 0; }
.area-sla      { font-size: 9px; font-weight: 700; padding: 2px 7px; border-radius: 8px; flex-shrink: 0; width: 44px; text-align: center; }

/* Leyendas */
.leg-item { display: flex; align-items: center; gap: 5px; font-size: 10px; color: var(--text-sub); }
.ld       { width: 10px; height: 3px; border-radius: 2px; flex-shrink: 0; display: inline-block; }
.svol-legend { display: flex; gap: 14px; margin-top: 10px; }
</style>
