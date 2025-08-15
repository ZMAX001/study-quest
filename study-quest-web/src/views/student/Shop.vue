<template>
  <div class="shop-page">
    <div class="shop-header">
      <h1>装备商店</h1>
      <p>用金币兑换游戏时间和道具</p>
    </div>
    
    <div class="shop-content">
      <div class="shop-card">
        <h2>商店建设中...</h2>
        <p>此功能正在开发中</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// 商店页面组件
</script>

<style scoped>
.shop-page {
  padding: 20px;
  min-height: 100vh;
  background: #f5f7fa;
}

.shop-header {
  text-align: center;
  margin-bottom: 30px;
}

.shop-header h1 {
  color: #333;
  margin-bottom: 10px;
}

.shop-header p {
  color: #666;
}

.shop-content {
  max-width: 800px;
  margin: 0 auto;
}

.shop-card {
  background: white;
  padding: 40px;
  border-radius: 15px;
  text-align: center;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.shop-card h2 {
  color: #333;
  margin-bottom: 15px;
}

.shop-card p {
  color: #666;
}
</style> 