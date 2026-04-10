import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useExam } from '../hooks/useExam';
import { examService } from '../services/examService';
import { ArrowLeft, Loader, MessageCircle } from 'lucide-react';
import { SubtopicSidePanel } from '../components/SubtopicSidePanel';
import { PracticeMode } from '../components/PracticeMode';
import { AdaptiveTestMode } from '../components/AdaptiveTestMode';
import { ChatBot } from '../components/ChatBot';
import '../styles/topics-tree.css';

export const TopicsPage = () => {
  const [topics, setTopics] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showPanel, setShowPanel] = useState(false);
  const [selectedSubtopic, setSelectedSubtopic] = useState(null);
  const [mode, setMode] = useState(null); // null, 'practice', or 'test'
  const [subtopicProgress, setSubtopicProgress] = useState({}); // Track progress by subtopic ID
  const [isChatOpen, setIsChatOpen] = useState(false);
  const { selectedModule, setSelectedTopic } = useExam();
  const navigate = useNavigate();

  useEffect(() => {
    if (!selectedModule) {
      navigate('/modules');
      return;
    }
    fetchTopics();
  }, [selectedModule]);

  const fetchTopics = async () => {
    try {
      setLoading(true);
      const data = await examService.getTopicsByModule(selectedModule);
      setTopics(data || []);
    } catch (err) {
      setError('Failed to load topics');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleSelectSubtopic = (topicId, subtopic) => {
    setSelectedTopic(topicId);
    setSelectedSubtopic(subtopic);
    setShowPanel(true);
    setMode(null);
  };

  const handleClosePractice = () => {
    setMode(null);
    setShowPanel(true);
  };

  const handleCloseTest = () => {
    setMode(null);
    setShowPanel(true);
  };

  const handleStartPractice = (subtopicId) => {
    setMode('practice');
  };

  const handleStatusChange = (subtopicId, newStatus) => {
    setSubtopicProgress(prev => ({
      ...prev,
      [subtopicId]: newStatus
    }));
  };

  const handleClosePanel = () => {
    setShowPanel(false);
    setSelectedSubtopic(null);
    setMode(null);
  };

  // Show Practice Mode
  if (mode === 'practice' && selectedSubtopic) {
    return (
      <PracticeMode 
        subtopicId={selectedSubtopic.id} 
        onBack={handleClosePractice}
      />
    );
  }

  // Show Adaptive Test Mode
  if (mode === 'test' && selectedSubtopic) {
    return (
      <AdaptiveTestMode
        moduleId={selectedModule}
        onBack={handleCloseTest}
      />
    );
  }

  if (loading) {
    return (
      <div className="topics-tree-container loading-state">
        <Loader size={48} className="spinner" />
        <p>Loading topics...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="topics-tree-container error-state">
        <h2>Error</h2>
        <p>{error}</p>
        <button onClick={fetchTopics} className="retry-btn">
          Retry
        </button>
      </div>
    );
  }

  return (
    <div className="topics-tree-container">
      <div className="topics-header">
        <button 
          onClick={() => navigate('/modules')}
          className="back-btn"
        >
          <ArrowLeft size={20} />
          Back
        </button>
        <div>
          <h1>Learning Hierarchy</h1>
          <p>Topics & Subtopics - Mind Map View</p>
        </div>
        <button 
          onClick={() => setIsChatOpen(true)}
          className="chat-toggle-btn"
          title="Open AI Tutor Chat"
        >
          <MessageCircle size={24} />
        </button>
      </div>

      <div className="tree-mind-map">
        {topics.map((topic, topicIndex) => (
          <div key={topic.id} className="topic-branch">
            {/* Topic Card */}
            <div className="topic-card">
              <div className="topic-title">{topic.title}</div>
              <div className="topic-count">{topic.subtopics?.length || 0} subtopics</div>
            </div>

            {/* Connecting Line */}
            {topic.subtopics && topic.subtopics.length > 0 && (
              <svg className="connector-line" viewBox="0 0 100 50">
                <path d="M 10 25 Q 50 10, 90 25" stroke="#667eea" strokeWidth="2" fill="none"/>
              </svg>
            )}

            {/* Subtopics Grid */}
            {topic.subtopics && topic.subtopics.length > 0 && (
              <div className="subtopics-row">
                {topic.subtopics.map((subtopic, subtopicIndex) => {
                  // Color rotation: green, yellow, gray
                  const colors = ['green', 'yellow', 'gray'];
                  const colorClass = colors[subtopicIndex % colors.length];
                  const progressStatus = subtopicProgress[subtopic.id] || 'pending';
                  
                  return (
                    <div
                      key={subtopic.id}
                      className={`subtopic-card ${colorClass} status-${progressStatus}`}
                      onClick={() => handleSelectSubtopic(topic.id, subtopic)}
                    >
                      <div className="subtopic-title">{subtopic.title}</div>
                      <div className="subtopic-count">
                        {subtopic.question_count} Q's
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </div>
        ))}
      </div>

      {/* Test Button at Bottom */}
      <div className="test-section">
        <button 
          className="btn-take-test"
          onClick={() => {
            setSelectedSubtopic({ id: selectedModule });
            setMode('test');
          }}
        >
          <span className="test-icon">📝</span>
          <span className="test-text">Take Full Module Test</span>
          <span className="test-arrow">→</span>
        </button>
      </div>

      {/* Side Panel - if showPanel is true and no mode is active */}
      {showPanel && mode === null && selectedSubtopic && (
        <SubtopicSidePanel
          subtopic={selectedSubtopic}
          onClose={handleClosePanel}
          onStartPractice={handleStartPractice}
          onStatusChange={handleStatusChange}
        />
      )}

      {/* AI Tutor Chat */}
      <ChatBot
        topicId={selectedSubtopic?.id}
        subtopicId={selectedSubtopic?.id}
        subtopicTitle={selectedSubtopic?.title}
        isOpen={isChatOpen}
        onClose={() => setIsChatOpen(false)}
      />
    </div>
  );
};

