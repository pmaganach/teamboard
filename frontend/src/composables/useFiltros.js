import { ref } from 'vue'

// Estado compartido entre todas las vistas
const desde = ref(null)
const hasta = ref(null)

export function useFiltros() {
  function filtros() {
    const f = {}
    if (desde.value) f.desde = desde.value
    if (hasta.value) f.hasta = hasta.value
    return f
  }

  function limpiar() {
    desde.value = null
    hasta.value = null
  }

  return { desde, hasta, filtros, limpiar }
}
