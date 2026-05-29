<template>
  <Teleport to="body">
    <div class="perfil-backdrop" @mousedown.self="$emit('cerrar')">
      <aside class="perfil-drawer">

        <!-- Header con banda de color -->
        <div class="perfil-hero" :style="{ '--uc': usuario.color }">
          <div class="hero-banda"></div>
          <div class="hero-content">
            <div class="perfil-avatar" :style="{ background: usuario.color + '22', color: usuario.color, borderColor: usuario.color }">
              {{ usuario.iniciales }}
            </div>
            <div class="perfil-identidad">
              <h2 class="perfil-nombre">{{ usuario.nombre }}</h2>
              <span class="perfil-rol" :class="usuario.rol">{{ usuario.rol }}</span>
            </div>
            <button class="perfil-close" @click="$emit('cerrar')">✕</button>
          </div>
        </div>

        <!-- Cuerpo -->
        <div class="perfil-body">

          <section class="perfil-section">
            <h3 class="section-label">Identificación</h3>
            <div class="campos-grid">
              <div class="campo">
                <span class="campo-icon">🪪</span>
                <div class="campo-data">
                  <span class="campo-label">RUT</span>
                  <span class="campo-valor">—</span>
                </div>
              </div>
              <div class="campo">
                <span class="campo-icon">🎓</span>
                <div class="campo-data">
                  <span class="campo-label">Matrícula</span>
                  <span class="campo-valor">—</span>
                </div>
              </div>
            </div>
          </section>

          <div class="divider"></div>

          <section class="perfil-section">
            <h3 class="section-label">Fechas</h3>
            <div class="campos-grid">
              <div class="campo">
                <span class="campo-icon">🎂</span>
                <div class="campo-data">
                  <span class="campo-label">Fecha de nacimiento</span>
                  <span class="campo-valor">—</span>
                </div>
              </div>
              <div class="campo">
                <span class="campo-icon">📅</span>
                <div class="campo-data">
                  <span class="campo-label">Fecha de ingreso</span>
                  <span class="campo-valor">—</span>
                </div>
              </div>
            </div>
          </section>

          <div class="divider"></div>

          <section class="perfil-section">
            <h3 class="section-label">Contacto</h3>
            <div class="campos-grid">
              <div class="campo">
                <span class="campo-icon">📞</span>
                <div class="campo-data">
                  <span class="campo-label">Teléfono</span>
                  <span class="campo-valor">—</span>
                </div>
              </div>
              <div class="campo">
                <span class="campo-icon">📍</span>
                <div class="campo-data">
                  <span class="campo-label">Comuna</span>
                  <span class="campo-valor">—</span>
                </div>
              </div>
              <div class="campo campo-full">
                <span class="campo-icon">🏠</span>
                <div class="campo-data">
                  <span class="campo-label">Dirección</span>
                  <span class="campo-valor">—</span>
                </div>
              </div>
            </div>
          </section>

          <div class="divider"></div>

          <section class="perfil-section">
            <h3 class="section-label">Trabajos activos</h3>
            <div v-if="trabajos.length" class="trabajos-mini">
              <div v-for="t in trabajos" :key="t.id" class="trabajo-mini-item">
                <span class="mini-dot" :style="{ background: estadoColor(t.estado) }"></span>
                <span class="mini-nombre">{{ t.nombre }}</span>
                <span class="mini-estado" :style="{ color: estadoColor(t.estado) }">{{ estadoLabel(t.estado) }}</span>
              </div>
            </div>
            <p v-else class="sin-trabajos">Sin trabajos activos</p>
          </section>

        </div>
      </aside>
    </div>
  </Teleport>
</template>

<script setup>
defineProps({
  usuario:  { type: Object, required: true },
  trabajos: { type: Array,  default: () => [] },
})
defineEmits(['cerrar'])

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
.perfil-backdrop {
  position: fixed; inset: 0; z-index: 800;
  background: #00000033;
  backdrop-filter: blur(2px);
  animation: fadeIn 0.2s ease;
}

.perfil-drawer {
  position: fixed; top: 0; right: 0; bottom: 0;
  width: 360px;
  background: var(--surface);
  border-left: 1px solid var(--border);
  display: flex; flex-direction: column;
  overflow: hidden;
  box-shadow: -8px 0 32px #00000018;
  animation: slideIn 0.25s cubic-bezier(0.22, 1, 0.36, 1);
}

@keyframes fadeIn  { from { opacity: 0 } to { opacity: 1 } }
@keyframes slideIn { from { transform: translateX(100%) } to { transform: translateX(0) } }

/* ── Hero ── */
.perfil-hero {
  position: relative;
  padding: 0 0 20px;
  overflow: hidden;
}

.hero-banda {
  height: 72px;
  background: var(--uc, #636466);
  opacity: 0.12;
}

.hero-content {
  display: flex; align-items: flex-end; gap: 14px;
  padding: 0 20px;
  margin-top: -28px;
  position: relative;
}

.perfil-avatar {
  width: 56px; height: 56px; border-radius: 14px;
  font-size: 18px; font-weight: 900;
  display: flex; align-items: center; justify-content: center;
  border: 2px solid;
  flex-shrink: 0;
  box-shadow: 0 4px 12px #00000018;
}

.perfil-identidad {
  flex: 1;
  padding-bottom: 2px;
}

.perfil-nombre {
  font-size: 15px; font-weight: 800;
  color: var(--text); margin: 0 0 4px;
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}

.perfil-rol {
  font-size: 9px; font-weight: 700; text-transform: uppercase;
  letter-spacing: 0.8px; padding: 3px 8px; border-radius: 5px;
}
.perfil-rol.analista { background: var(--accent-dim); color: var(--accent); }
.perfil-rol.gerente  { background: #f59e0b22; color: #f59e0b; }

.perfil-close {
  position: absolute; top: -56px; right: 0;
  background: none; border: none;
  color: #fff; font-size: 14px; cursor: pointer;
  padding: 6px 8px; opacity: 0.7; transition: opacity 0.15s;
}
.perfil-close:hover { opacity: 1; }

/* ── Body ── */
.perfil-body {
  flex: 1; overflow-y: auto;
  padding: 4px 0 24px;
}

.perfil-section { padding: 16px 20px 4px; }

.section-label {
  font-size: 9px; font-weight: 800; text-transform: uppercase;
  letter-spacing: 1px; color: var(--text-sub);
  margin: 0 0 12px;
}

.divider {
  height: 1px; background: var(--border);
  margin: 8px 20px;
}

/* ── Campos ── */
.campos-grid {
  display: grid; grid-template-columns: 1fr 1fr; gap: 8px;
}

.campo {
  display: flex; align-items: flex-start; gap: 8px;
  background: var(--surface2);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 10px 12px;
}
.campo-full { grid-column: 1 / -1; }

.campo-icon { font-size: 14px; flex-shrink: 0; margin-top: 1px; }

.campo-data { display: flex; flex-direction: column; gap: 2px; min-width: 0; }

.campo-label {
  font-size: 9px; font-weight: 700; text-transform: uppercase;
  letter-spacing: 0.6px; color: var(--text-sub);
}
.campo-valor {
  font-size: 12px; font-weight: 600; color: var(--text);
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}

/* ── Trabajos mini ── */
.trabajos-mini { display: flex; flex-direction: column; gap: 6px; }

.trabajo-mini-item {
  display: flex; align-items: center; gap: 8px;
  padding: 7px 10px;
  background: var(--surface2); border-radius: 8px;
  border: 1px solid var(--border);
}
.mini-dot {
  width: 7px; height: 7px; border-radius: 50%; flex-shrink: 0;
}
.mini-nombre {
  flex: 1; font-size: 11px; font-weight: 600; color: var(--text);
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
.mini-estado { font-size: 10px; font-weight: 600; flex-shrink: 0; }

.sin-trabajos { font-size: 11px; color: var(--text-sub); padding: 4px 0; }
</style>
