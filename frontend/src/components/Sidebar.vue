<template>
  <aside class="sidebar">
    <!-- Logo -->
    <div class="logo">
      <span class="logo-mark">R</span>
      <div>
        <div class="logo-title">Radar</div>
        <div class="logo-sub">Customer Intelligence</div>
      </div>
    </div>

    <!-- Navegación principal -->
    <nav class="nav">
      <router-link to="/dashboard" class="nav-item" :class="{ active: ruta === '/dashboard' }">
        <span class="nav-icon">&#9632;</span> Dashboard
      </router-link>
      <router-link to="/agenda" class="nav-item" :class="{ active: ruta === '/agenda' }">
        <span class="nav-icon">&#128197;</span> Agenda
      </router-link>
      <router-link to="/kanban" class="nav-item" :class="{ active: ruta === '/kanban' }">
        <span class="nav-icon">&#9776;</span> Gestión
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
  </aside>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getUsuarios } from '../api/usuarios'
import ThemePicker from './ThemePicker.vue'

const route    = useRoute()
const ruta     = ref(route.path)
const usuarios = ref([])

route && (ruta.value = route.path)

onMounted(async () => {
  usuarios.value = await getUsuarios()
})
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
  background: var(--accent); color: #fff;
  font-size: 12px; font-weight: 900;
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
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
.nav-icon { font-size: 11px; }

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
</style>
