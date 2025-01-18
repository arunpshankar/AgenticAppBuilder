import requests
from typing import Dict, Optional
from src.config.setup import get_serp_api_key
from src.config.logging import logger
import json


def _make_api_request(url: str, params: Dict) -> Optional[Dict]:
    """
    Makes a request to the specified URL with the given parameters.

    Args:
        url (str): The URL to make the request to.
        params (Dict): The parameters to include in the request.

    Returns:
        Optional[Dict]: The JSON response as a dictionary, or None if an error occurs.
    """
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"API request failed: {e}")
        return None
    except json.JSONDecodeError as e:
      logger.error(f"JSON decode error: {e}")
      return None

def search_google_shopping(query: str) -> Optional[Dict]:
    """
    Searches for a product on Google Shopping using the SerpApi.

    Args:
        query (str): The search query (product name).

    Returns:
         Optional[Dict]: The JSON response as a dictionary, or None if an error occurs.
    """
    api_key = get_serp_api_key()
    if not api_key:
        logger.error("SERP API key not found.")
        return None

    url = "https://serpapi.com/search"
    params = {
        "engine": "google_shopping",
        "q": query,
        "api_key": api_key,
        "hl": "en",
        "gl": "us"
    }
    return _make_api_request(url, params)

def search_walmart(query: str) -> Optional[Dict]:
    """
    Searches for a product on Walmart using the SerpApi.

    Args:
        query (str): The search query (product name).

    Returns:
        Optional[Dict]: The JSON response as a dictionary, or None if an error occurs.
    """
    api_key = get_serp_api_key()
    if not api_key:
        logger.error("SERP API key not found.")
        return None

    url = "https://serpapi.com/search"
    params = {
        "engine": "walmart",
        "query": query,
        "api_key": api_key,
        "page": 1,
    }
    return _make_api_request(url, params)


def search_google(query: str) -> Optional[Dict]:
    """
    Searches for a product on Google using the SerpApi.

    Args:
      query (str): The search query (product name).

    Returns:
       Optional[Dict]: The JSON response as a dictionary, or None if an error occurs.
    """
    api_key = get_serp_api_key()
    if not api_key:
        logger.error("SERP API key not found.")
        return None
    
    url = "https://serpapi.com/search"
    params = {
        "engine": "google",
        "q": query,
        "api_key": api_key,
        "hl": "en",
        "gl": "us"
    }
    return _make_api_request(url, params)

def search_google_local(query: str) -> Optional[Dict]:
    """
    Searches for a local product on Google using the SerpApi.

    Args:
      query (str): The search query (product name).

    Returns:
        Optional[Dict]: The JSON response as a dictionary, or None if an error occurs.
    """
    api_key = get_serp_api_key()
    if not api_key:
      logger.error("SERP API key not found.")
      return None
    
    url = "https://serpapi.com/search"
    params = {
        "engine": "google_local",
        "q": query,
        "api_key": api_key,
        "hl": "en",
        "gl": "us",
        "location": "New York, NY"
    }
    return _make_api_request(url,params)