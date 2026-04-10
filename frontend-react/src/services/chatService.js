import api from './api';

const chatService = {
  // Start a new chat session
  startSession: async (params) => {
    try {
      const response = await api.post('/api/chat/start-session', {
        topic_id: params.topicId,
        subtopic_id: params.subtopicId,
        title: params.title
      });
      return response.data;
    } catch (error) {
      console.error('Error starting chat session:', error);
      throw error.response?.data || error.message;
    }
  },

  // Send message and get AI response
  sendMessage: async (sessionId, message) => {
    try {
      console.log('Sending message:', { sessionId, message });
      const response = await api.post('/api/chat/send-message', {
        session_id: sessionId,
        message: message
      });
      console.log('Send message response:', response.data);
      return response.data;
    } catch (error) {
      console.error('Error sending message:', error);
      console.error('Error response:', error.response?.data);
      console.error('Error status:', error.response?.status);
      throw error.response?.data || { detail: error.message };
    }
  },

  // Get chat history (optional - for retrieving past conversations)
  getHistory: async (sessionId) => {
    try {
      const response = await api.get(`/api/chat/history/${sessionId}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching chat history:', error);
      throw error.response?.data || error.message;
    }
  },

  // Get all sessions for user (optional)
  getSessions: async () => {
    try {
      const response = await api.get('/api/chat/sessions');
      return response.data;
    } catch (error) {
      console.error('Error fetching sessions:', error);
      throw error.response?.data || error.message;
    }
  },

  // Delete a chat session
  deleteSession: async (sessionId) => {
    try {
      console.log('Attempting to delete session:', sessionId);
      const response = await api.delete(`/api/chat/sessions/${sessionId}`);
      console.log('Delete response:', response.data);
      return response.data;
    } catch (error) {
      console.error('=== DELETE ERROR ===');
      console.error('Full error:', error);
      console.error('Error response:', error.response);
      console.error('Error status:', error.response?.status);
      console.error('Error data:', error.response?.data);
      
      const errorData = error.response?.data;
      const errorDetail = errorData?.detail || error.message || 'Unknown error';
      
      throw {
        detail: errorDetail,
        status: error.response?.status,
        _raw: error
      };
    }
  }
};

export default chatService;
