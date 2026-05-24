import { createApp } from 'vue'
import App    from './App.vue'
import router from './router'

// Restaurar tema guardado
const tema = localStorage.getItem('tema') || 't-light'
document.body.className = tema

createApp(App).use(router).mount('#app')
