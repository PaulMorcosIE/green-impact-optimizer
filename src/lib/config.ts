
// Configuration for API endpoints
export const API_CONFIG = {
  // Use Railway backend URL in production, localhost in development
  BASE_URL: import.meta.env.PROD 
    ? import.meta.env.VITE_API_URL || 'https://your-app-name.railway.app'
    : 'http://localhost:5000',
  
  ENDPOINTS: {
    HEALTH: '/api/health',
    OPTIMIZE: '/api/optimize',
    DATASET_STATS: '/api/dataset/stats',
    SEARCH: '/api/search'
  }
};

export const getApiUrl = (endpoint: string) => {
  return `${API_CONFIG.BASE_URL}${endpoint}`;
};
