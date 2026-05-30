import axios from 'axios';

// In dev, Vite proxies /api → http://localhost:8000 (see vite.config.js)
// In prod, set VITE_API_URL to your deployed API base URL
const API_BASE = import.meta.env.VITE_API_URL || '/api';

const api = axios.create({ baseURL: API_BASE, timeout: 15000 });

export const checkHealth = () => api.get('/health');

export const startAnalysis = (source, language) =>
  api.post('/analyse', { source, language });

export const pollStatus = (jobId) => api.get(`/status/${jobId}`);

export const sendChatMessage = (jobId, question) =>
  api.post(`/chat/${jobId}`, { question });

export default api;
