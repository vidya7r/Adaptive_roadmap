import React from 'react';
import { useAuth } from '../hooks/useAuth';
import { useNavigate } from 'react-router-dom';
import { LogOut, Flame, BookOpen, ArrowRight, BarChart3 } from 'lucide-react';
import '../styles/dashboard.css';

export const DashboardPage = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const handleStartLearning = () => {
    navigate('/exam-selection');
  };

  const handleViewAnalytics = () => {
    navigate('/analytics');
  };

  return (
    <div className="dashboard-container">
      <div className="dashboard-header">
        <div>
          <h1>Welcome, {user?.name}! 🎉</h1>
          <p>Ready to ace your NDA exam? Let's get started!</p>
        </div>
      </div>

      <div className="dashboard-content">
        <div className="dashboard-card spotlight">
          <div className="card-icon">
            <BookOpen size={48} />
          </div>
          <div className="card-text">
            <h2>Start Learning</h2>
            <p>Begin your exam preparation journey with structured modules and adaptive learning</p>
          </div>
          <button 
            onClick={handleStartLearning}
            className="btn btn-primary"
          >
            Get Started
            <ArrowRight size={18} />
          </button>
        </div>

        <div className="dashboard-card">
          <div className="card-icon">
            <BarChart3 size={48} />
          </div>
          <div className="card-text">
            <h2>View Analytics</h2>
            <p>Track your progress, analyze weak areas, and get personalized recommendations</p>
          </div>
          <button 
            onClick={handleViewAnalytics}
            className="btn btn-primary"
          >
            View Dashboard
            <ArrowRight size={18} />
          </button>
        </div>

        <div className="dashboard-stats">
          <div className="stat-card">
            <div className="stat-value">0</div>
            <div className="stat-label">Tests Completed</div>
          </div>
          <div className="stat-card">
            <div className="stat-value">0</div>
            <div className="stat-label">Days Streak</div>
          </div>
          <div className="stat-card">
            <div className="stat-value">0%</div>
            <div className="stat-label">Progress</div>
          </div>
        </div>
      </div>

      <div className="dashboard-footer">
        <button
          onClick={handleLogout}
          className="btn btn-logout"
        >
          <LogOut size={18} />
          Logout
        </button>
      </div>
    </div>
  );
};
