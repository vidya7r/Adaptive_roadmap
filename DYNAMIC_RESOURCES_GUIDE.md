# Dynamic Resources Implementation - Setup Guide

## ✅ What's Been Implemented

### Backend Architecture

**New Service Layer:** `backend/app/services/resource_service.py`
- **Modular design** with ResourceService class
- Three main methods:
  - `fetch_youtube_videos()` - Searches YouTube and returns top 3 videos
  - `generate_pdf_search_url()` - Creates Google Search URL for PDFs
  - `generate_article_search_url()` - Creates Google Search URL for articles
  - `get_all_resources()` - Fetches all types at once

**New API Endpoints:** `backend/app/routers/resources.py`
- **4 new dynamic endpoints:**
  - `GET /api/resources/youtube/{subtopic_id}` - YouTube videos
  - `GET /api/resources/pdf/{subtopic_id}` - PDF search URL
  - `GET /api/resources/article/{subtopic_id}` - Article search URL
  - `GET /api/resources/all/{subtopic_id}` - All resources combined

### Frontend Integration

**Updated Component:** `frontend-react/src/components/ResourcesList.jsx`
- Tabs: Videos | PDF Notes | Study Material
- Displays YouTube video thumbnails with descriptions
- Opens videos on YouTube (click "Watch" button)
- Provides Google Search URLs for PDFs and articles
- Loading, error, and empty states

**Updated Service:** `frontend-react/src/services/resourceService.js`
- New methods for each resource type
- `getYouTubeVideos()`, `getPDFResource()`, `getArticleResource()`
- `getAllResources()` for comprehensive fetch

---

## 🔧 Setup Instructions

### Step 1: Get YouTube API Key

1. Go to: https://console.cloud.google.com/
2. Create a new project
3. Enable "YouTube Data API v3" (Search for it in APIs)
4. Go to "Credentials" → Create API Key
5. Copy your API key

### Step 2: Set Environment Variable

**Option A: Create `.env` file in `backend/` folder:**
```
YOUTUBE_API_KEY=YOUR_API_KEY_HERE
```

**Option B: Set as system environment variable:**
```bash
# Windows PowerShell
$env:YOUTUBE_API_KEY = "YOUR_API_KEY_HERE"

# Or permanently:
# Settings → Environment Variables → New → YOUTUBE_API_KEY
```

### Step 3: Restart Backend

```bash
cd d:\COMPETITIVE_EXAM\backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

---

##  Testing the API

### Test YouTube Videos Endpoint

```bash
curl -X GET "http://localhost:8001/api/resources/youtube/1" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -s | python -m json.tool
```

**Expected Response:**
```json
{
  "subtopic_id": 1,
  "subtopic_title": "Kinematics",
  "videos": [
    {
      "title": "Kinematics nda basics tutorial...",
      "videoId": "dQw4w9WgXcQ",
      "description": "...",
      "thumbnail": "...",
      "channelTitle": "..."
    }
  ],
  "total": 3
}
```

### Test PDF Endpoint

```bash
curl -X GET "http://localhost:8001/api/resources/pdf/1" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -s | python -m json.tool
```

### Test Article Endpoint

```bash
curl -X GET "http://localhost:8001/api/resources/article/1" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -s | python -m json.tool
```

### Test All Resources

```bash
curl -X GET "http://localhost:8001/api/resources/all/1" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -s | python -m json.tool
```

---

## 🎯 Frontend Testing

1. **Navigate to:** Topics Page → Select any subtopic
2. **Click:** "Resources" tab in side panel
3. **You should see:** 3 tabs (Videos | PDF | Study Material)
4. **Videos tab:**
   - Shows YouTube thumbnails
   - Click "Watch on YouTube" opens YouTube
5. **PDF/Article tabs:**
   - Shows Google Search link
   - Click "Search PDFs/Materials" opens Google

---

## 📊 How It Works

### Without YouTube API Key
- Falls back to **mock videos** (for demo/testing)
- Simulates 3 sample videos
- Still generates PDF and Article search URLs

### With YouTube API Key
- **Real YouTube search** using official API
- Returns actual video thumbnails and metadata
- Sorted by relevance
- Limited by YouTube API quotas (10K quota per day)

---

## 🔑 Key Files Modified

| File | Change |
|------|--------|
| `backend/app/services/resource_service.py` | NEW - Service logic |
| `backend/app/routers/resources.py` | UPDATED - New endpoints |
| `backend/app/main.py` | Already registered router |
| `frontend-react/src/services/resourceService.js` | UPDATED - New methods |
| `frontend-react/src/components/ResourcesList.jsx` | UPDATED - Dynamic display |
| `frontend-react/src/styles/resources-list.css` | UPDATED - New styling |
| `backend/.env.example` | NEW - Config template |

---

## 🚀 Production Considerations

1. **YouTube API Quota:**
   - Limited to 10,000 quota units/day (free tier)
   - Each search = 100 quota units
   - Consider caching popular searches

2. **Error Handling:**
   - Automatically falls back to mock videos if API fails
   - Returns search URLs even if API down

3. **Scalability:**
   - No database storage needed (dynamic)
   - Minimal backend overhead
   - Search URLs are static/cacheable

---

## 📝 Example Usage Flow

```
User selects Subtopic: "Kinematics"
↓
Frontend calls: GET /api/resources/all/1
↓
Backend receives request & fetches subtopic title from DB
↓
Service layer:
  - Searches YouTube for "Kinematics nda basics tutorial"
  - Formats: "https://www.google.com/search?q=kinematics+nda+notes+pdf+filetype:pdf"
  - Returns responses
↓
Frontend displays tabs with results
↓
User clicks "Watch" → Opens YouTube
User clicks "Search PDFs" → Opens Google with query
```

---

## ❓ Troubleshooting

| Issue | Solution |
|-------|----------|
| 404 on endpoints | Restart backend after adding router |
| Mock videos showing | YouTube API key not set or invalid |
| No results | Try searching manually in YouTube Data API explorer |
| Timeout errors | Increase timeout in frontend api.js (currently 60s) |

---

## Next Steps

1. ✅ Get YouTube API key
2. ✅ Set YOUTUBE_API_KEY environment variable
3. ✅ Restart backend
4. ✅ Test endpoints via curl
5. ✅ Refresh frontend and test Resources tab
6. ✅ Enjoy dynamic learning materials!
