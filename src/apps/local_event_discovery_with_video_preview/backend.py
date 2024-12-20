import requests
from src.config.serp import get_api_key
from src.config.logging import logger
import json
from typing import Dict, Tuple, Optional

def fetch_events_and_videos(country_code: str, language_code: str, event_type: str) -> Tuple[Optional[Dict], Optional[Dict]]:
    """
    Fetches local events from the Google Events API and related YouTube videos.

    Args:
        country_code (str): The country code (e.g., US, GB).
        language_code (str): The language code (e.g., en, es).
        event_type (str): The type of event to search for (e.g., concert, festival).

    Returns:
        Tuple[Optional[Dict], Optional[Dict]]: A tuple containing event data and video data, or None if an error occurs.
    """
    try:
        api_key = get_api_key()
        if not api_key:
            logger.error("API key not found.")
            return None, None

        events_data = _fetch_events(api_key, country_code, language_code, event_type)
        video_data = _fetch_videos(api_key, country_code, language_code, event_type)

        return events_data, video_data

    except Exception as e:
        logger.error(f"An error occurred while fetching data: {e}")
        return None, None

def _fetch_events(api_key: str, country_code: str, language_code: str, event_type: str) -> Optional[Dict]:
    """
    Fetches event data from the Google Events API.

    Args:
        api_key (str): The API key for the SERP API.
        country_code (str): The country code.
        language_code (str): The language code.
        event_type (str): The type of event.

    Returns:
        Optional[Dict]: A dictionary containing event data, or None on error.
    """
    url = "https://serpapi.com/search"
    params = {
        "engine": "google_events",
        "q": event_type,
        "hl": language_code,
        "gl": country_code,
        "api_key": api_key,
        "htich" : "true"
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        events = data.get("events_results", [])

        if not events:
            logger.info("No events found for the specified criteria.")
            return {"events": []} # Return an empty list in a dict
        
        return {"events": events} # return event data as dictionary with "events" as key

    except requests.exceptions.RequestException as e:
        logger.error(f"Error during Google Events API request: {e}")
        return None
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON response from Google Events API: {e}")
        return None

def _fetch_videos(api_key: str, country_code: str, language_code: str, event_type: str) -> Optional[Dict]:
    """
    Fetches video data from the YouTube API.

    Args:
        api_key (str): The API key for the SERP API.
        country_code (str): The country code.
        language_code (str): The language code.
        event_type (str): The type of event.

    Returns:
        Optional[Dict]: A dictionary containing video data, or None on error.
    """
    url = "https://serpapi.com/search"
    params = {
        "engine": "youtube",
        "search_query": f"{event_type} past events",
        "gl": country_code,
        "hl": language_code,
         "api_key": api_key,
         "num": 3, # limit to 3 videos
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        videos = data.get("video_results", [])

        if not videos:
            logger.info("No videos found for the specified criteria.")
            return {"videos" : []} # Return empty videos in a dict

        return {"videos" : videos}  # return video data as dictionary with "videos" as key

    except requests.exceptions.RequestException as e:
        logger.error(f"Error during YouTube API request: {e}")
        return None
    except json.JSONDecodeError as e:
         logger.error(f"Error decoding JSON response from YouTube API: {e}")
         return None
`