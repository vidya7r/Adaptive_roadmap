import React, { useState, useRef, useEffect } from 'react';
import { Send, X, MessageCircle, Loader, Plus, Trash2, Clock } from 'lucide-react';
import chatService from '../services/chatService';
import '../styles/chatbot.css';

export const ChatBot = ({ topicId, subtopicId, subtopicTitle, isOpen, onClose }) => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [loading, setLoading] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const [sessionStarting, setSessionStarting] = useState(false);
  const [conversationHistory, setConversationHistory] = useState([]);
  const [currentConversationTitle, setCurrentConversationTitle] = useState('');
  const [showHistory, setShowHistory] = useState(false);
  const messagesEndRef = useRef(null);

  // Start chat session on mount
  useEffect(() => {
    if (isOpen && !sessionId) {
      initializeChat();
      loadConversationHistory();
    }
  }, [isOpen, sessionId]);

  // Scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const loadConversationHistory = async () => {
    try {
      const sessions = await chatService.getSessions();
      if (sessions?.sessions) {
        // Filter out sessions with no messages (blank chats)
        const sessionsWithMessages = sessions.sessions.filter(s => s.message_count > 0);
        setConversationHistory(sessionsWithMessages);
      }
    } catch (err) {
      console.error('Error loading conversation history:', err);
    }
  };

  const initializeChat = async () => {
    try {
      setSessionStarting(true);
      const session = await chatService.startSession({
        topicId,
        subtopicId,
        title: subtopicTitle || 'Study Chat'
      });
      
      setSessionId(session.session_id);
      setCurrentConversationTitle(session.title || `Chat - ${new Date().toLocaleDateString()}`);
      
      // Add welcome message
      setMessages([
        {
          role: 'assistant',
          content: `👋 Welcome to AI Tutor! I'm here to help you with ${subtopicTitle || 'your studies'}. Ask me anything!`
        }
      ]);
    } catch (err) {
      console.error('Error starting chat:', err);
      setMessages([
        {
          role: 'assistant',
          content: `❌ Error: Unable to start chat. ${err?.detail || err?.message || 'Please try again.'}`
        }
      ]);
    } finally {
      setSessionStarting(false);
    }
  };

  const handleSendMessage = async () => {
    if (!inputValue.trim() || !sessionId) return;

    const userMessage = inputValue.trim();
    setInputValue('');

    // Add user message to display
    setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
    setLoading(true);

    try {
      console.log('Sending message via chatService...');
      const response = await chatService.sendMessage(sessionId, userMessage);
      console.log('Got response:', response);
      
      if (response?.assistant_response) {
        setMessages(prev => [...prev, { role: 'assistant', content: response.assistant_response }]);
        // Reload history to show this conversation (after first message)
        loadConversationHistory();
      } else {
        throw new Error('No assistant response in server response');
      }
    } catch (err) {
      console.error('Error sending message:', err);
      console.error('Error detail:', err?.detail);
      console.error('Error message:', err?.message);
      
      let errorMsg = 'Failed to get response. Try again.';
      if (typeof err === 'object') {
        errorMsg = err?.detail || err?.message || errorMsg;
      } else if (typeof err === 'string') {
        errorMsg = err;
      }
      
      setMessages(prev => [...prev, { role: 'assistant', content: `❌ ${errorMsg}` }]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const handleNewChat = () => {
    setSessionId(null);
    setMessages([]);
    setInputValue('');
    setCurrentConversationTitle('');
    initializeChat();
    loadConversationHistory();
  };

  const handleLoadConversation = async (conversation) => {
    try {
      const history = await chatService.getHistory(conversation.session_id);
      setSessionId(conversation.session_id);
      setCurrentConversationTitle(conversation.title);
      
      // Convert history to message format
      if (history?.messages) {
        setMessages(history.messages);
      }
      setInputValue('');
      setShowHistory(false);
    } catch (err) {
      console.error('Error loading conversation:', err);
      alert('Failed to load conversation');
    }
  };

  const handleDeleteConversation = async (conversation, e) => {
    e.stopPropagation();
    if (window.confirm('Delete this conversation?')) {
      try {
        console.log('Starting delete for:', conversation.session_id);
        const response = await chatService.deleteSession(conversation.session_id);
        console.log('Delete successful:', response);
        
        // Remove from UI immediately
        setConversationHistory(prev => prev.filter(c => c.session_id !== conversation.session_id));
        
        // If we deleted the current chat, start a new one
        if (sessionId === conversation.session_id) {
          handleNewChat();
        }
      } catch (err) {
        console.error('Failed to delete:', err);
        alert(`Delete failed: ${err?.detail || err?.message || 'Unknown error'}`);
      }
    }
  };

  if (!isOpen) return null;

  return (
    <div className="chatbot-overlay">
      <div className="chatbot-container">
        {/* Sidebar with History */}
        <div className={`chatbot-sidebar ${showHistory ? 'open' : ''}`}>
          <button className="new-chat-btn" onClick={handleNewChat}>
            <Plus size={20} />
            New Chat
          </button>

          <div className="history-section">
            <h3>
              <Clock size={16} />
              Conversation History
            </h3>
            {conversationHistory.length > 0 ? (
              <div className="history-list">
                {conversationHistory.map(conv => (
                  <div
                    key={conv.session_id}
                    className={`history-item ${sessionId === conv.session_id ? 'active' : ''}`}
                    onClick={() => handleLoadConversation(conv)}
                  >
                    <span className="history-title">{conv.title}</span>
                    <button
                      className="delete-btn"
                      onClick={(e) => handleDeleteConversation(conv, e)}
                    >
                      <Trash2 size={14} />
                    </button>
                  </div>
                ))}
              </div>
            ) : (
              <p className="empty-history">No conversations yet</p>
            )}
          </div>
        </div>

        {/* Main Chat Area */}
        <div className="chatbot-main">
          {/* Header */}
          <div className="chatbot-header">
            <div className="chatbot-title">
              <MessageCircle size={24} />
              <div>
                <h3>AI Tutor</h3>
                <p>{currentConversationTitle || 'Study Chat'}</p>
              </div>
            </div>
            <div className="header-actions">
              <button 
                className="toggle-history-btn"
                onClick={() => setShowHistory(!showHistory)}
                title="Toggle history"
              >
                <Clock size={20} />
              </button>
              <button className="close-btn" onClick={onClose}>
                <X size={24} />
              </button>
            </div>
          </div>

          {/* Messages Container */}
          <div className="chatbot-messages">
            {messages.map((msg, index) => (
              <div key={index} className={`message ${msg.role}`}>
                <div className="message-bubble">
                  {msg.content}
                </div>
              </div>
            ))}
            {loading && (
              <div className="message assistant">
                <div className="message-bubble typing">
                  <span className="typing-dot"></span>
                  <span className="typing-dot"></span>
                  <span className="typing-dot"></span>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Input Area */}
          <div className="chatbot-input-area">
            <textarea
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask me anything... (Shift+Enter for new line)"
              rows="2"
              disabled={loading || sessionStarting}
              className="chat-input"
            />
            <button
              onClick={handleSendMessage}
              disabled={!inputValue.trim() || loading || sessionStarting || !sessionId}
              className="send-btn"
            >
              {loading ? <Loader size={20} className="spin" /> : <Send size={20} />}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
