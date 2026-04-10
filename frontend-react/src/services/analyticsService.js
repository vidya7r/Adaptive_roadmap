import api from './api';

const analyticsService = {
  // Get complete analytics summary
  getAnalyticsSummary: async () => {
    try {
      const response = await api.get('/api/analytics/summary');
      return response.data;
    } catch (error) {
      console.error('Error fetching analytics summary:', error);
      // Return mock data if API fails
      return {
        overallStats: {
          totalTests: 8,
          totalQuestionsAnswered: 42,
          averageAccuracy: 76,
          averageScore: 76,
          totalTimeSpent: 2340,
          streakDays: 5,
        },
        topicsMastery: [
          {
            name: 'Linear Equations',
            accuracy: 92,
            tests: 3,
            status: 'Mastered',
            color: '#4CAF50'
          },
          {
            name: 'Quadratic Equations',
            accuracy: 68,
            tests: 2,
            status: 'Needs Work',
            color: '#FFC107'
          },
          {
            name: 'Calculus - Derivatives',
            accuracy: 55,
            tests: 1,
            status: 'Weak',
            color: '#F44336'
          },
        ],
        progressTimeline: [
          { date: '2024-01-15', score: 65, accuracy: 65, testType: 'Practice' },
          { date: '2024-01-16', score: 72, accuracy: 72, testType: 'Adaptive' },
          { date: '2024-01-17', score: 68, accuracy: 68, testType: 'Practice' },
          { date: '2024-01-18', score: 78, accuracy: 78, testType: 'Adaptive' },
        ],
        recommendations: [
          'Focus on Calculus - Derivatives (55% accuracy)',
          'Practice Quadratic Equations more (68% accuracy)',
          'Great work on Linear Equations! Keep it up!',
          'Complete 2 more tests to unlock advanced features',
        ],
      };
    }
  },

  // Get overall statistics
  getOverview: async () => {
    try {
      const response = await api.get('/api/analytics/overview');
      return response.data;
    } catch (error) {
      console.error('Error fetching analytics overview:', error);
      return {
        totalTests: 0,
        totalQuestionsAnswered: 0,
        averageAccuracy: 0,
        averageScore: 0,
        totalTimeSpent: 0,
        streakDays: 0,
      };
    }
  },

  // Get topics performance/mastery
  getTopicsPerformance: async () => {
    try {
      const response = await api.get('/api/analytics/topics-performance');
      return response.data;
    } catch (error) {
      console.error('Error fetching topics performance:', error);
      return { topicsMastery: [] };
    }
  },

  // Get weak subtopics
  getWeakSubtopics: async () => {
    try {
      const response = await api.get('/api/analytics/weak-subtopics');
      return response.data;
    } catch (error) {
      console.error('Error fetching weak subtopics:', error);
      return [];
    }
  },

  // Get test history
  getTestHistory: async () => {
    try {
      const response = await api.get('/api/analytics/test-history');
      return response.data;
    } catch (error) {
      console.error('Error fetching test history:', error);
      return [];
    }
  },

  // Get recommendations
  getRecommendations: async () => {
    try {
      const response = await api.get('/api/analytics/recommendations');
      return response.data;
    } catch (error) {
      console.error('Error fetching recommendations:', error);
      return {
        focus_now: [],
        revise_later: [],
      };
    }
  },

  // Get topic mastery
  getTopicMastery: async () => {
    try {
      const response = await api.get('/api/analytics/topic-mastery');
      return response.data;
    } catch (error) {
      console.error('Error fetching topic mastery:', error);
      return {
        total_topics: 0,
        completed_topics: 0,
        in_progress_topics: 0,
        not_started_topics: 0,
      };
    }
  },
};

export default analyticsService;
