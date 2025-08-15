import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home.vue'),
    meta: { title: '学习冒险 - 首页' }
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: { title: '登录' }
  },
  {
    path: '/student',
    name: 'StudentDashboard',
    component: () => import('@/views/student/Dashboard.vue'),
    meta: { title: '学生控制台', requiresAuth: true, role: 'student' }
  },
  {
    path: '/student/quest',
    name: 'QuestMap',
    component: () => import('@/views/student/QuestMap.vue'),
    meta: { title: '任务地图', requiresAuth: true, role: 'student' }
  },
  {
    path: '/student/battle',
    name: 'Battle',
    component: () => import('@/views/student/Battle.vue'),
    meta: { title: '学习战斗', requiresAuth: true, role: 'student' }
  },
  {
    path: '/student/shop',
    name: 'Shop',
    component: () => import('@/views/student/Shop.vue'),
    meta: { title: '装备商店', requiresAuth: true, role: 'student' }
  },
  {
    path: '/parent',
    name: 'ParentDashboard',
    component: () => import('@/views/parent/Dashboard.vue'),
    meta: { title: '家长控制台', requiresAuth: true, role: 'parent' }
  },
  {
    path: '/teacher',
    name: 'TeacherDashboard',
    component: () => import('@/views/teacher/Dashboard.vue'),
    meta: { title: '教师控制台', requiresAuth: true, role: 'teacher' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  // 设置页面标题
  if (to.meta.title) {
    document.title = to.meta.title as string
  }
  
  // 检查是否需要认证
  if (to.meta.requiresAuth) {
    const token = localStorage.getItem('token')
    if (!token) {
      next('/login')
      return
    }
    
    // 检查角色权限
    const userRole = localStorage.getItem('userRole')
    if (to.meta.role && to.meta.role !== userRole) {
      next('/')
      return
    }
  }
  
  next()
})

export default router 