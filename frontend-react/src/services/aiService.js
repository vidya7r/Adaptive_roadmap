import api from './api';

const aiService = {
  /**
   * Generate a dynamic description for a subtopic
   * @param {number} subtopicId - ID of the subtopic
   * @returns {Promise} Description data
   */
  async getDescription(subtopicId) {
    try {
      const response = await api.get(`/ai/generate-description/${subtopicId}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching description:', error);
      throw error;
    }
  },

  /**
   * Generate description by title (POST method)
   * @param {string} title - Title of the topic/subtopic
   * @returns {Promise} Description data
   */
  async generateDescription(title) {
    try {
      const response = await api.post('/ai/generate-description', {
        title: title
      });
      return response.data;
    } catch (error) {
      console.error('Error generating description:', error);
      throw error;
    }
  }
};

export default aiService;
