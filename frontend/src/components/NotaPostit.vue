<template>
  <Teleport to="body">
    <div class="postit-overlay" @mousedown.self="$emit('cerrar')">
      <div class="postit">
        <!-- Encabezado -->
        <div class="postit-top">
          <span class="postit-avatar" :style="{ background: usuario.color + '33', color: usuario.color }">
            {{ usuario.iniciales }}
          </span>
          <span class="postit-nombre">{{ usuario.nombre }}</span>
          <button class="postit-close" @click="$emit('cerrar')">×</button>
        </div>

        <!-- Línea decorativa -->
        <div class="postit-line" :style="{ background: usuario.color }"></div>

        <!-- Lista de notas -->
        <div class="postit-notas" ref="listRef">
          <div v-if="!notas.length" class="postit-empty">Sin notas aún…</div>
          <div v-for="n in notas" :key="n.id" class="nota-item">
            <div class="nota-meta">
              <span class="nota-origen" :style="{ color: n.origen_color }">{{ n.origen_iniciales }}</span>
              <span class="nota-texto">{{ n.texto }}</span>
              <button class="nota-del" @click="borrar(n)">×</button>
            </div>
          </div>
        </div>

        <!-- Input nueva nota -->
        <div class="postit-input-row">
          <textarea
            v-model="nuevaNota"
            class="postit-textarea"
            placeholder="Escribe una nota…"
            rows="2"
            maxlength="200"
            @keydown.enter.prevent="enviar"
          />
          <button class="postit-send" :disabled="!nuevaNota.trim() || !origenId" @click="enviar">↑</button>
        </div>
        <p class="postit-hint">Enter para enviar</p>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import { getNotas, agregarNota, eliminarNota, marcarLeidas } from '../api/usuarios'
import { useAuth } from '../composables/useAuth'

const props = defineProps({
  usuario:  { type: Object, required: true },
  usuarios: { type: Array,  default: () => [] },
})
const emit = defineEmits(['cerrar', 'actualizado'])

const { user } = useAuth()

// Obtener usuario_id robusto: desde auth o buscando por nombre en lista
const origenId = computed(() => {
  if (user.value?.usuario_id) return user.value.usuario_id
  const match = props.usuarios.find(u => u.nombre === user.value?.nombre)
  return match?.id || null
})
const notas     = ref([])
const nuevaNota = ref('')
const listRef   = ref(null)

async function cargar() {
  const r = await getNotas(props.usuario.id)
  notas.value = r.data
  await marcarLeidas(props.usuario.id)
  emit('actualizado')
  await nextTick()
  if (listRef.value) listRef.value.scrollTop = listRef.value.scrollHeight
}

async function enviar() {
  console.log('[Notas] enviar | origenId:', origenId.value, '| texto:', nuevaNota.value)
  if (!nuevaNota.value.trim() || !origenId.value) {
    console.warn('[Notas] bloqueado — origenId null o texto vacío')
    return
  }
  try {
    const r = await agregarNota(props.usuario.id, nuevaNota.value.trim(), origenId.value)
    console.log('[Notas] ok:', r.data)
    nuevaNota.value = ''
    await cargar()
  } catch (e) {
    console.error('[Notas] error:', e.response?.data || e.message)
  }
}

async function borrar(nota) {
  await eliminarNota(props.usuario.id, nota.id)
  await cargar()
}

onMounted(cargar)
</script>

<style scoped>
.postit-overlay {
  position: fixed; inset: 0; z-index: 900;
  background: transparent;
}

.postit {
  position: absolute; top: 50%; left: 50%;
  transform: translate(-50%, -50%);
  width: 300px;
  background: #fffde7;
  border-radius: 3px 3px 6px 6px;
  box-shadow: 3px 4px 18px #0003, 0 1px 2px #0002;
  display: flex; flex-direction: column;
  font-family: 'Segoe UI', sans-serif;
  overflow: hidden;
}

.postit-top {
  display: flex; align-items: center; gap: 8px;
  padding: 10px 12px 8px;
  background: #fff9c4;
}
.postit-avatar {
  width: 26px; height: 26px; border-radius: 50%;
  font-size: 10px; font-weight: 800;
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
}
.postit-nombre {
  flex: 1; font-size: 12px; font-weight: 700; color: #333;
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
.postit-close {
  background: none; border: none; font-size: 20px;
  color: #999; cursor: pointer; line-height: 1; padding: 0 2px;
}
.postit-close:hover { color: #e00; }

.postit-line { height: 3px; width: 100%; }

/* Lista notas */
.postit-notas {
  min-height: 80px; max-height: 220px;
  overflow-y: auto; padding: 10px 12px; display: flex; flex-direction: column; gap: 8px;
  /* líneas de libreta */
  background-image: repeating-linear-gradient(
    to bottom, transparent, transparent 27px, #e0d88855 27px, #e0d88855 28px
  );
  background-size: 100% 28px;
}
.postit-empty { font-size: 11px; color: #aaa; text-align: center; margin-top: 12px; }

.nota-item { display: flex; flex-direction: column; }
.nota-meta { display: flex; align-items: flex-start; gap: 6px; }
.nota-origen {
  font-size: 10px; font-weight: 800; flex-shrink: 0; margin-top: 1px;
}
.nota-texto {
  flex: 1; font-size: 12px; color: #333; line-height: 1.5; word-break: break-word;
}
.nota-del {
  background: none; border: none; font-size: 15px;
  color: #ccc; cursor: pointer; padding: 0; flex-shrink: 0;
  line-height: 1;
}
.nota-del:hover { color: #e00; }

/* Input */
.postit-input-row {
  display: flex; gap: 6px; padding: 8px 12px 4px;
  border-top: 1px dashed #e0d888;
  background: #fffde7;
}
.postit-textarea {
  flex: 1; resize: none; border: none; outline: none;
  background: transparent; font-size: 12px; color: #333;
  font-family: 'Segoe UI', sans-serif; line-height: 1.5;
}
.postit-send {
  width: 28px; height: 28px; border-radius: 50%;
  background: #f9c;
  border: none; cursor: pointer; font-size: 14px;
  flex-shrink: 0; align-self: flex-end;
  transition: background 0.15s;
}
.postit-send:hover:not(:disabled) { background: #f6a; }
.postit-send:disabled { opacity: 0.35; cursor: default; }

.postit-hint {
  font-size: 9px; color: #bbb; text-align: right;
  padding: 0 12px 8px; background: #fffde7;
}
</style>
