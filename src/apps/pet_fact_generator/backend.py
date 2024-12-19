import requests
from typing import Dict, Optional
import random

def get_cat_fact() -> Optional[Dict]:
    """
    Retrieves a random cat fact from the catfact.ninja API.

    Returns:
        Optional[Dict]: A dictionary containing the cat fact or None if there is an error.
    """
    try:
        response = requests.get("https://catfact.ninja/facts?limit=1")
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        data = response.json()
        if data and "data" in data and data["data"]:
            return data["data"][0]
        else:
           return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching cat fact: {e}")
        return None

def get_dog_image() -> Optional[Dict]:
    """
    Retrieves a random dog image URL from the dog.ceo API.

    Returns:
        Optional[Dict]: A dictionary containing the dog image URL or None if there is an error.
    """
    try:
        response = requests.get("https://dog.ceo/api/breeds/image/random")
        response.raise_for_status()
        data = response.json()
        if data and data.get("status") == "success":
            return data
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching dog image: {e}")
        return None