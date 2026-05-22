<template>
  <header class="topbar">
    <div class="topbar-left">
      <h1 class="topbar-title">{{ titulo }}</h1>
      <span class="topbar-sub">{{ sub }}</span>
    </div>
    <div class="topbar-right">
      <slot name="filtros" />
      <button class="btn-nuevo" @click="$emit('nuevo')">
        + Nuevo trabajo
      </button>
    </div>
  </header>
</template>

<script setup>
defineProps({
  titulo: { type: String, default: 'TeamBoard' },
  sub:    { type: String, default: '' },
})
defineEmits(['nuevo'])
</script>

<style scoped>
.topbar {
  display: flex; align-items: center; justify-content: space-between;
  padding: 14px 24px;
  background: var(--topbar-bg);
  border-bottom: 1px solid var(--border);
  gap: 16px;
}
.topbar-left { display: flex; align-items: baseline; gap: 10px; }
.topbar-title { font-size: 16px; font-weight: 700; color: var(--text); }
.topbar-sub   { font-size: 11px; color: var(--text-sub); }

.topbar-right { display: flex; align-items: center; gap: 10px; }

.btn-nuevo {
  background: var(--accent); color: #fff;
  padding: 7px 14px; border-radius: 8px;
  font-size: 12px; font-weight: 700;
  transition: opacity 0.15s;
  white-space: nowrap;
}
.btn-nuevo:hover { opacity: 0.88; }
</style>
