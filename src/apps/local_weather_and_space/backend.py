import requests
import json
from typing import Dict, Tuple
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

def get_weather_data(latitude: float, longitude: float) -> Dict:
    """
    Fetches weather data from the 7timer! API.

    Args:
        latitude (float): Latitude of the location.
        longitude (float): Longitude of the location.

    Returns:
        Dict: Weather data as a dictionary, or an empty dictionary on failure.
    """
    base_url = "http://www.7timer.info/bin/api.pl"
    params = {
        "lon": longitude,
        "lat": latitude,
        "product": "astro",
        "output": "json"
    }
    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return {}

def get_iss_location() -> Dict:
    """
    Fetches current ISS location data from the Open Notify API.

    Returns:
        Dict: ISS location data as a dictionary, or an empty dictionary on failure.
    """
    base_url = "http://api.open-notify.org/iss-now.json"
    try:
        response = requests.get(base_url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching ISS location: {e}")
        return {}

def get_weather_and_iss_data(latitude: float, longitude: float) -> Tuple[Dict, Dict]:
    """
    Retrieves weather data and ISS location data.

    Args:
        latitude (float): Latitude of the location.
        longitude (float): Longitude of the location.

    Returns:
        Tuple[Dict, Dict]: A tuple containing weather data and ISS data.
    """
    weather_data = get_weather_data(latitude, longitude)
    iss_data = get_iss_location()
    return weather_data, iss_data