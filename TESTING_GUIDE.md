# End-to-End Testing Guide

Complete this guide to test the entire NDA preparation platform.

## 1. Verify Servers Are Running

### Backend Server
```bash
Open terminal, go to d:\COMPETITIVE_EXAM\backend
Run: python -m uvicorn app.main:app --host 127.0.0.1 --port 8001 --reload
Expected: "Uvicorn running on http://127.0.0.1:8001"
```

### Frontend Server
```bash
Open another terminal, go to d:\COMPETITIVE_EXAM\frontend
Run: npm start
Expected: "Frontend server running at http://localhost:3000"
```

## 2. Open Application

**URL:** http://localhost:3000

**Expected:** Login form with pre-filled credentials

## 3. Test Authentication Flow

### Test Login
1. **Page:** Login
2. **Email:** test@example.com (pre-filled)
3. **Password:** password (pre-filled)
4. **Click:** Login button
5. **Expected Result:** 
   - Token stored in localStorage
   - Redirects to Modules page
   - Shows 8 exam sections

### Alternative: Test Signup
1. **Page:** Login → Click "Don't have an account?"
2. **Name:** Test User
3. **Email:** newuser@example.com
4. **Password:** password123
5. **Click:** Signup button
6. **Expected Result:**
   - Account created
   - Auto-login with new account
   - Redirects to Modules page

## 4. Test Navigation Flow

### Step 1: Select Module
1. **Page:** Modules
2. **Action:** Click on any module (e.g., "Written Exam - Mathematics")
3. **Expected:** 
   - Module loads topics
   - Shows list of topics for selected module
   - Back button visible

### Step 2: Select Topic
1. **Page:** Topics
2. **Action:** Click on any topic
3. **Expected:**
   - Shows subtopics for selected topic
   - Each subtopic has "Study" and "Test" buttons
   - Back button to go to modules

### Step 3: View Subtopic Details
1. **Page:** Subtopics
2. **Action:** Click "Study" button on any subtopic
3. **Expected:**
   - Shows subtopic title
   - Shows description/explanation
   - Shows "Start Test" button
   - Back button

### Step 4: Take Test
1. **Page:** Subtopic Detail
2. **Action:** Click "Start Test" button
3. **Expected:**
   - Test questions load
   - Progress bar shows (1/5, 1/10, etc.)
   - Question text visible
   - Four radio button options (A, B, C, D)
   - Submit button disabled until all answered

### Step 5: Answer All Questions
1. **Page:** Test
2. **Action:** Click radio button for each question
3. **Expected:**
   - Radio buttons highlight when clicked
   - User answers tracked
   - Progress bar updates
   - Submit button becomes enabled

### Step 6: Submit Test
1. **Page:** Test (all questions answered)
2. **Action:** Click "Submit" button
3. **Expected:**
   - Loading spinner appears
   - API call to /test/submit
   - Results page displays:
     - Score (e.g., "7/10")
     - Accuracy percentage
     - "Try Again" button
     - "Back to Modules" button

### Step 7: View Results
1. **Page:** Results
2. **Expected:**
   - Score clearly displayed
   - Accuracy percentage shown
   - Option to retry test
   - Option to go back
   - Logout button visible

## 5. Test Error Handling

### Test Invalid Login
1. **Page:** Login
2. **Email:** invalid@example.com
3. **Password:** wrongpassword
4. **Click:** Login
5. **Expected:** Error message displayed

### Test Missing Answers
1. **Page:** Test (partially answered)
2. **Action:** Leave some questions unanswered
3. **Click:** Submit button
4. **Expected:** 
   - Error message: "Please answer all questions"
   - Submit blocked until all answered

### Test Backend Connection Issue
1. **Stop backend server** (Ctrl+C in backend terminal)
2. **Action:** Try to login or take test
3. **Expected:** Error message about server connection

## 6. Test UI Responsiveness

### Desktop (1920px or larger)
1. Open http://localhost:3000
2. Verify:
   - Multi-column grid for modules
   - Proper spacing
   - All buttons visible

### Tablet (768px - 1024px)
1. Open DevTools (F12)
2. Set device type to "iPad"
3. Verify:
   - Single column grid
   - Touch-friendly buttons
   - Readable text

### Mobile (320px - 480px)
1. Open DevTools (F12)
2. Set device type to "iPhone"
3. Verify:
   - Stacked layout
   - Full-width buttons
   - Scrollable content
   - No horizontal scroll

## 7. Test Data Persistence

### Test Session Persistence
1. **Action:** Login and go to Modules
2. **Open DevTools:** F12 → Applications → LocalStorage
3. **Verify:** Token is stored with key starting with `token`
4. **Refresh page:** Should stay logged in
5. **Close browser:** Reopen localhost:3000 → Should be logged out (session ended)

### Test Answer Persistence
1. **Page:** Test
2. **Answer question 1:** Select option A
3. **Answer question 2:** Select option B
4. **Refresh page:** Should lose answers (by design)
5. **Go back and restart test:** Should load fresh questions

## 8. Verify All Endpoints

Check backend is responding to all endpoints:

```bash
# Test Module Endpoint
curl http://127.0.0.1:8001/api/modules

# Test Topics Endpoint (replace 1 with actual module ID)
curl http://127.0.0.1:8001/api/topics/1

# Test Subtopics Endpoint (replace 1 with actual topic ID)
curl http://127.0.0.1:8001/api/subtopics/1

# Test Login
curl -X POST http://127.0.0.1:8001/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "email=test@example.com&password=password"

# Test Generate Test (requires token)
curl http://127.0.0.1:8001/test/generate/1 \
  -H "Authorization: Bearer <YOUR_TOKEN>"
```

## 9. Browser Console Checks

Open DevTools (F12) and check Console tab:

### No errors should appear:
- ❌ "Objects are not valid as React child"
- ❌ "TypeError: Cannot read property..."
- ❌ "Uncaught SyntaxError..."

### Expected console logs:
- ✅ API calls being made
- ✅ Token being stored/retrieved
- ✅ Page transitions happening

## 10. Performance Checks

### Initial Load Time
1. Open http://localhost:3000
2. Check browser DevTools Network tab
3. **Expected:** 
   - index.html: ~1KB
   - app.js: ~15KB
   - api.js: ~5KB
   - styles.css: ~30KB
   - Total time: <500ms

### Page Transition Time
1. Go from Modules → Topics → Subtopics
2. Each transition should be instant (<100ms)
3. No spinning wheels except during API calls

### Test Loading Time
1. Click "Start Test"
2. Questions should load within 1-2 seconds
3. No blank areas or flashing

## 11. Functionality Checklist

- [ ] Login works with test@example.com
- [ ] Signup creates new account
- [ ] Can browse modules
- [ ] Can select topics
- [ ] Can view subtopics
- [ ] Study page shows content
- [ ] Test page loads questions
- [ ] Can answer all questions
- [ ] Submit button enables after answering all
- [ ] Results display score
- [ ] Results display accuracy %
- [ ] Can retry test
- [ ] Can go back to modules
- [ ] Logout clears session
- [ ] Mobile layout works
- [ ] Desktop layout works
- [ ] No JavaScript errors in console

## 12. Success Criteria

✅ **All tests passed if:**
1. Can complete full flow: Login → Module → Topic → Subtopic → Test → Result
2. Score and accuracy display correctly
3. No errors in browser console
4. Responsive on mobile and desktop
5. All buttons and forms work
6. Backend connection stable

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Login fails | Check backend is running on 127.0.0.1:8001 |
| Test questions won't load | Check if topics have questions in database |
| Styling looks broken | Clear cache (Ctrl+Shift+Delete) and refresh |
| Submit button disabled | Ensure all questions are answered |
| Backend subprocess error | This is normal, backend still runs |
| Frontend not responding | Kill node.exe in Task Manager, restart |

## Performance Metrics

| Metric | Target | Expected |
|--------|--------|----------|
| Page Load | <500ms | ~200ms |
| Module Load | <200ms | ~100ms |
| Test Load | <2s | ~1s |
| Answer Submit | <3s | ~1-2s |
| Bundle Size | <100KB | ~50KB |

---

**Test Date:** _______________  
**Tester:** _______________  
**Result:** ✅ PASS / ❌ FAIL

**Notes:**
_________________________________
_________________________________
_________________________________
