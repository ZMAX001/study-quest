<template>
  <div class="student-dashboard">
    <!-- 顶部导航栏 -->
    <div class="top-nav">
      <div class="nav-left">
        <h1>学生控制台</h1>
      </div>
      <div class="nav-right">
        <el-button @click="logout" type="danger" size="small">
          退出登录
        </el-button>
      </div>
    </div>

    <!-- 用户信息卡片 -->
    <div class="user-info-card">
      <div class="user-avatar">
        <el-avatar :size="80" :src="userStore.currentUser?.avatar">
          {{ userStore.currentUser?.nickname?.charAt(0) }}
        </el-avatar>
      </div>
      <div class="user-details">
        <h2>{{ userStore.currentUser?.nickname }}</h2>
        <p class="user-level">等级 {{ userStore.currentUser?.level }}</p>
        <div class="user-stats">
          <div class="stat-item">
            <span class="stat-label">经验值</span>
            <span class="stat-value">{{ userStore.currentUser?.experience }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">金币</span>
            <span class="stat-value">🪙 {{ userStore.currentUser?.goldCoins }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 快速操作 -->
    <div class="quick-actions">
      <h3>快速操作</h3>
      <div class="action-grid">
        <div class="action-card" @click="goToQuestMap">
          <div class="action-icon">🗺️</div>
          <h4>任务地图</h4>
          <p>查看学习任务</p>
        </div>
        <div class="action-card" @click="goToBattle">
          <div class="action-icon">⚔️</div>
          <h4>开始战斗</h4>
          <p>答题挑战</p>
        </div>
        <div class="action-card" @click="goToShop">
          <div class="action-icon">🛒</div>
          <h4>装备商店</h4>
          <p>兑换奖励</p>
        </div>
        <div class="action-card" @click="startStudy">
          <div class="action-icon">⏰</div>
          <h4>番茄钟</h4>
          <p>专注学习</p>
        </div>
      </div>
    </div>

    <!-- 今日任务 -->
    <div class="today-tasks">
      <h3>今日任务</h3>
      <div class="task-list">
        <div 
          v-for="task in todayTasks" 
          :key="task.id"
          class="task-item"
          :class="{ completed: task.isCompleted }"
        >
          <div class="task-info">
            <h4>{{ task.title }}</h4>
            <p>{{ task.description }}</p>
            <div class="task-meta">
              <span class="subject">{{ task.subject }}</span>
              <span class="difficulty" :class="task.difficulty">
                {{ getDifficultyText(task.difficulty) }}
              </span>
            </div>
          </div>
          <div class="task-actions">
            <el-button 
              v-if="!task.isCompleted"
              type="primary" 
              size="small"
              @click="startTask(task)"
            >
              开始任务
            </el-button>
            <el-tag v-else type="success">已完成</el-tag>
          </div>
        </div>
      </div>
    </div>

    <!-- 学习统计 -->
    <div class="learning-stats">
      <h3>学习统计</h3>
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-number">{{ weeklyStudyTime }}</div>
          <div class="stat-label">本周学习时长(小时)</div>
        </div>
        <div class="stat-card">
          <div class="stat-number">{{ completedTasksCount }}</div>
          <div class="stat-label">完成任务数</div>
        </div>
        <div class="stat-card">
          <div class="stat-number">{{ streakDays }}</div>
          <div class="stat-label">连续学习天数</div>
        </div>
        <div class="stat-card">
          <div class="stat-number">{{ accuracyRate }}%</div>
          <div class="stat-label">答题正确率</div>
        </div>
      </div>
    </div>

    <!-- 番茄钟弹窗 -->
    <el-dialog v-model="showPomodoro" title="番茄钟学习" width="400px">
      <div class="pomodoro-content">
        <div class="timer-display">
          <div class="time-left">{{ formatTime(timeLeft) }}</div>
          <div class="timer-status">{{ timerStatus }}</div>
        </div>
        <div class="timer-controls">
          <el-button 
            v-if="!timerRunning" 
            type="primary" 
            @click="startTimer"
          >
            开始学习
          </el-button>
          <el-button 
            v-else 
            type="warning" 
            @click="pauseTimer"
          >
            暂停
          </el-button>
          <el-button @click="resetTimer">重置</el-button>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/user'
import type { Quest } from '@/types/quest'

const router = useRouter()
const userStore = useUserStore()

// 番茄钟相关
const showPomodoro = ref(false)
const timeLeft = ref(25 * 60) // 25分钟
const timerRunning = ref(false)
const timerInterval = ref<NodeJS.Timeout | null>(null)
const timerStatus = ref('准备开始')

// 模拟数据
const todayTasks = ref<Quest[]>([
  {
    id: '1',
    title: '数学函数基础',
    description: '完成函数概念的学习和练习',
    subject: '数学',
    difficulty: 'easy',
    experienceReward: 50,
    goldReward: 10,
    deadline: new Date().toISOString(),
    isCompleted: false,
    progress: 0,
    type: 'daily'
  },
  {
    id: '2',
    title: '英语阅读理解',
    description: '阅读短文并回答问题',
    subject: '英语',
    difficulty: 'medium',
    experienceReward: 80,
    goldReward: 15,
    deadline: new Date().toISOString(),
    isCompleted: true,
    progress: 100,
    type: 'daily'
  }
])

const weeklyStudyTime = ref(12)
const streakDays = ref(5)
const accuracyRate = ref(85)

// 计算属性
const completedTasksCount = computed(() => 
  todayTasks.value.filter(task => task.isCompleted).length
)

// 方法
const logout = () => {
  userStore.logout()
  router.push('/')
  ElMessage.success('已退出登录')
}

const goToQuestMap = () => {
  router.push('/student/quest')
}

const goToBattle = () => {
  router.push('/student/battle')
}

const goToShop = () => {
  router.push('/student/shop')
}

const startStudy = () => {
  showPomodoro.value = true
}

const startTask = (task: Quest) => {
  ElMessage.info(`开始任务: ${task.title}`)
  // 这里可以跳转到具体的任务页面
}

const getDifficultyText = (difficulty: string) => {
  const difficultyMap = {
    easy: '简单',
    medium: '中等',
    hard: '困难'
  }
  return difficultyMap[difficulty as keyof typeof difficultyMap] || difficulty
}

const startTimer = () => {
  timerRunning.value = true
  timerStatus.value = '学习中...'
  timerInterval.value = setInterval(() => {
    if (timeLeft.value > 0) {
      timeLeft.value--
    } else {
      completePomodoro()
    }
  }, 1000)
}

const pauseTimer = () => {
  timerRunning.value = false
  timerStatus.value = '已暂停'
  if (timerInterval.value) {
    clearInterval(timerInterval.value)
    timerInterval.value = null
  }
}

const resetTimer = () => {
  timeLeft.value = 25 * 60
  timerRunning.value = false
  timerStatus.value = '准备开始'
  if (timerInterval.value) {
    clearInterval(timerInterval.value)
    timerInterval.value = null
  }
}

const completePomodoro = () => {
  timerRunning.value = false
  timerStatus.value = '学习完成！'
  if (timerInterval.value) {
    clearInterval(timerInterval.value)
    timerInterval.value = null
  }
  
  // 奖励金币和经验
  userStore.addGoldCoins(10)
  userStore.addExperience(25)
  
  ElMessage.success('番茄钟学习完成！获得10金币和25经验值')
  
  setTimeout(() => {
    showPomodoro.value = false
    resetTimer()
  }, 2000)
}

const formatTime = (seconds: number) => {
  const minutes = Math.floor(seconds / 60)
  const remainingSeconds = seconds % 60
  return `${minutes.toString().padStart(2, '0')}:${remainingSeconds.toString().padStart(2, '0')}`
}

onMounted(() => {
  userStore.initializeFromStorage()
})

onUnmounted(() => {
  if (timerInterval.value) {
    clearInterval(timerInterval.value)
  }
})
</script>

<style scoped>
.student-dashboard {
  min-height: 100vh;
  background: #f5f7fa;
  padding: 20px;
}

.top-nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  padding: 20px;
  background: white;
  border-radius: 15px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.top-nav h1 {
  color: #333;
  margin: 0;
}

.user-info-card {
  display: flex;
  align-items: center;
  background: white;
  padding: 30px;
  border-radius: 15px;
  margin-bottom: 30px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.user-avatar {
  margin-right: 30px;
}

.user-details h2 {
  margin: 0 0 10px 0;
  color: #333;
}

.user-level {
  color: #667eea;
  font-weight: bold;
  margin-bottom: 15px;
}

.user-stats {
  display: flex;
  gap: 30px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stat-label {
  font-size: 0.9rem;
  color: #666;
  margin-bottom: 5px;
}

.stat-value {
  font-weight: bold;
  color: #333;
}

.quick-actions {
  background: white;
  padding: 30px;
  border-radius: 15px;
  margin-bottom: 30px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.quick-actions h3 {
  margin: 0 0 20px 0;
  color: #333;
}

.action-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

.action-card {
  background: #f8f9fa;
  padding: 25px;
  border-radius: 12px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.action-card:hover {
  transform: translateY(-5px);
  border-color: #667eea;
  background: white;
}

.action-icon {
  font-size: 3rem;
  margin-bottom: 15px;
}

.action-card h4 {
  margin: 0 0 10px 0;
  color: #333;
}

.action-card p {
  margin: 0;
  color: #666;
  font-size: 0.9rem;
}

.today-tasks {
  background: white;
  padding: 30px;
  border-radius: 15px;
  margin-bottom: 30px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.today-tasks h3 {
  margin: 0 0 20px 0;
  color: #333;
}

.task-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border: 1px solid #e4e7ed;
  border-radius: 10px;
  margin-bottom: 15px;
  transition: all 0.3s ease;
}

.task-item:hover {
  border-color: #667eea;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.1);
}

.task-item.completed {
  background: #f0f9ff;
  border-color: #67c23a;
}

.task-info h4 {
  margin: 0 0 8px 0;
  color: #333;
}

.task-info p {
  margin: 0 0 10px 0;
  color: #666;
  font-size: 0.9rem;
}

.task-meta {
  display: flex;
  gap: 15px;
}

.subject {
  background: #e3f2fd;
  color: #1976d2;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.8rem;
}

.difficulty {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: bold;
}

.difficulty.easy {
  background: #e8f5e8;
  color: #4caf50;
}

.difficulty.medium {
  background: #fff3e0;
  color: #ff9800;
}

.difficulty.hard {
  background: #ffebee;
  color: #f44336;
}

.learning-stats {
  background: white;
  padding: 30px;
  border-radius: 15px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.learning-stats h3 {
  margin: 0 0 20px 0;
  color: #333;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

.stat-card {
  text-align: center;
  padding: 25px;
  background: #f8f9fa;
  border-radius: 12px;
  transition: transform 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-5px);
}

.stat-number {
  font-size: 2.5rem;
  font-weight: bold;
  color: #667eea;
  margin-bottom: 10px;
}

.stat-label {
  color: #666;
  font-size: 0.9rem;
}

.pomodoro-content {
  text-align: center;
}

.timer-display {
  margin-bottom: 30px;
}

.time-left {
  font-size: 3rem;
  font-weight: bold;
  color: #667eea;
  margin-bottom: 10px;
}

.timer-status {
  color: #666;
  font-size: 1.1rem;
}

.timer-controls {
  display: flex;
  justify-content: center;
  gap: 15px;
}

@media (max-width: 768px) {
  .user-info-card {
    flex-direction: column;
    text-align: center;
  }
  
  .user-avatar {
    margin-right: 0;
    margin-bottom: 20px;
  }
  
  .user-stats {
    justify-content: center;
  }
  
  .action-grid {
    grid-template-columns: 1fr;
  }
  
  .task-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 15px;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
}
</style> 