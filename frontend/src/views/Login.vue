<template>
  <div class="login-wrap">
    <div class="login-box">

      <div class="login-logo">
        <img src="/logo-verisure.png" alt="Verisure" class="login-logo-img" />
      </div>

      <div class="login-header">
        <h1 class="login-title">Bitácora</h1>
        <p class="login-sub">Customer Intelligence · Verisure</p>
      </div>

      <!-- Paso 1: email -->
      <div v-if="paso === 1" class="login-form">
        <div class="campo">
          <label>Correo corporativo</label>
          <input
            v-model="email"
            type="email"
            placeholder="nombre@verisure.cl"
            @keydown.enter="solicitarCodigo"
            :disabled="cargando"
            autofocus
          />
        </div>
        <p v-if="error" class="login-error">{{ error }}</p>
        <button class="btn-login" @click="solicitarCodigo" :disabled="cargando || !email">
          <span v-if="cargando">Enviando...</span>
          <span v-else>Continuar</span>
        </button>
      </div>

      <!-- Paso 2: OTP -->
      <div v-if="paso === 2" class="login-form">
        <p class="otp-hint">Ingresa el código de 6 dígitos enviado a <strong>{{ email }}</strong></p>
        <div class="campo">
          <label>Código de acceso</label>
          <input
            v-model="codigo"
            type="text"
            maxlength="6"
            placeholder="000000"
            class="otp-input"
            @keydown.enter="verificarCodigo"
            :disabled="cargando"
            autofocus
          />
        </div>
        <p v-if="error" class="login-error">{{ error }}</p>
        <button class="btn-login" @click="verificarCodigo" :disabled="cargando || codigo.length < 6">
          <span v-if="cargando">Verificando...</span>
          <span v-else>Ingresar</span>
        </button>
        <button class="btn-volver" @click="paso = 1; error = ''">← Cambiar correo</button>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { requestOtp, verifyOtp } from '../api/auth'
import { useAuth } from '../composables/useAuth'

const router  = useRouter()
const { login } = useAuth()

const paso    = ref(1)
const email   = ref('')
const codigo  = ref('')
const error   = ref('')
const cargando = ref(false)

async function solicitarCodigo() {
  if (!email.value) return
  error.value   = ''
  cargando.value = true
  try {
    await requestOtp(email.value.trim().toLowerCase())
    paso.value = 2
  } catch (e) {
    error.value = e.response?.data?.detail || 'Error al enviar el código'
  } finally {
    cargando.value = false
  }
}

async function verificarCodigo() {
  if (codigo.value.length < 6) return
  error.value   = ''
  cargando.value = true
  try {
    const res = await verifyOtp(email.value.trim().toLowerCase(), codigo.value.trim())
    login(res.data)
    router.push('/dashboard')
  } catch (e) {
    error.value = e.response?.data?.detail || 'Código incorrecto'
  } finally {
    cargando.value = false
  }
}
</script>

<style scoped>
.login-wrap {
  min-height: 100vh; width: 100%;
  display: flex; align-items: center; justify-content: center;
  background: var(--bg);
}

.login-box {
  width: 100%; max-width: 380px;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 20px;
  padding: 36px 32px;
  display: flex; flex-direction: column; gap: 24px;
}

.login-logo { display: flex; justify-content: center; }
.login-logo-img { width: 56px; height: 56px; object-fit: contain; }

.login-header { text-align: center; }
.login-title { font-size: 22px; font-weight: 900; color: var(--text); margin-bottom: 4px; }
.login-sub   { font-size: 12px; color: var(--text-sub); }

.login-form { display: flex; flex-direction: column; gap: 14px; }

.campo { display: flex; flex-direction: column; gap: 5px; }
.campo label {
  font-size: 11px; font-weight: 700; color: var(--text-sub);
  text-transform: uppercase; letter-spacing: 0.4px;
}
.campo input {
  background: var(--surface2); border: 1px solid var(--border);
  border-radius: 10px; padding: 11px 14px;
  color: var(--text); font-size: 14px; font-family: inherit;
  transition: border-color 0.15s; width: 100%;
}
.campo input:focus { outline: none; border-color: var(--accent); }
.campo input:disabled { opacity: 0.5; }

.otp-input { font-size: 22px; font-weight: 800; letter-spacing: 6px; text-align: center; }
.otp-hint  { font-size: 12px; color: var(--text-sub); text-align: center; line-height: 1.5; }

.btn-login {
  background: var(--accent); color: #fff;
  border-radius: 10px; padding: 12px;
  font-size: 14px; font-weight: 700;
  transition: opacity 0.15s; width: 100%;
}
.btn-login:hover:not(:disabled) { opacity: 0.88; }
.btn-login:disabled { opacity: 0.4; cursor: not-allowed; }

.btn-volver {
  font-size: 12px; color: var(--text-sub);
  text-align: center; transition: color 0.15s;
}
.btn-volver:hover { color: var(--text); }

.login-error {
  font-size: 12px; color: #ED002F;
  background: #ED002F12; border-radius: 8px;
  padding: 8px 12px; text-align: center;
}
</style>
