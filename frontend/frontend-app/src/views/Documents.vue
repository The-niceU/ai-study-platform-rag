<template>
  <AppLayout>
    <div class="documents-page">
      <el-card class="main-card page-card">
        <template #header>
          <div class="header">
            <div>
              <h2 class="page-title">文档管理</h2>
              <p class="page-subtitle">上传、查看、删除课程资料，支持 txt / docx / pdf 文件</p>
            </div>
            <el-button type="primary" plain @click="$router.push('/')">返回首页</el-button>
          </div>
        </template>

        <div class="upload-panel">
          <div class="upload-left">
            <div class="upload-title">上传新文档</div>
            <div class="upload-desc">
              仅支持 txt / docx / pdf 文件，单次只能选择 1 个文件。
            </div>
          </div>

          <div class="upload-right">
            <el-upload
              ref="uploadRef"
              class="upload-box"
              :auto-upload="false"
              :show-file-list="true"
              :on-change="handleFileChange"
              :before-upload="beforeUpload"
              :limit="1"
              accept=".txt,.docx,.pdf"
            >
              <template #trigger>
                <el-button type="primary">选择文件</el-button>
              </template>

              <el-button
                type="success"
                style="margin-left: 12px"
                :disabled="!selectedFile"
                @click="handleUpload"
              >
                上传文件
              </el-button>
            </el-upload>
          </div>
        </div>

        <el-divider />

        <div class="table-header">
          <div class="table-title">已上传文档</div>
          <el-tag type="info">{{ documents.length }} 个文件</el-tag>
        </div>

        <el-empty
          v-if="documents.length === 0"
          description="当前还没有上传文档，请先上传 txt / docx / pdf 文件开始使用。"
        />

        <el-table
          v-else
          :data="documents"
          class="doc-table"
          style="width: 100%"
        >
          <el-table-column prop="id" label="ID" width="80" />
          <el-table-column prop="file_name" label="文件名" min-width="260" />
          <el-table-column prop="file_type" label="类型" width="120">
            <template #default="scope">
              <el-tag size="small">{{ scope.row.file_type }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column label="上传时间" width="220">
            <template #default="scope">
              {{ formatTime(scope.row.uploaded_at) }}
            </template>
          </el-table-column>
          <el-table-column label="操作" width="140" fixed="right">
            <template #default="scope">
              <el-button
                type="danger"
                size="small"
                @click="handleDelete(scope.row.id)"
              >
                删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-card>
    </div>
  </AppLayout>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import AppLayout from '../components/AppLayout.vue'
import {
  getDocumentListApi,
  uploadDocumentApi,
  deleteDocumentApi,
} from '../api/document'

const documents = ref([])
const selectedFile = ref(null)
const uploadRef = ref(null)

const loadDocuments = async () => {
  try {
    const res = await getDocumentListApi()
    documents.value = res.data
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || '获取文档列表失败')
  }
}

const beforeUpload = (file) => {
  const allowedTypes = ['txt', 'docx', 'pdf']
  const ext = file.name.split('.').pop()?.toLowerCase()

  if (!allowedTypes.includes(ext)) {
    ElMessage.error('仅支持上传 txt / docx / pdf 文件')
    return false
  }

  return true
}

const handleFileChange = (file) => {
  const ext = file.name.split('.').pop()?.toLowerCase()

  if (!['txt', 'docx', 'pdf'].includes(ext)) {
    selectedFile.value = null
    uploadRef.value?.clearFiles()
    ElMessage.error('仅支持上传 txt / docx / pdf 文件')
    return
  }

  selectedFile.value = file.raw
}

const handleUpload = async () => {
  if (!selectedFile.value) {
    ElMessage.warning('请先选择文件')
    return
  }

  try {
    await uploadDocumentApi(selectedFile.value)
    ElMessage.success('上传成功')
    selectedFile.value = null
    uploadRef.value?.clearFiles()
    loadDocuments()
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || '上传失败')
  }
}

const handleDelete = async (documentId) => {
  try {
    await ElMessageBox.confirm('确认删除该文档吗？删除后不可恢复。', '提示', {
      confirmButtonText: '确认',
      cancelButtonText: '取消',
      type: 'warning',
    })

    await deleteDocumentApi(documentId)
    ElMessage.success('删除成功')
    loadDocuments()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error(error.response?.data?.detail || '删除失败')
    }
  }
}

const formatTime = (timeStr) => {
  if (!timeStr) return '-'
  const date = new Date(timeStr)
  if (Number.isNaN(date.getTime())) return timeStr

  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  const hour = String(date.getHours()).padStart(2, '0')
  const minute = String(date.getMinutes()).padStart(2, '0')
  const second = String(date.getSeconds()).padStart(2, '0')

  return `${year}-${month}-${day} ${hour}:${minute}:${second}`
}

onMounted(() => {
  loadDocuments()
})
</script>

<style scoped>
.documents-page {
  padding: 8px 0 24px;
}

.main-card {
  border-radius: 24px;
  border: none;
  box-shadow: 0 14px 40px rgba(31, 35, 41, 0.08);
}

.page-card {
  background: linear-gradient(135deg, #ffffff 0%, #fafcff 100%);
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 20px;
  flex-wrap: wrap;
}

.page-title {
  margin: 0 0 8px;
  font-size: 28px;
  font-weight: 800;
  color: #1f2329;
}

.page-subtitle {
  margin: 0;
  color: #606266;
  line-height: 1.8;
}

.upload-panel {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 24px;
  flex-wrap: wrap;
  padding: 20px 22px;
  border-radius: 18px;
  background: #f7faff;
  border: 1px solid #edf2ff;
}

.upload-title {
  font-size: 18px;
  font-weight: 700;
  color: #1f2329;
  margin-bottom: 8px;
}

.upload-desc {
  color: #606266;
  line-height: 1.8;
  font-size: 14px;
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.table-title {
  font-size: 18px;
  font-weight: 700;
  color: #1f2329;
}

.doc-table :deep(.el-table__cell) {
  padding-top: 14px;
  padding-bottom: 14px;
}

@media (max-width: 768px) {
  .upload-panel {
    align-items: flex-start;
  }

  .page-title {
    font-size: 24px;
  }
}
</style>