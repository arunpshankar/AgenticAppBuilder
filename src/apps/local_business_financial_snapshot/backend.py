import requests
from typing import Dict, Optional, Tuple
from src.config.serp import get_api_key
from src.config.logging import logger
import json

def search_business(business_name: str, location: Optional[str] = None) -> Tuple[Optional[Dict], Optional[Dict]]:
    """
    Searches for local business information and financial data using SerpApi.

    Args:
        business_name (str): The name of the business to search for.
        location (Optional[str]): The location of the business (optional).

    Returns:
        Tuple[Optional[Dict], Optional[Dict]]: A tuple containing local business data and financial data as dictionaries.
                                              Returns (None, None) if an error occurs.
    """
    api_key = get_api_key()
    if not api_key:
        logger.error("SERP API key not found.")
        return None, None

    local_business_data = _search_local_business(business_name, location, api_key)
    financial_data = _search_financial_data(business_name, api_key)
    
    return local_business_data, financial_data

def _search_local_business(business_name: str, location: Optional[str], api_key: str) -> Optional[Dict]:
    """
    Searches for local business information using the SerpApi Google Local API.

    Args:
        business_name (str): The name of the business to search for.
        location (Optional[str]): The location of the business (optional).
        api_key (str): The SerpApi API key.

    Returns:
        Optional[Dict]: A dictionary containing the local business search results, or None if an error occurs.
    """
    base_url = "https://serpapi.com/search"
    params = {
        "engine": "google_local",
        "q": business_name,
        "api_key": api_key,
        "hl": "en",
        "gl": "us"
    }
    if location:
        params["location"] = location
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        data = response.json()

        if data.get("error"):
            logger.error(f"SERP API Error for local business search: {data.get('error')}")
            return None
        
        if data.get("local_results"):
             return data
        else:
             logger.info("No local results found for query")
             return {}

    except requests.exceptions.RequestException as e:
        logger.error(f"Error during local business search: {e}")
        return None
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON for local business search: {e}")
        return None


def _search_financial_data(business_name: str, api_key: str) -> Optional[Dict]:
    """
    Searches for financial data using the SerpApi Google Finance API.

    Args:
        business_name (str): The name of the business to search for.
        api_key (str): The SerpApi API key.

    Returns:
        Optional[Dict]: A dictionary containing the financial search results, or None if an error occurs.
    """
    base_url = "https://serpapi.com/search"
    params = {
        "engine": "google_finance",
        "q": business_name,
        "api_key": api_key,
        "hl": "en",
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        data = response.json()

        if data.get("error"):
            logger.error(f"SERP API Error for financial data search: {data.get('error')}")
            return None

        if data.get("summary"):
            return data
        else:
            logger.info("No financial data found for query")
            return {}
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error during financial data search: {e}")
        return None
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON for financial search: {e}")
        return None