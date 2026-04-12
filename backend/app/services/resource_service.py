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
from dotenv import load_dotenv  # Load environment variables
from pathlib import Path

# Load .env file from backend directory
env_path = r"D:\COMPETITIVE_EXAM\backend\.env"
if os.path.exists(env_path):
    load_dotenv(env_path)

logger = logging.getLogger(__name__)

# YouTube API Configuration - Load from environment
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "YOUR_YOUTUBE_API_KEY_HERE").strip()

# Log on startup whether API key is available
if YOUTUBE_API_KEY and YOUTUBE_API_KEY != "YOUR_YOUTUBE_API_KEY_HERE":
    logger.info(f"✅ YouTube API Key loaded successfully! Using real YouTube API")
else:
    logger.warning("❌ YouTube API Key NOT found in .env - will use mock videos")

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
                logger.warning("❌ YouTube API key not configured - using mock videos")
                return ResourceService._get_mock_videos(subtopic_title)
            
            logger.info(f"✅ Using YouTube API with key configured")
            youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
            
            # Search query: "<subtopic_title> nda basics"
            search_query = f"{subtopic_title} nda basics tutorial"
            logger.info(f"🔍 Searching YouTube for: '{search_query}'")
            
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
                video_id = item["id"]["videoId"]
                video_data = {
                    "title": item["snippet"]["title"],
                    "videoId": video_id,
                    "description": item["snippet"]["description"],
                    # Try multiple thumbnail sizes for better compatibility
                    # Order: medium > high > standard > default
                    "thumbnail": (
                        item["snippet"]["thumbnails"].get("medium", {}).get("url") or
                        item["snippet"]["thumbnails"].get("high", {}).get("url") or
                        item["snippet"]["thumbnails"].get("standard", {}).get("url") or
                        item["snippet"]["thumbnails"].get("default", {}).get("url") or
                        f"https://img.youtube.com/vi/{video_id}/mqdefault.jpg"
                    ),
                    "channelTitle": item["snippet"]["channelTitle"]
                }
                videos.append(video_data)
                logger.info(f"✅ Fetched YouTube video: {video_data['title'][:50]}...")
            
            logger.info(f"✅ Fetched {len(videos)} YouTube videos for '{subtopic_title}'")
            return videos
            
        except HttpError as e:
            logger.error(f"❌ YouTube API Error: {e}")
            return ResourceService._get_mock_videos(subtopic_title)
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
    def _get_mock_videos(subtopic_title: str = "NDA") -> List[Dict]:
        """
        Return dynamic videos specific to the subtopic using YouTube search
        When API key is not configured, provides search URLs and placeholder data
        """
        # Map subtopic keywords to search queries and popular channel videos
        video_database = {
            "linear": {
                "search": "linear equations tutorial",
                "videos": [
                    {"title": "Linear Equations Explained - Khan Academy", "videoId": "k7RM-ot2NWY", "channel": "Khan Academy"},
                    {"title": "Solving Linear Equations - Professor Leonard", "videoId": "DPuapIUJn34", "channel": "Professor Leonard"},
                    {"title": "Linear Equations for Beginners - Maths Antics", "videoId": "qVWRumyBd0E", "channel": "Maths Antics"},
                ]
            },
            "quadratic": {
                "search": "quadratic equations tutorial",
                "videos": [
                    {"title": "Quadratic Equations - Khan Academy", "videoId": "xGOEl8-ysDw", "channel": "Khan Academy"},
                    {"title": "Solving Quadratic Equations - Professor Leonard", "videoId": "qN_8ZLqYIw4", "channel": "Professor Leonard"},
                    {"title": "Quadratic Formula Explained - Maths Antics", "videoId": "b0z_EhJZRYQ", "channel": "Maths Antics"},
                ]
            },
            "calculus": {
                "search": "calculus derivatives and integration",
                "videos": [
                    {"title": "Calculus - Derivatives - Khan Academy", "videoId": "rjwelMX3SJU", "channel": "Khan Academy"},
                    {"title": "Introduction to Calculus - Professor Leonard", "videoId": "WsQQvHm4lSw", "channel": "Professor Leonard"},
                    {"title": "Calculus Explained - 3Blue1Brown", "videoId": "WUvTyaaNkzM", "channel": "3Blue1Brown"},
                ]
            },
            "trigonometry": {
                "search": "trigonometry tutorial",
                "videos": [
                    {"title": "Trigonometry - Khan Academy", "videoId": "a_S2R-XzVxE", "channel": "Khan Academy"},
                    {"title": "Trigonometric Ratios - Professor Leonard", "videoId": "rMmjwVkVa64", "channel": "Professor Leonard"},
                    {"title": "Trigonometry Basics - Maths Antics", "videoId": "RlYhlI_v4N0", "channel": "Maths Antics"},
                ]
            },
            "algebra": {
                "search": "algebra sequences and series",
                "videos": [
                    {"title": "Algebra - Khan Academy", "videoId": "F8yV8Z0QJVM", "channel": "Khan Academy"},
                    {"title": "Sequences and Series - Professor Leonard", "videoId": "F2CsCCyF9c8", "channel": "Professor Leonard"},
                    {"title": "Algebra Fundamentals - Maths Antics", "videoId": "NybHckSEQBI", "channel": "Maths Antics"},
                ]
            },
            "geometry": {
                "search": "geometry shapes and angles",
                "videos": [
                    {"title": "Geometry - Khan Academy", "videoId": "eKdp0kqLSMI", "channel": "Khan Academy"},
                    {"title": "Circle Geometry - Professor Leonard", "videoId": "ygdOI1U4gpc", "channel": "Professor Leonard"},
                    {"title": "Geometry Shapes - Maths Antics", "videoId": "7dSekZ3HFSY", "channel": "Maths Antics"},
                ]
            },
            "probability": {
                "search": "probability and statistics",
                "videos": [
                    {"title": "Probability - Khan Academy", "videoId": "m5DVvy2qsKc", "channel": "Khan Academy"},
                    {"title": "Statistics Basics - Professor Leonard", "videoId": "YAlJCEDH2uY", "channel": "Professor Leonard"},
                    {"title": "Permutations and Combinations - Maths Antics", "videoId": "PJjqxW4fKOQ", "channel": "Maths Antics"},
                ]
            },
            "english": {
                "search": "english grammar and vocabulary",
                "videos": [
                    {"title": "English Grammar - Khan Academy", "videoId": "7jRCH9T5b-A", "channel": "Khan Academy"},
                    {"title": "Vocabulary Building - TED-Ed", "videoId": "kOvQgUbVWWk", "channel": "TED-Ed"},
                    {"title": "English for Exams - English Addict with Mr. Duncan", "videoId": "qVWRumyBd0E", "channel": "English Addict"},
                ]
            },
        }
        
        # Find matching videos by subtitle keyword
        subtitle_lower = subtopic_title.lower()
        video_data = None
        
        for keyword, data in video_database.items():
            if keyword in subtitle_lower:
                video_data = data
                break
        
        # Default if no match
        if not video_data:
            from urllib.parse import quote
            search_query = quote(f"{subtopic_title} tutorial")
            video_data = {
                "search": subtitle_lower,
                "videos": [
                    {"title": f"{subtopic_title} - Learn with us", "videoId": "RlYhlI_v4N0", "channel": "Education Channel"},
                    {"title": f"Master {subtopic_title}", "videoId": "qVWRumyBd0E", "channel": "NDA Academy"},
                    {"title": f"{subtopic_title} Complete Guide", "videoId": "WUvTyaaNkzM", "channel": "Study Hall"},
                ]
            }
        
        # Format videos with YouTube thumbnail URLs
        result = []
        for video in video_data.get("videos", []):
            result.append({
                "title": video["title"],
                "videoId": video["videoId"],
                "description": f"Learn about {subtopic_title}. This video is from {video['channel']} - a trusted educational source",
                "thumbnail": f"https://img.youtube.com/vi/{video['videoId']}/mqdefault.jpg",
                "channelTitle": video["channel"]
            })
        
        return result


# Singleton instance
resource_service = ResourceService()
