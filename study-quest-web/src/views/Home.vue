<template>
  <div class="home">
    <div class="hero-section">
      <div class="hero-content">
        <h1 class="hero-title">
          <span class="title-main">Study Quest</span>
          <span class="title-sub">学习冒险之旅</span>
        </h1>
        <p class="hero-description">
          将枯燥的学习变成刺激的冒险！通过完成任务、击败难题、收集奖励，让学习变得有趣而高效。
        </p>
        
        <div class="role-selection">
          <h3>选择你的身份</h3>
          <div class="role-cards">
            <div 
              v-for="role in roles" 
              :key="role.key"
              class="role-card"
              :class="{ active: selectedRole === role.key }"
              @click="selectedRole = role.key"
            >
              <div class="role-icon">
                <el-icon :size="48">
                  <component :is="role.icon" />
                </el-icon>
              </div>
              <h4>{{ role.name }}</h4>
              <p>{{ role.description }}</p>
            </div>
          </div>
        </div>

        <div class="action-buttons">
          <el-button 
            type="primary" 
            size="large" 
            @click="goToLogin"
            :disabled="!selectedRole"
          >
            开始冒险
          </el-button>
          <el-button 
            size="large" 
            @click="showDemo"
          >
            查看演示
          </el-button>
        </div>
      </div>
    </div>

    <div class="features-section">
      <h2>核心特色</h2>
      <div class="features-grid">
        <div class="feature-card">
          <div class="feature-icon">🎯</div>
          <h3>任务系统</h3>
          <p>可视化学科知识树，章节转化为副本，动态难度调整</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">🏆</div>
          <h3>奖励机制</h3>
          <p>虚拟经济系统，金币兑换游戏时间，连续学习解锁宝箱</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">⚔️</div>
          <h3>战斗系统</h3>
          <p>实时答题反馈，组队挑战模式，排行榜竞争</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">👨‍👩‍👧‍👦</div>
          <h3>家长监督</h3>
          <p>学习时长监控，契约制定，成就审核</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import type { UserRole } from '@/types/user'

const router = useRouter()
const selectedRole = ref<UserRole | null>(null)

const roles = [
  {
    key: 'student' as UserRole,
    name: '学生',
    description: '开始你的学习冒险之旅',
    icon: 'User'
  },
  {
    key: 'parent' as UserRole,
    name: '家长',
    description: '监督孩子的学习进度',
    icon: 'House'
  },
  {
    key: 'teacher' as UserRole,
    name: '教师',
    description: '管理班级学习任务',
    icon: 'School'
  }
]

const goToLogin = () => {
  if (selectedRole.value) {
    router.push({
      path: '/login',
      query: { role: selectedRole.value }
    })
  }
}

const showDemo = () => {
  // 显示演示功能
  console.log('演示功能开发中...')
}
</script>

<style scoped>
.home {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.hero-section {
  padding: 80px 20px;
  text-align: center;
  color: white;
}

.hero-content {
  max-width: 1200px;
  margin: 0 auto;
}

.hero-title {
  margin-bottom: 30px;
}

.title-main {
  display: block;
  font-size: 4rem;
  font-weight: bold;
  margin-bottom: 10px;
  text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
}

.title-sub {
  display: block;
  font-size: 1.5rem;
  opacity: 0.9;
}

.hero-description {
  font-size: 1.2rem;
  margin-bottom: 50px;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
  line-height: 1.6;
}

.role-selection {
  margin-bottom: 50px;
}

.role-selection h3 {
  margin-bottom: 30px;
  font-size: 1.5rem;
}

.role-cards {
  display: flex;
  justify-content: center;
  gap: 30px;
  margin-bottom: 40px;
  flex-wrap: wrap;
}

.role-card {
  background: rgba(255, 255, 255, 0.1);
  border: 2px solid transparent;
  border-radius: 15px;
  padding: 30px 20px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
  min-width: 200px;
}

.role-card:hover {
  transform: translateY(-5px);
  background: rgba(255, 255, 255, 0.2);
}

.role-card.active {
  border-color: #ffd700;
  background: rgba(255, 215, 0, 0.1);
}

.role-icon {
  margin-bottom: 20px;
  color: #ffd700;
}

.role-card h4 {
  font-size: 1.3rem;
  margin-bottom: 10px;
}

.role-card p {
  font-size: 0.9rem;
  opacity: 0.8;
  line-height: 1.4;
}

.action-buttons {
  display: flex;
  justify-content: center;
  gap: 20px;
  flex-wrap: wrap;
}

.action-buttons .el-button {
  padding: 15px 30px;
  font-size: 1.1rem;
  border-radius: 25px;
}

.features-section {
  background: white;
  padding: 80px 20px;
  text-align: center;
}

.features-section h2 {
  font-size: 2.5rem;
  margin-bottom: 50px;
  color: #333;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 40px;
  max-width: 1200px;
  margin: 0 auto;
}

.feature-card {
  padding: 40px 20px;
  border-radius: 15px;
  background: #f8f9fa;
  transition: transform 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-10px);
}

.feature-icon {
  font-size: 3rem;
  margin-bottom: 20px;
}

.feature-card h3 {
  font-size: 1.5rem;
  margin-bottom: 15px;
  color: #333;
}

.feature-card p {
  color: #666;
  line-height: 1.6;
}

@media (max-width: 768px) {
  .title-main {
    font-size: 2.5rem;
  }
  
  .role-cards {
    flex-direction: column;
    align-items: center;
  }
  
  .role-card {
    min-width: 250px;
  }
  
  .action-buttons {
    flex-direction: column;
    align-items: center;
  }
}
</style> 