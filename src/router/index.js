import Vue from 'vue'
import VueRouter from 'vue-router'
import BudgetChart from '../components/BudgetChart.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/budget',
    name: 'budget',
    component: BudgetChart,
  }
]

const router = new VueRouter({
  routes
})

export default router
