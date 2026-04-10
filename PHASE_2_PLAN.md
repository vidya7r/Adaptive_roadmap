# 🎯 PHASE 2 - EXAM SELECTION (Written/SSB)

## 📋 Requirements:

### User Flow:
```
After Login (Dashboard)
    ↓
Click "Start Learning" or navigate to Exam Selection
    ↓
Two Options: Written Exam or SSB
    ↓
Click one → Navigate to Modules Selection
```

### Data Structure:
- **From DB:** `sections` table (Written, SSB)
- **Display:** Beautiful cards with icons
- **Interaction:** Click to select → Store selection in context → Navigate to Modules

---

## 📁 Files to Create:

### 1. **ExamSelectionPage.jsx** - The main page
### 2. **ExamContext.jsx** - Global exam state (which exam selected)
### 3. **Update App.jsx** - Add new route & context provider
### 4. **Update DashboardPage.jsx** - Add button to start learning

---

## 🎨 UI Mockup:

```
┌────────────────────────────────────┐
│         NDA Exam Selection          │
│                                    │
│  [Written]  [SSB]                 │
│   Exam       Interview             │
│                                    │
└────────────────────────────────────┘

Each card with:
- Icon (📝 for Written, 🎖️ for SSB)
- Title
- Description
- Click to select
```

---

## 🔧 API Endpoint Needed:

```bash
GET /api/sections

Response:
{
  "sections": [
    {"id": 1, "title": "Written", "icon": "📝"},
    {"id": 2, "title": "SSB", "icon": "🎖️"}
  ]
}
```

---

## 💾 ExamContext Structure:

```javascript
{
  selectedSection: 1 or 2,
  selectedModuleId: null,
  selectedTopicId: null,
  selectedSubtopicId: null,
  setSelectedSection(id),
  setSelectedModuleId(id),
  ...
}
```

---

## ✅ Phase 2 Checklist:

- [ ] Create ExamContext.jsx
- [ ] Add ExamProvider to App.jsx
- [ ] Create ExamSelectionPage.jsx
- [ ] Fetch sections from /api/sections
- [ ] Display as beautiful cards
- [ ] Click handler to save selection
- [ ] Navigate to /modules after selection
- [ ] Update DashboardPage with "Start Learning" button
- [ ] Test the flow

---

Ready to build! Let me know when you've tested login/signup!
