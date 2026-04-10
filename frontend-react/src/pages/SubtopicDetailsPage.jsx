import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useExam } from '../hooks/useExam';
import { examService } from '../services/examService';
import { ArrowLeft, Loader, Play, BookOpen } from 'lucide-react';
import '../styles/subtopic-details.css';

export const SubtopicDetailsPage = () => {
  const [subtopic, setSubtopic] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const { selectedTopic, selectedSubtopic } = useExam();
  const navigate = useNavigate();

  useEffect(() => {
    if (!selectedSubtopic) {
      navigate('/topics');
      return;
    }
    fetchSubtopicDetails();
  }, [selectedSubtopic]);

  const fetchSubtopicDetails = async () => {
    try {
      setLoading(true);
      const data = await examService.getSubtopicDetails(selectedSubtopic);
      setSubtopic(data);
    } catch (err) {
      setError('Failed to load subtopic details');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="subtopic-details-container loading-state">
        <Loader size={48} className="spinner" />
        <p>Loading subtopic...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="subtopic-details-container error-state">
        <h2>Error</h2>
        <p>{error}</p>
        <button onClick={fetchSubtopicDetails} className="retry-btn">
          Retry
        </button>
      </div>
    );
  }

  return (
    <div className="subtopic-details-container">
      <div className="details-header">
        <button 
          onClick={() => navigate('/topics')}
          className="back-btn"
        >
          <ArrowLeft size={20} />
          Back
        </button>
        <div>
          <h1>{subtopic?.title}</h1>
          <p>Master this topic step by step</p>
        </div>
      </div>

      <div className="details-content">
        {/* Learning Section */}
        <div className="learning-section">
          <div className="section-header">
            <BookOpen size={24} />
            <h2>Learn</h2>
          </div>
          
          <div className="description-box">
            {subtopic?.description ? (
              <p>{subtopic.description}</p>
            ) : (
              <p className="no-description">No description available for this subtopic yet.</p>
            )}
          </div>

          <div className="action-buttons">
            <button 
              className="btn btn-primary"
              onClick={() => navigate('/practice', { state: { subtopicId: selectedSubtopic } })}
            >
              <Play size={18} />
              Start Practice ({subtopic?.question_count || 0} questions)
            </button>
          </div>
        </div>

        {/* Stats */}
        <div className="stats-grid">
          <div className="stat-card">
            <div className="stat-icon">📚</div>
            <div className="stat-value">{subtopic?.question_count || 0}</div>
            <div className="stat-label">Questions</div>
          </div>

          <div className="stat-card">
            <div className="stat-icon">⭐</div>
            <div className="stat-value">-</div>
            <div className="stat-label">Your Score</div>
          </div>

          <div className="stat-card">
            <div className="stat-icon">📊</div>
            <div className="stat-value">0%</div>
            <div className="stat-label">Progress</div>
          </div>
        </div>
      </div>
    </div>
  );
};
