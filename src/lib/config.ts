
// Configuration for API endpoints
export const API_CONFIG = {
  // Use localhost for local development
  BASE_URL: 'http://localhost:5000',
  
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
