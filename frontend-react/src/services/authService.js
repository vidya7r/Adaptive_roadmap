import api from './api';

export const authService = {
  // Signup
  signup: async (name, email, password) => {
    try {
      const response = await api.post('/auth/signup', {
        name,
        email,
        password,
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || error.message;
    }
  },

  // Login
  login: async (email, password) => {
    try {
      console.log('Attempting login with email:', email);
      console.log('API base URL:', api.defaults.baseURL);
      const response = await api.post('/auth/login', {
        email,
        password,
      });
      
      console.log('Login response:', response);
      
      if (response.data.access_token) {
        console.log('Token received, storing in localStorage');
        localStorage.setItem('token', response.data.access_token);
        localStorage.setItem('user', JSON.stringify(response.data));
        return response.data;
      } else {
        throw new Error('No access token in response');
      }
    } catch (error) {
      console.error('Login error:', error);
      console.error('Error code:', error.code);
      console.error('Error message:', error.message);
      console.error('Error response:', error.response);
      console.error('Full error:', JSON.stringify(error, null, 2));
      
      // Better error message handling
      let errorMsg = 'Network Error - Unable to reach server';
      
      if (error.response?.data?.detail) {
        errorMsg = error.response.data.detail;
      } else if (error.response?.data?.message) {
        errorMsg = error.response.data.message;
      } else if (error.message) {
        errorMsg = error.message;
      } else if (error.code === 'ECONNREFUSED') {
        errorMsg = 'Backend server is not running';
      } else if (error.code === 'ERR_NETWORK') {
        errorMsg = 'Network error - check your connection';
      }
      
      const err = new Error(errorMsg);
      throw err;
    }
  },

  // Get current user
  getCurrentUser: async () => {
    try {
      const response = await api.get('/auth/me');
      localStorage.setItem('user', JSON.stringify(response.data));
      return response.data;
    } catch (error) {
      throw error.response?.data || error.message;
    }
  },

  // Logout
  logout: () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  },
};
