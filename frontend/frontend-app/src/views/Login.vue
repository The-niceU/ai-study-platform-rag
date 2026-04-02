<template>
  <div class="auth-page">
    <div class="auth-container">
      <div class="auth-left">
        <div class="brand-badge">AI</div>
        <h1 class="brand-title">AI 学习平台</h1>
        <p class="brand-desc">
          基于 Vue + FastAPI + RAG 的课程资料智能问答与文档管理系统。
        </p>

        <div class="feature-list">
          <div class="feature-item">· 课程资料上传与管理</div>
          <div class="feature-item">· 基于资料的智能问答</div>
          <div class="feature-item">· 引用来源可追溯</div>
        </div>
      </div>

      <el-card class="auth-card">
        <template #header>
          <div class="card-header">
            <h2>用户登录</h2>
            <p>欢迎回来，请登录后继续使用系统</p>
          </div>
        </template>

        <el-form :model="form" label-width="80px">
          <el-form-item label="用户名">
            <el-input v-model="form.username" placeholder="请输入用户名" />
          </el-form-item>

          <el-form-item label="密码">
            <el-input
              v-model="form.password"
              type="password"
              placeholder="请输入密码"
              show-password
            />
          </el-form-item>

          <el-form-item>
            <div class="action-row">
              <el-button type="primary" @click="handleLogin">登录</el-button>
              <el-button @click="$router.push('/register')">去注册</el-button>
              <el-button text @click="$router.push('/')">返回首页</el-button>
            </div>
          </el-form-item>
        </el-form>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { reactive } from 'vue'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'
import { loginApi } from '../api/auth'

const router = useRouter()

const form = reactive({
  username: '',
  password: '',
})

const handleLogin = async () => {
  try {
    const res = await loginApi(form)
    localStorage.setItem('token', res.data.access_token)
    ElMessage.success('登录成功')
    router.push('/')
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || '登录失败')
  }
}
</script>

<style scoped>
.auth-page {
  min-height: 100vh;
  background:
    radial-gradient(circle at top left, rgba(64, 158, 255, 0.1), transparent 25%),
    radial-gradient(circle at bottom right, rgba(124, 92, 255, 0.1), transparent 25%),
    #f6f8fb;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
}

.auth-container {
  width: 100%;
  max-width: 1120px;
  display: grid;
  grid-template-columns: 1.1fr 0.9fr;
  gap: 28px;
  align-items: center;
}

.auth-left {
  padding: 24px 12px 24px 8px;
}

.brand-badge {
  width: 64px;
  height: 64px;
  border-radius: 18px;
  background: linear-gradient(135deg, #409eff, #7c5cff);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 26px;
  font-weight: 800;
  box-shadow: 0 16px 36px rgba(64, 158, 255, 0.22);
  margin-bottom: 24px;
}

.brand-title {
  margin: 0 0 14px;
  font-size: 42px;
  font-weight: 800;
  color: #1f2329;
}

.brand-desc {
  margin: 0 0 24px;
  color: #606266;
  line-height: 1.9;
  font-size: 16px;
  max-width: 520px;
}

.feature-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  color: #303133;
  font-size: 15px;
}

.auth-card {
  border-radius: 24px;
  border: none;
  box-shadow: 0 18px 46px rgba(31, 35, 41, 0.08);
}

.card-header h2 {
  margin: 0 0 8px;
  font-size: 28px;
  font-weight: 800;
  color: #1f2329;
}

.card-header p {
  margin: 0;
  color: #909399;
  line-height: 1.8;
}

.action-row {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

@media (max-width: 900px) {
  .auth-container {
    grid-template-columns: 1fr;
  }

  .auth-left {
    padding: 0;
  }

  .brand-title {
    font-size: 32px;
  }
}
</style>