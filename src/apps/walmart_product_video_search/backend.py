import requests
from typing import Dict, List, Optional
from src.config.serp import get_api_key
from src.config.logging import logger
from urllib.parse import urlencode

SERP_API_KEY = get_api_key()

def search_products(query: str, min_price: float, max_price: float) -> Optional[Dict]:
    """
    Searches for products on Walmart API with price filters.
    Args:
        query (str): The product search term.
        min_price (float): The minimum price filter.
        max_price (float): The maximum price filter.
    Returns:
        Optional[Dict]: A dictionary containing product search results or None if an error occurs.
    """
    api_key = SERP_API_KEY
    if not api_key:
        logger.error("SERP API key not found.")
        return None

    base_url = "https://serpapi.com/search.json"

    params = {
        "engine": "walmart",
        "query": query,
        "api_key": api_key,
        "min_price": min_price,
        "max_price": max_price,
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        if data and 'products' in data:
             return {"products": data.get('products')}
        else:
          logger.warning(f"No products found for query: {query}")
          return {"products":[]}

    except requests.exceptions.RequestException as e:
        logger.error(f"API request error for product search: {e}")
        return None
    except Exception as e:
         logger.error(f"An error occurred during product search: {e}")
         return None

def search_youtube_videos(query: str) -> Optional[Dict]:
    """
    Searches for videos on Youtube using the SerpApi.
    Args:
        query (str): The search term.
    Returns:
        Optional[Dict]: A dictionary containing video search results or None if an error occurs.
    """
    api_key = SERP_API_KEY
    if not api_key:
        logger.error("SERP API key not found.")
        return None

    base_url = "https://serpapi.com/search.json"
    params = {
        "engine": "youtube",
        "search_query": query,
        "api_key": api_key,
        "gl": "us",
        "hl": "en"
        
    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        if data and 'video_results' in data and data['video_results']:
            videos = []
            for video in data['video_results']:
                 videos.append({
                     "title": video.get('title'),
                     "link": video.get('link')
                 })
            return {"videos":videos}

        else:
            logger.warning(f"No videos found for query: {query}")
            return {"videos":[]}
    except requests.exceptions.RequestException as e:
        logger.error(f"API request error for video search: {e}")
        return None
    except Exception as e:
         logger.error(f"An error occurred during video search: {e}")
         return None
`