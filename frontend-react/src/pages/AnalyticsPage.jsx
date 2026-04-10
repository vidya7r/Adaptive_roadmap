import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft, TrendingUp, BookOpen, Target, Award, Calendar, Clock, Flame } from 'lucide-react';
import analyticsService from '../services/analyticsService';
import '../styles/analytics-page.css';

export const AnalyticsPage = ({ onBack }) => {
  const navigate = useNavigate();
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAnalytics();
  }, []);

  const fetchAnalytics = async () => {
    try {
      setLoading(true);
      const data = await analyticsService.getAnalyticsSummary();
      setAnalytics(data);
    } catch (err) {
      console.error('Error fetching analytics:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="analytics-container loading">
        <div className="loader"></div>
        <p>Loading your analytics...</p>
      </div>
    );
  }

  if (!analytics) {
    return (
      <div className="analytics-container error">
        <p>Unable to load analytics. Please try again.</p>
      </div>
    );
  }

  const { overallStats, topicsMastery, progressTimeline, recommendations } = analytics;

  // Format time
  const formatTime = (seconds) => {
    const hours = Math.floor(seconds / 3600);
    const mins = Math.floor((seconds % 3600) / 60);
    return `${hours}h ${mins}m`;
  };

  // Get streak status
  const getStreakEmoji = (days) => {
    if (days >= 7) return '🔥🔥🔥';
    if (days >= 5) return '🔥🔥';
    if (days >= 3) return '🔥';
    return '⏳';
  };

  // Get stat color based on value
  const getStatColor = (value, thresholds) => {
    if (value >= thresholds.excellent) return '#4CAF50';
    if (value >= thresholds.good) return '#66BB6A';
    if (value >= thresholds.fair) return '#FFC107';
    return '#F44336';
  };

  return (
    <div className="analytics-container">
      {/* Header */}
      <div className="analytics-header">
        <button className="back-btn" onClick={() => onBack ? onBack() : navigate('/dashboard')}>
          <ArrowLeft size={20} />
        </button>
        <h1>📊 Performance Analytics</h1>
        <div className="header-spacer" />
      </div>

      {/* Overview Tab */}
      <>
          {/* Key Stats Grid */}
          <div className="stats-grid">
            <div className="stat-card">
              <div className="stat-icon" style={{ background: '#667eea' }}>
                <Target size={24} />
              </div>
              <div className="stat-info">
                <div className="stat-value">{overallStats.averageAccuracy}%</div>
                <div className="stat-label">Average Accuracy</div>
              </div>
            </div>

            <div className="stat-card">
              <div className="stat-icon" style={{ background: '#4CAF50' }}>
                <BookOpen size={24} />
              </div>
              <div className="stat-info">
                <div className="stat-value">{overallStats.totalTests}</div>
                <div className="stat-label">Tests Completed</div>
              </div>
            </div>

            <div className="stat-card">
              <div className="stat-icon" style={{ background: '#FF9800' }}>
                <Clock size={24} />
              </div>
              <div className="stat-info">
                <div className="stat-value">{formatTime(overallStats.totalTimeSpent)}</div>
                <div className="stat-label">Total Study Time</div>
              </div>
            </div>

            <div className="stat-card">
              <div className="stat-icon" style={{ background: '#F44336' }}>
                <Flame size={24} />
              </div>
              <div className="stat-info">
                <div className="stat-value">{overallStats.streakDays} {getStreakEmoji(overallStats.streakDays)}</div>
                <div className="stat-label">Day Streak</div>
              </div>
            </div>
          </div>

          {/* Recommendations */}
          <div className="recommendations-section">
            <h2>💡 Personalized Recommendations</h2>
            <div className="recommendations-list">
              {recommendations.map((rec, index) => (
                <div key={index} className="recommendation-item">
                  <span className="rec-icon">
                    {rec.includes('Great') ? '✅' : rec.includes('Focus') ? '⚠️' : rec.includes('Practice') ? '📚' : '🎯'}
                  </span>
                  <span className="rec-text">{rec}</span>
                </div>
              ))}
            </div>
          </div>
        </>
    </div>
  );
};
