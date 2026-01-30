import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Auth API
export const authAPI = {
  signup: (data: { full_name: string; email: string; password: string }) =>
    api.post('/auth/signup', data),
  login: (data: { email: string; password: string }) =>
    api.post('/auth/login', data),
};

// Onboarding API
export const onboardingAPI = {
  complete: (data: any) => api.post('/onboarding/complete', data),
  getStatus: () => api.get('/onboarding/status'),
};

// Dashboard API
export const dashboardAPI = {
  get: () => api.get('/dashboard/'),
};

// Profile API
export const profileAPI = {
  get: () => api.get('/profile/'),
  update: (data: any) => api.put('/profile/', data),
};

// Universities API
export const universitiesAPI = {
  seed: () => api.get('/universities/seed'),
  search: (params?: any) => api.get('/universities/search', { params }),
  getRecommendations: (params?: any) => api.get('/universities/recommendations', { params }),
  shortlist: (data: { university_id: number; category: string }) =>
    api.post('/universities/shortlist', data),
  getShortlisted: () => api.get('/universities/shortlisted'),
  lock: (id: number) => api.post(`/universities/lock/${id}`),
  unlock: (id: number) => api.post(`/universities/unlock/${id}`),
  removeShortlist: (id: number) => api.delete(`/universities/shortlist/${id}`),
};

// Todos API
export const todosAPI = {
  getAll: (includeCompleted = false) =>
    api.get('/todos', { params: { include_completed: includeCompleted } }),
  create: (data: any) => api.post('/todos', data),
  update: (id: number, data: any) => api.patch(`/todos/${id}`, data),
  delete: (id: number) => api.delete(`/todos/${id}`),
};

// Counselor API
export const counselorAPI = {
  chat: (message: string) => api.post('/counselor/chat', { message }),
  getHistory: (limit = 50) => api.get('/counselor/history', { params: { limit } }),
  clearHistory: () => api.delete('/counselor/history'),
  getQuestions: () => api.get('/counselor/questions'),
};

export default api;
