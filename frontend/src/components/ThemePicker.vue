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
  { id: 't-light',      nombre: 'Claro',       color: '#e0e0e0' },
  { id: 't-dark',       nombre: 'Oscuro',      color: '#252525' },
  { id: 't-rose',     nombre: 'Rose',     color: '#d4407a' },
  { id: 't-storm',    nombre: 'Storm',    color: '#3d4f6a' },
  { id: 't-plum',     nombre: 'Plum',     color: '#3d1f5a' },
  { id: 't-denim',    nombre: 'Denim',    color: '#4a6fa5' },
  { id: 't-jade',     nombre: 'Jade',     color: '#1a5a4a' },
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
