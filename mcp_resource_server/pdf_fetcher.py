"""
PDF Fetcher - Fetches academic PDFs from arXiv
Uses arXiv API to find relevant research papers
"""

import requests
import xml.etree.ElementTree as ET
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)


class PDFFetcher:
    """Fetch PDFs from arXiv API"""
    
    BASE_URL = "http://export.arxiv.org/api/query"
    
    @staticmethod
    def fetch_pdfs(topic: str, max_results: int = 5) -> List[Dict]:
        """
        Fetch PDFs from arXiv for a given topic
        
        Args:
            topic: Topic to search for (e.g., "Kinematics")
            max_results: Number of papers to return
            
        Returns:
            List of PDF data with title, url, author, etc.
        """
        try:
            # Create subtopic-specific search query
            # Use a flexible search that includes the topic and related terms
            # Format: all:keyword - searches across all fields
            search_query = f'all:({topic})'
            
            params = {
                "search_query": search_query,
                "start": 0,
                "max_results": max_results,
                "sortBy": "relevance",
                "sortOrder": "descending"
            }
            
            logger.info(f"🔍 Searching arXiv for subtopic: '{topic}' (flexible search)")
            response = requests.get(PDFFetcher.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            
            # Parse XML response
            root = ET.fromstring(response.content)
            pdfs = []
            
            # arXiv namespace
            ns = {'arxiv': 'http://arxiv.org/schemas/atom'}
            
            for entry in root.findall('atom:entry', {'atom': 'http://www.w3.org/2005/Atom'}):
                try:
                    # Extract data
                    title = entry.find('{http://www.w3.org/2005/Atom}title').text.strip()
                    
                    # Get PDF link
                    pdf_url = None
                    for link in entry.findall('{http://www.w3.org/2005/Atom}link'):
                        if link.get('type') == 'application/pdf':
                            pdf_url = link.get('href')
                            break
                    
                    if not pdf_url:
                        # arXiv papers: construct PDF URL from arxiv ID
                        arxiv_id = entry.find('{http://arxiv.org/schemas/atom}id').text
                        arxiv_id = arxiv_id.split('/abs/')[-1]
                        pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
                    
                    # Get authors
                    authors = []
                    for author in entry.findall('{http://www.w3.org/2005/Atom}author'):
                        name_elem = author.find('{http://www.w3.org/2005/Atom}name')
                        if name_elem is not None:
                            authors.append(name_elem.text)
                    
                    # Get published date
                    published = entry.find('{http://www.w3.org/2005/Atom}published').text.split('T')[0]
                    
                    # Get summary
                    summary = entry.find('{http://www.w3.org/2005/Atom}summary').text.strip()
                    
                    pdf_data = {
                        "title": title,
                        "url": pdf_url,
                        "source": "arXiv",
                        "authors": authors,
                        "author_display": authors[0] if authors else "Unknown",
                        "published_date": published,
                        "description": summary[:200] + "..." if len(summary) > 200 else summary,
                        "type": "pdf",
                        "pages": "N/A",
                        "file_size": "N/A",
                        "rating": 4.5,
                        "filtered_by": topic  # Track which subtopic this was filtered for
                    }
                    
                    pdfs.append(pdf_data)
                    
                except Exception as e:
                    logger.error(f"Error parsing PDF entry: {e}")
                    continue
            
            logger.info(f"✅ Found {len(pdfs)} subtopic-specific PDFs from arXiv for '{topic}'")
            return pdfs
            
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Error fetching from arXiv: {e}")
            return []
        except Exception as e:
            logger.error(f"❌ Unexpected error in PDF fetcher: {e}")
            return []
