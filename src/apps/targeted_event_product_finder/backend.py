import requests
from typing import Dict, Optional, List
from src.config.setup import get_serp_api_key
from src.config.logging import logger
import json

def _safe_get(data: dict, keys: List[str], default=None):
    """
    Safely retrieves a nested value from a dictionary using a list of keys.

    Args:
        data: The dictionary to retrieve from.
        keys: A list of keys to navigate through.
        default: The default value to return if the key is not found.

    Returns:
        The value found or the default value.
    """
    current = data
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default
    return current

def search_events(location: str, query: str) -> Optional[Dict]:
    """
    Searches for events based on location and query using the Google Events API.

    Args:
        location: The location to search for events.
        query: The query for the type of event.

    Returns:
        A dictionary containing event information or None if an error occurs.
    """
    api_key = get_serp_api_key()
    if not api_key:
        logger.error("SERP API key not found.")
        return None

    url = "https://serpapi.com/search"
    params = {
        "engine": "google_events",
        "q": query,
        "location": location,
        "api_key": api_key,
        "hl": "en" #Force English
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        events = _safe_get(data, ['events_results'], [])
        
        formatted_events = []
        for event in events:
            formatted_event = {
                "title": _safe_get(event, ['title'], 'N/A'),
                "description": _safe_get(event, ['description'], 'N/A'),
                "date": _safe_get(event, ['date', 'when'], 'N/A'),
                 "address": _safe_get(event, ['address'], 'N/A'),

            }
            formatted_events.append(formatted_event)

        return {"events": formatted_events}


    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching event data: {e}")
        return None
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON response: {e}")
        return None


def search_products_for_event(events: List[Dict], event_query: str) -> Optional[Dict]:
    """
    Searches for products related to the given event, filtering the shopping query with event context.

    Args:
        events: A list of dictionaries containing event information.
        event_query: The query term related to the event.

    Returns:
        A dictionary containing product information or None if an error occurs.
    """
    api_key = get_serp_api_key()
    if not api_key:
        logger.error("SERP API key not found.")
        return None
    
    combined_query = f"{event_query}"

    if events and events[0] and events[0].get('title'):
        combined_query += f" {events[0].get('title')}"
    
    url = "https://serpapi.com/search"
    params = {
        "engine": "google_shopping",
        "q": combined_query,
        "api_key": api_key,
        "hl": "en",
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()


        shopping_results = _safe_get(data, ['shopping_results'], [])
        formatted_results = []

        for result in shopping_results:
            formatted_product = {
               "title": _safe_get(result, ['title'], 'N/A'),
               "price": _safe_get(result, ['price'], 'N/A'),
               "link": _safe_get(result, ['product_link'], 'N/A'),
               "description": _safe_get(result, ['description'], 'N/A'),
               "thumbnail": _safe_get(result, ['thumbnail'], 'N/A')

            }
            formatted_results.append(formatted_product)


        return {"shopping_results": formatted_results}



    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching product data: {e}")
        return None
    except json.JSONDecodeError as e:
         logger.error(f"Error decoding JSON response: {e}")
         return None