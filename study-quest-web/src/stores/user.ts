import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { User, UserRole } from '@/types/user'

export const useUserStore = defineStore('user', () => {
  // 状态
  const currentUser = ref<User | null>(null)
  const token = ref<string | null>(null)
  const isAuthenticated = ref(false)

  // 计算属性
  const userRole = computed(() => currentUser.value?.role || null)
  const isStudent = computed(() => userRole.value === 'student')
  const isParent = computed(() => userRole.value === 'parent')
  const isTeacher = computed(() => userRole.value === 'teacher')

  // 动作
  const login = async (credentials: { username: string; password: string; role: UserRole }) => {
    try {
      // 这里应该调用API进行认证
      // 暂时模拟登录成功
      const mockUser: User = {
        id: '1',
        username: credentials.username,
        role: credentials.role,
        nickname: credentials.username,
        avatar: '',
        level: 1,
        experience: 0,
        goldCoins: 100,
        createdAt: new Date().toISOString()
      }

      currentUser.value = mockUser
      token.value = 'mock-token-' + Date.now()
      isAuthenticated.value = true

      // 保存到本地存储
      localStorage.setItem('token', token.value)
      localStorage.setItem('userRole', credentials.role)
      localStorage.setItem('userInfo', JSON.stringify(mockUser))

      return { success: true, user: mockUser }
    } catch (error) {
      console.error('登录失败:', error)
      return { success: false, error: '登录失败' }
    }
  }

  const logout = () => {
    currentUser.value = null
    token.value = null
    isAuthenticated.value = false

    // 清除本地存储
    localStorage.removeItem('token')
    localStorage.removeItem('userRole')
    localStorage.removeItem('userInfo')
  }

  const updateUserInfo = (updates: Partial<User>) => {
    if (currentUser.value) {
      currentUser.value = { ...currentUser.value, ...updates }
      localStorage.setItem('userInfo', JSON.stringify(currentUser.value))
    }
  }

  const addGoldCoins = (amount: number) => {
    if (currentUser.value) {
      currentUser.value.goldCoins += amount
      localStorage.setItem('userInfo', JSON.stringify(currentUser.value))
    }
  }

  const addExperience = (amount: number) => {
    if (currentUser.value) {
      currentUser.value.experience += amount
      
      // 检查是否升级
      const newLevel = Math.floor(currentUser.value.experience / 100) + 1
      if (newLevel > currentUser.value.level) {
        currentUser.value.level = newLevel
        // 升级奖励
        addGoldCoins(50)
      }
      
      localStorage.setItem('userInfo', JSON.stringify(currentUser.value))
    }
  }

  // 初始化时从本地存储恢复状态
  const initializeFromStorage = () => {
    const storedToken = localStorage.getItem('token')
    const storedUserInfo = localStorage.getItem('userInfo')
    
    if (storedToken && storedUserInfo) {
      try {
        token.value = storedToken
        currentUser.value = JSON.parse(storedUserInfo)
        isAuthenticated.value = true
      } catch (error) {
        console.error('恢复用户状态失败:', error)
        logout()
      }
    }
  }

  return {
    // 状态
    currentUser,
    token,
    isAuthenticated,
    
    // 计算属性
    userRole,
    isStudent,
    isParent,
    isTeacher,
    
    // 动作
    login,
    logout,
    updateUserInfo,
    addGoldCoins,
    addExperience,
    initializeFromStorage
  }
}) 