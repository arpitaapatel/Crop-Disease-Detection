import axios from 'axios'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export interface PredictionResponse {
  disease_name: string
  confidence_score: number
  treatment_suggestion: string
}

export const predictDisease = async (file: File): Promise<PredictionResponse> => {
  try {
    const formData = new FormData()
    formData.append('file', file)

    const response = await axios.post(`${API_BASE_URL}/predict`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      timeout: 30000, // 30 seconds timeout
    })

    return response.data
  } catch (error) {
    if (axios.isAxiosError(error)) {
      if (error.response) {
        // Server responded with error status
        throw new Error(error.response.data.detail || 'Server error occurred')
      } else if (error.request) {
        // Request was made but no response received
        throw new Error('Unable to connect to the server. Please check your connection.')
      }
    }
    // Other error
    throw new Error('An unexpected error occurred')
  }
}

export const checkApiHealth = async (): Promise<boolean> => {
  try {
    const response = await axios.get(`${API_BASE_URL}/health`, {
      timeout: 5000,
    })
    return response.data.status === 'healthy'
  } catch (error) {
    return false
  }
}
