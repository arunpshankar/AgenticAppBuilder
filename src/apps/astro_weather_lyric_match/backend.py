import requests
from typing import Dict, List, Optional
from src.config.serp import get_api_key
from src.config.logging import logger
import json

def get_astro_weather(latitude: float, longitude: float) -> Optional[Dict]:
    """
    Fetches astronomical weather data from the 7timer! API.

    Args:
        latitude (float): The latitude of the location.
        longitude (float): The longitude of the location.

    Returns:
        Optional[Dict]: A dictionary containing the weather data, or None if an error occurred.
    """
    base_url = "http://www.7timer.info/bin/api.pl"
    params = {
        "lon": longitude,
        "lat": latitude,
        "product": "astro",
        "output": "json"
    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching weather data: {e}")
        return None
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON response: {e}")
        return None


def search_lyrics_by_theme(theme: str) -> Optional[List[Dict]]:
    """
    Searches for song lyrics that match a given theme using the lyrics.ovh API.
    This is a simplified example and may need to be adapted for complex themes.

    Args:
        theme (str): The theme to search for in song lyrics.

    Returns:
        Optional[List[Dict]]: A list of dictionaries containing song information and lyrics, or None if an error occurs.
    """
    base_url = "https://api.lyrics.ovh/v1/"
    search_terms = theme.lower().split() # Split the theme text into individual words for search
    lyrics_results = []

    if not search_terms:
        logger.warning("No search terms provided for lyrics search.")
        return None

    try:
      # Simplified logic - searching for the first word from theme (best attempt)
      first_term = search_terms[0]
      artist = None
      title = None
      
      # In real scenario, a more complex search and parsing logic should be implemented
      response = requests.get(f"https://api.lyrics.ovh/suggest/{first_term}")
      response.raise_for_status()
      suggested_data = response.json()

      if suggested_data and suggested_data.get('data'):
          first_suggestion = suggested_data['data'][0] # take first suggestion for now

          artist = first_suggestion.get('artist', {}).get('name')
          title = first_suggestion.get('title')
          if artist and title:

            url = f"{base_url}{artist}/{title}"
            response = requests.get(url)
            response.raise_for_status()
            song_data = response.json()

            if song_data and 'lyrics' in song_data:
              lyrics_results.append({'artist': artist, 'title': title, 'lyrics': song_data.get('lyrics')})
            else:
                logger.warning(f"No lyrics found for artist: {artist}, title: {title}")
                return None

      return lyrics_results

    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching lyrics: {e}")
        return None
    except json.JSONDecodeError as e:
      logger.error(f"Error decoding lyrics response: {e}")
      return None
    except Exception as e:
      logger.error(f"An unexpected error occured during lyrics search: {e}")
      return None