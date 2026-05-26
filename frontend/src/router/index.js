import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../views/Dashboard.vue'
import Agenda    from '../views/Agenda.vue'
import Kanban    from '../views/Kanban.vue'
import Analitica from '../views/Analitica.vue'
import Login     from '../views/Login.vue'

const routes = [
  { path: '/login',     component: Login,     meta: { public: true } },
  { path: '/',          redirect: '/dashboard' },
  { path: '/dashboard', component: Dashboard  },
  { path: '/agenda',    component: Agenda     },
  { path: '/kanban',    component: Kanban     },
  { path: '/analitica', component: Analitica  },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to) => {
  const user = JSON.parse(localStorage.getItem('bitacora_user') || 'null')
  if (!to.meta.public && !user) return '/login'
})

export default router
