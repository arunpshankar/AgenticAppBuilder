import requests
from typing import Dict, Optional
from src.config.serp import get_api_key
from src.config.logging import logger


def search_hotels(location: str, check_in_date: str, check_out_date: str) -> Optional[Dict]:
    """
    Searches for hotels using the Google Hotels API.

    Args:
        location (str): The location to search for hotels.
        check_in_date (str): The check-in date in YYYY-MM-DD format.
        check_out_date (str): The check-out date in YYYY-MM-DD format.

    Returns:
        Optional[Dict]: A dictionary containing hotel search results, or None if an error occurs.
    """
    api_key = get_api_key()
    if not api_key:
        logger.error("API key not found")
        return None

    base_url = "https://serpapi.com/search"
    params = {
        "engine": "google_hotels",
        "q": location,
        "check_in_date": check_in_date,
        "check_out_date": check_out_date,
        "api_key": api_key,
        "hl": "en",  
        "gl": "us",
        "currency": "USD"
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()

        if data and "properties" in data:
           return data
        else:
            logger.warning("No hotel data found or invalid response.")
            return None

    except requests.exceptions.RequestException as e:
        logger.error(f"Request error occurred: {e}")
        return None
    except ValueError as e:
        logger.error(f"JSON decoding error: {e}")
        return None

def search_youtube_videos(search_query: str) -> Optional[Dict]:
    """
    Searches for YouTube videos based on the search query.

    Args:
        search_query (str): The query to search for on YouTube.

    Returns:
        Optional[Dict]: A dictionary containing video search results, or None if an error occurs.
    """
    api_key = get_api_key()
    if not api_key:
        logger.error("API key not found")
        return None

    base_url = "https://serpapi.com/search"
    params = {
        "engine": "youtube",
        "search_query": search_query,
        "api_key": api_key,
        "hl": "en",
        "gl": "us"
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        if data and "video_results" in data:
            return data
        else:
            logger.warning("No youtube data found or invalid response.")
            return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Request error occurred: {e}")
        return None
    except ValueError as e:
         logger.error(f"JSON decoding error: {e}")
         return None