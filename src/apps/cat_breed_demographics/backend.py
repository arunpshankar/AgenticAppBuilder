import requests
from typing import Dict, List, Optional
import json
from src.llm.gemini import generate_content
from src.config.client import initialize_genai_client

gemini_client = initialize_genai_client()
MODEL_ID = "gemini-2.0-flash-exp"

def process_with_gemini(prompt: str) -> str:
    """
    Process content through Gemini and format as markdown.
    
    Args:
        prompt (str): Input prompt for Gemini
        
    Returns:
        str: Formatted markdown response
    """
    response = generate_content(gemini_client, MODEL_ID, prompt)
    return response.text

def get_cat_breeds() -> Optional[List[Dict]]:
    """
    Fetches a list of cat breeds from the Cat Facts API.

    Returns:
        Optional[List[Dict]]: A list of dictionaries containing breed information, 
                           or None if the API request fails.
    """
    try:
        response = requests.get("https://catfact.ninja/breeds")
        response.raise_for_status()
        data = response.json()
        if data and "data" in data:
            return data["data"]
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching cat breeds: {e}")
        return None

def get_gender_from_name(name: str) -> Optional[Dict]:
    """
    Retrieves the predicted gender for a given name from the Genderize.io API.

    Args:
        name (str): The name to predict the gender for.

    Returns:
        Optional[Dict]: A dictionary containing gender prediction information, 
                       or None if the API request fails.
    """
    try:
        response = requests.get(f"https://api.genderize.io/?name={name}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
         print(f"Error fetching gender for name: {e}")
         return None


def get_nationality_from_name(name: str) -> Optional[Dict]:
    """
    Retrieves the predicted nationality for a given name from the Nationalize.io API.

    Args:
        name (str): The name to predict the nationality for.

    Returns:
        Optional[Dict]: A dictionary containing nationality prediction information,
                       or None if the API request fails.
    """
    try:
        response = requests.get(f"https://api.nationalize.io/?name={name}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching nationality for name: {e}")
        return None