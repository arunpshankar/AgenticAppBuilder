import requests
from typing import Dict, Optional, Any
from src.config.serp import get_api_key
from src.config.logging import logger
import json


def search_images(query: str, num_results: int = 5) -> Optional[Dict]:
    """
    Searches for images using the Google Images API.

    Args:
        query (str): The search query.
        num_results (int): Number of results to return.

    Returns:
        Optional[Dict]: A dictionary containing the image search results, or None on error.
    """
    api_key = get_api_key()
    if not api_key:
        logger.error("SERP API key not found.")
        return None
    
    url = "https://serpapi.com/search"
    params = {
        "engine": "google_images",
        "q": query,
        "ijn": 0,
        "api_key": api_key,
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        data = response.json()
        logger.info(f"Successfully retrieved image search results for query: {query}")
        if 'images_results' in data:
            return data
        else:
             logger.warning(f"No image results found for query: {query}")
             return {}

    except requests.exceptions.RequestException as e:
        logger.error(f"Error during image search request for query '{query}': {e}")
        return None
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON response for image search for query '{query}': {e}")
        return None
    

def search_walmart(query: str, page: int = 1) -> Optional[Dict]:
    """
    Searches for products on Walmart using the Walmart API.

    Args:
        query (str): The search query.
        page (int): The page number for results.

    Returns:
        Optional[Dict]: A dictionary containing Walmart product results, or None on error.
    """
    api_key = get_api_key()
    if not api_key:
        logger.error("SERP API key not found.")
        return None
    
    url = "https://serpapi.com/search"
    params = {
        "engine": "walmart",
        "query": query,
        "page": page,
        "api_key": api_key,
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        data = response.json()
        logger.info(f"Successfully retrieved Walmart search results for query: {query}, page: {page}")
        if 'organic_results' in data:
           return data
        else:
            logger.warning(f"No product results found for query: {query}, page: {page}")
            return {}
            
    except requests.exceptions.RequestException as e:
        logger.error(f"Error during Walmart search request for query '{query}', page: {page}: {e}")
        return None
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON response for Walmart search for query '{query}', page: {page}: {e}")
        return None