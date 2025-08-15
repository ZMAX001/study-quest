<template>
  <div class="battle-page">
    <div class="battle-header">
      <h1>学习战斗</h1>
      <p>通过答题挑战提升技能</p>
    </div>
    
    <div class="battle-content">
      <div class="battle-card">
        <h2>战斗准备中...</h2>
        <p>此功能正在开发中</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// 战斗页面组件
</script>

<style scoped>
.battle-page {
  padding: 20px;
  min-height: 100vh;
  background: #f5f7fa;
}

.battle-header {
  text-align: center;
  margin-bottom: 30px;
}

.battle-header h1 {
  color: #333;
  margin-bottom: 10px;
}

.battle-header p {
  color: #666;
}

.battle-content {
  max-width: 800px;
  margin: 0 auto;
}

.battle-card {
  background: white;
  padding: 40px;
  border-radius: 15px;
  text-align: center;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.battle-card h2 {
  color: #333;
  margin-bottom: 15px;
}

.battle-card p {
  color: #666;
}
</style> 