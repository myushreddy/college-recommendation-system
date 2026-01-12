import axios from 'axios'
import type { NLPQueryResponse, SearchResponse, CollegeDetailResponse } from '@/types'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const nlpService = {
  async processQuery(query: string): Promise<NLPQueryResponse> {
    const response = await apiClient.post('/api/nlp/query', { query })
    return response.data
  },

  async getExamples() {
    const response = await apiClient.get('/api/nlp/examples')
    return response.data
  },
}

export const collegeService = {
  async search(params: Record<string, any>): Promise<SearchResponse> {
    const response = await apiClient.get('/api/colleges/search', { params })
    return response.data
  },

  async getDetails(collegeId: number): Promise<CollegeDetailResponse> {
    const response = await apiClient.get(`/api/colleges/${collegeId}`)
    return response.data
  },

  async compare(collegeIds: number[]) {
    const response = await apiClient.post('/api/colleges/compare', { college_ids: collegeIds })
    return response.data
  },

  async getRecommendations(preferences: Record<string, any>) {
    const response = await apiClient.post('/api/colleges/recommendations', preferences)
    return response.data
  },

  async getStats() {
    const response = await apiClient.get('/api/colleges/stats/overview')
    return response.data
  },
}

export default apiClient
