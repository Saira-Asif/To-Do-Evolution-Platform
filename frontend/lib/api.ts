import ky from 'ky';

// Base API configuration
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

// Create a base client with common configuration
const apiClient = ky.extend({
  prefixUrl: API_BASE_URL,
  timeout: 10000, // 10 seconds timeout
  hooks: {
    beforeRequest: [
      (request) => {
        // Add auth token to requests if available
        const token = localStorage.getItem('auth_token');
        if (token) {
          request.headers.set('Authorization', `Bearer ${token}`);
        }
      },
    ],
    afterResponse: [
      async (request, options, response) => {
        // Handle specific status codes if needed
        if (response.status === 401) {
          // Token might be expired, redirect to login
          localStorage.removeItem('auth_token');
          window.location.href = '/login';
        }
        return response;
      },
    ],
  },
});

export { apiClient, API_BASE_URL };