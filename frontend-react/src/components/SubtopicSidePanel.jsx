import React, { useState, useEffect, useRef } from 'react';
import { X, Play, BookOpen, ChevronDown, Send, Loader } from 'lucide-react';
import { examService } from '../services/examService';
import chatService from '../services/chatService';
import aiService from '../services/aiService';
import { ResourcesList } from './ResourcesList';
import '../styles/side-panel.css';

export const SubtopicSidePanel = ({ subtopic, onClose, onStartPractice, onStatusChange }) => {
  const [activeTab, setActiveTab] = useState('resources');
  const [status, setStatus] = useState('pending');
  const [showDropdown, setShowDropdown] = useState(false);
  const [loading, setLoading] = useState(false);
  const [chatMessages, setChatMessages] = useState([]);
  const [chatInput, setChatInput] = useState('');
  const [chatSessionId, setChatSessionId] = useState(null);
  const [chatLoading, setChatLoading] = useState(false);
  const [description, setDescription] = useState(null);
  const [descriptionLoading, setDescriptionLoading] = useState(false);
  const [descriptionError, setDescriptionError] = useState(null);
  const messagesEndRef = useRef(null);

  const statusOptions = [
    { value: 'pending', label: 'Pending', color: '#999' },
    { value: 'done', label: 'Done', color: '#4CAF50' },
    { value: 'in-progress', label: 'In Progress', color: '#FFC107' },
    { value: 'skip', label: 'Skip', color: '#F44336' },
  ];

  const currentStatus = statusOptions.find(opt => opt.value === status);

  // Load progress when panel opens
  useEffect(() => {
    loadProgress();
  }, [subtopic?.id]);

  const loadProgress = async () => {
    try {
      const progress = await examService.getSubtopicProgress(subtopic?.id);
      if (progress?.status) {
        setStatus(progress.status);
      }
    } catch (err) {
      console.error('Error loading progress:', err);
    }
  };

  // Initialize chat when AI Tutor tab is opened
  useEffect(() => {
    if (activeTab === 'ai-tutor' && !chatSessionId && subtopic?.id) {
      initializeChat();
    }
  }, [activeTab, subtopic?.id]);

  // Fetch description when Description tab is opened
  useEffect(() => {
    if (activeTab === 'description' && subtopic?.id && !description) {
      loadDescription();
    }
  }, [activeTab, subtopic?.id]);

  const loadDescription = async () => {
    try {
      setDescriptionLoading(true);
      setDescriptionError(null);
      const result = await aiService.getDescription(subtopic?.id);
      if (result?.success) {
        setDescription(result.description);
      } else {
        setDescriptionError(result?.message || 'Failed to load description');
      }
    } catch (err) {
      console.error('Error loading description:', err);
      setDescriptionError(err?.response?.data?.detail || err?.message || 'Failed to load description');
    } finally {
      setDescriptionLoading(false);
    }
  };

  // Scroll to bottom of messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [chatMessages]);

  const initializeChat = async () => {
    try {
      setChatLoading(true);
      const session = await chatService.startSession({
        subtopicId: subtopic?.id,
        title: subtopic?.title
      });
      
      setChatSessionId(session.session_id);
      setChatMessages([
        {
          role: 'assistant',
          content: `👋 Hi! I'm your AI tutor. I'm here to help you understand ${subtopic?.title}. Ask me anything!`
        }
      ]);
    } catch (err) {
      console.error('Error starting chat:', err);
      setChatMessages([
        {
          role: 'assistant',
          content: `⚠️ ${err?.detail || err?.message || 'Chat temporarily unavailable. Please try again.'}`
        }
      ]);
    } finally {
      setChatLoading(false);
    }
  };

  const handleSendChatMessage = async () => {
    if (!chatInput.trim() || !chatSessionId) return;

    const userMessage = chatInput.trim();
    setChatInput('');

    // Add user message
    setChatMessages(prev => [...prev, { role: 'user', content: userMessage }]);
    setChatLoading(true);

    try {
      const response = await chatService.sendMessage(chatSessionId, userMessage);
      setChatMessages(prev => [...prev, { role: 'assistant', content: response.assistant_response }]);
    } catch (err) {
      console.error('Error sending message:', err);
      setChatMessages(prev => [...prev, { role: 'assistant', content: `❌ ${err?.detail || err?.message || 'Failed to get response. Try again.'}` }]);
    } finally {
      setChatLoading(false);
    }
  };

  const handleStatusChange = async (newStatus) => {
    try {
      setLoading(true);
      
      // Save to backend
      const result = await examService.saveSubtopicProgress(subtopic?.id, newStatus);
      
      // Only update if save was successful
      if (result?.success) {
        setStatus(newStatus);
        
        // Notify parent component to update visual display
        if (onStatusChange) {
          onStatusChange(subtopic?.id, newStatus);
        }
      } else {
        console.error('Save failed:', result);
        alert('Failed to save progress. Please try again.');
      }
      
      setShowDropdown(false);
    } catch (err) {
      console.error('Error saving progress:', err);
      alert(`Error: ${err.message || 'Failed to save progress'}`);
      // Rollback on error
      loadProgress();
    } finally {
      setLoading(false);
    }
  };

  const handleReset = async () => {
    if (!window.confirm('Are you sure you want to reset this topic progress?')) {
      return;
    }

    try {
      setLoading(true);
      console.log(`🔄 Resetting progress for subtopic ${subtopic?.id}`);
      
      const result = await examService.resetSubtopicProgress(subtopic?.id);
      
      if (result?.success) {
        setStatus('pending');
        
        // Notify parent component
        if (onStatusChange) {
          onStatusChange(subtopic?.id, 'pending');
        }
        
        alert('Progress reset successfully!');
      } else {
        alert('Failed to reset progress.');
      }
    } catch (err) {
      console.error('Error resetting progress:', err);
      alert(`Error: ${err.message || 'Failed to reset progress'}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="side-panel-overlay" onClick={onClose}>
      <div className="side-panel" onClick={(e) => e.stopPropagation()}>
        {/* Header */}
        <div className="panel-header">
          <div>
            <h2>{subtopic?.title}</h2>
            <p className="panel-meta">{subtopic?.question_count} questions available</p>
          </div>
          <button className="close-btn" onClick={onClose}>
            <X size={24} />
          </button>
        </div>

        {/* Status Dropdown */}
        <div className="panel-progress">
          <div className="status-label">Mark Progress</div>
          <div className="status-dropdown-wrapper">
            <button 
              className="status-dropdown-btn"
              onClick={() => setShowDropdown(!showDropdown)}
              style={{ borderColor: currentStatus?.color }}
            >
              <span 
                className="status-dot" 
                style={{ backgroundColor: currentStatus?.color }}
              />
              <span className="status-text">{currentStatus?.label}</span>
              <ChevronDown size={18} className={`chevron ${showDropdown ? 'open' : ''}`} />
            </button>

            {showDropdown && (
              <div className="status-dropdown-menu">
                {statusOptions.map(option => (
                  <button
                    key={option.value}
                    className={`dropdown-item ${status === option.value ? 'active' : ''}`}
                    onClick={() => handleStatusChange(option.value)}
                    disabled={loading}
                  >
                    <span 
                      className="option-dot" 
                      style={{ backgroundColor: option.color }}
                    />
                    <span className="option-label">{option.label}</span>
                    {status === option.value && <span className="checkmark">✓</span>}
                  </button>
                ))}
              </div>
            )}
          </div>

          <button 
            className="reset-btn"
            onClick={handleReset}
            disabled={loading || status === 'pending'}
            title="Reset progress back to pending"
          >
            🔄 Reset
          </button>
        </div>

        {/* Tabs */}
        <div className="panel-tabs">
          <button
            className={`tab ${activeTab === 'resources' ? 'active' : ''}`}
            onClick={() => setActiveTab('resources')}
          >
            <BookOpen size={18} />
            Resources
          </button>
          <button
            className={`tab ${activeTab === 'description' ? 'active' : ''}`}
            onClick={() => setActiveTab('description')}
          >
            📖 Description
          </button>
          <button
            className={`tab ${activeTab === 'ai-tutor' ? 'active' : ''}`}
            onClick={() => setActiveTab('ai-tutor')}
          >
            🤖 AI Tutor
          </button>
        </div>

        {/* Content */}
        <div className="panel-content">
          {activeTab === 'description' && (
            <div className="description-section">
              <h3>📖 Topic Overview</h3>
              
              {descriptionLoading && (
                <div className="loading-state">
                  <Loader size={24} className="spin" />
                  <p>Generating description...</p>
                </div>
              )}
              
              {descriptionError && (
                <div className="error-state">
                  <p>⚠️ {descriptionError}</p>
                  <button 
                    onClick={loadDescription}
                    className="retry-btn"
                  >
                    Retry
                  </button>
                </div>
              )}
              
              {description && !descriptionLoading && (
                <div className="description-content">
                  <div className="description-text">
                    {description.split('\n\n').map((para, idx) => (
                      <p key={idx}>{para}</p>
                    ))}
                  </div>
                  <button 
                    onClick={() => {
                      setDescription(null);
                      loadDescription();
                    }}
                    className="refresh-btn"
                  >
                    🔄 Refresh
                  </button>
                </div>
              )}
            </div>
          )}

          {activeTab === 'resources' && (
            <div className="resources-section">
              <h3>Learning Materials</h3>
              <p className="description">
                {subtopic?.description || 'No description available'}
              </p>

              <ResourcesList 
                subtopicId={subtopic?.id}
                subtopicTitle={subtopic?.title}
              />
            </div>
          )}

          {activeTab === 'ai-tutor' && (
            <div className="ai-tutor-section">
              <h3>AI Tutor Chat</h3>
              
              {/* Chat Messages */}
              <div className="ai-chat-messages">
                {chatMessages.map((msg, index) => (
                  <div key={index} className={`chat-message ${msg.role}`}>
                    <div className="message-bubble">{msg.content}</div>
                  </div>
                ))}
                {chatLoading && (
                  <div className="chat-message assistant">
                    <div className="message-bubble typing">
                      <span className="dot"></span>
                      <span className="dot"></span>
                      <span className="dot"></span>
                    </div>
                  </div>
                )}
                <div ref={messagesEndRef} />
              </div>

              {/* Chat Input */}
              <div className="ai-chat-input">
                <input
                  type="text"
                  value={chatInput}
                  onChange={(e) => setChatInput(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && handleSendChatMessage()}
                  placeholder="Ask a question..."
                  disabled={chatLoading || !chatSessionId}
                />
                <button
                  onClick={handleSendChatMessage}
                  disabled={!chatInput.trim() || chatLoading || !chatSessionId}
                  className="send-btn"
                >
                  {chatLoading ? <Loader size={18} /> : <Send size={18} />}
                </button>
              </div>
            </div>
          )}
        </div>

        {/* Action Buttons */}
        <div className="panel-actions">
          <button className="btn btn-practice" onClick={onStartPractice}>
            <Play size={18} />
            Practice (5 Q's)
          </button>
        </div>
      </div>
    </div>
  );
};
