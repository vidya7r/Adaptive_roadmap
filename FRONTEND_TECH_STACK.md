# 🚀 FRONTEND TECH STACK & ARCHITECTURE - PROFESSIONAL NDA PLATFORM

## 📊 DATABASE MAPPING (16 TABLES CONFIRMED)

### ✅ Core Tables Ready:
| Table | Purpose | Key Fields |
|-------|---------|-----------|
| **users** | Authentication | id, name, email, password_hash, created_at |
| **sections** | Written / SSB | id, title, icon |
| **exams** | Exam types | (link sections to modules) |
| **modules** | Math, Physics, etc | id, title, icon, section_id |
| **topics** | Algebra, Geometry | id, module_id, title |
| **subtopics** | Linear Equations | id, topic_id, title, description |
| **questions** | MCQ with options | id, subtopic_id, question, option_a/b/c/d, correct_answer, difficulty |
| **options** | Question choices | ⚙️ (already in questions) |
| **resources** | YouTube/PDF links | id, subtopic_id, type (youtube/pdf), url, title |
| **streaks** | Daily streaks | id, user_id, current_streak, last_activity_date |
| **user_subtopic_progress** | Learning progress | user_id, subtopic_id, is_completed, score, accuracy |
| **user_topic_progress** | Topic progress | user_id, topic_id, is_completed, score, accuracy |
| **topic_tests** | Test history | id, user_id, topic_id, score, accuracy, time_taken |
| **test_question_logs** | Question tracking | logs each question answered |
| **chat_sessions** | AI tutor chats | id, user_id, topic_id, title, created_at |
| **chat_messages** | Chat history | id, session_id, role (user/assistant), content |

---

## ✨ COMPLETE USER JOURNEY MAPPING

```
LOGIN/SIGNUP
    ↓
SELECT EXAM (Written / SSB) [from sections table]
    ↓
SELECT MODULE (Math, Physics, etc) [filter by section_id]
    ↓
SELECT TOPIC (Algebra, Geometry, etc) [filter by module_id]
    ↓
SELECT SUBTOPIC (Linear Equations, etc) [filter by topic_id]
    ↓
LEARNING RESOURCES VIEW:
    - Get description from subtopics.description
    - Get resources from resources table (YouTube + PDF)
    - Display with embedded player / PDF viewer
    ↓
MARK AS COMPLETE
    ↓
SELECT LEARNING MODE:
    a) PRACTICE QUESTIONS (from questions table, random)
    b) TAKE TEST (questions from topic)
    c) ADAPTIVE TEST (AI adjusts difficulty)
    ↓
PRACTICE QUESTIONS
    - Get all questions for subtopic
    - One question at a time
    - Track in test_question_logs
    ↓
TESTS
    - Regular: All questions from topic
    - Adaptive: Start medium → hard/easy based on performance
    ↓
ANALYTICS
    - Weak subtopics (low scores)
    - Test history (from topic_tests table)
    - Streak count (from streaks table)
    ↓
AI TUTOR CHAT
    - Persistent chat (chat_sessions, chat_messages)
    - Send message → get AI response
    ↓
STREAK SYSTEM
    - Update daily (from streaks table)
    - Show motivational message
```

---

## 🎨 BEST TECH STACK RECOMMENDATION

### **Frontend Technology:**

#### **Option 1: React.js (RECOMMENDED - Most Professional)**
```
✅ PROS:
- Component reusability (Card, Button, Modal, etc)
- State management (Context API or Redux)
- Virtual DOM = Fast rendering
- Huge ecosystem (routing, UI libraries)
- Easy to scale and maintain
- Great for complex dashboards (Analytics)

❌ CONS:
- Learning curve if new
- Build process setup

TECH COMBO:
- React 18 (UI framework)
- React Router (navigation)
- Axios / TanStack Query (API calls)
- Tailwind CSS OR Material-UI (styling)
- Chart.js OR Recharts (analytics charts)
- Redux Toolkit (state management)
```

#### **Option 2: Vue.js (Balanced - Fast to Build)**
```
✅ PROS:
- Easier learning curve than React
- Progressive framework (can use parts)
- Great documentation
- Fast development

❌ CONS:
- Smaller ecosystem than React
- Less third-party integrations

TECH COMBO:
- Vue 3 + Vite
- Vue Router
- Pinia (state management)
- Tailwind CSS
```

#### **Option 3: Vanilla HTML/CSS/JavaScript (Current Approach - Simpler)**
```
✅ PROS:
- No build process
- No learning curve
- Fast prototyping
- Works everywhere

❌ CONS:
- Hard to manage as app grows
- Repetitive code
- State management manual
- Not scalable for 10+ pages

NOT RECOMMENDED for this scope - too complex
```

---

## 🏆 FINAL RECOMMENDATION: **React.js + Vite + Tailwind CSS + Recharts**

### Why?
- **Professional quality** → Production-ready
- **Fast development** → Reusable components
- **Scalable** → Easy to maintain & add features
- **Great UX** → Smooth animations & transitions
- **Analytics ready** → Beautiful charts for dashboard
- **Mobile responsive** → Works on all devices

---

## 📁 RECOMMENDED FOLDER STRUCTURE

```
frontend/
├── src/
│   ├── components/               # Reusable UI components
│   │   ├── Navbar.jsx
│   │   ├── Sidebar.jsx
│   │   ├── Card.jsx
│   │   ├── Button.jsx
│   │   ├── Modal.jsx
│   │   └── ...
│   │
│   ├── pages/                    # Full page components
│   │   ├── LoginPage.jsx
│   │   ├── DashboardPage.jsx
│   │   ├── ExamSelectionPage.jsx
│   │   ├── ModulesPage.jsx
│   │   ├── TopicsPage.jsx
│   │   ├── SubtopicsPage.jsx
│   │   ├── LearningPage.jsx
│   │   ├── PracticeQuestionsPage.jsx
│   │   ├── TestPage.jsx
│   │   ├── AdaptiveTestPage.jsx
│   │   ├── AnalyticsPage.jsx
│   │   └── ChatPage.jsx
│   │
│   ├── services/                 # API calls
│   │   ├── authService.js
│   │   ├── contentService.js     # modules, topics, subtopics
│   │   ├── testService.js
│   │   ├── analyticsService.js
│   │   └── chatService.js
│   │
│   ├── hooks/                    # Custom React hooks
│   │   ├── useAuth.js
│   │   ├── useFetch.js
│   │   └── useStreak.js
│   │
│   ├── context/                  # Global state (Context API)
│   │   ├── AuthContext.jsx
│   │   ├── ExamContext.jsx
│   │   └── UserContext.jsx
│   │
│   ├── styles/                   # Tailwind config & globals
│   │   └── globals.css
│   │
│   ├── App.jsx                   # Main app component
│   ├── main.jsx                  # Entry point
│   └── index.css
│
├── public/
│   └── assets/
│       └── icons/
│
├── .env                          # API URLs
├── vite.config.js
├── tailwind.config.js
└── package.json
```

---

## 🔌 API ENDPOINT SUMMARY (Frontend Perspective)

### Authentication
```
POST   /auth/signup
POST   /auth/login
GET    /auth/me
```

### Content Navigation
```
GET    /api/sections               # Written, SSB
GET    /api/modules?section_id=X   # Filter by section
GET    /api/topics?module_id=X     # Filter by module
GET    /api/subtopics?topic_id=X   # Filter by topic
GET    /api/subtopics/:id          # Single subtopic + description
```

### Resources (YouTube/PDF)
```
GET    /api/resources?subtopic_id=X   # Get all resources for subtopic
```

### Questions & Tests
```
GET    /api/questions?subtopic_id=X   # Get practice questions
POST   /test/submit                    # Submit test
GET    /adaptive/questions?difficulty=X # Get adaptive question
POST   /adaptive/submit                # Submit adaptive test
```

### Analytics
```
GET    /analytics/weak-subtopics
GET    /analytics/test-history
GET    /analytics/topic-performance
```

### AI Chat
```
POST   /chat/start-session
POST   /chat/send-message
GET    /chat/history/:session_id
GET    /chat/sessions
DELETE /chat/end-session/:session_id
```

### Streak
```
GET    /streak/current
POST   /streak/mark-activity
GET    /streak/history
```

---

## 📋 STARTUP STEPS FOR REACT FRONTEND

### Step 1: Setup Project
```bash
npm create vite@latest nda-frontend -- --template react
cd nda-frontend
npm install
```

### Step 2: Install Dependencies
```bash
npm install axios react-router-dom chart.js react-chartjs-2 tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

### Step 3: Structure (Create folders)
```bash
mkdir -p src/{components,pages,services,hooks,context,styles}
```

### Step 4: Create Base Setup
- `src/App.jsx` - Main routing
- `src/main.jsx` - Entry point
- `src/context/AuthContext.jsx` - Auth state
- `src/services/api.js` - Axios config

### Step 5: Start Building Pages (in order)
1. LoginPage (PHASE 1)
2. ExamSelectionPage
3. ModulesPage
4. TopicsPage
5. SubtopicsPage
6. LearningPage
7. PracticeQuestionsPage
8. TestPage
9. AdaptiveTestPage
10. AnalyticsPage
11. ChatPage

---

## 🎯 COMPONENT BREAKDOWN

### **Navbar Component**
```jsx
<Navbar>
  - User profile dropdown
  - Logo
  - Current streak counter (🔥 15 days)
  - Logout button
</Navbar>
```

### **Sidebar Component**
```jsx
<Sidebar>
  - Home
  - Learn (Modules)
  - Practice
  - Tests
  - Analytics
  - AI Tutor
  - Settings
</Sidebar>
```

### **Card Component (Reusable)**
```jsx
<Card 
  title="Linear Equations"
  icon="📖"
  onClick={handleClick}
  badges={["Completed", "95% Accuracy"]}
/>
```

### **Test Question Component**
```jsx
<TestQuestion
  question="What is 2+2?"
  options={["3", "4", "5", "6"]}
  onSelect={handleAnswer}
  showCorrectAnswer={isSubmitted}
/>
```

### **AnalyticsChart Component**
```jsx
<PerformanceChart
  data={weakSubtopics}
  type="bar"
/>
```

---

## 🎨 FINAL DESIGN FRAMEWORK

### Color Palette
```
Primary:      #667eea (Purple)
Secondary:    #764ba2 (Dark Purple)
Accent:       #45b7d1 (Cyan)
Success:      #11c76d (Green)
Warning:      #ff9900 (Orange)
Danger:       #ff3860 (Red)
Background:   #f8f9ff (Light Blue)
Text:         #333333 (Dark)
Light Text:   #999999 (Gray)
```

### Layout Patterns
1. **Dashboard/Grid Layout** - Modules, Topics, Subtopics
2. **3-Column Layout** - Chat (Menu | Content | History)
3. **Full-Width Content** - Learning resources, Tests
4. **Top Navigation + Sidebar** - All pages

### Animations
- Smooth card hover (lift effect)
- Fade-in on page load
- Slide transitions between pages
- Skeleton loading for async content

---

## ✅ IMPLEMENTATION CHECKLIST

### Before Starting:
- [ ] Confirm all 16 DB tables are populated with sample data
- [ ] Test all API endpoints are working
- [ ] Verify Ollama Mistral integration for AI responses
- [ ] Check YouTube/PDF resource URLs are valid

### Phase 1 (Week 1):
- [ ] Setup React + Vite + Tailwind
- [ ] Create LoginPage & SignupPage
- [ ] Create Navbar + Sidebar
- [ ] Setup AuthContext for JWT storage
- [ ] Test login flow

### Phase 2 (Week 2):
- [ ] ExamSelectionPage (Written/SSB dropdown)
- [ ] ModulesPage (grid of 8 modules)
- [ ] TopicsPage (topics for selected module)
- [ ] SubtopicsPage (subtopics for selected topic)
- [ ] Basic routing setup

### Phase 3 (Week 3):
- [ ] LearningPage (subtopic + resources)
- [ ] YouTube player integration
- [ ] PDF viewer integration
- [ ] Mark as complete functionality
- [ ] Resource display from DB

### Phase 4 (Week 4):
- [ ] PracticeQuestionsPage (one question at a time)
- [ ] Answer submission & validation
- [ ] Score tracking
- [ ] "Next Question" navigation

### Phase 5 (Week 5):
- [ ] TestPage (all questions at once)
- [ ] Test timer
- [ ] Review questions before submit
- [ ] Final score calculation
- [ ] Save test results to DB

### Phase 6 (Week 6):
- [ ] AdaptiveTestPage (difficulty adjustment logic)
- [ ] Algorithm: Easy/Medium/Hard based on answers
- [ ] Difficulty indicator
- [ ] Final adaptive score

### Phase 7 (Week 7):
- [ ] AnalyticsPage (charts & metrics)
- [ ] Weak subtopics list
- [ ] Performance over time
- [ ] Accuracy charts
- [ ] Time spent analytics

### Phase 8 (Week 8):
- [ ] ChatPage (AI tutor messaging)
- [ ] Chat history loading
- [ ] Delete chat functionality
- [ ] Real-time message display

### Phase 9 (Week 9):
- [ ] StreakComponent (daily counter)
- [ ] Streak display in Navbar
- [ ] Mark activity endpoint
- [ ] Motivational messages

### Polish & Testing (Week 10):
- [ ] Responsive design (mobile)
- [ ] Cross-browser testing
- [ ] Performance optimization
- [ ] Error handling & edge cases
- [ ] User testing & feedback

---

## 🚀 READY TO START?

### Next Actions:
1. **Do you want React.js stack confirmed?** (Yes/No)
2. **Should I create boilerplate React setup?** (Yes/No)
3. **Start with Phase 1 (Login)?** (Yes/No)

I'm ready to build! Just confirm and we'll create a professional, production-ready frontend! 💪
