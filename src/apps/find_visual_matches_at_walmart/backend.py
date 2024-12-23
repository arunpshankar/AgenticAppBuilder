import requests
from typing import Dict, List, Optional
from src.config.serp import get_api_key
from io import BytesIO
from PIL import Image
import base64
from src.config.logging import logger
import json

def get_image_url(image_bytes: bytes) -> Optional[str]:
    """
    Retrieves an image URL from Google Images based on provided image bytes.

    Args:
        image_bytes (bytes): The image data in bytes.

    Returns:
        Optional[str]: The URL of the image if found, otherwise None.
    """
    try:
        api_key = get_api_key()
        if not api_key:
             logger.error("SERP API key is missing or invalid.")
             return None

        base64_image = base64.b64encode(image_bytes).decode("utf-8")
        params = {
            "engine": "google_images",
            "image_base64": base64_image,
            "api_key": api_key
        }

        response = requests.get("https://serpapi.com/search", params=params)
        response.raise_for_status()
        data = response.json()
        
        if data and data.get("images_results"):
            first_result = data["images_results"][0]
            if first_result and first_result.get("original"):
                return first_result["original"]
            else:
                logger.warning("No original image URL found in the response.")
                return None
        else:
            logger.warning("No image results found in the response.")
            return None


    except requests.exceptions.RequestException as e:
        logger.error(f"Error during Google Images API request: {e}")
        return None
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON response from Google Images API: {e}")
        return None
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return None

def get_keywords_from_image_url(image_url: str) -> Optional[List[str]]:
    """
    Extracts keywords from a given image URL using Google Images.

    Args:
        image_url (str): The URL of the image.

    Returns:
        Optional[List[str]]: A list of keywords extracted from the image if successful, otherwise None.
    """
    try:
        api_key = get_api_key()
        if not api_key:
            logger.error("SERP API key is missing or invalid.")
            return None
        params = {
            "engine": "google_images",
            "url": image_url,
            "api_key": api_key
        }

        response = requests.get("https://serpapi.com/search", params=params)
        response.raise_for_status()
        data = response.json()

        if data and data.get("knowledge_graph") and data["knowledge_graph"].get("title"):
            return [data["knowledge_graph"]["title"]]
        elif data and data.get("search_information") and data["search_information"].get("query_displayed"):
            return [data["search_information"]["query_displayed"]]
        else:
            logger.warning("Could not find suitable keywords in the response.")
            return None

    except requests.exceptions.RequestException as e:
         logger.error(f"Error during Google Images API request: {e}")
         return None
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON response from Google Images API: {e}")
        return None
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return None

def search_walmart_products(keywords: List[str], page: int = 1) -> Optional[Dict]:
    """
    Searches for products on Walmart based on a list of keywords.

    Args:
        keywords (List[str]): A list of keywords to use in the search.
        page (int, optional): The page number of results to fetch. Defaults to 1.

    Returns:
        Optional[Dict]: A dictionary containing the search results, or None if an error occurred.
    """
    try:
        api_key = get_api_key()
        if not api_key:
            logger.error("SERP API key is missing or invalid.")
            return None
        query = " ".join(keywords)
        params = {
            "engine": "walmart",
            "query": query,
            "page": page,
            "api_key": api_key
        }

        response = requests.get("https://serpapi.com/search", params=params)
        response.raise_for_status()
        data = response.json()
        if data and data.get("organic_results"):
            return data["organic_results"]
        else:
            logger.warning("No organic results found in Walmart search.")
            return None

    except requests.exceptions.RequestException as e:
         logger.error(f"Error during Walmart API request: {e}")
         return None
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON response from Walmart API: {e}")
        return None
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return None