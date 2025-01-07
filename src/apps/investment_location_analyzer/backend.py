import requests
from typing import Dict, Tuple, Optional, List
from src.config.setup import get_api_key
from src.config.logging import logger
import json


def fetch_local_data(query: str, location: str) -> Optional[List[Dict]]:
    """
    Fetches local business results using the Google Local Basic Search API.

    Args:
        query (str): The search query (e.g., 'coffee shops').
        location (str): The location to search in (e.g., 'New York, NY').

    Returns:
        Optional[List[Dict]]: A list of dictionaries containing local business results, or None if an error occurs.
    """
    api_key = get_api_key()
    if not api_key:
         logger.error("API key is not set.")
         return None
    
    base_url = "https://serpapi.com/search"
    params = {
        "engine": "google_local",
        "q": query,
        "location": location,
        "api_key": api_key,
        "hl": "en",
        "gl": "us"
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        if data.get("error"):
             logger.error(f"API error: {data.get('error')}")
             return None
        local_results = data.get("local_results", [])
        if local_results:
            return local_results
        else:
             logger.info("No local results found")
             return []
            
    except requests.exceptions.RequestException as e:
        logger.error(f"Request exception: {e}")
        return None
    except json.JSONDecodeError as e:
         logger.error(f"JSON decoding error: {e}")
         return None

def fetch_finance_data(query: str) -> Optional[Dict]:
    """
    Fetches financial data using the Google Finance Basic Search API.

    Args:
        query (str): The search query (e.g., 'NASDAQ:GOOGL').

    Returns:
         Optional[Dict]: A dictionary containing financial data, or None if an error occurs.
    """
    api_key = get_api_key()
    if not api_key:
         logger.error("API key is not set.")
         return None

    base_url = "https://serpapi.com/search"
    params = {
        "engine": "google_finance",
        "q": query,
        "api_key": api_key,
        "hl": "en"
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()

        if data.get("error"):
             logger.error(f"API error: {data.get('error')}")
             return None
        summary = data.get("summary",{})
        news_results = data.get("news_results", [])
        if summary or news_results:
              return {"summary": summary, "news_results": news_results}
        else:
              logger.info("No finance results found.")
              return {}
    except requests.exceptions.RequestException as e:
        logger.error(f"Request exception: {e}")
        return None
    except json.JSONDecodeError as e:
         logger.error(f"JSON decoding error: {e}")
         return None

def fetch_data(location: str, industry: str) -> Tuple[Optional[List[Dict]], Optional[Dict]]:
    """
    Fetches both local and financial data based on the provided location and industry.

    Args:
        location (str): The location for local search.
        industry (str): The industry for both local and finance searches.

    Returns:
        Tuple[Optional[List[Dict]], Optional[Dict]]: A tuple containing local and finance results.
    """
    local_query = industry
    finance_query = f"stock of {industry}"
    local_results = fetch_local_data(local_query, location)
    finance_results = fetch_finance_data(finance_query)
    return local_results, finance_results