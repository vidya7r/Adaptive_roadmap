#!/usr/bin/env python3
"""
MCP Resource Server
Provides tools to fetch PDFs and Articles for study materials
"""

import asyncio
import json
from typing import Any
from mcp.server import Server
from mcp.types import Tool, TextContent
import logging

from pdf_fetcher import PDFFetcher
from article_fetcher import ArticleFetcher

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize MCP Server
server = Server("resource-fetcher")


# Tools Definition
@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools"""
    return [
        Tool(
            name="fetch_pdfs",
            description="Fetch academic PDFs from arXiv for a given topic",
            inputSchema={
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": "Topic to search for (e.g., 'Kinematics', 'Thermodynamics')"
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Maximum number of PDFs to fetch (default: 5)",
                        "default": 5
                    }
                },
                "required": ["topic"]
            }
        ),
        Tool(
            name="fetch_articles",
            description="Fetch educational articles from multiple sources (Dev.to, Hackernoon, GeeksforGeeks)",
            inputSchema={
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": "Topic to search for (e.g., 'Kinematics', 'Thermodynamics')"
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Maximum number of articles to fetch (default: 5)",
                        "default": 5
                    }
                },
                "required": ["topic"]
            }
        ),
        Tool(
            name="fetch_all_resources",
            description="Fetch both PDFs and articles for a given topic",
            inputSchema={
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": "Topic to search for"
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Maximum number of resources to fetch per type",
                        "default": 5
                    }
                },
                "required": ["topic"]
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> Any:
    """Execute a tool"""
    
    if name == "fetch_pdfs":
        topic = arguments.get("topic")
        max_results = arguments.get("max_results", 5)
        
        logger.info(f"Fetching PDFs for topic: {topic}")
        pdfs = PDFFetcher.fetch_pdfs(topic, max_results)
        
        return {
            "status": "success",
            "topic": topic,
            "type": "pdfs",
            "total": len(pdfs),
            "data": pdfs
        }
    
    elif name == "fetch_articles":
        topic = arguments.get("topic")
        max_results = arguments.get("max_results", 5)
        
        logger.info(f"Fetching articles for topic: {topic}")
        articles = ArticleFetcher.fetch_articles(topic, max_results)
        
        return {
            "status": "success",
            "topic": topic,
            "type": "articles",
            "total": len(articles),
            "data": articles
        }
    
    elif name == "fetch_all_resources":
        topic = arguments.get("topic")
        max_results = arguments.get("max_results", 5)
        
        logger.info(f"Fetching all resources for topic: {topic}")
        
        pdfs = PDFFetcher.fetch_pdfs(topic, max_results)
        articles = ArticleFetcher.fetch_articles(topic, max_results)
        
        return {
            "status": "success",
            "topic": topic,
            "pdfs": {
                "type": "pdfs",
                "total": len(pdfs),
                "data": pdfs
            },
            "articles": {
                "type": "articles",
                "total": len(articles),
                "data": articles
            }
        }
    
    else:
        raise ValueError(f"Unknown tool: {name}")


def main():
    """Run the MCP server"""
    server.run()


if __name__ == "__main__":
    main()
