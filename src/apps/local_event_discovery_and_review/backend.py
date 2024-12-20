import requests
from typing import Dict, Optional
from src.config.serp import get_api_key
from src.config.logging import logger

def search_yelp(location: str, search_term: str) -> Dict:
    """
    Searches Yelp for businesses based on location and search term.

    Args:
        location (str): The location to search in.
        search_term (str): The search term (e.g., "pizza", "restaurants").

    Returns:
        Dict: A dictionary containing Yelp search results or an error message.
    """
    api_key = get_api_key()
    if not api_key:
        logger.error("SERP API key not found.")
        return {"error": "SERP API key not found"}
    
    base_url = "https://serpapi.com/search"
    params = {
        "engine": "yelp",
        "find_loc": location,
        "find_desc": search_term,
        "api_key": api_key,
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        
        if data and "search_metadata" in data and data["search_metadata"].get("status") == "Success":
            logger.info(f"Successfully fetched Yelp results for {search_term} in {location}.")
            return data
        else:
             logger.warning(f"No Yelp results found for {search_term} in {location} or invalid response.")
             return {"error": "No Yelp results found or invalid response"}


    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching Yelp results: {e}")
        return {"error": f"Request error: {e}"}
    except Exception as e:
         logger.error(f"An unexpected error occurred while fetching Yelp data: {e}")
         return {"error": f"An unexpected error occurred: {e}"}


def search_youtube(search_query: str) -> Dict:
    """
    Searches YouTube for videos based on the provided search query.

    Args:
        search_query (str): The query to search for on YouTube.

    Returns:
        Dict: A dictionary containing YouTube search results or an error message.
    """
    api_key = get_api_key()
    if not api_key:
         logger.error("SERP API key not found.")
         return {"error": "SERP API key not found"}

    base_url = "https://serpapi.com/search"
    params = {
        "engine": "youtube",
        "search_query": search_query,
        "api_key": api_key,
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        if data and "search_metadata" in data and data["search_metadata"].get("status") == "Success":
            logger.info(f"Successfully fetched YouTube results for {search_query}.")
            return data
        else:
              logger.warning(f"No Youtube results found for {search_query} or invalid response.")
              return {"error": "No YouTube results found or invalid response"}

    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching YouTube results: {e}")
        return {"error": f"Request error: {e}"}
    except Exception as e:
         logger.error(f"An unexpected error occurred while fetching YouTube data: {e}")
         return {"error": f"An unexpected error occurred: {e}"}