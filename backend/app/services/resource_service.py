"""
Resource Service - Handles dynamic resource fetching
Fetches YouTube videos, PDFs, and articles on-the-fly based on subtopic titles
Now integrates with MCP Resource Server for PDF and Article fetching
"""

import os
import sys
from typing import List, Dict, Optional, TYPE_CHECKING
from googleapiclient.discovery import build  # type: ignore
from googleapiclient.errors import HttpError  # type: ignore
import logging
import requests

logger = logging.getLogger(__name__)

# YouTube API Configuration
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "YOUR_YOUTUBE_API_KEY_HERE")

# Type checking imports (for IDE support only)
if TYPE_CHECKING:
    from mcp_resource_server.pdf_fetcher import PDFFetcher  # type: ignore
    from mcp_resource_server.article_fetcher import ArticleFetcher  # type: ignore
else:
    PDFFetcher = None
    ArticleFetcher = None

# Add MCP server path to imports - Runtime import
try:
    # Get the project root directory
    # resource_service.py is at: backend/app/services/
    # We need to go up 3 levels to get to project root
    file_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(file_dir)))
    mcp_server_path = os.path.join(project_root, 'mcp_resource_server')
    
    # Only try to import if the path exists
    if os.path.exists(mcp_server_path):
        sys.path.insert(0, mcp_server_path)
        from pdf_fetcher import PDFFetcher  # type: ignore  # noqa
        from article_fetcher import ArticleFetcher  # type: ignore  # noqa
        logger.info(f"✅ MCP Resource Fetchers loaded from: {mcp_server_path}")
    else:
        logger.warning(f"⚠️ MCP Resource Server path not found: {mcp_server_path}")
except (ImportError, Exception) as e:
    logger.warning(f"⚠️ Could not load MCP Resource Fetchers: {e}")
    PDFFetcher = None
    ArticleFetcher = None


class ResourceService:
    """Service for fetching dynamic resources (YouTube videos, PDFs)"""

    @staticmethod
    def fetch_youtube_videos(subtopic_title: str, max_results: int = 3) -> List[Dict]:
        """
        Fetch YouTube videos related to a subtopic
        
        Args:
            subtopic_title: Title of the subtopic (e.g., "Kinematics")
            max_results: Number of videos to return (default: 3)
            
        Returns:
            List of video objects with 'title' and 'videoId'
            
        Example:
            >>> videos = ResourceService.fetch_youtube_videos("Kinematics")
            >>> # Returns: [{"title": "...", "videoId": "..."}, ...]
        """
        try:
            if YOUTUBE_API_KEY == "YOUR_YOUTUBE_API_KEY_HERE":
                logger.warning("YouTube API key not configured")
                return ResourceService._get_mock_videos()
            
            youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
            
            # Search query: "<subtopic_title> nda basics"
            search_query = f"{subtopic_title} nda basics tutorial"
            
            request = youtube.search().list(
                q=search_query,
                type="video",
                part="snippet",
                maxResults=max_results,
                relevanceLanguage="en",
                order="relevance"
            )
            
            response = request.execute()
            
            videos = []
            for item in response.get("items", []):
                video_data = {
                    "title": item["snippet"]["title"],
                    "videoId": item["id"]["videoId"],
                    "description": item["snippet"]["description"],
                    "thumbnail": item["snippet"]["thumbnails"]["default"]["url"],
                    "channelTitle": item["snippet"]["channelTitle"]
                }
                videos.append(video_data)
            
            logger.info(f"✅ Fetched {len(videos)} YouTube videos for '{subtopic_title}'")
            return videos
            
        except HttpError as e:
            logger.error(f"❌ YouTube API Error: {e}")
            return ResourceService._get_mock_videos()
        except Exception as e:
            logger.error(f"❌ Error fetching YouTube videos: {e}")
            return []

    @staticmethod
    def generate_pdf_search_url(subtopic_title: str) -> Dict[str, str]:
        """
        DEPRECATED: Use fetch_pdfs() instead
        Generate Google Search URL for PDF resources
        
        Args:
            subtopic_title: Title of the subtopic (e.g., "Kinematics")
            
        Returns:
            Dictionary with 'pdf_url' and 'search_query'
            
        Example:
            >>> result = ResourceService.generate_pdf_search_url("Kinematics")
            >>> # Returns: {"pdf_url": "https://www.google.com/search?q=...", "search_query": "..."}
        """
        try:
            # Format search query
            search_query = f"{subtopic_title} nda notes pdf"
            
            # URL encode the search query
            from urllib.parse import quote
            encoded_query = quote(search_query)
            
            # Generate Google Search URL
            pdf_url = f"https://www.google.com/search?q={encoded_query}+filetype:pdf"
            
            logger.info(f"✅ Generated PDF search URL for '{subtopic_title}'")
            
            return {
                "pdf_url": pdf_url,
                "search_query": search_query,
                "type": "pdf"
            }
            
        except Exception as e:
            logger.error(f"❌ Error generating PDF URL: {e}")
            return {
                "pdf_url": "https://www.google.com/search?q=nda+notes+pdf",
                "search_query": "nda notes pdf",
                "error": str(e)
            }

    @staticmethod
    def fetch_pdfs(subtopic_title: str, max_results: int = 5) -> List[Dict]:
        """
        Fetch actual PDF resources from arXiv using MCP Resource Fetcher
        
        Args:
            subtopic_title: Title of the subtopic (e.g., "Kinematics")
            max_results: Number of PDFs to return
            
        Returns:
            List of PDF data with title, url, author, description, etc.
        """
        try:
            if PDFFetcher is None:
                logger.warning("PDFFetcher not available, returning fallback")
                return ResourceService._get_fallback_pdfs(subtopic_title)
            
            logger.info(f"🔍 Fetching PDFs for '{subtopic_title}'")
            pdfs = PDFFetcher.fetch_pdfs(subtopic_title, max_results)
            
            logger.info(f"✅ Successfully fetched {len(pdfs)} PDFs for '{subtopic_title}'")
            return pdfs
            
        except Exception as e:
            logger.error(f"❌ Error fetching PDFs: {e}")
            return ResourceService._get_fallback_pdfs(subtopic_title)

    @staticmethod
    def generate_article_search_url(subtopic_title: str) -> Dict[str, str]:
        """
        DEPRECATED: Use fetch_articles() instead
        Generate Google Search URL for article/study materials
        
        Args:
            subtopic_title: Title of the subtopic
            
        Returns:
            Dictionary with 'article_url' and 'search_query'
        """
        try:
            search_query = f"{subtopic_title} nda study material"
            
            from urllib.parse import quote
            encoded_query = quote(search_query)
            
            article_url = f"https://www.google.com/search?q={encoded_query}"
            
            logger.info(f"✅ Generated article search URL for '{subtopic_title}'")
            
            return {
                "article_url": article_url,
                "search_query": search_query,
                "type": "article"
            }
            
        except Exception as e:
            logger.error(f"❌ Error generating article URL: {e}")
            return {
                "article_url": "https://www.google.com/search?q=nda+study+material",
                "search_query": "nda study material",
                "error": str(e)
            }

    @staticmethod
    def fetch_articles(subtopic_title: str, max_results: int = 5) -> List[Dict]:
        """
        Fetch actual articles from multiple sources using MCP Article Fetcher
        
        Args:
            subtopic_title: Title of the subtopic (e.g., "Kinematics")
            max_results: Number of articles to return
            
        Returns:
            List of article data with title, url, author, description, etc.
        """
        try:
            if ArticleFetcher is None:
                logger.warning("ArticleFetcher not available, returning fallback")
                return ResourceService._get_fallback_articles(subtopic_title)
            
            logger.info(f"🔍 Fetching articles for '{subtopic_title}'")
            articles = ArticleFetcher.fetch_articles(subtopic_title, max_results)
            
            logger.info(f"✅ Successfully fetched {len(articles)} articles for '{subtopic_title}'")
            return articles
            
        except Exception as e:
            logger.error(f"❌ Error fetching articles: {e}")
            return ResourceService._get_fallback_articles(subtopic_title)

    @staticmethod
    def get_all_resources(subtopic_title: str) -> Dict:
        """
        Get all dynamic resources for a subtopic (videos, PDFs, and articles)
        
        Args:
            subtopic_title: Title of the subtopic
            
        Returns:
            Dictionary containing videos, PDFs, and articles
        """
        try:
            return {
                "subtopic": subtopic_title,
                "videos": ResourceService.fetch_youtube_videos(subtopic_title),
                "pdfs": ResourceService.fetch_pdfs(subtopic_title),
                "articles": ResourceService.fetch_articles(subtopic_title)
            }
        except Exception as e:
            logger.error(f"❌ Error getting all resources: {e}")
            return {
                "subtopic": subtopic_title,
                "videos": [],
                "pdfs": [],
                "articles": [],
                "error": str(e)
            }

    @staticmethod
    def _get_fallback_pdfs(topic: str) -> List[Dict]:
        """Return fallback/sample PDFs when fetcher is not available"""
        return [
            {
                "title": f"Complete Guide to {topic}",
                "url": f"https://arxiv.org/search/?query={topic}&searchtype=all",
                "source": "arXiv",
                "author_display": "Academic Database",
                "published_date": "2024",
                "description": f"Comprehensive research on {topic} from arXiv",
                "type": "pdf",
                "pages": "50+",
                "file_size": "2.5 MB",
                "rating": 4.5
            }
        ]
    
    @staticmethod
    def _get_fallback_articles(topic: str) -> List[Dict]:
        """Return fallback/sample articles when fetcher is not available"""
        return [
            {
                "title": f"Understanding {topic}",
                "url": f"https://www.geeksforgeeks.org/?s={topic}",
                "source": "GeeksforGeeks",
                "author_display": "GeeksforGeeks Team",
                "published_date": "2024",
                "description": f"Tutorial and guide on {topic} for competitive exams",
                "type": "article",
                "reading_time": "10 min read",
                "category": "Tutorial",
                "views": 5000
            }
        ]

    @staticmethod
    def _get_mock_videos() -> List[Dict]:
        """
        Return mock videos when API key is not configured
        Used for testing/demo purposes
        """
        return [
            {
                "title": "NDA Basics - Introduction",
                "videoId": "dQw4w9WgXcQ",
                "description": "Mock video - Configure YouTube API key to see real videos",
                "thumbnail": "https://via.placeholder.com/120x90",
                "channelTitle": "Demo Channel"
            },
            {
                "title": "Complete NDA Tutorial",
                "videoId": "dQw4w9WgXcQ",
                "description": "Mock video - Configure YouTube API key to see real videos",
                "thumbnail": "https://via.placeholder.com/120x90",
                "channelTitle": "Demo Channel"
            },
            {
                "title": "Quick NDA Review",
                "videoId": "dQw4w9WgXcQ",
                "description": "Mock video - Configure YouTube API key to see real videos",
                "thumbnail": "https://via.placeholder.com/120x90",
                "channelTitle": "Demo Channel"
            }
        ]


# Singleton instance
resource_service = ResourceService()
