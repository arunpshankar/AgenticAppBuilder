import requests
from typing import Dict, Optional
from requests import Response
import json
import time
from geopy.geocoders import Nominatim

def get_iss_location() -> Optional[Dict]:
    """
    Fetches the current ISS location using the Open Notify API.

    Returns:
        Optional[Dict]: A dictionary containing ISS location data
                         or None if an error occurs.
    """
    url = "http://api.open-notify.org/iss-now.json"
    try:
        response: Response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        data = response.json()
        if data.get('message') == 'success':
           return data['iss_position']
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching ISS location: {e}")
        return None


def get_coordinates_from_location(location: str) -> Optional[Dict]:
    """
    Converts a location string to coordinates using the Nominatim API.

    Args:
        location (str): The location string (e.g., city, address).

    Returns:
        Optional[Dict]: A dictionary containing latitude and longitude
                         or None if the location is invalid or an error occurs.
    """
    geolocator = Nominatim(user_agent="spacestation_app")
    try:
       location_data = geolocator.geocode(location, timeout=10)
       if location_data:
        return {"latitude": location_data.latitude, "longitude": location_data.longitude}
       else:
           return None
    except Exception as e:
        print(f"Error geocoding location: {e}")
        return None