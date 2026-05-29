import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  base: '/alarmas/mkt_cliente/bitacora-equipo-ci/',
  plugins: [vue()],
  server: {
    port: 5173
  }
})
