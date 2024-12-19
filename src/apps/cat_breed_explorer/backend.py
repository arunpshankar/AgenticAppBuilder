import requests
from typing import Dict, Optional, List
import json

BASE_URL = "https://catfact.ninja"

def fetch_cat_breeds() -> Optional[Dict]:
    """
    Fetches a list of cat breeds from the API.
    
    Returns:
        Optional[Dict]: A dictionary containing the list of breeds, 
                         or None if an error occurs.
    """
    try:
        url = f"{BASE_URL}/breeds"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching cat breeds: {e}")
        return None

def fetch_cat_fact() -> Optional[Dict]:
    """
    Fetches a random cat fact from the API.
    
    Returns:
       Optional[Dict]: A dictionary containing a single cat fact,
                       or None if an error occurs.
    """
    try:
        url = f"{BASE_URL}/fact"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching cat fact: {e}")
        return None
`