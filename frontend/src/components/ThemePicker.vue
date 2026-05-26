<template>
  <div class="theme-picker">
    <p class="picker-label">Tema visual</p>
    <div class="temas">
      <button
        v-for="t in temas"
        :key="t.id"
        class="tema-btn"
        :class="{ active: temaActivo === t.id }"
        :title="t.nombre"
        :style="{ '--tc': t.color }"
        @click="elegir(t.id)"
      >
        <span class="dot"></span>
        <span class="tema-nombre">{{ t.nombre }}</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const temas = [
  { id: 't-light',  nombre: 'Claro',    color: '#e0e0e0' },
  { id: 't-dark',   nombre: 'Oscuro',   color: '#3a3a3a' },
  { id: 't-red',    nombre: 'Verisure', color: '#AB0020' },
  { id: 't-ocean',  nombre: 'Ocean',    color: '#0e4d6e' },
  { id: 't-forest', nombre: 'Forest',   color: '#2d6e4e' },
  { id: 't-dusk',   nombre: 'Dusk',     color: '#5b3fa6' },
  { id: 't-rose',   nombre: 'Rose',     color: '#c45070' },
]

const temaActivo = ref(localStorage.getItem('tema') || 't-light')

function elegir(id) {
  temaActivo.value = id
  document.body.className = id
  localStorage.setItem('tema', id)
}
</script>

<style scoped>
.theme-picker { padding: 12px 0; }
.picker-label {
  font-size: 10px; font-weight: 700; text-transform: uppercase;
  letter-spacing: 0.8px; color: var(--text-sub); margin-bottom: 8px;
  padding: 0 16px;
}
.temas { display: flex; flex-direction: column; gap: 2px; }
.tema-btn {
  display: flex; align-items: center; gap: 10px;
  padding: 6px 16px; border-radius: 6px;
  font-size: 12px; color: var(--text-sub);
  transition: background 0.15s, color 0.15s;
  width: 100%; text-align: left;
}
.tema-btn:hover { background: var(--surface2); color: var(--text); }
.tema-btn.active { color: var(--text); font-weight: 600; }
.dot {
  width: 10px; height: 10px; border-radius: 50%;
  background: var(--tc); flex-shrink: 0;
}
</style>
