#!/usr/bin/env python3
"""Quick test for arXiv PDF fetcher"""
from mcp_resource_server.pdf_fetcher import PDFFetcher

print("\n" + "="*60)
print("Testing arXiv PDF Fetcher with Multiple Topics")
print("="*60)

topics = ['Motion', 'Newton', 'Mechanics', 'Kinematics Physics']

for topic in topics:
    print(f"\n🔍 Searching: {topic}")
    try:
        pdfs = PDFFetcher.fetch_pdfs(topic, max_results=2)
        print(f"✅ Found {len(pdfs)} PDFs")
        for i, pdf in enumerate(pdfs, 1):
            print(f"   {i}. {pdf['title'][:70]}")
            print(f"      URL: {pdf['url'][:80]}")
    except Exception as e:
        print(f"❌ Error: {e}")

print("\n" + "="*60)
