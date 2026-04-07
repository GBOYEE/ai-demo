"""
Web content scraper using requests and BeautifulSoup.
"""

import requests
from bs4 import BeautifulSoup
from typing import Optional


def scrape_url(url: str, max_length: int = 10000) -> str:
    """
    Scrape the main text content from a URL.

    Args:
        url: The URL to scrape
        max_length: Maximum characters to return (truncates if longer)

    Returns:
        Extracted text content

    Raises:
        requests.RequestException: If the request fails
        ValueError: If the URL is invalid or content cannot be extracted
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        raise requests.RequestException(f"Failed to fetch URL: {e}")

    soup = BeautifulSoup(response.content, 'html.parser')

    # Remove script and style elements
    for script in soup(["script", "style", "nav", "header", "footer", "aside"]):
        script.decompose()

    # Get text from common content containers
    content_tags = soup.find_all(['p', 'article', 'main', 'div'])
    text_parts = []

    for tag in content_tags:
        # Skip very short or likely navigation items
        if tag.get('class'):
            class_str = ' '.join(tag.get('class')).lower()
            if any(x in class_str for x in ['nav', 'menu', 'footer', 'header', 'sidebar']):
                continue

        text = tag.get_text(separator=' ', strip=True)
        if text and len(text) > 50:  # Only include substantial text
            text_parts.append(text)

    full_text = ' '.join(text_parts)

    # Clean up whitespace
    import re
    full_text = re.sub(r'\s+', ' ', full_text).strip()

    if not full_text:
        raise ValueError("No content could be extracted from the URL")

    # Truncate if too long
    if len(full_text) > max_length:
        full_text = full_text[:max_length] + "... [truncated]"

    return full_text
