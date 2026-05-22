import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../views/Dashboard.vue'
import Agenda    from '../views/Agenda.vue'
import Kanban    from '../views/Kanban.vue'

const routes = [
  { path: '/',          redirect: '/dashboard' },
  { path: '/dashboard', component: Dashboard },
  { path: '/agenda',    component: Agenda    },
  { path: '/kanban',    component: Kanban    },
]

export default createRouter({
  history: createWebHistory(),
  routes
})
