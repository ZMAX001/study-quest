<template>
  <div class="teacher-dashboard">
    <div class="dashboard-header">
      <h1>教师控制台</h1>
      <p>管理班级学习任务</p>
    </div>
    
    <div class="dashboard-content">
      <div class="dashboard-card">
        <h2>教师功能开发中...</h2>
        <p>此功能正在开发中</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// 教师控制台组件
</script>

<style scoped>
.teacher-dashboard {
  padding: 20px;
  min-height: 100vh;
  background: #f5f7fa;
}

.dashboard-header {
  text-align: center;
  margin-bottom: 30px;
}

.dashboard-header h1 {
  color: #333;
  margin-bottom: 10px;
}

.dashboard-header p {
  color: #666;
}

.dashboard-content {
  max-width: 800px;
  margin: 0 auto;
}

.dashboard-card {
  background: white;
  padding: 40px;
  border-radius: 15px;
  text-align: center;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.dashboard-card h2 {
  color: #333;
  margin-bottom: 15px;
}

.dashboard-card p {
  color: #666;
}
</style> 