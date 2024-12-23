import requests
from typing import Dict, Optional, List
from src.config.serp import get_api_key
from src.config.logging import logger
import json
import time

def get_travel_info(mode: str) -> Optional[Dict]:
    """
    Fetches real-time status data for a given mode of transport in London.

    Args:
        mode (str): The mode of transport (e.g., 'tube', 'bus', 'dlr').

    Returns:
        Optional[Dict]: A dictionary containing the API response data or None if an error occurs.
    """
    base_url = "https://api.tfl.gov.uk"
    endpoint = f"/Line/Mode/{mode}/Status"

    try:
        response = requests.get(f"{base_url}{endpoint}")
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching travel data for mode {mode}: {e}")
        return None

def search_lyrics(artist: str, title: str) -> Optional[str]:
    """
    Fetches lyrics for a given song by artist and title.

    Args:
        artist (str): The name of the artist.
        title (str): The title of the song.

    Returns:
        Optional[str]: The lyrics of the song or None if not found.
    """
    base_url = "https://api.lyrics.ovh"
    endpoint = f"/v1/{artist}/{title}"
    try:
        response = requests.get(f"{base_url}{endpoint}")
        response.raise_for_status()
        data = response.json()
        return data.get("lyrics", None)
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching lyrics for {artist} - {title}: {e}")
        return None

def calculate_travel_time(start_location: str, destination: str) -> Optional[int]:
    """
    Estimates travel time between two locations using a dummy calculation.

    Args:
      start_location (str): starting location
      destination (str): destination

    Returns:
        Optional[int]: the estimated travel time or None in case of an error
    """
    time.sleep(1)
    return 25 # Dummy value

if __name__ == "__main__":
    # Example usage
    tube_data = get_travel_info("tube")
    if tube_data:
      logger.info("Tube data fetched successfully")
    else:
      logger.error("Tube data fetch failed")
    
    artist = "Coldplay"
    title = "Yellow"
    lyrics = search_lyrics(artist, title)
    if lyrics:
        logger.info(f"Lyrics for {artist} - {title} fetched successfully.")
    else:
      logger.error(f"Lyrics for {artist} - {title} fetch failed.")