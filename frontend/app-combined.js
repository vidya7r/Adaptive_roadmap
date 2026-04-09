// ========================================
// API LAYER
// ========================================
const API_BASE_URL = 'http://127.0.0.1:8001';

const api = {
  login: async (email, password) => {
    const formData = new URLSearchParams();
    formData.append('username', email);
    formData.append('password', password);
    const response = await fetch(`${API_BASE_URL}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: formData,
    });
    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new Error(error.detail || 'Login failed');
    }
    const data = await response.json();
    localStorage.setItem('token', data.access_token);
    return data;
  },

  signup: async (name, email, password) => {
    const response = await fetch(`${API_BASE_URL}/auth/signup`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, email, password }),
    });
    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new Error(error.detail || 'Signup failed');
    }
    return await response.json();
  },

  getModules: async () => {
    const response = await fetch(`${API_BASE_URL}/api/modules`);
    if (!response.ok) throw new Error('Failed to load modules');
    return await response.json();
  },

  getTopicsByModule: async (moduleId) => {
    const response = await fetch(`${API_BASE_URL}/api/topics/${moduleId}`);
    if (!response.ok) throw new Error('Failed to load topics');
    return await response.json();
  },

  getSubtopicsByTopic: async (topicId) => {
    const response = await fetch(`${API_BASE_URL}/api/subtopics/${topicId}`);
    if (!response.ok) throw new Error('Failed to load subtopics');
    return await response.json();
  },

  getSubtopicDetail: async (subtopicId) => {
    const response = await fetch(`${API_BASE_URL}/api/subtopic/${subtopicId}`);
    if (!response.ok) throw new Error('Failed to load subtopic');
    return await response.json();
  },

  generateTest: async (topicId) => {
    const token = localStorage.getItem('token');
    const response = await fetch(`${API_BASE_URL}/test/generate/${topicId}`, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    if (!response.ok) throw new Error('Failed to generate test');
    return await response.json();
  },

  generateSubtopicTest: async (subtopicId) => {
    const token = localStorage.getItem('token');
    const response = await fetch(`${API_BASE_URL}/test/generate-subtopic/${subtopicId}`, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    if (!response.ok) throw new Error('Failed to generate test');
    return await response.json();
  },

  submitTest: async (topicId, answers) => {
    const token = localStorage.getItem('token');
    const response = await fetch(`${API_BASE_URL}/test/submit`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
      body: JSON.stringify({ topic_id: topicId, answers })
    });
    if (!response.ok) throw new Error('Failed to submit test');
    return await response.json();
  },

  submitSubtopicTest: async (subtopicId, answers) => {
    const token = localStorage.getItem('token');
    const response = await fetch(`${API_BASE_URL}/test/submit-subtopic`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
      body: JSON.stringify({ subtopic_id: subtopicId, answers })
    });
    if (!response.ok) throw new Error('Failed to submit test');
    return await response.json();
  },

  getWeakSubtopics: async () => {
    const token = localStorage.getItem('token');
    const response = await fetch(`${API_BASE_URL}/analytics/weak-subtopics`, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    if (!response.ok) throw new Error('Failed to fetch weak subtopics');
    return await response.json();
  },

  getTestHistory: async () => {
    const token = localStorage.getItem('token');
    const response = await fetch(`${API_BASE_URL}/analytics/test-history`, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    if (!response.ok) throw new Error('Failed to fetch test history');
    return await response.json();
  },

  getRecommendations: async () => {
    const token = localStorage.getItem('token');
    const response = await fetch(`${API_BASE_URL}/analytics/recommendations`, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    if (!response.ok) throw new Error('Failed to fetch recommendations');
    return await response.json();
  },

  startChatSession: async (topicId = null, subtopicId = null, title = null) => {
    const token = localStorage.getItem('token');
    const response = await fetch(`${API_BASE_URL}/chat/start-session`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
      body: JSON.stringify({ topic_id: topicId, subtopic_id: subtopicId, title: title })
    });
    if (!response.ok) throw new Error('Failed to start chat session');
    return await response.json();
  },

  sendChatMessage: async (sessionId, message) => {
    const token = localStorage.getItem('token');
    const response = await fetch(`${API_BASE_URL}/chat/send-message`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
      body: JSON.stringify({ session_id: sessionId, message: message })
    });
    if (!response.ok) throw new Error('Failed to send message');
    return await response.json();
  },

  getChatHistory: async (sessionId) => {
    const token = localStorage.getItem('token');
    const response = await fetch(`${API_BASE_URL}/chat/history/${sessionId}`, {
      method: 'GET',
      headers: { 'Authorization': `Bearer ${token}` }
    });
    if (!response.ok) throw new Error('Failed to get chat history');
    return await response.json();
  },

  getUserSessions: async () => {
    const token = localStorage.getItem('token');
    const response = await fetch(`${API_BASE_URL}/chat/sessions`, {
      method: 'GET',
      headers: { 'Authorization': `Bearer ${token}` }
    });
    if (!response.ok) throw new Error('Failed to get chat sessions');
    return await response.json();
  },

  deleteChatSession: async (sessionId) => {
    const token = localStorage.getItem('token');
    const response = await fetch(`${API_BASE_URL}/chat/end-session/${sessionId}`, {
      method: 'DELETE',
      headers: { 'Authorization': `Bearer ${token}` }
    });
    if (!response.ok) throw new Error('Failed to delete chat session');
    return await response.json();
  }
};

// ========================================
// APP STATE
// ========================================
const state = {
  currentPage: 'login',
  token: localStorage.getItem('token'),
  selectedModule: null,
  selectedTopic: null,
  selectedSubtopic: null,
  testQuestions: [],
  userAnswers: {},
  testResult: null,
  currentQuestionIndex: 0,
  isAdaptiveTest: false,
  chatSessionId: null,
  chatMessages: [],
  chatTopicId: null,
  chatSubtopicId: null,
  chatTitle: null,
  chatSessions: [],
};

// ========================================
// NAVIGATION
// ========================================
function goToPage(page) {
  state.currentPage = page;
  render();
}

function goToModules() {
  state.selectedModule = null;
  state.selectedTopic = null;
  state.selectedSubtopic = null;
  goToPage('modules');
}

function goToTopics(moduleId) {
  state.selectedModule = moduleId;
  state.selectedTopic = null;
  state.selectedSubtopic = null;
  goToPage('topics');
}

function goToSubtopics(topicId) {
  state.selectedTopic = topicId;
  state.selectedSubtopic = null;
  goToPage('subtopics');
}

function goToSubtopicDetail(subtopicId) {
  state.selectedSubtopic = subtopicId;
  goToPage('subtopic-detail');
}

function goToTest(subtopicId) {
  state.selectedSubtopic = subtopicId;
  state.userAnswers = {};
  state.currentQuestionIndex = 0;
  state.isAdaptiveTest = false;
  goToPage('test-loading');
  loadTest(subtopicId);
}

function goToCommonTest(topicId) {
  state.selectedTopic = topicId;
  state.selectedSubtopic = null;  // Clear subtopic since this is topic-wide
  state.userAnswers = {};
  state.currentQuestionIndex = 0;
  state.isAdaptiveTest = true;
  goToPage('test-loading');
  loadCommonTest(topicId);
}

async function goToAnalytics() {
  goToPage('analytics');
  try {
    // Fetch with timeout and error handling
    const fetchWithTimeout = (url, options) => {
      return Promise.race([
        fetch(url, options),
        new Promise((_, reject) => 
          setTimeout(() => reject(new Error('Request timeout')), 5000)
        )
      ]);
    };

    const token = localStorage.getItem('token');
    const headers = { 'Authorization': `Bearer ${token}` };

    let weakSubtopics = [];
    let testHistory = [];
    let recommendations = { message: '' };

    try {
      const res1 = await fetchWithTimeout(`${API_BASE_URL}/analytics/weak-subtopics`, { headers });
      if (res1.ok) weakSubtopics = await res1.json();
    } catch (e) {
      console.warn('Failed to load weak-subtopics:', e);
    }

    try {
      const res2 = await fetchWithTimeout(`${API_BASE_URL}/analytics/test-history`, { headers });
      if (res2.ok) testHistory = await res2.json();
    } catch (e) {
      console.warn('Failed to load test-history:', e);
    }

    try {
      const res3 = await fetchWithTimeout(`${API_BASE_URL}/analytics/recommendations`, { headers });
      if (res3.ok) recommendations = await res3.json();
    } catch (e) {
      console.warn('Failed to load recommendations:', e);
    }

    state.weakSubtopics = weakSubtopics;
    state.testHistory = testHistory;
    state.recommendations = recommendations;
    render();
  } catch (error) {
    console.error('Analytics error:', error);
    alert('Error loading analytics. Please try again.');
    goToModules();
  }
}

async function goToChat(topicId = null, subtopicId = null) {
  try {
    state.chatTopicId = topicId;
    state.chatSubtopicId = subtopicId;
    
    // Determine chat title based on topic/subtopic
    let chatTitle = 'AI Tutor Chat';
    if (topicId && subtopicId) {
      chatTitle = 'Chat - Subtopic';
    } else if (topicId) {
      chatTitle = 'Chat - Topic';
    }
    state.chatTitle = chatTitle;
    
    // Don't create session yet - will be created on first message
    state.chatSessionId = null;
    state.chatMessages = [];
    
    // Load all user chat sessions for sidebar
    try {
      const sessionsData = await api.getUserSessions();
      state.chatSessions = sessionsData.sessions || [];
    } catch (error) {
      console.log('Failed to load chat sessions');
      state.chatSessions = [];
    }
    
    goToPage('chat');
  } catch (error) {
    console.error('Chat error:', error);
    alert('Failed to start chat: ' + error.message);
  }
}

async function loadChatSession(sessionId) {
  try {
    state.chatSessionId = sessionId;
    
    // Load chat history for the selected session
    const history = await api.getChatHistory(sessionId);
    state.chatMessages = history.messages || [];
    state.chatTitle = history.title || 'AI Tutor Chat';
    state.chatTopicId = history.topic_id;
    state.chatSubtopicId = history.subtopic_id;
    
    render();
    
    // Auto-scroll to bottom
    setTimeout(() => {
      const messagesDiv = document.querySelector('.chat-messages');
      if (messagesDiv) {
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
      }
    }, 100);
  } catch (error) {
    console.error('Failed to load chat session:', error);
    alert('Failed to load chat: ' + error.message);
  }
}

async function deleteChat(sessionId) {
  if (!confirm('Are you sure you want to delete this chat?')) {
    return;
  }
  
  try {
    await api.deleteChatSession(sessionId);
    
    // If deleted chat was active, go back to modules
    if (state.chatSessionId === sessionId) {
      state.chatSessionId = null;
      state.chatMessages = [];
      state.chatSessions = state.chatSessions.filter(s => s.session_id !== sessionId);
      goToModules(); // Go back to modules, not to a new chat
    } else {
      // Remove deleted chat from sessions list
      state.chatSessions = state.chatSessions.filter(s => s.session_id !== sessionId);
      render();
    }
  } catch (error) {
    console.error('Failed to delete chat:', error);
    alert('Failed to delete chat: ' + error.message);
  }
}

// ========================================
// PAGE RENDERERS
// ========================================
function renderLogin() {
  return `
    <div class="container">
      <div class="card">
        <h1>NDA Preparation Platform</h1>
        <h2>Login</h2>
        <div class="form-group">
          <label>Email:</label>
          <input type="email" id="email" placeholder="test@example.com" value="test@example.com">
        </div>
        <div class="form-group">
          <label>Password:</label>
          <input type="password" id="password" placeholder="password" value="password">
        </div>
        <button class="btn btn-primary" onclick="handleLogin()">Login</button>
        <button class="btn btn-secondary" onclick="goToPage('signup')">Create Account</button>
      </div>
    </div>
  `;
}

function renderSignup() {
  return `
    <div class="container">
      <div class="card">
        <h1>Create Account</h1>
        <div class="form-group">
          <label>Name:</label>
          <input type="text" id="name" placeholder="Your Name">
        </div>
        <div class="form-group">
          <label>Email:</label>
          <input type="email" id="email" placeholder="your@email.com">
        </div>
        <div class="form-group">
          <label>Password:</label>
          <input type="password" id="password" placeholder="password">
        </div>
        <button class="btn btn-primary" onclick="handleSignup()">Sign Up</button>
        <button class="btn btn-secondary" onclick="goToPage('login')">Back to Login</button>
      </div>
    </div>
  `;
}

function renderModules() {
  return `
    <div class="main-layout">
      <aside class="sidebar">
        <div class="sidebar-header">
          <h2>Menu</h2>
        </div>
        <nav class="sidebar-nav">
          <button class="sidebar-btn active" onclick="goToModules()">
            <span class="icon">📚</span> Modules
          </button>
          <button class="sidebar-btn" onclick="goToAnalytics()">
            <span class="icon">📊</span> Analytics
          </button>
          <button class="sidebar-btn" onclick="goToChat()">
            <span class="icon">💬</span> AI Tutor
          </button>
          <button class="sidebar-btn logout-btn" onclick="handleLogout()">
            <span class="icon">🚪</span> Logout
          </button>
        </nav>
      </aside>
      <div class="container">
        <div class="header">
          <h1>NDA Exam Sections</h1>
        </div>
        <div id="modules-list" class="grid"></div>
      </div>
    </div>
  `;
}

function renderTopics() {
  return `
    <div class="container">
      <div class="header">
        <button class="btn btn-back" onclick="goToModules()">Back</button>
        <h1>Topics</h1>
        <button class="btn btn-logout" onclick="handleLogout()">Logout</button>
      </div>
      <div id="topics-list" class="grid"></div>
    </div>
  `;
}

function renderSubtopics() {
  const topicId = state.selectedTopic || 0;
  return `
    <div class="container">
      <div class="header">
        <button class="btn btn-back" onclick="goToTopics(${state.selectedModule})">Back</button>
        <h1>Subtopics</h1>
        <button class="btn btn-logout" onclick="handleLogout()">Logout</button>
      </div>
      <div id="subtopics-list" class="grid"></div>
      <div class="info-box" style="margin-top: 30px; padding: 20px; background: #e3f2fd; border-left: 4px solid #667eea; border-radius: 5px;">
        <p style="margin: 0; font-size: 14px; color: #1565c0;">
          <strong>💡 Tip:</strong> Complete all subtopic practice tests to improve your fundamentals, then take the <strong>Adaptive Topic Test</strong> when you're ready. The adaptive test adjusts difficulty based on your answers!
        </p>
      </div>
      <div style="text-align: center; margin-top: 30px;">
        <button class="btn btn-success" onclick="goToCommonTest(${topicId})" style="padding: 15px 40px; font-size: 18px;">🎯 Topic Test (10 Adaptive Questions)</button>
      </div>
    </div>
  `;
}

function renderSubtopicDetail() {
  return `
    <div class="container">
      <div class="header">
        <button class="btn btn-back" onclick="goToSubtopics(${state.selectedTopic})">Back</button>
        <h1>Study Material</h1>
        <button class="btn btn-logout" onclick="handleLogout()">Logout</button>
      </div>
      <div id="subtopic-detail" class="card"></div>
    </div>
  `;
}

function renderTestLoading() {
  return `
    <div class="container">
      <div class="loading">
        <div class="spinner"></div>
        <p>Loading test questions...</p>
      </div>
    </div>
  `;
}

function renderTest() {
  const questions = state.testQuestions;
  const currentIdx = state.currentQuestionIndex;
  const currentQuestion = questions[currentIdx];
  
  if (!currentQuestion) {
    return `<div class="container"><p>No questions available</p></div>`;
  }
  
  const totalAnswered = Object.keys(state.userAnswers).length;
  const isLastQuestion = currentIdx === questions.length - 1;
  
  let html = `
    <div class="container">
      <div class="header">
        <button class="btn btn-back" onclick="goBackFromTest()">Back</button>
        <h1>Test</h1>
      </div>
      <div class="test-container">
        <div class="progress">
          <div class="progress-bar" style="width: ${(totalAnswered / questions.length) * 100}%"></div>
        </div>
        <div class="progress-text">Question ${currentIdx + 1}/${questions.length}</div>
        
        <div class="question single-question">
          <h3>Q${currentIdx + 1}: ${currentQuestion.question}</h3>
          <div class="options">
            <label class="option">
              <input type="radio" name="current_q" value="A" ${state.userAnswers[currentQuestion.id] === 'A' ? 'checked' : ''} onchange="saveAnswer('${currentQuestion.id}', 'A')">
              A) ${currentQuestion.options.a}
            </label>
            <label class="option">
              <input type="radio" name="current_q" value="B" ${state.userAnswers[currentQuestion.id] === 'B' ? 'checked' : ''} onchange="saveAnswer('${currentQuestion.id}', 'B')">
              B) ${currentQuestion.options.b}
            </label>
            <label class="option">
              <input type="radio" name="current_q" value="C" ${state.userAnswers[currentQuestion.id] === 'C' ? 'checked' : ''} onchange="saveAnswer('${currentQuestion.id}', 'C')">
              C) ${currentQuestion.options.c}
            </label>
            <label class="option">
              <input type="radio" name="current_q" value="D" ${state.userAnswers[currentQuestion.id] === 'D' ? 'checked' : ''} onchange="saveAnswer('${currentQuestion.id}', 'D')">
              D) ${currentQuestion.options.d}
            </label>
          </div>
        </div>
      </div>
      
      <div class="test-actions">
        ${currentIdx > 0 ? `<button class="btn btn-secondary" onclick="previousQuestion()">← Previous</button>` : ''}
        ${!isLastQuestion ? `<button class="btn btn-primary" onclick="nextQuestion()">Next →</button>` : ''}
        ${isLastQuestion ? `<button class="btn btn-success" onclick="submitTest()">✓ Submit Test</button>` : ''}
      </div>
    </div>
  `;
  return html;
}

function saveAnswer(questionId, answer) {
  state.userAnswers[questionId] = answer;
}

function nextQuestion() {
  if (state.currentQuestionIndex < state.testQuestions.length - 1) {
    state.currentQuestionIndex++;
    render();
  }
}

function previousQuestion() {
  if (state.currentQuestionIndex > 0) {
    state.currentQuestionIndex--;
    render();
  }
}

function goBackFromTest() {
  state.currentQuestionIndex = 0;
  state.testQuestions = [];
  state.userAnswers = {};
  if (state.selectedSubtopic) {
    goToSubtopicDetail(state.selectedSubtopic);
  } else {
    goToSubtopics(state.selectedTopic);
  }
}

function renderResult() {
  const result = state.testResult;
  
  let weakAreasHTML = '';
  if (result.weak_areas && result.weak_areas.length > 0) {
    weakAreasHTML = `
      <div class="weak-areas">
        <h3>📚 Topics to Review:</h3>
        <div class="topics-list">
          ${result.weak_areas.map(area => `
            <div class="weak-topic">
              <div class="topic-name">${area.name}</div>
              <div class="topic-score">${area.correct}/${area.total} (${area.accuracy}%)</div>
            </div>
          `).join('')}
        </div>
      </div>
    `;
  }
  
  return `
    <div class="container">
      <div class="header">
        <h1>Test Result</h1>
        <button class="btn btn-logout" onclick="handleLogout()">Logout</button>
      </div>
      <div class="card result-card">
        <h2>Your Score</h2>
        <div class="score-display">
          <div class="large-number">${result.score}/${result.total}</div>
          <div class="accuracy">${result.accuracy.toFixed(2)}%</div>
        </div>
        ${weakAreasHTML}
        <div class="recommendation">
          <p>${result.recommendation || 'Great effort on this test!'}</p>
        </div>
        <button class="btn btn-primary" onclick="goToSubtopics(${state.selectedTopic})">Back to Subtopics</button>
        <button class="btn btn-secondary" onclick="${state.selectedSubtopic ? `goToTest(${state.selectedSubtopic})` : `goToCommonTest(${state.selectedTopic})`}">Retake Test</button>
      </div>
    </div>
  `;
}

function renderAnalytics() {
  const weakSubtopics = state.weakSubtopics || [];
  const testHistory = state.testHistory || [];
  const recommendations = state.recommendations || {};

  let weakSubtopicsHTML = '<p>No weak areas detected yet. Keep practicing!</p>';
  if (weakSubtopics.length > 0) {
    weakSubtopicsHTML = weakSubtopics.map(item => `
      <div class="analytics-item">
        <div class="analytics-title">${item.subtopic_title}</div>
        <div class="analytics-stats">
          <span class="accuracy-badge" style="background: ${item.accuracy < 30 ? '#ff4444' : item.accuracy < 60 ? '#ffaa00' : '#44aa44'};">
            Accuracy: ${item.accuracy.toFixed(1)}%
          </span>
          <span class="attempts">Attempts: ${item.attempts}</span>
          <span class="correct">Correct: ${item.correct_answers}</span>
        </div>
      </div>
    `).join('');
  }

  let testHistoryHTML = '<p>No tests completed yet.</p>';
  if (testHistory.length > 0) {
    testHistoryHTML = testHistory.slice(0, 10).map(test => `
      <div class="analytics-item">
        <div class="analytics-title">${test.topic_title}</div>
        <div class="analytics-stats">
          <span class="score">${test.score}/${test.total}</span>
          <span class="date">${new Date(test.created_at).toLocaleDateString()}</span>
        </div>
      </div>
    `).join('');
  }

  let recommendationsHTML = '';
  if (recommendations) {
    if (recommendations.message) {
      recommendationsHTML = `
        <div class="recommendation-box">
          <p>${recommendations.message}</p>
        </div>
      `;
    } else if (recommendations.focus_now && recommendations.focus_now.length > 0) {
      recommendationsHTML = `
        <div class="recommendation-box">
          <h3>🎯 Focus Areas (Weak Topics)</h3>
          <p>Practice these topics to improve your weak areas:</p>
          <ul style="margin-top: 10px;">
            ${recommendations.focus_now.map(item => `<li>${item.subtopic_title} (${item.accuracy.toFixed(1)}%)</li>`).join('')}
          </ul>
        </div>
      `;
    } else {
      recommendationsHTML = `
        <div class="recommendation-box">
          <p>💪 Complete more tests to get personalized recommendations!</p>
        </div>
      `;
    }
  }

  return `
    <div class="main-layout">
      <aside class="sidebar">
        <div class="sidebar-header">
          <h2>Menu</h2>
        </div>
        <nav class="sidebar-nav">
          <button class="sidebar-btn" onclick="goToModules()">
            <span class="icon">📚</span> Modules
          </button>
          <button class="sidebar-btn active" onclick="goToAnalytics()">
            <span class="icon">📊</span> Analytics
          </button>
          <button class="sidebar-btn logout-btn" onclick="handleLogout()">
            <span class="icon">🚪</span> Logout
          </button>
        </nav>
      </aside>
      <div class="container">
        <div class="header">
          <h1>📊 Analytics Dashboard</h1>
        </div>

        <div class="card">
          <h2>📈 Weak Topics (Accuracy < 60%)</h2>
          <div class="analytics-list">
            ${weakSubtopicsHTML}
          </div>
        </div>

        <div class="card">
          <h2>🎯 Test History</h2>
          <div class="analytics-list">
            ${testHistoryHTML}
          </div>
        </div>

        <div class="card">
          <h2>💡 Recommendations</h2>
          ${recommendationsHTML || '<p>Complete more tests to get personalized recommendations.</p>'}
        </div>
      </div>
    </div>
  `;
}

function renderChat() {
  const messages = state.chatMessages || [];
  const sessions = state.chatSessions || [];
  
  const messagesHTML = messages.map(msg => `
    <div class="chat-message ${msg.role}">
      <div class="message-role">${msg.role === 'user' ? '👤 You' : '🤖 AI Tutor'}</div>
      <div class="message-content">${msg.content}</div>
    </div>
  `).join('');
  
  const sessionsHTML = sessions.map(session => `
    <div class="chat-history-item">
      <button class="chat-history-btn ${state.chatSessionId === session.session_id ? 'active' : ''}" 
              onclick="loadChatSession(${session.session_id})"
              title="${session.title}">
        <span class="chat-history-icon">💬</span>
        <div class="chat-history-text">
          <span class="chat-history-title">${session.title}</span>
          <span class="chat-history-count">${session.message_count} msg${session.message_count !== 1 ? 's' : ''}</span>
        </div>
      </button>
      <button class="chat-delete-btn" onclick="deleteChat(${session.session_id})" title="Delete this chat" aria-label="Delete">
        ✕
      </button>
    </div>
  `).join('');
  
  return `
    <div class="chat-layout">
      <!-- LEFT SIDEBAR - MAIN MENU -->
      <aside class="sidebar sidebar-left">
        <div class="sidebar-header">
          <h2>Menu</h2>
        </div>
        <nav class="sidebar-nav">
          <button class="sidebar-btn" onclick="goToModules()">
            <span class="icon">📚</span> Modules
          </button>
          <button class="sidebar-btn" onclick="goToAnalytics()">
            <span class="icon">📊</span> Analytics
          </button>
          <button class="sidebar-btn logout-btn" onclick="handleLogout()">
            <span class="icon">🚪</span> Logout
          </button>
        </nav>
      </aside>
      
      <!-- CENTER - CHAT AREA -->
      <div class="chat-main">
        <div class="header">
          <button class="btn btn-back" onclick="goToModules()">Back</button>
          <h1>💬 ${state.chatTitle || 'AI Tutor Chat'}</h1>
        </div>
        
        <div class="chat-container">
          <div class="chat-messages">
            ${messagesHTML || '<div style="text-align: center; color: #999; padding: 20px;">Start the conversation by asking a question!</div>'}
          </div>
          
          <div class="chat-input-area">
            <input type="text" id="chatInput" placeholder="Ask me anything..." class="chat-input">
            <button class="btn btn-primary" onclick="sendChatMessage()">Send</button>
          </div>
        </div>
      </div>
      
      <!-- RIGHT SIDEBAR - CHAT HISTORY -->
      <aside class="sidebar sidebar-right">
        <div class="sidebar-header">
          <h2>History</h2>
        </div>
        
        <div class="chat-history-section">
          ${sessions.length > 0 ? `
            <div class="chat-history-list">
              ${sessionsHTML}
            </div>
          ` : '<p class="no-history">No previous chats</p>'}
        </div>
      </aside>
    </div>
  `;
}

// ========================================
// MAIN RENDER FUNCTION
// ========================================
function render() {
  const app = document.getElementById('app');
  if (!state.token && state.currentPage !== 'login' && state.currentPage !== 'signup') {
    state.currentPage = 'login';
  }
  
  let content = '';
  switch (state.currentPage) {
    case 'login': content = renderLogin(); break;
    case 'signup': content = renderSignup(); break;
    case 'modules': content = renderModules(); break;
    case 'topics': content = renderTopics(); break;
    case 'subtopics': content = renderSubtopics(); break;
    case 'subtopic-detail': content = renderSubtopicDetail(); break;
    case 'test-loading': content = renderTestLoading(); break;
    case 'test': content = renderTest(); break;
    case 'result': content = renderResult(); break;
    case 'analytics': content = renderAnalytics(); break;
    case 'chat': content = renderChat(); break;
    default: content = renderLogin();
  }
  
  app.innerHTML = content;
  attachEventListeners();
}

// ========================================
// EVENT HANDLERS
// ========================================
async function handleLogin() {
  const email = document.getElementById('email').value;
  const password = document.getElementById('password').value;
  if (!email || !password) {
    alert('Please fill all fields');
    return;
  }
  try {
    await api.login(email, password);
    state.token = localStorage.getItem('token');
    goToModules();
  } catch (error) {
    alert('Login failed: ' + error.message);
  }
}

async function handleSignup() {
  const name = document.getElementById('name').value;
  const email = document.getElementById('email').value;
  const password = document.getElementById('password').value;
  if (!name || !email || !password) {
    alert('Please fill all fields');
    return;
  }
  try {
    await api.signup(name, email, password);
    await api.login(email, password);
    state.token = localStorage.getItem('token');
    goToModules();
  } catch (error) {
    alert('Signup failed: ' + error.message);
  }
}

function handleLogout() {
  localStorage.removeItem('token');
  state.token = null;
  state.userAnswers = {};
  goToPage('login');
}

// ========================================
// PAGE LOADERS
// ========================================
async function loadModules() {
  try {
    const modules = await api.getModules();
    const list = document.getElementById('modules-list');
    list.innerHTML = modules.map(m => `
      <div class="card clickable" onclick="goToTopics(${m.id})" style="min-height: 180px;">
        <div class="card-icon">📖</div>
        <div class="card-title">${m.title}</div>
        <p style="font-size: 12px; color: #999; margin-top: 8px;">Explore topics →</p>
      </div>
    `).join('');
  } catch (error) {
    alert('Failed to load modules: ' + error.message);
  }
}

async function loadTopics() {
  try {
    const topics = await api.getTopicsByModule(state.selectedModule);
    const list = document.getElementById('topics-list');
    list.innerHTML = topics.map(t => `
      <div class="card clickable" onclick="goToSubtopics(${t.id})" style="min-height: 200px;">
        <div class="card-icon">🎯</div>
        <div class="card-title">${t.title}</div>
        <p style="font-size: 12px; color: #999; margin-top: 8px;">Master this topic →</p>
      </div>
    `).join('');
  } catch (error) {
    alert('Failed to load topics: ' + error.message);
  }
}

async function loadSubtopics() {
  try {
    const subtopics = await api.getSubtopicsByTopic(state.selectedTopic);
    const list = document.getElementById('subtopics-list');
    list.innerHTML = subtopics.map(s => `
      <div class="card" style="padding: 25px; display: flex; flex-direction: column; justify-content: space-between; min-height: 220px;">
        <div>
          <div class="card-icon" style="margin-bottom: 12px;">📚</div>
          <div class="card-title" style="margin-bottom: 16px;">${s.title}</div>
          <p style="font-size: 13px; color: #666; line-height: 1.5; margin-bottom: 20px;">Learn concepts and prepare for practice</p>
        </div>
        <div class="button-group" style="margin: 0; gap: 8px;">
          <button class="btn btn-primary" style="flex: 1; margin: 0; padding: 10px;" onclick="goToSubtopicDetail(${s.id})">📖 Study</button>
          <button class="btn btn-success" style="flex: 1; margin: 0; padding: 10px;" onclick="goToTest(${s.id})">✏️ Practice</button>
        </div>
      </div>
    `).join('');
  } catch (error) {
    alert('Failed to load subtopics: ' + error.message);
  }
}

async function loadSubtopicDetail() {
  try {
    const subtopic = await api.getSubtopicDetail(state.selectedSubtopic);
    const detail = document.getElementById('subtopic-detail');
    detail.innerHTML = `
      <h2>${subtopic.title}</h2>
      <div class="description">${subtopic.description || 'No description available'}</div>
      <button class="btn btn-primary" onclick="goToTest(${state.selectedSubtopic})">📝 Practice (5 Questions)</button>
      <button class="btn btn-info" onclick="goToChat(${state.selectedTopic}, ${state.selectedSubtopic})">💬 Ask AI Tutor</button>
      <button class="btn btn-secondary" onclick="goToSubtopics(${state.selectedTopic})">← Back</button>
    `;
  } catch (error) {
    alert('Failed to load subtopic detail: ' + error.message);
  }
}

async function loadTest(subtopicId) {
  try {
    const questions = await api.generateSubtopicTest(subtopicId);
    state.testQuestions = questions;
    state.currentQuestionIndex = 0;
    state.currentPage = 'test';
    render();
  } catch (error) {
    alert('Failed to load test: ' + error.message);
    goToSubtopicDetail(state.selectedSubtopic);
  }
}

async function loadCommonTest(topicId) {
  try {
    const questions = await api.generateTest(topicId);
    state.testQuestions = questions;
    state.currentQuestionIndex = 0;
    state.currentPage = 'test';
    render();
  } catch (error) {
    alert('Failed to load test: ' + error.message);
    goToSubtopics(state.selectedTopic);
  }
}

async function submitTest() {
  if (Object.keys(state.userAnswers).length !== state.testQuestions.length) {
    alert('Please answer all questions');
    return;
  }
  try {
    let result;
    if (state.selectedSubtopic) {
      // Subtopic practice test
      result = await api.submitSubtopicTest(state.selectedSubtopic, state.userAnswers);
    } else {
      // Topic-wide adaptive test
      result = await api.submitTest(state.selectedTopic, state.userAnswers);
    }
    
    state.testResult = {
      score: result.score,
      total: result.total,
      accuracy: result.accuracy,
      weak_areas: result.weak_areas || [],
      recommendation: result.recommendation || 'Great effort on this test!'
    };
    state.currentQuestionIndex = 0;
    goToPage('result');
  } catch (error) {
    alert('Failed to submit test: ' + error.message);
  }
}

async function sendChatMessage() {
  const input = document.getElementById('chatInput');
  const message = input.value.trim();
  
  if (!message) {
    alert('Please enter a message');
    return;
  }
  
  try {
    // Create session on first message if it doesn't exist
    if (!state.chatSessionId) {
      const session = await api.startChatSession(state.chatTopicId, state.chatSubtopicId, state.chatTitle);
      state.chatSessionId = session.session_id;
    }
    
    // Add user message to display immediately
    state.chatMessages.push({
      role: 'user',
      content: message
    });
    input.value = '';
    render();
    
    // Call API to get AI response
    const response = await api.sendChatMessage(state.chatSessionId, message);
    
    // Add AI response to chat
    if (response.assistant_response) {
      state.chatMessages.push({
        role: 'assistant',
        content: response.assistant_response
      });
    }
    
    render();
    
    // Scroll to bottom
    setTimeout(() => {
      const messagesDiv = document.querySelector('.chat-messages');
      if (messagesDiv) {
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
      }
    }, 100);
    
  } catch (error) {
    console.error('Chat error:', error);
    alert('Failed to send message: ' + error.message);
    // Remove the last user message if send failed
    state.chatMessages.pop();
    render();
  }
}

// ========================================
// EVENT LISTENERS
// ========================================
function attachEventListeners() {
  if (state.currentPage === 'modules') {
    loadModules();
  } else if (state.currentPage === 'topics') {
    loadTopics();
  } else if (state.currentPage === 'subtopics') {
    loadSubtopics();
  } else if (state.currentPage === 'subtopic-detail') {
    loadSubtopicDetail();
  }
  
  if (state.currentPage === 'test') {
    state.testQuestions.forEach(q => {
      const radios = document.querySelectorAll(`input[name="q${q.id}"]`);
      radios.forEach(radio => {
        radio.addEventListener('change', (e) => {
          state.userAnswers[q.id] = e.target.value;
        });
      });
    });
  }
  
  if (state.currentPage === 'chat') {
    const chatInput = document.getElementById('chatInput');
    if (chatInput) {
      chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
          e.preventDefault();
          sendChatMessage();
        }
      });
      chatInput.focus();
    }
  }
}

// ========================================
// INITIALIZE
// ========================================
document.addEventListener('DOMContentLoaded', () => {
  // Clear localStorage to ensure fresh start
  localStorage.clear();
  
  // Reset state
  state.token = null;
  state.currentPage = 'login';
  state.selectedModule = null;
  state.selectedTopic = null;
  state.selectedSubtopic = null;
  
  // Now render the login page
  render();
});
