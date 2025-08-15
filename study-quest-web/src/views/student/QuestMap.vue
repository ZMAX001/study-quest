<template>
  <div class="quest-map">
    <!-- 顶部导航 -->
    <div class="top-nav">
      <div class="nav-left">
        <el-button @click="goBack" icon="ArrowLeft" text>
          返回控制台
        </el-button>
        <h1>任务地图</h1>
      </div>
      <div class="nav-right">
        <el-select v-model="selectedSubject" placeholder="选择学科" @change="filterQuests">
          <el-option
            v-for="subject in subjects"
            :key="subject.id"
            :label="subject.name"
            :value="subject.id"
          />
        </el-select>
      </div>
    </div>

    <!-- 学科选择标签 -->
    <div class="subject-tabs">
      <div 
        v-for="subject in subjects"
        :key="subject.id"
        class="subject-tab"
        :class="{ active: selectedSubject === subject.id }"
        @click="selectSubject(subject.id)"
      >
        <div class="subject-icon">{{ subject.icon }}</div>
        <div class="subject-info">
          <h4>{{ subject.name }}</h4>
          <p>{{ subject.completedQuests }}/{{ subject.totalQuests }}</p>
        </div>
      </div>
    </div>

    <!-- 任务地图内容 -->
    <div class="map-content">
      <div class="knowledge-tree">
        <div class="tree-node root-node">
          <div class="node-content">
            <div class="node-icon">🌳</div>
            <h3>知识树</h3>
            <p>选择学科开始学习</p>
          </div>
        </div>

        <!-- 数学学科 -->
        <div v-if="selectedSubject === 'math' || !selectedSubject" class="subject-section math">
          <h3 class="section-title">📐 数学</h3>
          <div class="chapters-grid">
            <div 
              v-for="chapter in mathChapters"
              :key="chapter.id"
              class="chapter-node"
              :class="{ 
                unlocked: chapter.isUnlocked,
                completed: chapter.isCompleted 
              }"
              @click="selectChapter(chapter)"
            >
              <div class="chapter-icon">{{ chapter.icon }}</div>
              <h4>{{ chapter.name }}</h4>
              <p>{{ chapter.description }}</p>
              <div class="chapter-progress">
                <el-progress 
                  :percentage="chapter.progress" 
                  :color="getProgressColor(chapter.progress)"
                />
              </div>
              <div class="chapter-status">
                <el-tag 
                  v-if="chapter.isCompleted" 
                  type="success" 
                  size="small"
                >
                  已完成
                </el-tag>
                <el-tag 
                  v-else-if="chapter.isUnlocked" 
                  type="primary" 
                  size="small"
                >
                  进行中
                </el-tag>
                <el-tag 
                  v-else 
                  type="info" 
                  size="small"
                >
                  未解锁
                </el-tag>
              </div>
            </div>
          </div>
        </div>

        <!-- 英语学科 -->
        <div v-if="selectedSubject === 'english' || !selectedSubject" class="subject-section english">
          <h3 class="section-title">🇺🇸 英语</h3>
          <div class="chapters-grid">
            <div 
              v-for="chapter in englishChapters"
              :key="chapter.id"
              class="chapter-node"
              :class="{ 
                unlocked: chapter.isUnlocked,
                completed: chapter.isCompleted 
              }"
              @click="selectChapter(chapter)"
            >
              <div class="chapter-icon">{{ chapter.icon }}</div>
              <h4>{{ chapter.name }}</h4>
              <p>{{ chapter.description }}</p>
              <div class="chapter-progress">
                <el-progress 
                  :percentage="chapter.progress" 
                  :color="getProgressColor(chapter.progress)"
                />
              </div>
              <div class="chapter-status">
                <el-tag 
                  v-if="chapter.isCompleted" 
                  type="success" 
                  size="small"
                >
                  已完成
                </el-tag>
                <el-tag 
                  v-else-if="chapter.isUnlocked" 
                  type="primary" 
                  size="small"
                >
                  进行中
                </el-tag>
                <el-tag 
                  v-else 
                  type="info" 
                  size="small"
                >
                  未解锁
                </el-tag>
              </div>
            </div>
          </div>
        </div>

        <!-- 物理学科 -->
        <div v-if="selectedSubject === 'physics' || !selectedSubject" class="subject-section physics">
          <h3 class="section-title">⚡ 物理</h3>
          <div class="chapters-grid">
            <div 
              v-for="chapter in physicsChapters"
              :key="chapter.id"
              class="chapter-node"
              :class="{ 
                unlocked: chapter.isUnlocked,
                completed: chapter.isCompleted 
              }"
              @click="selectChapter(chapter)"
            >
              <div class="chapter-icon">{{ chapter.icon }}</div>
              <h4>{{ chapter.name }}</h4>
              <p>{{ chapter.description }}</p>
              <div class="chapter-progress">
                <el-progress 
                  :percentage="chapter.progress" 
                  :color="getProgressColor(chapter.progress)"
                />
              </div>
              <div class="chapter-status">
                <el-tag 
                  v-if="chapter.isCompleted" 
                  type="success" 
                  size="small"
                >
                  已完成
                </el-tag>
                <el-tag 
                  v-else-if="chapter.isUnlocked" 
                  type="primary" 
                  size="small"
                >
                  进行中
                </el-tag>
                <el-tag 
                  v-else 
                  type="info" 
                  size="small"
                >
                  未解锁
                </el-tag>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 章节详情弹窗 -->
    <el-dialog 
      v-model="showChapterDetail" 
      :title="selectedChapter?.name" 
      width="600px"
    >
      <div v-if="selectedChapter" class="chapter-detail">
        <div class="chapter-header">
          <div class="chapter-icon-large">{{ selectedChapter.icon }}</div>
          <div class="chapter-info">
            <h3>{{ selectedChapter.name }}</h3>
            <p>{{ selectedChapter.description }}</p>
          </div>
        </div>

        <div class="quests-list">
          <h4>任务列表</h4>
          <div 
            v-for="quest in selectedChapter.quests"
            :key="quest.id"
            class="quest-item"
            :class="{ completed: quest.isCompleted }"
          >
            <div class="quest-info">
              <h5>{{ quest.title }}</h5>
              <p>{{ quest.description }}</p>
              <div class="quest-meta">
                <span class="difficulty" :class="quest.difficulty">
                  {{ getDifficultyText(quest.difficulty) }}
                </span>
                <span class="reward">奖励: {{ quest.experienceReward }}经验 + {{ quest.goldReward }}金币</span>
              </div>
            </div>
            <div class="quest-actions">
              <el-button 
                v-if="!quest.isCompleted"
                type="primary" 
                size="small"
                @click="startQuest(quest)"
              >
                开始任务
              </el-button>
              <el-tag v-else type="success">已完成</el-tag>
            </div>
          </div>
        </div>

        <div class="chapter-actions">
          <el-button 
            v-if="selectedChapter.isUnlocked && !selectedChapter.isCompleted"
            type="primary" 
            @click="startChapter(selectedChapter)"
          >
            开始学习
          </el-button>
          <el-button @click="showChapterDetail = false">
            关闭
          </el-button>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const router = useRouter()

// 状态
const selectedSubject = ref('')
const showChapterDetail = ref(false)
const selectedChapter = ref<any>(null)

// 学科数据
const subjects = ref([
  { id: 'math', name: '数学', icon: '📐', totalQuests: 24, completedQuests: 8 },
  { id: 'english', name: '英语', icon: '🇺🇸', totalQuests: 18, completedQuests: 6 },
  { id: 'physics', name: '物理', icon: '⚡', totalQuests: 20, completedQuests: 5 }
])

// 数学章节
const mathChapters = ref([
  {
    id: 'math-1',
    name: '函数基础',
    description: '学习函数的概念、性质和图像',
    icon: '📊',
    isUnlocked: true,
    isCompleted: false,
    progress: 60,
    quests: [
      { id: 'q1', title: '函数概念', description: '理解函数的定义', difficulty: 'easy', experienceReward: 20, goldReward: 5, isCompleted: true },
      { id: 'q2', title: '函数图像', description: '绘制基本函数图像', difficulty: 'medium', experienceReward: 30, goldReward: 8, isCompleted: false }
    ]
  },
  {
    id: 'math-2',
    name: '三角函数',
    description: '掌握三角函数的定义和性质',
    icon: '📐',
    isUnlocked: true,
    isCompleted: false,
    progress: 30,
    quests: [
      { id: 'q3', title: '正弦函数', description: '学习正弦函数的性质', difficulty: 'medium', experienceReward: 35, goldReward: 10, isCompleted: false }
    ]
  },
  {
    id: 'math-3',
    name: '导数应用',
    description: '应用导数解决实际问题',
    icon: '📈',
    isUnlocked: false,
    isCompleted: false,
    progress: 0,
    quests: []
  }
])

// 英语章节
const englishChapters = ref([
  {
    id: 'english-1',
    name: '阅读理解',
    description: '提高英语阅读理解能力',
    icon: '📖',
    isUnlocked: true,
    isCompleted: true,
    progress: 100,
    quests: [
      { id: 'q4', title: '短文阅读', description: '阅读短文并回答问题', difficulty: 'easy', experienceReward: 25, goldReward: 6, isCompleted: true }
    ]
  },
  {
    id: 'english-2',
    name: '语法练习',
    description: '掌握英语语法规则',
    icon: '🔤',
    isUnlocked: true,
    isCompleted: false,
    progress: 45,
    quests: [
      { id: 'q5', title: '时态练习', description: '练习各种时态的使用', difficulty: 'medium', experienceReward: 30, goldReward: 8, isCompleted: false }
    ]
  }
])

// 物理章节
const physicsChapters = ref([
  {
    id: 'physics-1',
    name: '力学基础',
    description: '学习牛顿运动定律',
    icon: '⚖️',
    isUnlocked: true,
    isCompleted: false,
    progress: 70,
    quests: [
      { id: 'q6', title: '牛顿第一定律', description: '理解惯性定律', difficulty: 'easy', experienceReward: 20, goldReward: 5, isCompleted: true },
      { id: 'q7', title: '牛顿第二定律', description: '掌握F=ma公式', difficulty: 'medium', experienceReward: 30, goldReward: 8, isCompleted: false }
    ]
  }
])

// 方法
const goBack = () => {
  router.push('/student')
}

const selectSubject = (subjectId: string) => {
  selectedSubject.value = subjectId
}

const filterQuests = () => {
  // 根据选择的学科过滤任务
}

const selectChapter = (chapter: any) => {
  if (chapter.isUnlocked) {
    selectedChapter.value = chapter
    showChapterDetail.value = true
  } else {
    ElMessage.warning('该章节尚未解锁，请先完成前置章节')
  }
}

const startQuest = (quest: any) => {
  ElMessage.info(`开始任务: ${quest.title}`)
  // 这里可以跳转到具体的任务页面
}

const startChapter = (chapter: any) => {
  ElMessage.info(`开始学习章节: ${chapter.name}`)
  // 这里可以跳转到章节学习页面
}

const getProgressColor = (progress: number) => {
  if (progress >= 80) return '#67c23a'
  if (progress >= 50) return '#e6a23c'
  return '#f56c6c'
}

const getDifficultyText = (difficulty: string) => {
  const difficultyMap = {
    easy: '简单',
    medium: '中等',
    hard: '困难'
  }
  return difficultyMap[difficulty as keyof typeof difficultyMap] || difficulty
}
</script>

<style scoped>
.quest-map {
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

.nav-left {
  display: flex;
  align-items: center;
  gap: 20px;
}

.nav-left h1 {
  margin: 0;
  color: #333;
}

.subject-tabs {
  display: flex;
  gap: 20px;
  margin-bottom: 30px;
  flex-wrap: wrap;
}

.subject-tab {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 20px;
  background: white;
  border-radius: 15px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 2px solid transparent;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.subject-tab:hover {
  transform: translateY(-2px);
}

.subject-tab.active {
  border-color: #667eea;
  background: #f0f4ff;
}

.subject-icon {
  font-size: 2rem;
}

.subject-info h4 {
  margin: 0 0 5px 0;
  color: #333;
}

.subject-info p {
  margin: 0;
  color: #666;
  font-size: 0.9rem;
}

.map-content {
  background: white;
  border-radius: 15px;
  padding: 30px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.knowledge-tree {
  position: relative;
}

.tree-node {
  text-align: center;
  margin-bottom: 40px;
}

.root-node {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  padding: 40px;
  border-radius: 20px;
  margin-bottom: 50px;
}

.node-icon {
  font-size: 4rem;
  margin-bottom: 20px;
}

.root-node h3 {
  font-size: 2rem;
  margin: 0 0 10px 0;
}

.root-node p {
  font-size: 1.1rem;
  opacity: 0.9;
}

.subject-section {
  margin-bottom: 50px;
}

.section-title {
  font-size: 1.8rem;
  color: #333;
  margin-bottom: 30px;
  text-align: center;
}

.chapters-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 25px;
}

.chapter-node {
  background: #f8f9fa;
  border: 2px solid #e4e7ed;
  border-radius: 15px;
  padding: 25px;
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: center;
}

.chapter-node:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
}

.chapter-node.unlocked {
  border-color: #667eea;
  background: white;
}

.chapter-node.completed {
  border-color: #67c23a;
  background: #f0f9ff;
}

.chapter-icon {
  font-size: 3rem;
  margin-bottom: 15px;
}

.chapter-node h4 {
  margin: 0 0 10px 0;
  color: #333;
  font-size: 1.3rem;
}

.chapter-node p {
  margin: 0 0 20px 0;
  color: #666;
  line-height: 1.5;
}

.chapter-progress {
  margin-bottom: 15px;
}

.chapter-status {
  display: flex;
  justify-content: center;
}

.chapter-detail {
  padding: 20px 0;
}

.chapter-header {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid #e4e7ed;
}

.chapter-icon-large {
  font-size: 4rem;
}

.chapter-info h3 {
  margin: 0 0 10px 0;
  color: #333;
}

.chapter-info p {
  margin: 0;
  color: #666;
  line-height: 1.5;
}

.quests-list h4 {
  margin: 0 0 20px 0;
  color: #333;
}

.quest-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border: 1px solid #e4e7ed;
  border-radius: 10px;
  margin-bottom: 15px;
  transition: all 0.3s ease;
}

.quest-item:hover {
  border-color: #667eea;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.1);
}

.quest-item.completed {
  background: #f0f9ff;
  border-color: #67c23a;
}

.quest-info h5 {
  margin: 0 0 8px 0;
  color: #333;
}

.quest-info p {
  margin: 0 0 10px 0;
  color: #666;
  font-size: 0.9rem;
}

.quest-meta {
  display: flex;
  gap: 15px;
  align-items: center;
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

.reward {
  font-size: 0.8rem;
  color: #666;
}

.chapter-actions {
  display: flex;
  justify-content: center;
  gap: 15px;
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px solid #e4e7ed;
}

@media (max-width: 768px) {
  .subject-tabs {
    flex-direction: column;
  }
  
  .chapters-grid {
    grid-template-columns: 1fr;
  }
  
  .chapter-header {
    flex-direction: column;
    text-align: center;
  }
  
  .quest-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 15px;
  }
  
  .quest-meta {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
}
</style> 