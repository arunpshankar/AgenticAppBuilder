import requests
from typing import Dict, List, Tuple
from src.config.serp import get_api_key
from src.llm.gemini_text import generate_content
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

def fetch_kids_content(search_term: str) -> Tuple[List[Dict], List[Dict]]:
    """
    Fetches kid-friendly video search results and top app charts.

    Args:
        search_term: The term to search for videos.

    Returns:
        A tuple containing lists of video and app dictionaries.
    """
    api_key = get_api_key()
    video_results = fetch_safe_search_videos(api_key, search_term)
    app_results = fetch_top_child_apps(api_key)
    return video_results, app_results

def fetch_safe_search_videos(api_key: str, search_term: str) -> List[Dict]:
    """
    Fetches video results from Google Videos API with safe search.

    Args:
        api_key: The Serp API key.
        search_term: The term to search for.

    Returns:
        A list of dictionaries containing video information.
    """
    url = "https://serpapi.com/search"
    params = {
        "engine": "google_videos",
        "q": search_term,
        "api_key": api_key,
        "safe": "active"  # Activate Safe Search
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()

        video_results = []
        if 'videos_results' in data and data['videos_results']:
          for item in data['videos_results']:
            video_results.append({
              "title": item.get('title', 'No Title'),
              "description": item.get('description', 'No description'),
              "url": item.get('link', 'No URL')
            })
        return video_results
    except requests.exceptions.RequestException as e:
        print(f"Error fetching videos: {e}")
        return []

def fetch_top_child_apps(api_key: str) -> List[Dict]:
    """
    Fetches top app chart data from Google Play Store API.

    Args:
        api_key: The Serp API key.

    Returns:
        A list of dictionaries containing app information.
    """
    url = "https://serpapi.com/search"
    params = {
        "engine": "google_play_store_top_charts",
        "category": "FAMILY",
        "api_key": api_key
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        app_results = []
        if 'top_charts' in data and data['top_charts']:
          for item in data['top_charts']:
            app_results.append({
                "title": item.get('title', 'No Title'),
                "category": item.get('category', 'No Category'),
                "url": item.get('link', 'No URL')
            })
        return app_results
    except requests.exceptions.RequestException as e:
        print(f"Error fetching apps: {e}")
        return []