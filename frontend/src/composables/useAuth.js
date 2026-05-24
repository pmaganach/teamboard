import { ref, computed } from 'vue'

const _user = ref(JSON.parse(localStorage.getItem('bitacora_user') || 'null'))

export function useAuth() {
  const user      = _user
  const isLoggedIn = computed(() => !!_user.value)
  const isGerente  = computed(() => _user.value?.rol === 'gerente')

  function login(userData) {
    _user.value = userData
    localStorage.setItem('bitacora_user', JSON.stringify(userData))
  }

  function logout() {
    _user.value = null
    localStorage.removeItem('bitacora_user')
  }

  return { user, isLoggedIn, isGerente, login, logout }
}
