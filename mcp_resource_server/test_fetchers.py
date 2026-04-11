#!/usr/bin/env python3
"""
Test script for MCP Resource Fetchers
Tests PDF and Article fetching functionality
"""

import sys
import os

# Add MCP server to path
sys.path.insert(0, os.path.dirname(__file__))

from pdf_fetcher import PDFFetcher
from article_fetcher import ArticleFetcher


def test_pdf_fetcher():
    """Test PDF fetcher with a sample topic"""
    print("\n" + "="*60)
    print("Testing PDF Fetcher")
    print("="*60)
    
    topic = "Kinematics"
    print(f"\n🔍 Searching for PDFs on: {topic}")
    
    try:
        pdfs = PDFFetcher.fetch_pdfs(topic, max_results=3)
        
        if pdfs:
            print(f"✅ Found {len(pdfs)} PDFs\n")
            for i, pdf in enumerate(pdfs, 1):
                print(f"\n  PDF {i}:")
                print(f"    Title: {pdf['title'][:60]}...")
                print(f"    Source: {pdf['source']}")
                print(f"    Author: {pdf['author_display']}")
                print(f"    URL: {pdf['url']}")
                print(f"    Date: {pdf['published_date']}")
                print(f"    Description: {pdf['description'][:100]}...")
        else:
            print("❌ No PDFs found")
            
    except Exception as e:
        print(f"❌ Error: {e}")


def test_article_fetcher():
    """Test Article fetcher with a sample topic"""
    print("\n\n" + "="*60)
    print("Testing Article Fetcher")
    print("="*60)
    
    topic = "Thermodynamics"
    print(f"\n🔍 Searching for articles on: {topic}")
    
    try:
        articles = ArticleFetcher.fetch_articles(topic, max_results=5)
        
        if articles:
            print(f"✅ Found {len(articles)} articles\n")
            for i, article in enumerate(articles, 1):
                print(f"\n  Article {i}:")
                print(f"    Title: {article['title'][:60]}...")
                print(f"    Source: {article['source']}")
                print(f"    Author: {article['author_display']}")
                print(f"    URL: {article['url']}")
                print(f"    Date: {article['published_date']}")
                print(f"    Reading Time: {article.get('reading_time', 'N/A')}")
                print(f"    Description: {article['description'][:100]}...")
        else:
            print("❌ No articles found")
            
    except Exception as e:
        print(f"❌ Error: {e}")


def test_resource_service():
    """Test resource service from backend"""
    print("\n\n" + "="*60)
    print("Testing Resource Service Integration")
    print("="*60)
    
    try:
        # Try to import from backend
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../backend'))
        from app.services.resource_service import resource_service
        
        topic = "Physics"
        print(f"\n🔍 Testing backend integration with: {topic}")
        
        # Test fetching all resources
        print("\n📚 Fetching all resources...")
        resources = resource_service.get_all_resources(topic)
        
        print(f"\n✅ Backend Integration Successful!")
        print(f"   Videos: {len(resources.get('videos', []))} found")
        print(f"   PDFs: {len(resources.get('pdfs', []))} found")
        print(f"   Articles: {len(resources.get('articles', []))} found")
        
    except ImportError:
        print("⚠️  Backend not available in this environment (expected for standalone test)")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    print("\n🚀 MCP Resource Fetchers Test Suite")
    
    # Test PDF fetcher
    test_pdf_fetcher()
    
    # Test Article fetcher
    test_article_fetcher()
    
    # Test resource service integration
    test_resource_service()
    
    print("\n" + "="*60)
    print("✅ Tests Complete!")
    print("="*60 + "\n")
