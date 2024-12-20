import requests
from typing import Dict, Optional, Any
from src.config.serp import get_api_key
from src.config.logging import logger
import json

def get_iss_location() -> Optional[Dict[str, float]]:
    """
    Fetches the current location of the International Space Station.

    Returns:
        Optional[Dict[str, float]]: A dictionary containing the latitude and longitude of the ISS,
                                     or None if an error occurs.
    """
    try:
        response = requests.get("http://api.open-notify.org/iss-now.json")
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        data = response.json()

        if data["message"] == "success":
            iss_position = data["iss_position"]
            latitude = float(iss_position["latitude"])
            longitude = float(iss_position["longitude"])
            return {"latitude": latitude, "longitude": longitude}
        else:
             logger.error(f"Failed to fetch ISS location. API message: {data.get('message')}")
             return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching ISS location: {e}")
        return None
    except (ValueError, KeyError, TypeError) as e:
        logger.error(f"Error parsing ISS location data: {e}")
        return None


def search_events_near_location(latitude: float, longitude: float) -> Optional[Dict[str, Any]]:
    """
    Searches for events near a given location using the Google Events Basic Search API.

    Args:
        latitude (float): The latitude of the location.
        longitude (float): The longitude of the location.

    Returns:
         Optional[Dict[str, Any]]: A dictionary containing the event data from the API
                or None if an error occurred.
    """
    api_key = get_api_key()
    if not api_key:
        logger.error("SERP API key not found.")
        return {"error":"SERP API key not found."}
    
    url = "https://serpapi.com/search.json"
    params = {
        "engine": "google_events",
        "q": "events near me",
        "lat": latitude,
        "lng": longitude,
        "api_key": api_key,
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status() # Raise an exception for bad status codes
        data = response.json()
        if data.get("events_results"):
            return {"events": data["events_results"]}
        else:
             logger.info(f"No events found near given location")
             return {"events": []}
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching events data: {e}")
        return {"error":f"Error fetching events data: {e}"}
    except (ValueError, KeyError, TypeError) as e:
        logger.error(f"Error parsing events data: {e}")
        return {"error": f"Error parsing events data: {e}"}