// API Configuration
const API_BASE_URL = 'http://127.0.0.1:8001';

// Store token
let authToken = localStorage.getItem('token');

// API Functions
const api = {
  // Auth
  login: async (email, password) => {
    const formData = new URLSearchParams();
    formData.append('username', email);
    formData.append('password', password);
    
    const response = await fetch(`${API_BASE_URL}/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: formData,
    });
    
    if (!response.ok) {
      throw new Error('Login failed');
    }
    
    const data = await response.json();
    authToken = data.access_token;
    localStorage.setItem('token', authToken);
    return data;
  },

  signup: async (name, email, password) => {
    const response = await fetch(`${API_BASE_URL}/auth/signup`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ name, email, password }),
    });
    
    if (!response.ok) {
      throw new Error('Signup failed');
    }
    
    return await response.json();
  },

  // Modules/Sections
  getModules: async () => {
    const response = await fetch(`${API_BASE_URL}/api/modules`);
    if (!response.ok) throw new Error('Failed to fetch modules');
    return await response.json();
  },

  // Topics
  getTopicsByModule: async (moduleId) => {
    const response = await fetch(`${API_BASE_URL}/api/topics/${moduleId}`);
    if (!response.ok) throw new Error('Failed to fetch topics');
    return await response.json();
  },

  // Subtopics
  getSubtopicsByTopic: async (topicId) => {
    const response = await fetch(`${API_BASE_URL}/api/subtopics/${topicId}`);
    if (!response.ok) throw new Error('Failed to fetch subtopics');
    return await response.json();
  },

  getSubtopicDetail: async (subtopicId) => {
    const response = await fetch(`${API_BASE_URL}/api/subtopic/${subtopicId}`);
    if (!response.ok) throw new Error('Failed to fetch subtopic detail');
    return await response.json();
  },

  // Test
  generateTest: async (topicId) => {
    const response = await fetch(`${API_BASE_URL}/test/generate/${topicId}`, {
      headers: {
        'Authorization': `Bearer ${authToken}`,
      },
    });
    
    if (!response.ok) throw new Error('Failed to generate test');
    return await response.json();
  },

  submitTest: async (topicId, answers) => {
    const response = await fetch(`${API_BASE_URL}/test/submit`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${authToken}`,
      },
      body: JSON.stringify({ topic_id: topicId, answers }),
    });
    
    if (!response.ok) throw new Error('Failed to submit test');
    return await response.json();
  },
};
