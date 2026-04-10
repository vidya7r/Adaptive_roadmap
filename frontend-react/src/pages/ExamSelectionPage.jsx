import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useExam } from '../hooks/useExam';
import { examService } from '../services/examService';
import { BookOpen, Users, Loader, ArrowLeft } from 'lucide-react';
import '../styles/exam-selection.css';

export const ExamSelectionPage = () => {
  const [sections, setSections] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const { setSelectedSection } = useExam();
  const navigate = useNavigate();

  useEffect(() => {
    fetchSections();
  }, []);

  const fetchSections = async () => {
    try {
      setLoading(true);
      const data = await examService.getSections();
      setSections(data.sections || []);
    } catch (err) {
      setError('Failed to load exam sections');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleSelectSection = (sectionId) => {
    setSelectedSection(sectionId);
    navigate('/modules');
  };

  const handleBack = () => {
    navigate('/dashboard');
  };

  if (loading) {
    return (
      <div className="exam-selection-container loading-state">
        <Loader size={48} className="spinner" />
        <p>Loading exam options...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="exam-selection-container error-state">
        <h2>Error</h2>
        <p>{error}</p>
        <button onClick={fetchSections} className="retry-btn">
          Retry
        </button>
      </div>
    );
  }

  return (
    <div className="exam-selection-container">
      <div className="exam-header">
        <button className="back-btn" onClick={handleBack}>
          <ArrowLeft size={20} />
        </button>
        <div>
          <h1>Select Your Exam Path</h1>
          <p>Choose the exam you want to prepare for</p>
        </div>
      </div>

      <div className="exam-grid">
        {sections.map((section) => (
          <div
            key={section.id}
            className="exam-card"
            onClick={() => handleSelectSection(section.id)}
          >
            <div className="exam-icon">
              {section.title === 'Written' ? (
                <BookOpen size={64} />
              ) : (
                <Users size={64} />
              )}
            </div>
            <div className="exam-content">
              <h2>{section.title}</h2>
              <p>
                {section.title === 'Written'
                  ? 'Written Examination - Mathematics, English, General Knowledge'
                  : 'Service Selection Board - Interview & Assessment'}
              </p>
            </div>
            <div className="exam-arrow">→</div>
          </div>
        ))}
      </div>
    </div>
  );
};
