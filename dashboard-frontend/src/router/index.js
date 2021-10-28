import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'dashboard',
    component: () => import('@/views/Dashboard.vue'),
    meta: {
      layout: 'content',
    },
  },
  {
    path: '/add-housing',
    name: 'add-housing',
    component: () => import('@/views/AddHousing.vue'),
    meta: {
      layout: 'content',
    },
  },
  {
    path: '/mon_logement_1',
    name: 'mon_logement_1',
    component: () => import('@/views/HousingView.vue'),
    meta: {
      layout: 'content',
    },
  },
  {
    path: '/login',
    name: 'auth-login',
    component: () => import('@/views/login/Login.vue'),
    meta: {
      layout: 'blank',
    },
  },
  {
    path: '*',
    redirect: 'error-404',
  },
]

const router = new VueRouter({
  mode: 'history',
  base: '/dashboard',
  routes,
  scrollBehavior() {
    return { x: 0, y: 0 }
  },
})

export default router
