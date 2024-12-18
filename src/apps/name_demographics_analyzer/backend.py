import requests
from typing import Dict, Optional, List
import json

def get_gender_by_name(name: str) -> Optional[Dict]:
    """
    Fetches the predicted gender for a given name using the genderize.io API.

    Args:
        name (str): The name to analyze.

    Returns:
        Optional[Dict]: A dictionary containing the predicted gender and probability, 
                        or None if the API request fails or returns an error.
    """
    url = f"https://api.genderize.io/?name={name}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        data = response.json()
        if data and data.get('gender'):
            return {
                "gender": data['gender'],
                "probability": data['probability']
            }
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error during API request: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON response: {e}")
        return None

def get_nationality_by_name(name: str) -> Optional[Dict]:
    """
    Fetches the predicted nationalities for a given name using the nationalize.io API.
    
    Args:
        name (str): The name to analyze.
    
    Returns:
        Optional[Dict]: A dictionary containing a list of predicted countries and their probabilities,
                        or None if the API request fails or returns an error.
    """
    url = f"https://api.nationalize.io/?name={name}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data and data.get('country'):
            return {
              "country": data['country']
            }
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error during API request: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON response: {e}")
        return None