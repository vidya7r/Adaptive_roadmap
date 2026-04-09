// APP State
const state = {
  currentPage: 'login',
  token: localStorage.getItem('token'),
  selectedModule: null,
  selectedTopic: null,
  selectedSubtopic: null,
  testQuestions: [],
  userAnswers: {},
  testResult: null,
};

// Page Navigation
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

function goToTest(topicId) {
  state.selectedTopic = topicId;
  state.userAnswers = {};
  goToPage('test-loading');
  loadTest(topicId);
}

// Main Render Function
function render() {
  try {
    const app = document.getElementById('app');
    console.log('Rendering page:', state.currentPage);
    
    // Check if user is logged in
    if (!state.token && state.currentPage !== 'login' && state.currentPage !== 'signup') {
      console.log('Not logged in, showing login');
      state.currentPage = 'login';
    }
    
    let content = '';
    
    switch (state.currentPage) {
      case 'login':
        content = renderLogin();
        break;
      case 'signup':
        content = renderSignup();
        break;
      case 'modules':
        content = renderModules();
        break;
      case 'topics':
        content = renderTopics();
        break;
      case 'subtopics':
        content = renderSubtopics();
        break;
      case 'subtopic-detail':
        content = renderSubtopicDetail();
        break;
      case 'test-loading':
        content = renderTestLoading();
        break;
      case 'test':
        content = renderTest();
        break;
      case 'result':
        content = renderResult();
        break;
      default:
        content = renderLogin();
    }
    
    if (!content) {
      throw new Error('No content generated for page: ' + state.currentPage);
    }
    
    app.innerHTML = content;
    console.log('Page rendered successfully');
    attachEventListeners();
  } catch (error) {
    console.error('Render error:', error);
    document.getElementById('app').innerHTML = `<div style="color: red; padding: 20px; font-family: monospace;">ERROR: ${error.message}</div>`;
  }
}

// PAGE RENDERERS
function renderLogin() {
  try {
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
  } catch (error) {
    console.error('renderLogin error:', error);
    return `<div style="color: red; padding: 20px;">Login render error: ${error.message}</div>`;
  }
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
    <div class="container">
      <div class="header">
        <h1>📚 NDA Exam Sections</h1>
        <button class="btn btn-logout" onclick="handleLogout()">Logout</button>
      </div>
      <div id="modules-list" class="grid"></div>
    </div>
  `;
}

function renderTopics() {
  return `
    <div class="container">
      <div class="header">
        <button class="btn btn-back" onclick="goToModules()">← Back</button>
        <h1>📖 Topics</h1>
        <button class="btn btn-logout" onclick="handleLogout()">Logout</button>
      </div>
      <div id="topics-list" class="grid"></div>
    </div>
  `;
}

function renderSubtopics() {
  return `
    <div class="container">
      <div class="header">
        <button class="btn btn-back" onclick="goToTopics(${state.selectedModule})">← Back</button>
        <h1>📝 Subtopics</h1>
        <button class="btn btn-logout" onclick="handleLogout()">Logout</button>
      </div>
      <div id="subtopics-list" class="grid"></div>
    </div>
  `;
}

function renderSubtopicDetail() {
  return `
    <div class="container">
      <div class="header">
        <button class="btn btn-back" onclick="goToSubtopics(${state.selectedTopic})">← Back</button>
        <h1>📚 Study Material</h1>
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
  
  let html = `
    <div class="container">
      <div class="header">
        <button class="btn btn-back" onclick="goToSubtopics(${state.selectedTopic})">← Back</button>
        <h1>📋 Test</h1>
      </div>
      <div class="test-container">
        <div class="progress">
          <div class="progress-bar" style="width: ${(Object.keys(state.userAnswers).length / questions.length) * 100}%"></div>
        </div>
        <div class="progress-text">Answered: ${Object.keys(state.userAnswers).length}/${questions.length}</div>
  `;
  
  questions.forEach((q, idx) => {
    const isAnswered = state.userAnswers[q.id] !== undefined;
    html += `
      <div class="question">
        <h3>Q${idx + 1}: ${q.text}</h3>
        <div class="options">
          <label class="option">
            <input type="radio" name="q${q.id}" value="A" ${state.userAnswers[q.id] === 'A' ? 'checked' : ''}>
            A) ${q.options[0] || q.options.A}
          </label>
          <label class="option">
            <input type="radio" name="q${q.id}" value="B" ${state.userAnswers[q.id] === 'B' ? 'checked' : ''}>
            B) ${q.options[1] || q.options.B}
          </label>
          <label class="option">
            <input type="radio" name="q${q.id}" value="C" ${state.userAnswers[q.id] === 'C' ? 'checked' : ''}>
            C) ${q.options[2] || q.options.C}
          </label>
          <label class="option">
            <input type="radio" name="q${q.id}" value="D" ${state.userAnswers[q.id] === 'D' ? 'checked' : ''}>
            D) ${q.options[3] || q.options.D}
          </label>
        </div>
      </div>
    `;
  });
  
  html += `
    </div>
    <div class="test-actions">
      <button class="btn btn-primary" onclick="submitTest()">Submit Test</button>
    </div>
  </div>
  `;
  
  return html;
}

function renderResult() {
  const result = state.testResult;
  return `
    <div class="container">
      <div class="header">
        <h1>🎯 Test Result</h1>
        <button class="btn btn-logout" onclick="handleLogout()">Logout</button>
      </div>
      <div class="card result-card">
        <h2>Your Score</h2>
        <div class="score-display">
          <div class="large-number">${result.score}/${result.total}</div>
          <div class="accuracy">${result.accuracy.toFixed(2)}%</div>
        </div>
        
        <div class="score-details">
          <p><strong>Correct Answers:</strong> ${result.correct}</p>
          <p><strong>Wrong Answers:</strong> ${result.total - result.correct}</p>
          <p><strong>Accuracy:</strong> ${result.accuracy.toFixed(2)}%</p>
        </div>
        
        <button class="btn btn-primary" onclick="goToSubtopics(${state.selectedTopic})">Back to Subtopics</button>
        <button class="btn btn-secondary" onclick="goToTest(${state.selectedTopic})">Retake Test</button>
      </div>
    </div>
  `;
}

// EVENT HANDLERS
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
    // Auto-login after signup
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

// PAGE LOADERS
async function loadModules() {
  try {
    const modules = await api.getModules();
    const list = document.getElementById('modules-list');
    list.innerHTML = modules.map(m => `
      <div class="card clickable" onclick="goToTopics(${m.id})">
        <div class="card-icon">${m.icon}</div>
        <div class="card-title">${m.title}</div>
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
      <div class="card clickable" onclick="goToSubtopics(${t.id})">
        <div class="card-title">${t.title}</div>
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
      <div class="card">
        <div class="card-title">${s.title}</div>
        <button class="btn btn-primary" onclick="goToSubtopicDetail(${s.id})">Study</button>
        <button class="btn btn-secondary" onclick="goToTest(${state.selectedTopic})">Test</button>
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
      <div class="description">${subtopic.description}</div>
      <button class="btn btn-primary" onclick="goToTest(${state.selectedTopic})">Start Test</button>
      <button class="btn btn-secondary" onclick="goToSubtopics(${state.selectedTopic})">Back</button>
    `;
  } catch (error) {
    alert('Failed to load subtopic detail: ' + error.message);
  }
}

async function loadTest(topicId) {
  try {
    const questions = await api.generateTest(topicId);
    state.testQuestions = questions;
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
    const result = await api.submitTest(state.selectedTopic, state.userAnswers);
    state.testResult = {
      score: result.correct,
      total: result.total,
      correct: result.correct,
      accuracy: result.accuracy,
    };
    goToPage('result');
  } catch (error) {
    alert('Failed to submit test: ' + error.message);
  }
}

// ATTACH EVENT LISTENERS
function attachEventListeners() {
  // Load page content
  if (state.currentPage === 'modules') {
    loadModules();
  } else if (state.currentPage === 'topics') {
    loadTopics();
  } else if (state.currentPage === 'subtopics') {
    loadSubtopics();
  } else if (state.currentPage === 'subtopic-detail') {
    loadSubtopicDetail();
  }
  
  // Attach radio button listeners for test
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
}

// INITIALIZE
function init() {
  try {
    console.log('App init: Starting...');
    const app = document.getElementById('app');
    console.log('App element found:', app);
    
    if (state.token) {
      console.log('Token found, going to modules');
      goToModules();
    } else {
      console.log('No token, rendering login');
      render();
    }
  } catch (error) {
    console.error('Init error:', error);
    document.getElementById('app').innerHTML = `<div style="color: red; padding: 20px; font-family: monospace;">ERROR: ${error.message}</div>`;
  }
}

// Wait for DOM to be ready
if (document.readyState === 'loading') {
  console.log('DOM still loading, waiting...');
  document.addEventListener('DOMContentLoaded', () => {
    console.log('DOMContentLoaded fired');
    init();
  });
} else {
  console.log('DOM already ready');
  init();
}
