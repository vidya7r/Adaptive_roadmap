"""
MCP Resource Server Package
Provides PDF and Article fetchers for study materials
"""

try:
    from .pdf_fetcher import PDFFetcher  # type: ignore
    from .article_fetcher import ArticleFetcher  # type: ignore
    __all__ = ['PDFFetcher', 'ArticleFetcher']
except ImportError:
    # Fallback if imports fail
    PDFFetcher = None
    ArticleFetcher = None
    __all__ = []

