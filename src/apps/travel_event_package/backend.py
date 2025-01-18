import requests
from typing import Dict, Optional, Any
from src.config.setup import get_serp_api_key
from src.config.logging import logger
import json

SERP_API_KEY = get_serp_api_key()

def get_public_ip() -> Optional[str]:
    """
    Fetches the public IP address of the client.
    Returns:
        Optional[str]: The public IP address as a string, or None if an error occurs.
    """
    try:
        response = requests.get("https://api.ipify.org?format=json")
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()
        return data.get("ip")
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching public IP: {e}")
        return None
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON response: {e}")
        return None

def search_events_by_location(location_ip: str) -> Optional[Dict[str, Any]]:
    """
    Searches for events near the given location using Google Events Basic Search API.

    Args:
        location_ip (str): The IP address representing the location to search near.

    Returns:
        Optional[Dict[str, Any]]: A dictionary containing events data, or None if an error occurs.
    """
    url = "https://serpapi.com/search"
    params = {
        "engine": "google_events",
        "q": "events near me",
        "location": location_ip,
        "api_key": SERP_API_KEY,
        "hl": "en",
        "gl": "us",
        "num": 5
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        logger.error(f"Error during event search: {e}")
        return None
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON event search response: {e}")
        return None


def search_products_for_event(event_name: str) -> Optional[Dict[str, Any]]:
    """
    Searches for products related to a given event using Google Shopping Search API.

    Args:
        event_name (str): The name of the event to search related products for.

    Returns:
        Optional[Dict[str, Any]]: A dictionary containing shopping results, or None if an error occurs.
    """
    url = "https://serpapi.com/search"
    params = {
        "engine": "google_shopping",
        "q": f"products related to {event_name}",
        "api_key": SERP_API_KEY,
        "hl": "en",
        "gl": "us",
        "num": 5,
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        logger.error(f"Error during product search: {e}")
        return None
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON product search response: {e}")
        return None