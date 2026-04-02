import request from './auth'

export const uploadDocumentApi = (file) => {
  const formData = new FormData()
  formData.append('file', file)

  return request.post('/documents/upload', formData, {
    headers: {
      Authorization: `Bearer ${localStorage.getItem('token')}`,
      'Content-Type': 'multipart/form-data',
    },
  })
}

export const getDocumentListApi = () => {
  return request.get('/documents/', {
    headers: {
      Authorization: `Bearer ${localStorage.getItem('token')}`,
    },
  })
}

export const deleteDocumentApi = (documentId) => {
  return request.delete(`/documents/${documentId}`, {
    headers: {
      Authorization: `Bearer ${localStorage.getItem('token')}`,
    },
  })
}