<template>
  <aside class="sidebar">
    <!-- Logo -->
    <div class="logo">
      <div class="logo-mark">
        <img src="/logo-verisure.png" alt="Verisure" class="logo-img" />
      </div>
      <div>
        <div class="logo-title">Bitácora</div>
        <div class="logo-sub">Customer Intelligence</div>
      </div>
    </div>

    <!-- Navegación principal -->
    <nav class="nav">
      <router-link to="/dashboard" class="nav-item" :class="{ active: ruta === '/dashboard' }">
        <span class="nav-icon">🏠</span> Inicio
      </router-link>
      <router-link to="/agenda" class="nav-item" :class="{ active: ruta === '/agenda' }">
        <span class="nav-icon">📅</span> Agenda
      </router-link>
      <router-link to="/kanban" class="nav-item" :class="{ active: ruta === '/kanban' }">
        <span class="nav-icon">🗂️</span> Gestión
      </router-link>
      <router-link to="/analitica" class="nav-item" :class="{ active: ruta === '/analitica' }">
        <span class="nav-icon">📈</span> Analítica
      </router-link>
    </nav>

    <div class="divider"></div>

    <!-- Equipo -->
    <div class="section-label">Equipo</div>
    <div class="team-list">
      <div v-for="u in usuarios" :key="u.id" class="member-row">
        <div class="avatar" :style="{ background: u.color + '22', color: u.color, borderColor: u.color }">
          {{ u.iniciales }}
        </div>
        <div class="member-info">
          <div class="member-name">{{ u.nombre }}</div>
          <div class="member-rol">{{ u.rol }}</div>
        </div>
      </div>
    </div>

    <div class="divider"></div>

    <!-- Selector de tema -->
    <ThemePicker />

    <div class="divider"></div>

    <!-- Usuario actual + logout -->
    <div class="session" v-if="user">
      <div class="session-info">
        <div class="session-nombre">{{ user.nombre }}</div>
        <div class="session-rol">{{ user.rol }}</div>
      </div>
      <button class="btn-logout" @click="cerrarSesion" title="Cerrar sesión">↩</button>
    </div>
  </aside>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getUsuarios } from '../api/usuarios'
import { useAuth } from '../composables/useAuth'
import ThemePicker from './ThemePicker.vue'

const route    = useRoute()
const router   = useRouter()
const ruta     = ref(route.path)
const usuarios = ref([])
const { user, logout } = useAuth()

route && (ruta.value = route.path)

onMounted(async () => {
  usuarios.value = await getUsuarios()
})

function cerrarSesion() {
  logout()
  router.push('/login')
}
</script>

<style scoped>
.sidebar {
  width: 220px; min-width: 220px;
  background: var(--sidebar-bg);
  border-right: 1px solid var(--border);
  display: flex; flex-direction: column;
  overflow-y: auto; height: 100vh;
  position: sticky; top: 0;
}

.logo {
  display: flex; align-items: center; gap: 10px;
  padding: 20px 16px 16px;
  border-bottom: 1px solid var(--border);
}
.logo-mark {
  width: 32px; height: 32px; border-radius: 8px;
  background: var(--surface2);
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0; overflow: hidden;
}
.logo-img {
  width: 28px; height: 28px; object-fit: contain;
}
.logo-title { font-size: 13px; font-weight: 700; color: var(--text); }
.logo-sub   { font-size: 10px; color: var(--text-sub); }

.nav { display: flex; flex-direction: column; gap: 2px; padding: 12px 8px; }
.nav-item {
  display: flex; align-items: center; gap: 8px;
  padding: 8px 10px; border-radius: 8px;
  font-size: 13px; font-weight: 500; color: var(--text-sub);
  transition: background 0.15s, color 0.15s;
}
.nav-item:hover { background: var(--surface2); color: var(--text); }
.nav-item.active {
  background: var(--accent-dim); color: var(--accent); font-weight: 700;
}
.nav-icon { font-size: 11px; width: 16px; text-align: center; display: inline-block; flex-shrink: 0; }

.divider { height: 1px; background: var(--border); margin: 4px 0; }

.section-label {
  font-size: 10px; font-weight: 700; text-transform: uppercase;
  letter-spacing: 0.8px; color: var(--text-sub);
  padding: 10px 16px 6px;
}

.team-list { display: flex; flex-direction: column; gap: 2px; padding: 0 8px; }
.member-row {
  display: flex; align-items: center; gap: 8px;
  padding: 5px 8px; border-radius: 6px;
  transition: background 0.15s;
  cursor: default;
}
.member-row:hover { background: var(--surface2); }
.avatar {
  width: 28px; height: 28px; border-radius: 50%;
  font-size: 10px; font-weight: 700;
  display: flex; align-items: center; justify-content: center;
  border: 1.5px solid; flex-shrink: 0;
}
.member-name { font-size: 11px; font-weight: 600; color: var(--text); line-height: 1.2; }
.member-rol  { font-size: 10px; color: var(--text-sub); text-transform: capitalize; }

.session {
  display: flex; align-items: center; gap: 8px;
  padding: 10px 12px; margin: 4px 8px 8px;
  background: var(--surface2); border-radius: 8px;
}
.session-info  { flex: 1; min-width: 0; }
.session-nombre { font-size: 11px; font-weight: 700; color: var(--text); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.session-rol    { font-size: 10px; color: var(--text-sub); text-transform: capitalize; }
.btn-logout {
  font-size: 14px; color: var(--text-sub); padding: 4px 6px;
  border-radius: 6px; transition: background 0.15s, color 0.15s; flex-shrink: 0;
}
.btn-logout:hover { background: var(--border); color: var(--text); }
</style>
