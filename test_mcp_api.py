#!/usr/bin/env python3
"""
Test script for API endpoints with MCP Resource Fetchers
Tests authentication and resource fetching
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def print_header(title):
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)

def test_login():
    """Test login endpoint"""
    print_header("Step 1: Login")
    
    login_url = f"{BASE_URL}/auth/login"
    print(f"\n📝 POST {login_url}")
    
    # Login credentials
    payload = {
        "email": "test@example.com",
        "password": "password"
    }
    
    try:
        response = requests.post(login_url, json=payload, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            token = data.get("access_token")
            print(f"✅ Login successful!")
            print(f"   Token: {token[:50]}...")
            return token
        else:
            print(f"❌ Login failed")
            print(f"   Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_get_pdfs(token):
    """Test PDF fetching endpoint"""
    print_header("Step 2: Fetch PDFs")
    
    subtopic_id = 1
    url = f"{BASE_URL}/api/resources/pdf/{subtopic_id}"
    headers = {"Authorization": f"Bearer {token}"}
    
    print(f"\n📖 GET {url}")
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            pdfs = data.get("pdfs", [])
            
            print(f"✅ PDFs fetched successfully!")
            print(f"   Total: {len(pdfs)} PDFs")
            
            for i, pdf in enumerate(pdfs[:2], 1):  # Show first 2
                print(f"\n   PDF {i}:")
                print(f"     Title: {pdf.get('title', 'N/A')[:60]}")
                print(f"     Source: {pdf.get('source', 'N/A')}")
                print(f"     Author: {pdf.get('author_display', 'N/A')}")
                print(f"     URL: {pdf.get('url', 'N/A')[:50]}...")
            
            return True
        else:
            print(f"❌ Failed to fetch PDFs")
            print(f"   Response: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_get_articles(token):
    """Test Article fetching endpoint"""
    print_header("Step 3: Fetch Articles")
    
    subtopic_id = 1
    url = f"{BASE_URL}/api/resources/article/{subtopic_id}"
    headers = {"Authorization": f"Bearer {token}"}
    
    print(f"\n📚 GET {url}")
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            articles = data.get("articles", [])
            
            print(f"✅ Articles fetched successfully!")
            print(f"   Total: {len(articles)} Articles")
            
            for i, article in enumerate(articles[:2], 1):  # Show first 2
                print(f"\n   Article {i}:")
                print(f"     Title: {article.get('title', 'N/A')[:60]}")
                print(f"     Source: {article.get('source', 'N/A')}")
                print(f"     Author: {article.get('author_display', 'N/A')}")
                print(f"     URL: {article.get('url', 'N/A')[:50]}...")
            
            return True
        else:
            print(f"❌ Failed to fetch articles")
            print(f"   Response: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_get_all_resources(token):
    """Test combined resources endpoint"""
    print_header("Step 4: Fetch All Resources")
    
    subtopic_id = 1
    url = f"{BASE_URL}/api/resources/all/{subtopic_id}"
    headers = {"Authorization": f"Bearer {token}"}
    
    print(f"\n🎬 GET {url}")
    
    try:
        response = requests.get(url, headers=headers, timeout=20)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            videos = data.get("videos", [])
            pdfs = data.get("pdfs", [])
            articles = data.get("articles", [])
            
            print(f"✅ All resources fetched successfully!")
            print(f"\n   Summary:")
            print(f"     🎥 Videos: {len(videos)}")
            print(f"     📄 PDFs: {len(pdfs)}")
            print(f"     📖 Articles: {len(articles)}")
            print(f"     Total: {len(videos) + len(pdfs) + len(articles)}")
            
            return True
        else:
            print(f"❌ Failed to fetch all resources")
            print(f"   Response: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("\n" + "🚀 "*35)
    print("  MCP Resource Fetchers - API Test Suite")
    print("🚀 "*35)
    
    # Step 1: Login
    token = test_login()
    if not token:
        print("\n❌ Cannot proceed without authentication token")
        return
    
    # Step 2: Test PDF endpoint
    time.sleep(1)
    pdf_success = test_get_pdfs(token)
    
    # Step 3: Test Article endpoint
    time.sleep(1)
    article_success = test_get_articles(token)
    
    # Step 4: Test combined endpoint
    time.sleep(1)
    all_success = test_get_all_resources(token)
    
    # Summary
    print_header("Test Summary")
    print(f"\n✅ PDFs: {'PASS' if pdf_success else 'FAIL'}")
    print(f"✅ Articles: {'PASS' if article_success else 'FAIL'}")
    print(f"✅ All Resources: {'PASS' if all_success else 'FAIL'}")
    
    if pdf_success and article_success and all_success:
        print("\n" + "✅ "*35)
        print("  ALL TESTS PASSED!")
        print("✅ "*35 + "\n")
    else:
        print("\n" + "⚠️  "*35)
        print("  SOME TESTS FAILED - CHECK OUTPUT ABOVE")
        print("⚠️  "*35 + "\n")

if __name__ == "__main__":
    main()
