"""
Resource Service - Handles dynamic resource fetching
Fetches YouTube videos and PDF resources on-the-fly based on subtopic titles
"""

import os
from typing import List, Dict, Optional
from googleapiclient.discovery import build  # type: ignore
from googleapiclient.errors import HttpError  # type: ignore
import logging

logger = logging.getLogger(__name__)

# YouTube API Configuration
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "YOUR_YOUTUBE_API_KEY_HERE")


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
    def generate_article_search_url(subtopic_title: str) -> Dict[str, str]:
        """
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
    def get_all_resources(subtopic_title: str) -> Dict:
        """
        Get all dynamic resources for a subtopic
        
        Args:
            subtopic_title: Title of the subtopic
            
        Returns:
            Dictionary containing videos, PDFs, and articles
        """
        try:
            return {
                "subtopic": subtopic_title,
                "videos": ResourceService.fetch_youtube_videos(subtopic_title),
                "pdf": ResourceService.generate_pdf_search_url(subtopic_title),
                "article": ResourceService.generate_article_search_url(subtopic_title)
            }
        except Exception as e:
            logger.error(f"❌ Error getting all resources: {e}")
            return {
                "subtopic": subtopic_title,
                "videos": [],
                "pdf": None,
                "article": None,
                "error": str(e)
            }

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
