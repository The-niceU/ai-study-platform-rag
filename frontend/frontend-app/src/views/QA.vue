<template>
  <AppLayout>
    <div class="qa-page">
      <div class="qa-grid">
        <el-card class="main-card input-card">
          <template #header>
            <div class="panel-header">
              <div>
                <h2 class="panel-title">智能问答</h2>
                <p class="panel-subtitle">基于已上传课程资料进行检索增强问答</p>
              </div>
            </div>
          </template>

          <el-form>
            <el-form-item label="请输入问题">
              <el-input
                v-model="query"
                type="textarea"
                :rows="6"
                placeholder="例如：讲座播放的动画短片名称是什么？"
                :disabled="loading"
              />
            </el-form-item>

            <div class="example-box">
              <div class="example-title">示例问题</div>
              <div class="example-list">
                <el-button text @click="fillExample('讲座播放的动画短片名称是什么？')">
                  讲座播放的动画短片名称是什么？
                </el-button>
                <el-button text @click="fillExample('讲座动画短片的内容是什么？')">
                  讲座动画短片的内容是什么？
                </el-button>
                <el-button text @click="fillExample('讲座中提到的核心观点有哪些？')">
                  讲座中提到的核心观点有哪些？
                </el-button>
              </div>
            </div>

            <el-form-item label="返回片段数">
              <el-input-number v-model="topK" :min="1" :max="10" :disabled="loading" />
            </el-form-item>

            <el-form-item>
              <div class="action-row">
                <el-button type="primary" :loading="loading" @click="handleAsk">
                  {{ loading ? '问答中...' : '提交问题' }}
                </el-button>
                <el-button @click="handleClear" :disabled="loading">
                  清空问题
                </el-button>
                <el-button @click="handleCopyAnswer" :disabled="!answer">
                  复制答案
                </el-button>
              </div>
            </el-form-item>
          </el-form>
        </el-card>

        <el-card class="main-card result-card">
          <template #header>
            <div class="panel-header">
              <div>
                <h2 class="panel-title">回答结果</h2>
                <p class="panel-subtitle">系统将基于检索到的资料片段生成答案</p>
              </div>
            </div>
          </template>

          <div v-if="loading" class="loading-box">
            <el-skeleton :rows="8" animated />
          </div>

          <div v-else-if="answer">
            <el-card class="answer-box">
              <div class="answer-text">{{ answer }}</div>
            </el-card>
          </div>

          <div v-else class="empty-box">
            <el-empty description="请输入问题并提交，系统会基于已上传资料进行智能问答" />
          </div>

          <div v-if="sources.length > 0" class="sources-section">
            <div class="sources-title">引用来源</div>
            <el-collapse>
              <el-collapse-item
                v-for="(item, index) in sources"
                :key="index"
                :title="`来源 ${index + 1} | 文件=${item.file_name || '未知文件'} | chunk=${item.chunk_index} | score=${item.score?.toFixed(4)}`"
                :name="index"
              >
                <div class="source-content">{{ item.content }}</div>
              </el-collapse-item>
            </el-collapse>
          </div>
        </el-card>
      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import AppLayout from '../components/AppLayout.vue'
import { askQuestionApi } from '../api/qa'

const query = ref('')
const topK = ref(3)
const loading = ref(false)
const answer = ref('')
const sources = ref([])

const handleAsk = async () => {
  if (!query.value.trim()) {
    ElMessage.warning('请输入问题')
    return
  }

  loading.value = true
  answer.value = ''
  sources.value = []

  try {
    const res = await askQuestionApi({
      query: query.value,
      top_k: topK.value,
    })

    answer.value = res.data.answer
    sources.value = res.data.sources || []
    ElMessage.success('问答成功')
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || '问答失败')
  } finally {
    loading.value = false
  }
}

const handleClear = () => {
  query.value = ''
  answer.value = ''
  sources.value = []
}

const handleCopyAnswer = async () => {
  if (!answer.value) {
    ElMessage.warning('当前没有可复制的答案')
    return
  }

  try {
    await navigator.clipboard.writeText(answer.value)
    ElMessage.success('答案已复制')
  } catch {
    ElMessage.error('复制失败')
  }
}

const fillExample = (text) => {
  query.value = text
}
</script>

<style scoped>
.qa-page {
  padding: 8px 0 24px;
}

.qa-grid {
  display: grid;
  grid-template-columns: 420px 1fr;
  gap: 24px;
  align-items: start;
}

.main-card {
  border-radius: 24px;
  border: none;
  box-shadow: 0 14px 40px rgba(31, 35, 41, 0.08);
  background: linear-gradient(135deg, #ffffff 0%, #fafcff 100%);
}

.panel-title {
  margin: 0 0 8px;
  font-size: 26px;
  font-weight: 800;
  color: #1f2329;
}

.panel-subtitle {
  margin: 0;
  color: #606266;
  line-height: 1.8;
  font-size: 14px;
}

.example-box {
  margin-bottom: 18px;
  padding: 16px 18px;
  border-radius: 16px;
  background: #f7faff;
  border: 1px solid #edf2ff;
}

.example-title {
  font-size: 14px;
  font-weight: 700;
  color: #1f2329;
  margin-bottom: 10px;
}

.example-list {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 6px;
}

.action-row {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.answer-box {
  border-radius: 18px;
  border: none;
  background: #f8fafc;
  box-shadow: none;
}

.answer-text {
  white-space: pre-wrap;
  line-height: 1.9;
  font-size: 15px;
  color: #303133;
}

.sources-section {
  margin-top: 24px;
}

.sources-title {
  font-size: 18px;
  font-weight: 700;
  color: #1f2329;
  margin-bottom: 14px;
}

.source-content {
  white-space: pre-wrap;
  line-height: 1.8;
  color: #303133;
}

.loading-box,
.empty-box {
  margin-top: 8px;
}

@media (max-width: 1000px) {
  .qa-grid {
    grid-template-columns: 1fr;
  }
}
</style>