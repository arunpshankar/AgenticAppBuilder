import requests
from typing import Dict, List, Optional
from src.config.setup import get_serp_api_key
from src.config.logging import logger
import json

def search_images(query: str) -> Optional[Dict]:
    """
    Searches for images using the SerpApi Google Images API.

    Args:
        query: The image search query string.

    Returns:
        A dictionary containing the image search results, or None if an error occurs.
    """
    api_key = get_serp_api_key()
    if not api_key:
        logger.error("SERP API key not found.")
        return None
    
    url = "https://serpapi.com/search"
    params = {
        "q": query,
        "tbm": "isch",
        "api_key": api_key,
        "hl": "en",
        "gl": "us"
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()
        if data and data.get('images_results'):
           return data
        else:
            logger.warning("No image results found for the query.")
            return None

    except requests.exceptions.RequestException as e:
         logger.error(f"Error during image search request: {e}")
         return None
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON response from image search API: {e}")
        return None
    
def extract_keywords_from_image_results(image_search_results: Dict) -> List[str]:
    """
    Extract keywords from image search results.

    Args:
        image_search_results: The dictionary containing image search results.

    Returns:
        A list of keywords extracted from the image results. Returns an empty list if no keywords are found.
    """
    keywords = []
    if image_search_results and image_search_results.get('images_results'):
        for image in image_search_results['images_results']:
            if image.get('title'):
                keywords.extend(image['title'].split())
    return list(set(keywords))

def search_text_from_keywords(keywords: List[str]) -> Optional[Dict]:
    """
    Searches for web pages using the SerpApi Google Search API based on keywords.

    Args:
        keywords: A list of keywords to search for.

    Returns:
       A dictionary containing the text search results, or None if an error occurs.
    """
    api_key = get_serp_api_key()
    if not api_key:
        logger.error("SERP API key not found.")
        return None
    
    url = "https://serpapi.com/search"
    
    # Combine keywords into a search query
    query = " ".join(keywords)
    
    params = {
        "q": query,
        "api_key": api_key,
        "hl": "en",
        "gl": "us",
        "num":5
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()
        if data and data.get('organic_results'):
            return data
        else:
            logger.warning("No organic results found for text search with keywords.")
            return None

    except requests.exceptions.RequestException as e:
         logger.error(f"Error during text search request: {e}")
         return None
    except json.JSONDecodeError as e:
         logger.error(f"Error decoding JSON response from text search API: {e}")
         return None