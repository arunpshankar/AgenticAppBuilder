import requests
import json
from typing import Dict, List, Optional

def get_location_data() -> Optional[Dict]:
    """
    Retrieves location data based on the user's public IP address.

    Returns:
        Optional[Dict]: A dictionary containing location data (city, region, country) or None if an error occurs.
    """
    try:
        ip_response = requests.get("https://api.ipify.org?format=json")
        ip_response.raise_for_status()
        ip_data = ip_response.json()
        ip_address = ip_data["ip"]
        
        geo_response = requests.get(f"http://ip-api.com/json/{ip_address}")
        geo_response.raise_for_status()
        geo_data = geo_response.json()
        
        if geo_data["status"] == "success":
          return {
                "city": geo_data.get("city"),
                "region": geo_data.get("regionName"),
                "country": geo_data.get("country")
            }
        else:
            return None

    except requests.exceptions.RequestException as e:
         print(f"Error during location retrieval: {e}")
         return None
    except json.JSONDecodeError as e:
        print(f"Error decoding location data: {e}")
        return None


def get_art_data(location_data: Dict) -> Optional[Dict]:
    """
    Retrieves art data from the Art Institute of Chicago API based on location.

    Args:
        location_data (Dict): A dictionary containing location data.

    Returns:
        Optional[Dict]: A dictionary containing art data or None if an error occurs.
    """
    try:
        params = {
             "limit": 5,
            "fields": "id,title,artist_display,date_display,description,image_id"
        }
        
        art_response = requests.get("https://api.artic.edu/api/v1/artworks", params=params)
        art_response.raise_for_status()
        art_data = art_response.json()
        return art_data
    except requests.exceptions.RequestException as e:
         print(f"Error during art data retrieval: {e}")
         return None
    except json.JSONDecodeError as e:
        print(f"Error decoding art data: {e}")
        return None