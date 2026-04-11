import api from './api';

const RESOURCES_API_BASE_URL = '/api/resources';

export const resourceService = {
  /**
   * Get all resources for a specific subtopic
   * @param {number} subtopicId - The subtopic ID
   * @returns {Promise} Resources data
   */
  getBySubtopic: async (subtopicId) => {
    try {
      const response = await api.get(`${RESOURCES_API_BASE_URL}/subtopic/${subtopicId}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching subtopic resources:', error);
      throw error;
    }
  },

  /**
   * Get YouTube videos dynamically for a subtopic
   * @param {number} subtopicId - The subtopic ID
   * @returns {Promise} YouTube videos data
   */
  getYouTubeVideos: async (subtopicId) => {
    try {
      const response = await api.get(`${RESOURCES_API_BASE_URL}/youtube/${subtopicId}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching YouTube videos:', error);
      throw error;
    }
  },

  /**
   * Get PDF search URL for a subtopic
   * @param {number} subtopicId - The subtopic ID
   * @returns {Promise} PDF search URL data
   */
  getPDFResource: async (subtopicId) => {
    try {
      const response = await api.get(`${RESOURCES_API_BASE_URL}/pdf/${subtopicId}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching PDF resource:', error);
      throw error;
    }
  },

  /**
   * Get article search URL for a subtopic
   * @param {number} subtopicId - The subtopic ID
   * @returns {Promise} Article search URL data
   */
  getArticleResource: async (subtopicId) => {
    try {
      const response = await api.get(`${RESOURCES_API_BASE_URL}/article/${subtopicId}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching article resource:', error);
      throw error;
    }
  },

  /**
   * Get all resources (videos, PDFs, articles) for a subtopic
   * @param {number} subtopicId - The subtopic ID
   * @returns {Promise} All resources data
   */
  getAllResources: async (subtopicId) => {
    try {
      const response = await api.get(`${RESOURCES_API_BASE_URL}/all/${subtopicId}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching all resources:', error);
      throw error;
    }
  },

  /**
   * Get all resources for a specific topic
   * @param {number} topicId - The topic ID
   * @returns {Promise} Resources data
   */
  getByTopic: async (topicId) => {
    try {
      const response = await api.get(`${RESOURCES_API_BASE_URL}/topic/${topicId}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching topic resources:', error);
      throw error;
    }
  },

  /**
   * Get a specific resource by ID
   * @param {number} resourceId - The resource ID
   * @returns {Promise} Resource data
   */
  getResource: async (resourceId) => {
    try {
      const response = await api.get(`${RESOURCES_API_BASE_URL}/${resourceId}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching resource:', error);
      throw error;
    }
  },

  /**
   * Create a new resource
   * @param {Object} resourceData - Resource data to create
   * @returns {Promise} Created resource data
   */
  create: async (resourceData) => {
    try {
      const response = await api.post(`${RESOURCES_API_BASE_URL}/create`, resourceData);
      return response.data;
    } catch (error) {
      console.error('Error creating resource:', error);
      throw error;
    }
  },

  /**
   * Update an existing resource
   * @param {number} resourceId - The resource ID to update
   * @param {Object} updateData - Data to update
   * @returns {Promise} Updated resource data
   */
  update: async (resourceId, updateData) => {
    try {
      const response = await api.put(`${RESOURCES_API_BASE_URL}/${resourceId}`, updateData);
      return response.data;
    } catch (error) {
      console.error('Error updating resource:', error);
      throw error;
    }
  },

  /**
   * Delete a resource
   * @param {number} resourceId - The resource ID to delete
   * @returns {Promise} Confirmation data
   */
  delete: async (resourceId) => {
    try {
      const response = await api.delete(`${RESOURCES_API_BASE_URL}/${resourceId}`);
      return response.data;
    } catch (error) {
      console.error('Error deleting resource:', error);
      throw error;
    }
  }
};

export default resourceService;
