# NDA Preparation Platform - Frontend

A lightweight, vanilla HTML/CSS/JavaScript frontend for the NDA preparation platform.

## Features

- ✅ Clean, responsive UI
- ✅ No heavy dependencies (no React, no build tools)
- ✅ Fast and simple
- ✅ Complete exam preparation flow
- ✅ Real-time test submissions

## Project Structure

```
frontend/
├── index.html      # Main HTML file
├── styles.css      # All styling
├── app.js          # Application logic & page rendering
├── api.js          # API client for backend calls
├── server.js       # Node.js server to serve files
└── package.json    # Node dependencies
```

## User Flow

The frontend follows this exact flow:

1. **Login** → Email/Password authentication
2. **Modules** → Select exam section (Written/SSB)
3. **Topics** → Choose topic from selected section
4. **Subtopics** → View subtopics for the topic
5. **Study** → Read explanation and prepare
6. **Test** → Take MCQ test for the topic
7. **Submit** → Submit answers
8. **Results** → View score and accuracy

## API Integration

The frontend uses these backend endpoints:

- `POST /auth/login` - User authentication
- `POST /auth/signup` - User registration
- `GET /api/modules` - Get all exam sections
- `GET /api/topics/{module_id}` - Get topics for section
- `GET /api/subtopics/{topic_id}` - Get subtopics for topic
- `GET /api/subtopic/{subtopic_id}` - Get subtopic details
- `GET /test/generate/{topic_id}` - Generate test questions
- `POST /test/submit` - Submit test answers

## Setup & Run

### Prerequisites
- Node.js installed

### Installation

```bash
cd d:\COMPETITIVE_EXAM\frontend
npm install  # No dependencies needed, just installs Node
```

### Start Frontend Server

```bash
npm start
# OR
node server.js
```

Frontend will be available at: **http://localhost:3000**

### Start Backend (in another terminal)

```bash
cd d:\COMPETITIVE_EXAM\backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8001 --reload
```

Backend will be available at: **http://127.0.0.1:8001**

## Default Test Credentials

**Email:** test@example.com  
**Password:** password

Or create a new account directly through signup.

## Features Implemented

### Authentication
- ✅ Login with email/password
- ✅ Signup with name/email/password
- ✅ JWT token storage
- ✅ Auto-logout functionality
- ✅ Session persistence

### Navigation
- ✅ Step-by-step exam flow
- ✅ Back buttons for navigation
- ✅ State management across pages
- ✅ No page refresh needed

### Study Materials
- ✅ Exam sections (modules)
- ✅ Topics per section
- ✅ Subtopics per topic
- ✅ AI-generated explanations
- ✅ Study material display

### Testing System
- ✅ MCQ test generation
- ✅ Question answering
- ✅ Real-time progress tracking
- ✅ Answer submission
- ✅ Score calculation
- ✅ Accuracy display

### UI/UX
- ✅ Responsive design
- ✅ Mobile-friendly
- ✅ Gradient backgrounds
- ✅ Smooth transitions
- ✅ Loading indicators
- ✅ Error handling

## Browser Compatibility

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers

## Performance

- **Bundle Size:** < 50KB (all files combined)
- **Load Time:** ~200ms
- **No build process required**
- **No dependencies to manage**

## Architecture

### State Management
```javascript
state = {
  currentPage,      // Current page being displayed
  token,            // JWT authentication token
  selectedModule,   // Current selected exam section
  selectedTopic,    // Current selected topic
  selectedSubtopic, // Current selected subtopic
  testQuestions,    // Questions for current test
  userAnswers,      // User's test answers
  testResult        // Final test results
}
```

### API Integration
- Centralized in `api.js`
- Automatic token attachment to requests
- Error handling for all endpoints
- Supports Bearer token authentication

## Troubleshooting

### Backend not connecting?
- Ensure backend is running on `http://127.0.0.1:8001`
- Check firewall settings
- Verify database is accessible

### Tests not loading?
- Ensure questions exist in database
- Check browser console for API errors
- Verify user is authenticated

### Styling issues?
- Clear browser cache (Ctrl+Shift+Delete)
- Hard refresh page (Ctrl+Shift+R)
- Check if styles.css is loaded

## Future Enhancements

- [ ] Offline mode (service workers)
- [ ] Analytics dashboard
- [ ] Performance tracking
- [ ] Adaptive difficulty
- [ ] Study reminders
- [ ] Question banking system
- [ ] Progress export

## Support

For issues or questions:
1. Check browser console for errors
2. Verify backend is running
3. Clear cache and try again
4. Check API endpoints are accessible

## License

MIT
