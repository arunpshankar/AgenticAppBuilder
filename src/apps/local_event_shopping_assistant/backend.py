import requests
from typing import Dict, Optional, Tuple
from src.config.setup import get_serp_api_key
from src.config.logging import logger
import json
from urllib.parse import urlencode


def _fetch_public_ip() -> Optional[str]:
    """Fetches the user's public IP address using ipify."""
    try:
        response = requests.get("https://api.ipify.org?format=json", timeout=5)
        response.raise_for_status()
        return response.json().get("ip")
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching IP address: {e}")
        return None


def _get_location_from_ip(ip_address: str) -> Optional[str]:
    """Retrieves the location based on the given IP address."""
    try:
        response = requests.get(f"http://ip-api.com/json/{ip_address}", timeout=5)
        response.raise_for_status()
        data = response.json()
        if data.get("status") == "success":
            return f"{data.get('city')}, {data.get('regionName')}"
        else:
            logger.error(f"Failed to get location from IP: {data.get('message')}")
            return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Error getting location from IP: {e}")
        return None

def _search_events(location: str, api_key: str) -> Optional[Dict]:
    """Searches for local events using the Google Events API."""
    try:
        params = {
            "engine": "google_events",
            "q": "events near " + location,
            "api_key": api_key,
            "hl": "en",
            "gl": "us"
        }

        url = "https://serpapi.com/search?" + urlencode(params)
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching events: {e}")
        return None


def _search_products(event_name: str, location: str, api_key: str) -> Optional[Dict]:
     """Searches for products related to a specific event using Google Shopping API."""
     try:
        params = {
            "engine": "google_shopping",
            "q": event_name + " near " + location,
            "api_key": api_key,
             "hl": "en",
            "gl": "us"
        }
        url = "https://serpapi.com/search?" + urlencode(params)
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
     except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching products: {e}")
        return None


def fetch_events_and_products(location_input: str) -> Tuple[Optional[Dict], Optional[Dict]]:
    """
    Fetches local events and related products using the SERP API.

    Args:
        location_input: The user-provided location or None to use IP-based location.

    Returns:
         A tuple containing events data and shopping data, both as dictionaries,
         or (None, None) if errors occur.
    """
    api_key = get_serp_api_key()
    if not api_key:
        logger.error("SERP API key not found.")
        return None, None

    if not location_input:
        ip_address = _fetch_public_ip()
        if ip_address:
            location = _get_location_from_ip(ip_address)
            if not location:
               logger.error("Could not fetch location based on IP address.")
               return None, None
        else:
           logger.error("Failed to fetch public IP.")
           return None, None
    else:
       location = location_input


    events_data = _search_events(location, api_key)
    if not events_data or not events_data.get('events_results'):
        logger.warning("No events found for the location provided")
        return {}, {}  # Return empty dictionaries if events are not found

    first_event = events_data['events_results'][0].get('title') if events_data.get('events_results') else None

    if first_event:
            shopping_data = _search_products(first_event,location, api_key)
            if not shopping_data:
                 logger.warning("No shopping results found for the events.")
                 return events_data, {} # Return event data even if no shopping results
            return events_data, shopping_data
    else:
            return events_data, {}