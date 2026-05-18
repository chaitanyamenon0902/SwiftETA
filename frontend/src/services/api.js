import axios from 'axios'

const API = axios.create({
  baseURL: 'http://127.0.0.1:8000'
})

export const predictETA = async (payload) => {
  const response = await API.post('/predict_eta', payload)
  return response.data
}

export const getAnalytics = async () => {
  const response = await API.get('/analytics')
  return response.data
}

export const getModelMetrics = async () => {
  const response = await API.get('/model/metrics')
  return response.data
}

export default API