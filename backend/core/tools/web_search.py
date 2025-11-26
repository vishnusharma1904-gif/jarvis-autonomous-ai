"""
Web Search Tool for Real-time Information
Uses DuckDuckGo for internet access
"""

from duckduckgo_search import DDGS
from typing import List, Dict
from datetime import datetime
import requests
from bs4 import BeautifulSoup

def get_current_time() -> str:
    """Get current date and time"""
    return datetime.now().strftime("%A, %B %d, %Y at %I:%M %p")

def search_web(query: str, max_results: int = 5) -> str:
    """
    Search the web using DuckDuckGo
    
    Args:
        query: Search query
        max_results: Maximum number of results
    
    Returns:
        Formatted search results
    """
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
        
        if not results:
            return "No search results found."
        
        formatted_results = f"🌐 Web Search Results for: '{query}'\n\n"
        
        for i, result in enumerate(results, 1):
            title = result.get('title', 'No title')
            snippet = result.get('body', 'No description')
            url = result.get('href', '')
            
            formatted_results += f"{i}. **{title}**\n"
            formatted_results += f"   {snippet}\n"
            formatted_results += f"   Source: {url}\n\n"
        
        return formatted_results.strip()
    
    except Exception as e:
        return f"Search failed: {str(e)}"

def scrape_webpage(url: str, max_length: int = 2000) -> str:
    """
    Scrape content from a webpage
    
    Args:
        url: URL to scrape
        max_length: Maximum content length
    
    Returns:
        Extracted text content
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()
        
        # Get text
        text = soup.get_text()
        
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        # Limit length
        if len(text) > max_length:
            text = text[:max_length] + "..."
        
        return text
    
    except Exception as e:
        return f"Failed to scrape webpage: {str(e)}"

def search_news(query: str, max_results: int = 5) -> str:
    """
    Search for news articles
    
    Args:
        query: Search query
        max_results: Maximum number of results
    
    Returns:
        Formatted news results
    """
    try:
        with DDGS() as ddgs:
            results = list(ddgs.news(query, max_results=max_results))
        
        if not results:
            return "No news results found."
        
        formatted_results = f"📰 News Results for: '{query}'\n\n"
        
        for i, result in enumerate(results, 1):
            title = result.get('title', 'No title')
            snippet = result.get('body', 'No description')
            url = result.get('url', '')
            date = result.get('date', 'Unknown date')
            
            formatted_results += f"{i}. **{title}** ({date})\n"
            formatted_results += f"   {snippet}\n"
            formatted_results += f"   Source: {url}\n\n"
        
        return formatted_results.strip()
    
    except Exception as e:
        return f"News search failed: {str(e)}"
