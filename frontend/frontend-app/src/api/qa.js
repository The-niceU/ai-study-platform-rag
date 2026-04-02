import request from './auth'

export const askQuestionApi = (data) => {
  return request.post('/qa/', data, {
    headers: {
      Authorization: `Bearer ${localStorage.getItem('token')}`,
    },
  })
}