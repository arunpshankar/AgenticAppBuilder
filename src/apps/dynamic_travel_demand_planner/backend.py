import requests
from typing import Dict, List, Optional
from src.config.serp import get_api_key
from src.config.logging import logger
import json


def get_google_trends_data(region: str) -> Optional[Dict]:
    """
    Fetches Google Trends data for a given region.

    Args:
        region: The region to query trends for.

    Returns:
        A dictionary containing trends data, or None if an error occurs.
    """
    api_key = get_api_key()
    if not api_key:
        logger.error("SERP API key not found.")
        return None

    url = "https://serpapi.com/trends-compared-breakdown-by-region"
    params = {
        "api_key": api_key,
        "region": region
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()
        if data and "data" in data:
            return data["data"]
        else:
             logger.warning(f"No 'data' key found in API response for region: {region}. Response: {data}")
             return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching trends data: {e}")
        return None
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON response: {e}")
        return None

def search_flights(origin: str, destination: str, airlines: Optional[List[str]] = None) -> Optional[List[Dict]]:
    """
    Searches for flights between two airports using the SERP API.

    Args:
        origin: The origin airport code (e.g., JFK).
        destination: The destination airport code (e.g., LAX).
        airlines: An optional list of airline codes to filter by (e.g., ['UA', 'AA']).

    Returns:
        A list of flight dictionaries, or None if an error occurs.
    """
    api_key = get_api_key()
    if not api_key:
        logger.error("SERP API key not found.")
        return None

    url = "https://serpapi.com/search"
    params = {
        "api_key": api_key,
        "engine": "google_flights",
        "from": origin,
        "to": destination,
    }
    if airlines:
         params["airlines"] = ','.join(airlines)
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
       
        if data and "flights" in data:
              return data["flights"]
        else:
            logger.warning(f"No 'flights' key found in API response for origin: {origin}, destination: {destination}. Response: {data}")
            return None

    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching flight data: {e}")
        return None
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON response: {e}")
        return None
```