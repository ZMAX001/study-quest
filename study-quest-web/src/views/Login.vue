<template>
  <div class="login-page">
    <div class="login-container">
      <div class="login-header">
        <h1>Study Quest</h1>
        <p>欢迎回来，{{ roleDisplayName }}</p>
      </div>

      <el-form 
        ref="loginFormRef"
        :model="loginForm"
        :rules="loginRules"
        class="login-form"
        @submit.prevent="handleLogin"
      >
        <el-form-item prop="username">
          <el-input
            v-model="loginForm.username"
            placeholder="用户名"
            size="large"
            prefix-icon="User"
          />
        </el-form-item>

        <el-form-item prop="password">
          <el-input
            v-model="loginForm.password"
            type="password"
            placeholder="密码"
            size="large"
            prefix-icon="Lock"
            show-password
          />
        </el-form-item>

        <el-form-item>
          <el-button
            type="primary"
            size="large"
            class="login-button"
            :loading="loading"
            @click="handleLogin"
          >
            {{ loading ? '登录中...' : '登录' }}
          </el-button>
        </el-form-item>

        <div class="demo-accounts">
          <p>演示账号：</p>
          <div class="demo-account" @click="fillDemoAccount('student')">
            <strong>学生账号：</strong> student / 123456
          </div>
          <div class="demo-account" @click="fillDemoAccount('parent')">
            <strong>家长账号：</strong> parent / 123456
          </div>
          <div class="demo-account" @click="fillDemoAccount('teacher')">
            <strong>教师账号：</strong> teacher / 123456
          </div>
        </div>
      </el-form>

      <div class="back-to-home">
        <el-button text @click="goHome">
          <el-icon><ArrowLeft /></el-icon>
          返回首页
        </el-button>
      </div>
    </div>

    <div class="background-decoration">
      <div class="floating-shapes">
        <div class="shape shape-1">📚</div>
        <div class="shape shape-2">⚡</div>
        <div class="shape shape-3">🎯</div>
        <div class="shape shape-4">🏆</div>
        <div class="shape shape-5">💡</div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage, type FormInstance, type FormRules } from 'element-plus'
import { useUserStore } from '@/stores/user'
import type { UserRole } from '@/types/user'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

const loginFormRef = ref<FormInstance>()
const loading = ref(false)

const loginForm = ref({
  username: '',
  password: '',
  role: route.query.role as UserRole || 'student'
})

const loginRules: FormRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度在 3 到 20 个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '密码长度在 6 到 20 个字符', trigger: 'blur' }
  ]
}

const roleDisplayName = computed(() => {
  const roleNames = {
    student: '学生',
    parent: '家长',
    teacher: '教师'
  }
  return roleNames[loginForm.value.role] || '学生'
})

const handleLogin = async () => {
  if (!loginFormRef.value) return
  
  try {
    await loginFormRef.value.validate()
    loading.value = true
    
    const result = await userStore.login({
      username: loginForm.value.username,
      password: loginForm.value.password,
      role: loginForm.value.role
    })
    
    if (result.success) {
      ElMessage.success('登录成功！')
      
      // 根据角色跳转到不同的页面
      const redirectPath = `/${loginForm.value.role}`
      router.push(redirectPath)
    } else {
      ElMessage.error(result.error || '登录失败')
    }
  } catch (error) {
    console.error('登录错误:', error)
    ElMessage.error('登录失败，请检查输入信息')
  } finally {
    loading.value = false
  }
}

const fillDemoAccount = (role: UserRole) => {
  loginForm.value.role = role
  if (role === 'student') {
    loginForm.value.username = 'student'
    loginForm.value.password = '123456'
  } else if (role === 'parent') {
    loginForm.value.username = 'parent'
    loginForm.value.password = '123456'
  } else if (role === 'teacher') {
    loginForm.value.username = 'teacher'
    loginForm.value.password = '123456'
  }
}

const goHome = () => {
  router.push('/')
}

onMounted(() => {
  // 如果URL中没有角色参数，默认设置为学生
  if (!route.query.role) {
    loginForm.value.role = 'student'
  }
})
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
}

.login-container {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-radius: 20px;
  padding: 40px;
  width: 100%;
  max-width: 400px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  position: relative;
  z-index: 2;
}

.login-header {
  text-align: center;
  margin-bottom: 30px;
}

.login-header h1 {
  font-size: 2.5rem;
  color: #667eea;
  margin-bottom: 10px;
  font-weight: bold;
}

.login-header p {
  color: #666;
  font-size: 1.1rem;
}

.login-form {
  margin-bottom: 20px;
}

.login-button {
  width: 100%;
  height: 50px;
  border-radius: 25px;
  font-size: 1.1rem;
  font-weight: bold;
}

.demo-accounts {
  background: #f8f9fa;
  border-radius: 10px;
  padding: 20px;
  margin-bottom: 20px;
}

.demo-accounts p {
  margin-bottom: 15px;
  color: #666;
  font-size: 0.9rem;
}

.demo-account {
  padding: 8px 12px;
  margin-bottom: 8px;
  background: white;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.9rem;
}

.demo-account:hover {
  background: #e3f2fd;
  transform: translateX(5px);
}

.demo-account:last-child {
  margin-bottom: 0;
}

.back-to-home {
  text-align: center;
}

.background-decoration {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 1;
}

.floating-shapes {
  position: relative;
  width: 100%;
  height: 100%;
}

.shape {
  position: absolute;
  font-size: 2rem;
  animation: float 6s ease-in-out infinite;
  opacity: 0.6;
}

.shape-1 {
  top: 20%;
  left: 10%;
  animation-delay: 0s;
}

.shape-2 {
  top: 60%;
  right: 15%;
  animation-delay: 1s;
}

.shape-3 {
  top: 80%;
  left: 20%;
  animation-delay: 2s;
}

.shape-4 {
  top: 30%;
  right: 25%;
  animation-delay: 3s;
}

.shape-5 {
  top: 70%;
  left: 60%;
  animation-delay: 4s;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0px) rotate(0deg);
  }
  50% {
    transform: translateY(-20px) rotate(180deg);
  }
}

@media (max-width: 480px) {
  .login-container {
    margin: 20px;
    padding: 30px 20px;
  }
  
  .login-header h1 {
    font-size: 2rem;
  }
}
</style> 