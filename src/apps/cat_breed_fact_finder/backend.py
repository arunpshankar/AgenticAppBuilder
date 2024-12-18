import requests
from typing import Dict, List, Optional

CAT_BREEDS_API_URL = "https://catfact.ninja/breeds"
CAT_FACT_API_URL = "https://catfact.ninja/fact"

def get_cat_breeds() -> Optional[List[Dict]]:
    """
    Retrieves a list of cat breeds from the API.

    Returns:
        Optional[List[Dict]]: A list of dictionaries containing cat breed data, or None on failure.
    """
    try:
        response = requests.get(CAT_BREEDS_API_URL)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()
        return data.get("data", [])  # Ensure we return an empty list if "data" is not present
    except requests.exceptions.RequestException as e:
        print(f"Error fetching cat breeds: {e}")
        return None

def get_cat_fact() -> Optional[Dict]:
    """
    Retrieves a random cat fact from the API.

    Returns:
        Optional[Dict]: A dictionary containing cat fact data, or None on failure.
    """
    try:
        response = requests.get(CAT_FACT_API_URL)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching cat fact: {e}")
        return None