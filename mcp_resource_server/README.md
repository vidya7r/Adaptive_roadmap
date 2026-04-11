# MCP Resource Server

## Overview
This is a Model Context Protocol (MCP) server that provides tools for fetching academic PDFs and educational articles for competitive exam preparation.

## Features
- **PDF Fetcher**: Fetches research papers from arXiv specifically related to exam topics
- **Article Fetcher**: Fetches educational articles from multiple sources:
  - Dev.to (technical articles)
  - Hackernoon (tech news & guides)
  - GeeksforGeeks (tutorials)

## Installation

### Prerequisites
- Python 3.8+
- requests library

### Setup

1. **Install dependencies**:
```bash
pip install -r requirements.txt
```

2. **Run as standalone MCP server** (optional):
```bash
python server.py
```

3. **Use from FastAPI backend** (recommended):
The fetchers are automatically imported and used by the FastAPI backend's resource service.

## Architecture

### File Structure
```
mcp_resource_server/
├── __init__.py                 # Package init
├── pdf_fetcher.py             # PDF fetching logic (arXiv API)
├── article_fetcher.py         # Article fetching logic
├── server.py                  # MCP server implementation
└── requirements.txt           # Dependencies
```

### Component Flow

```
FastAPI Backend
    ↓
resource_service.py
    ↓
[PDFFetcher] ← arXiv API
[ArticleFetcher] ← Dev.to / Hackernoon / GeeksforGeeks
    ↓
React Frontend
    ↓
ResourcesList Component
```

## Usage

### From FastAPI

```python
from backend.app.services.resource_service import resource_service

# Fetch PDFs for a topic
pdfs = resource_service.fetch_pdfs("Kinematics", max_results=5)

# Fetch Articles for a topic
articles = resource_service.fetch_articles("Kinematics", max_results=5)

# Get both
all_resources = resource_service.get_all_resources("Kinematics")
```

### PDF Response Format
```json
{
  "title": "Paper Title",
  "url": "https://arxiv.org/pdf/...",
  "source": "arXiv",
  "authors": ["Author 1", "Author 2"],
  "author_display": "Author 1",
  "published_date": "2024-01-15",
  "description": "Abstract...",
  "type": "pdf",
  "pages": "50+",
  "file_size": "2.5 MB",
  "rating": 4.5
}
```

### Article Response Format
```json
{
  "title": "Article Title",
  "url": "https://dev.to/...",
  "source": "Dev.to",
  "author_display": "Author Name",
  "published_date": "2024-01-15",
  "description": "Summary...",
  "type": "article",
  "reading_time": "10 min read",
  "category": "Tutorial",
  "views": 1000
}
```

## API Endpoints

### Get PDFs for a subtopic
```
GET /api/resources/pdf/{subtopic_id}
```

**Response**:
```json
{
  "subtopic_id": 1,
  "subtopic_title": "Kinematics",
  "pdfs": [...],
  "total": 5
}
```

### Get Articles for a subtopic
```
GET /api/resources/article/{subtopic_id}
```

**Response**:
```json
{
  "subtopic_id": 1,
  "subtopic_title": "Kinematics",
  "articles": [...],
  "total": 5
}
```

### Get All Resources
```
GET /api/resources/all/{subtopic_id}
```

**Response**:
```json
{
  "subtopic_id": 1,
  "subtopic_title": "Kinematics",
  "videos": [...],
  "pdfs": [...],
  "articles": [...]
}
```

## External APIs Used

### arXiv API
- **Base URL**: http://export.arxiv.org/api/query
- **No Authentication**: Free to use
- **Rate Limit**: Reasonable limits for educational use
- **Response Format**: Atom XML
- **Docs**: https://arxiv.org/help/api

### Dev.to API
- **Base URL**: https://dev.to/api
- **No Authentication**: Free to use (public articles only)
- **Rate Limit**: Reasonable limits
- **Response Format**: JSON
- **Docs**: https://docs.dev.to/api

### Hackernoon & GeeksforGeeks
- **Method**: Direct URL construction (no API available)
- **No Authentication**: Public URLs
- **No Rate Limit**: Directing to public websites

## Fallback Behavior

If any API fails or the fetcher is not available, the service returns fallback data:
- **PDFs**: Links to arXiv search results
- **Articles**: Links to GeeksforGeeks search results

## Future Enhancements

1. **Add More API Sources**:
   - Google Scholar (requires proxy)
   - ResearchGate API
   - Medium API (requires API key)

2. **Caching**:
   - Cache results for 24 hours
   - Store in database or Redis

3. **User Preferences**:
   - Allow users to customize sources
   - Save favorite resources

4. **Advanced Filtering**:
   - Filter by publication date
   - Filter by language
   - Filter by relevance score

5. **Full MCP Server**:
   - Implement as standalone MCP-compatible server
   - Use stdio transport for communication
   - Support multiple clients

## Troubleshooting

### No PDFs returned
- **Issue**: arXiv API might be slow or return no results for the search term
- **Solution**: Try using more general keywords; check arXiv.org directly

### Articles show fallback only
- **Issue**: Dev.to API might be down or rate-limited
- **Solution**: Check API status; increase cache time

### ImportError when loading fetchers
- **Issue**: MCP modules not properly installed or path issues
- **Solution**: Verify `mcp_resource_server` is in the correct directory; check sys.path

## License & Attribution

- **arXiv**: Data from arXiv is available under CC0 1.0 Universal
- **Dev.to**: Content from Dev.to community
- **Hackernoon & GeeksforGeeks**: Public educational content

## Contributing

To extend the resource fetchers:

1. Create a new fetcher module (e.g., `scholar_fetcher.py`)
2. Implement a static method following the same pattern
3. Add to the `resource_service.py`
4. Update backend routes to expose the new fetcher
5. Update frontend to display new resource type
