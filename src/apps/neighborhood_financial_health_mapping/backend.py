import requests
from typing import Dict, Tuple, Optional
from src.config.setup import get_serp_api_key
from src.config.logging import logger
import json

def fetch_local_businesses(query: str, location: str) -> Optional[Dict]:
    """
    Fetches local business data using the Google Local Basic Search API.

    Args:
        query (str): The search query (e.g., "coffee shops").
        location (str): The location to search in (e.g., "New York, NY").

    Returns:
        Optional[Dict]: A dictionary containing local business data, or None if an error occurs.
    """
    api_key = get_serp_api_key()
    base_url = "https://serpapi.com/search"
    params = {
        "engine": "google_local",
        "q": query,
        "location": location,
        "api_key": api_key,
    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        if data and "local_results" in data:
             return data
        else:
            logger.warning(f"No local business results found for {query} in {location}")
            return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching local business data: {e}")
        return None
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON response for local business data: {e}")
        return None

def fetch_finance_data(query: str) -> Optional[Dict]:
    """
    Fetches finance data using the Google Finance Basic Search API.

    Args:
        query (str): The search query (e.g., "NASDAQ:GOOGL").

    Returns:
        Optional[Dict]: A dictionary containing finance data, or None if an error occurs.
    """
    api_key = get_serp_api_key()
    base_url = "https://serpapi.com/search"
    params = {
        "engine": "google_finance",
        "q": query,
        "api_key": api_key,
    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        if data and "summary" in data or "news_results" in data:
           return data
        else:
            logger.warning(f"No finance data found for {query}")
            return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching finance data: {e}")
        return None
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON response for finance data: {e}")
        return None


def fetch_neighborhood_data(query: str, location: str) -> Tuple[Optional[Dict], Optional[Dict]]:
    """
    Fetches both local business and finance data for a given location and query.

    Args:
        query (str): The search query (e.g., "coffee shops").
        location (str): The location to search in (e.g., "New York, NY").

    Returns:
        Tuple[Optional[Dict], Optional[Dict]]: A tuple containing local business data and finance data, both of which can be None if an error occurs.
    """
    local_business_data = fetch_local_businesses(query, location)
    finance_query = f"financial data for businesses in {location} like {query}" #query modification to improve results
    finance_data = fetch_finance_data(finance_query)
    return local_business_data, finance_data