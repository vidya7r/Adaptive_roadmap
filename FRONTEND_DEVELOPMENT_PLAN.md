# 🎨 FRONTEND DEVELOPMENT PLAN - Professional NDA Exam Platform

## ✅ USER REQUIREMENTS UNDERSTOOD

1. **Professional Website** with smooth UX
2. **Exam Sections:** Written + SSB (dropdown)
3. **Content Hierarchy:** Modules → Topics → Subtopics → Learning Resources
4. **Dynamic Explanations:** Use Ollama Mistral AI (not static text)
5. **Learning Flow:** Roadmap-style learning path → Practice Questions → Tests
6. **Adaptive Testing:** Questions difficulty adjusted based on performance
7. **Analytics Page:** Show weak topics and areas to improve
8. **AI Tutor Chat:** ChatGPT/Gemini-like conversation
9. **Streak System:** Motivate user with learning streaks
10. **YouTube Links & PDFs:** Learning resources embedded

---

## 🏗️ FRONTEND ARCHITECTURE

### Page Structure:
```
├── 🔐 Login Page (unauthenticated)
├── 📝 Exam Selection (Written / SSB)
├── 📚 Module Selection (Mathematics, Physics, etc.)
├── 🎯 Topic Selection (Algebra, Geometry, etc.)
├── 📖 Subtopic View (Learning Resources + Explanation from Ollama)
├── 📝 Practice Questions
├── 📊 Regular Test
├── 🤖 Adaptive Test
├── 📈 Analytics Dashboard
├── 💬 AI Tutor Chat
└── ⚙️ User Profile/Settings
```

---

## 🎯 PHASE-BY-PHASE FRONTEND DEVELOPMENT PLAN

### **PHASE 1: Authentication & Navigation (FOUNDATION)**

**Pages:**
1. **Login Page** (`login.html`)
   - Email + Password input
   - Login button
   - Sign-up link
   - Store JWT token in localStorage

2. **Main Dashboard/Navigation**
   - Top navigation bar with user profile
   - Left sidebar with menu
   - Responsive design

**Backend Endpoints Used:**
- `POST /auth/login`
- `POST /auth/signup`
- `GET /auth/me` (get current user)

---

### **PHASE 2: Content Navigation (Roadmap)**

**Pages:**
1. **Exam Selection** (`exam.html`)
   - Dropdown: Written or SSB
   - Visual cards for each option

2. **Module Selection** (`modules.html`)
   - Display 8 modules: Math, Physics, Chemistry, etc.
   - Grid layout with icons
   - Click to see topics

3. **Topic Selection** (`topics.html`)
   - Show topics under selected module
   - Grid/list layout
   - Click to see subtopics

4. **Subtopic Selection** (`subtopics.html`)
   - Show subtopics under selected topic
   - Display progress (if any)
   - Click to view learning resources

**Backend Endpoints Used:**
- `GET /api/modules` (8 NDA modules)
- `GET /api/topics` (all topics)
- `GET /api/topics/{module_id}` (topics by module)
- `GET /api/subtopics/{topic_id}` (subtopics by topic)

---

### **PHASE 3: Learning Resources (CRUCIAL INNOVATION)**

**Page:**
1. **Subtopic Learning View** (`subtopic-learning.html`)
   - **Dynamic Explanation from Ollama:**
     - Instead of static `subtopic.description`, call backend to generate via Mistral
     - Endpoint: `GET /ai/explanation?subtopic_id=X` (NEW ENDPOINT NEEDED)
   - **Learning Resources:**
     - YouTube links (embedded player)
     - PDF links (with preview/download)
     - Roadmap visualization (like roadmap.sh)
   - **Mark as Complete** button

**Backend Endpoints Used:**
- `GET /api/subtopics/{id}` (get subtopic details)
- `GET /ai/explanation?subtopic_id=X` (NEED TO CREATE - Ollama Mistral for explanation)
- `GET /api/resources?subtopic_id=X` (if applicable)
- `POST /progress/mark-complete` (mark subtopic complete)

**INNOVATION:**
```
Flow: 
User clicks subtopic 
→ Frontend fetches from DB (gets subtopic_id)
→ Calls Ollama endpoint to generate AI explanation
→ Displays explanation + YouTube/PDF resources
→ User marks as complete (saves progress)
```

---

### **PHASE 4: Practice Questions**

**Page:**
1. **Practice Questions** (`practice.html`)
   - Display questions from selected subtopic
   - One question at a time or all? (UX decision)
   - Show options: A, B, C, D
   - Submit answer
   - Get explanation for correct answer
   - Move to next question

**Backend Endpoints Used:**
- `GET /api/questions?subtopic_id=X` (get all questions for subtopic)
- `POST /practice/submit` (submit answer & track progress)
- `GET /api/questions/{id}` (get single question)

---

### **PHASE 5: Testing (Regular + Adaptive)**

**Pages:**
1. **Test Selection** (`test-selection.html`)
   - Option 1: Topic-wise test (questions from selected topic)
   - Option 2: Adaptive test (AI adjusts difficulty)

2. **Regular Test** (`test.html`)
   - Display all test questions
   - Timer
   - Mark for review
   - Submit test
   - Show results

3. **Adaptive Test** (`adaptive-test.html`)
   - Starts with medium difficulty
   - If correct → next is hard
   - If incorrect → next is easy
   - AI algorithm adjusts based on performance
   - Show final score + difficulty achieved

**Backend Endpoints Used:**
- `GET /test/generate?topic_id=X` (generate test questions)
- `POST /test/submit` (submit test & calculate score)
- `GET /adaptive/questions?current_score=X&difficulty=Y` (get next question)
- `POST /adaptive/submit` (submit adaptive test)

---

### **PHASE 6: Analytics Dashboard**

**Page:**
1. **Analytics** (`analytics.html`)
   - **Weak Areas:** Show topics/subtopics with low scores
   - **Test History:** Recent test results with scores
   - **Accuracy Chart:** Progress over time
   - **Time Spent:** How long spent on each topic
   - **Recommendations:** "You need to focus on Topic X"

**Backend Endpoints Used:**
- `GET /analytics/weak-subtopics` (topics to improve)
- `GET /analytics/test-history` (past test results)
- `GET /analytics/accuracy-progress` (if available)
- `GET /analytics/time-spent` (if available)

---

### **PHASE 7: AI Tutor Chat (ChatGPT-style)**

**Page:**
1. **AI Tutor** (`ai-tutor.html`)
   - 3-column layout: Menu | Chat | History
   - Chat conversation area
   - Message input & send button
   - Chat history on right sidebar
   - Delete chat option
   - New chat option

**Backend Endpoints Used:**
- `POST /chat/start-session` (create new chat)
- `POST /chat/send-message` (send message & get AI response)
- `GET /chat/history/{session_id}` (load chat history)
- `GET /chat/sessions` (list all chats)
- `DELETE /chat/end-session/{session_id}` (delete chat)

---

### **PHASE 8: Streak System (Gamification)**

**Elements:**
1. **Daily Streak Counter**
   - Display current streak
   - Show calendar of learning days
   - Reset when no activity for 1 day

2. **UI Placement:**
   - Top right corner of dashboard
   - Show: "🔥 15 day streak"
   - Motivational message

**Backend Endpoints Needed:**
- `GET /streak/current` (get user's current streak)
- `POST /streak/update-daily` (update daily streak)
- `GET /streak/history` (get streak calendar)

---

### **PHASE 9: User Profile & Settings**

**Page:**
1. **Profile** (`profile.html`)
   - User info (name, email)
   - Progress summary
   - Account settings
   - Logout button

**Backend Endpoints Used:**
- `GET /auth/me` (current user info)
- `PUT /auth/profile` (update profile)
- `POST /auth/logout` (logout)

---

## 📊 DATABASE REQUIREMENTS FOR FRONTEND FUNCTIONALITY

### NEW ENDPOINTS NEEDED IN BACKEND:

1. **AI Explanation Endpoint:** `GET /ai/explanation?subtopic_id=X`
   - Calls Ollama Mistral
   - Returns AI-generated explanation
   - Caches result for performance

2. **Streak Endpoints:**
   - `GET /streak/current`
   - `POST /streak/update-daily`
   - `GET /streak/history`

3. **Resources Endpoint:** `GET /api/resources?subtopic_id=X`
   - Returns YouTube links + PDF links
   - Currently stored where? (Check if in DB)

---

## 🎨 UI/UX DESIGN FRAMEWORK

### Color Scheme:
- **Primary:** #667eea (Purple)
- **Secondary:** #764ba2 (Dark Purple)
- **Accent:** #45b7d1 (Cyan)
- **Background:** #f8f9ff (Light Blue)
- **Text:** #333333 (Dark Gray)

### Components:
- Modern gradient cards
- Smooth animations
- Responsive design (Mobile + Desktop)
- Clean typography
- Icons for each section

### Layout Patterns:
- 3-column layout for complex pages (Menu | Content | Sidebar)
- Grid layout for selections (Modules, Topics, Subtopics)
- Full-width content for reading/learning
- Modal popups for confirmations

---

## 🔄 DEVELOPMENT SEQUENCE (Recommended)

```
Week 1: PHASE 1 (Auth + Navigation)
Week 2: PHASE 2 (Content Navigation)
Week 3: PHASE 3 (Learning + Resources + Ollama Integration)
Week 4: PHASE 4 (Practice Questions)
Week 5: PHASE 5 (Testing)
Week 6: PHASE 6 (Analytics)
Week 7: PHASE 7 (AI Chat)
Week 8: PHASE 8-9 (Streak + Profile)
```

---

## ✅ VERIFICATION CHECKLIST

- [ ] Backend Exam Sections (Written/SSB) - Structure in DB?
- [ ] Ollama Mistral Integration - Already set up?
- [ ] YouTube/PDF resources - Stored in which table?
- [ ] Streak system - Database table exists?
- [ ] Chat system - All endpoints ready?
- [ ] Adaptive algorithm logic - Backend ready?

---

## 🚀 NEXT STEPS

1. **Verify with Backend Team:**
   - Confirm all required tables exist
   - Check which endpoints are missing
   - Clarify resources storage (YouTube links, PDFs)

2. **Import Base Files:**
   - Create HTML template structure
   - Set up CSS framework
   - Create JavaScript module system

3. **Start PHASE 1:**
   - Build login authentication
   - Create dashboard navigation

---

**Status:** ⏳ PENDING BACKEND VERIFICATION
