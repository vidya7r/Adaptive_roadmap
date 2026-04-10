import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useExam } from '../hooks/useExam';
import { examService } from '../services/examService';
import { ArrowLeft, Loader, Grid3x3 } from 'lucide-react';
import '../styles/modules.css';

export const ModulesPage = () => {
  const [modules, setModules] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const { selectedSection, setSelectedModule } = useExam();
  const navigate = useNavigate();

  useEffect(() => {
    if (!selectedSection) {
      navigate('/exam-selection');
      return;
    }
    fetchModules();
  }, [selectedSection]);

  const fetchModules = async () => {
    try {
      setLoading(true);
      const data = await examService.getModulesBySection(selectedSection);
      setModules(data.modules || []);
    } catch (err) {
      setError('Failed to load modules');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleSelectModule = (moduleId) => {
    setSelectedModule(moduleId);
    navigate('/topics');
  };

  if (loading) {
    return (
      <div className="modules-container loading-state">
        <Loader size={48} className="spinner" />
        <p>Loading modules...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="modules-container error-state">
        <h2>Error</h2>
        <p>{error}</p>
        <button onClick={fetchModules} className="retry-btn">
          Retry
        </button>
      </div>
    );
  }

  return (
    <div className="modules-container">
      <div className="modules-header">
        <button 
          onClick={() => navigate('/exam-selection')}
          className="back-btn"
        >
          <ArrowLeft size={20} />
          Back
        </button>
        <div>
          <h1>Select Your Module</h1>
          <p>Choose a module to start learning</p>
        </div>
      </div>

      <div className="modules-grid">
        {modules.map((module, index) => (
          <div
            key={module.id}
            className="module-card"
            onClick={() => handleSelectModule(module.id)}
          >
            <div className="module-number">{index + 1}</div>
            <div className="module-icon">
              <Grid3x3 size={40} />
            </div>
            <h3>{module.title}</h3>
            <p className="module-desc">{module.description || 'Module content'}</p>
            <div className="card-footer">
              <span className="topics-count">Topics</span>
              <span className="arrow">→</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
