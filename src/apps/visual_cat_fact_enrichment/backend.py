import requests
from typing import Dict, Optional
from src.config.setup import get_serp_api_key
from src.config.logging import logger
import json

def get_cat_fact() -> Optional[str]:
    """
    Fetches a random cat fact from the Cat Fact API.

    Returns:
        Optional[str]: A string containing the cat fact, or None if an error occurs.
    """
    try:
        response = requests.get("https://catfact.ninja/fact")
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        return data.get("fact")
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching cat fact: {e}")
        return None
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding cat fact response: {e}")
        return None


def search_image(query: str) -> Optional[str]:
    """
    Searches for an image using the Google Image Search API through SERP API.

    Args:
        query (str): The search query.

    Returns:
        Optional[str]: The URL of the first image found, or None if no image is found or an error occurs.
    """
    api_key = get_serp_api_key()
    if not api_key:
        logger.error("SERP API key not found.")
        return None

    params = {
        "q": query,
        "tbm": "isch",
        "api_key": api_key,
        "num": 1
    }
    
    try:
        response = requests.get("https://serpapi.com/search", params=params)
        response.raise_for_status()
        results = response.json()
        if results and "images_results" in results and results["images_results"]:
            return results["images_results"][0].get("original")
        else:
            logger.warning(f"No image results found for query: {query}")
            return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Error during image search: {e}")
        return None
    except json.JSONDecodeError as e:
         logger.error(f"Error decoding image search response: {e}")
         return None
    except KeyError as e:
         logger.error(f"KeyError accessing image search response: {e}")
         return None
    

def get_cat_fact_and_image() -> Optional[Dict[str, str]]:
    """
    Retrieves a cat fact and a related image URL.

    Returns:
        Optional[Dict[str, str]]: A dictionary containing the cat fact and image URL, or None if an error occurs.
    """
    fact = get_cat_fact()
    if not fact:
        return None
    
    image_url = search_image(fact + " cat")
    
    return {"fact": fact, "image_url": image_url}