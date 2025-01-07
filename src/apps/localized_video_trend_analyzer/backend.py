import requests
from typing import Dict, List, Tuple, Optional
from src.config.setup import get_serp_api_key
from src.config.logging import logger

def fetch_trending_regions(query: str, geo: str, region: str) -> Optional[Dict]:
    """
    Fetches trending regions data for a given query using the Google Trends API.

    Args:
        query (str): The search query.
        geo (str): The geographic location.
        region (str): The region type (e.g., CITY, STATE).

    Returns:
        Optional[Dict]: A dictionary containing the interest by region data, or None if an error occurs.
    """
    api_key = get_serp_api_key()
    if not api_key:
        logger.error("SERP API key not found.")
        return None

    url = "https://serpapi.com/search"
    params = {
        "engine": "google_trends",
        "q": query,
        "data_type": "GEO_MAP_0",
        "geo": geo,
        "region": region,
        "api_key": api_key
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        
        if data.get("search_metadata", {}).get("status") == "Success":
            return data.get("interest_by_region")
        else:
            logger.error(f"Google Trends API error: {data.get('error')}")
            return None

    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching trending regions data: {e}")
        return None
    except Exception as e:
        logger.error(f"An unexpected error occurred while fetching trends data: {e}")
        return None


def fetch_videos(query: str, hl: str = "en", gl: str = "us") -> Optional[List[Dict]]:
    """
    Fetches video search results for a given query using the Google Videos API.

    Args:
        query (str): The search query.
        hl (str): The language parameter (default is 'en').
        gl (str): The country parameter (default is 'us').

    Returns:
        Optional[List[Dict]]: A list of dictionaries containing video results, or None if an error occurs.
    """
    api_key = get_serp_api_key()
    if not api_key:
        logger.error("SERP API key not found.")
        return None

    url = "https://serpapi.com/search"
    params = {
        "engine": "google_videos",
        "q": query,
        "hl": hl,
        "gl": gl,
        "api_key": api_key
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if data.get("search_metadata", {}).get("status") == "Success":
           return data.get("video_results")
        else:
           logger.error(f"Google Video API error: {data.get('error')}")
           return None

    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching video search results: {e}")
        return None
    except Exception as e:
        logger.error(f"An unexpected error occurred while fetching videos: {e}")
        return None

def fetch_trending_videos(query: str, geo: str, region: str) -> Tuple[Optional[Dict], Optional[List[Dict]]]:
    """
    Fetches trending regions data and related videos for a given query.

    Args:
        query (str): The search query.
        geo (str): The geographic location code.
        region (str): The region type (e.g., CITY, STATE).

    Returns:
        Tuple[Optional[Dict], Optional[List[Dict]]]: A tuple containing:
            - A dictionary of trending regions data (or None if an error occurs).
            - A list of video search results (or None if an error occurs).
    """
    trends_data = fetch_trending_regions(query, geo, region)
    video_results = fetch_videos(query)
    return trends_data, video_results