import api from './api';

export const examService = {
  // Get all sections (Written, SSB)
  getSections: async () => {
    try {
      const response = await api.get('/api/sections');
      return response.data;
    } catch (error) {
      throw error.response?.data || error.message;
    }
  },

  // Get modules by section
  getModulesBySection: async (sectionId) => {
    try {
      const response = await api.get(`/api/modules?section_id=${sectionId}`);
      return response.data;
    } catch (error) {
      throw error.response?.data || error.message;
    }
  },

  // Get topics by module
  getTopicsByModule: async (moduleId) => {
    try {
      const response = await api.get(`/api/topics/${moduleId}`);
      return response.data;
    } catch (error) {
      throw error.response?.data || error.message;
    }
  },

  // Get subtopics by topic
  getSubtopicsByTopic: async (topicId) => {
    try {
      const response = await api.get(`/api/subtopics/${topicId}`);
      return response.data;
    } catch (error) {
      throw error.response?.data || error.message;
    }
  },

  // Get single subtopic with details
  getSubtopicDetails: async (subtopicId) => {
    try {
      const response = await api.get(`/api/subtopic/${subtopicId}`);
      return response.data;
    } catch (error) {
      throw error.response?.data || error.message;
    }
  },

  // Get subtopic progress status for current user
  getSubtopicProgress: async (subtopicId) => {
    try {
      const response = await api.get(`/api/subtopic/${subtopicId}/progress`);
      return response.data;
    } catch (error) {
      // If no progress yet, return default
      return { status: 'pending', completed: false };
    }
  },

  // Save subtopic progress status
  saveSubtopicProgress: async (subtopicId, status) => {
    try {
      console.log(`📝 Saving progress for subtopic ${subtopicId}: ${status}`);
      const response = await api.post(`/api/subtopic/${subtopicId}/progress`, {
        status: status,
      });
      console.log('✓ Progress saved:', response.data);
      return response.data;
    } catch (error) {
      console.error('✗ Error saving progress:', error);
      console.error('Response:', error.response?.data);
      console.error('Status:', error.response?.status);
      throw error.response?.data || error.message;
    }
  },

  // Reset subtopic progress to pending
  resetSubtopicProgress: async (subtopicId) => {
    try {
      console.log(`🔄 Resetting progress for subtopic ${subtopicId}`);
      const response = await api.delete(`/api/subtopic/${subtopicId}/progress`);
      console.log('✓ Progress reset:', response.data);
      return response.data;
    } catch (error) {
      console.error('✗ Error resetting progress:', error);
      console.error('Response:', error.response?.data);
      throw error.response?.data || error.message;
    }
  },
};
