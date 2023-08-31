import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import DashboardView from '@/views/DashboardView.vue';
import ResumesView from '@/views/ResumesView.vue';
import AllResumesView from '@/views/AllResumesView.vue';



const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  },
  {
    path: '/dashboard',
    name: 'Dashboard_view',
    component: DashboardView,
  },
  {
    path: '/resumes',
    name: 'Resumes_View',
    component: ResumesView,
    },
    {
      path: '/all_resumes',
      name: 'all_resumes_view',
      component: AllResumesView,
    },

]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
