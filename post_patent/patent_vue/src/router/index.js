import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import PatentView from '../views/PatentView.vue'
import KeywordView from '../views/KeywordView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/patents',
    name: 'Patents',
    component: PatentView
  },
  {
    path: '/keywords',
    name: 'Keywords',
    component: KeywordView
  },

]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
