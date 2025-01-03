import requests
from typing import Dict, Tuple, Optional
from src.config.serp import get_api_key
from src.config.logging import logger
import json

def fetch_local_data(location: str, query: str) -> Tuple[Optional[Dict], Optional[Dict], Optional[Dict]]:
    """
    Fetches local business, event, and trend data based on the given location and query.

    Args:
        location (str): The location to search for (e.g., "New York, NY").
        query (str): The search query (e.g., "coffee shops").

    Returns:
        Tuple[Optional[Dict], Optional[Dict], Optional[Dict]]: A tuple containing local results, event results, and trends results.
    """
    api_key = get_api_key()
    if not api_key:
        logger.error("SERP API key not found.")
        return None, None, None
    
    try:
        local_results = _fetch_local_businesses(api_key, location, query)
        events_results = _fetch_local_events(api_key, location, query)
        trends_results = _fetch_trends_data(api_key, location, query)
        return local_results, events_results, trends_results
    except Exception as e:
        logger.error(f"Error fetching data: {e}")
        return None, None, None

def _fetch_local_businesses(api_key: str, location: str, query: str) -> Optional[Dict]:
    """
    Fetches local business results from the SerpApi Google Local API.

    Args:
        api_key (str): The SerpApi API key.
        location (str): The location to search for.
        query (str): The search query.

    Returns:
        Optional[Dict]: The local business results as a dictionary, or None if an error occurs.
    """
    try:
        base_url = "https://serpapi.com/search"
        params = {
            "engine": "google_local",
            "q": query,
            "location": location,
            "hl": "en",
            "gl": "us",
            "api_key": api_key,
        }
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        if data and data.get("search_metadata", {}).get("status") == "Success":
             return data
        else:
            logger.warning(f"No local results or unsuccessful response: {data}")
            return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching local businesses: {e}")
        return None

def _fetch_local_events(api_key: str, location: str, query: str) -> Optional[Dict]:
    """
    Fetches local event results from the SerpApi Google Events API.

    Args:
        api_key (str): The SerpApi API key.
        location (str): The location to search for.
        query (str): The search query.

    Returns:
        Optional[Dict]: The local event results as a dictionary, or None if an error occurs.
    """
    try:
        base_url = "https://serpapi.com/search"
        params = {
            "engine": "google_events",
            "q": f"Events in {location}",
            "hl": "en",
            "gl": "us",
            "location": location,
            "api_key": api_key,
        }
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        if data and data.get("search_metadata", {}).get("status") == "Success":
            return data
        else:
           logger.warning(f"No event results or unsuccessful response: {data}")
           return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching local events: {e}")
        return None
    
def _fetch_trends_data(api_key: str, location: str, query: str) -> Optional[Dict]:
    """
    Fetches Google Trends data for the specified query and location.

    Args:
        api_key (str): The SerpApi API key.
        location (str): The location to search for.
        query (str): The search query.

    Returns:
        Optional[Dict]: The trend analysis as a dictionary, or None if an error occurs.
    """
    try:
        base_url = "https://serpapi.com/search"
        params = {
            "engine": "google_trends",
            "q": query,
            "data_type": "GEO_MAP",
            "geo": "US",
            "region": "COUNTRY",  # Use 'COUNTRY' to get region-specific trends within the US
            "date": "today 3-m",
            "api_key": api_key,
        }
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        if data and data.get("search_metadata", {}).get("status") == "Success":
            return data
        else:
             logger.warning(f"No trend data or unsuccessful response: {data}")
             return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching trend data: {e}")
        return None