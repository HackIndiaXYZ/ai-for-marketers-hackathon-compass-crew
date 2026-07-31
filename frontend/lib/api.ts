import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 120000, // 2 minutes timeout for AI generation
});

export interface Review {
  text: string;
  source: string;
}

export const analyzeBusiness = async (topic: string, reviews: Review[]) => {
  const response = await apiClient.post('/api/analyze', {
    business_topic: topic,
    reviews: reviews,
  });
  return response.data;
};
