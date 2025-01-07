import requests
from typing import Dict, Optional, List
from src.config.setup import get_serp_api_key
from src.config.logging import logger


def _make_api_request(url: str, params: Dict) -> Optional[Dict]:
    """
    Makes a request to the specified API endpoint with given parameters.

    Args:
        url (str): The URL to make the request to.
        params (Dict): The parameters for the API request.

    Returns:
        Optional[Dict]: The JSON response from the API, or None if an error occurred.
    """
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"API request failed: {e}")
        return None
    except ValueError as e:
        logger.error(f"JSON decoding failed: {e}")
        return None


def search_events(query: str) -> Optional[Dict]:
    """
    Searches for events using the Google Events API.

    Args:
        query (str): The search query for events.

    Returns:
        Optional[Dict]: A dictionary containing event search results, or None if an error occurred.
    """
    api_key = get_serp_api_key()
    if not api_key:
        logger.error("SERP API key not found.")
        return None
    
    url = "https://serpapi.com/search?engine=google_events"
    params = {
        "q": query,
        "api_key": api_key,
    }
    
    return _make_api_request(url, params)


def search_maps(query: str) -> Optional[Dict]:
    """
    Searches for locations using the Google Maps API.

    Args:
        query (str): The search query for the location.

    Returns:
        Optional[Dict]: A dictionary containing maps search results, or None if an error occurred.
    """
    api_key = get_serp_api_key()
    if not api_key:
        logger.error("SERP API key not found.")
        return None
        
    url = "https://serpapi.com/search?engine=google_maps"
    params = {
        "q": query,
        "api_key": api_key,
    }
    return _make_api_request(url, params)


def search_images(query: str) -> Optional[Dict]:
    """
    Searches for images using the Google Images API.

    Args:
        query (str): The search query for the images.

    Returns:
        Optional[Dict]: A dictionary containing image search results, or None if an error occurred.
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
    }
    return _make_api_request(url, params)