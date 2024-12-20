import requests
from typing import Dict, List, Tuple, Optional
from src.config.serp import get_api_key
import json

def fetch_walmart_data(query: str) -> Optional[List[Dict]]:
    """
    Fetches product data from Walmart using the Serp API.
    
    Args:
        query (str): The search query.
        
    Returns:
        Optional[List[Dict]]: A list of dictionaries containing product information, or None on failure.
    """
    api_key = get_api_key()
    url = "https://serpapi.com/search"
    params = {
        "engine": "walmart",
        "query": query,
        "api_key": api_key,
    }
    
    try:
      response = requests.get(url, params=params)
      response.raise_for_status()
      data = response.json()
      
      if data.get("organic_results"):
            results = []
            for item in data["organic_results"]:
                image_url = item.get("image")
                results.append({
                    "title": item.get("title"),
                    "price": item.get("price"),
                    "link": item.get("link"),
                    "image": image_url
                  })
            return results
      else:
            return None
    except requests.exceptions.RequestException as e:
      print(f"Error fetching Walmart data: {e}")
      return None

def fetch_google_images(query: str) -> Optional[List[Dict]]:
    """
    Fetches image results from Google Images using the Serp API.
    
    Args:
        query (str): The search query.
        
    Returns:
        Optional[List[Dict]]: A list of dictionaries containing image information, or None on failure.
    """
    api_key = get_api_key()
    url = "https://serpapi.com/search"
    params = {
        "engine": "google_images",
        "q": query,
        "api_key": api_key,
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        if data.get("images_results"):
            return data["images_results"]
        else:
            return None
    except requests.exceptions.RequestException as e:
      print(f"Error fetching Google Images data: {e}")
      return None
        
def verify_product_images(query: str) -> Tuple[Optional[List[Dict]], Optional[List[Dict]]]:
    """
    Verifies product images by comparing Walmart search results with Google Images search results.

    Args:
        query (str): The search query.

    Returns:
        Tuple[Optional[List[Dict]], Optional[List[Dict]]]: A tuple containing two lists: Walmart results and Google image results,
        or (None, None) if either or both API calls fail.
    """
    walmart_data = fetch_walmart_data(query)
    google_images_data = fetch_google_images(query)
    
    return walmart_data, google_images_data