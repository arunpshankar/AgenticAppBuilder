import requests
from typing import Dict, List
from src.config.serp import get_api_key
from src.config.logging import logger

def get_random_dog_images_by_breed(breed: str, num_images: int) -> Dict:
    """
    Fetches random images of a specific dog breed from the Dog API.
    
    Args:
        breed (str): The breed of dog to search for.
        num_images (int): The number of random images to retrieve.
    
    Returns:
        Dict: A dictionary containing a list of image URLs under the 'images' key, or an error message
                under the 'error' key.
        
    Raises:
        Exception: If there's an issue with the API call or data processing.
    """
    try:
        
        breed_image_url = f"https://dog.ceo/api/breed/{breed}/images/random"
        
        response = requests.get(breed_image_url)
        response.raise_for_status()
        
        breed_data = response.json()

        if response.status_code == 200 and breed_data and breed_data.get("status") == "success" and breed_data.get("message"):
            
            random_images_url = f"https://dog.ceo/api/breeds/image/random/{num_images}"
            response = requests.get(random_images_url)
            response.raise_for_status()
            
            random_images_data = response.json()
            
            if random_images_data and random_images_data.get("status") == "success" and random_images_data.get("message"):
                return {"images": random_images_data["message"]}
            else:
                logger.error(f"Error fetching multiple images for breed '{breed}'. API returned status code {response.status_code} and data: {random_images_data}")
                return {"error": f"Error fetching images, bad response: {response.status_code}, {random_images_data}"}
        else:
             logger.error(f"Error fetching single image for breed '{breed}'. API returned status code {response.status_code} and data: {breed_data}")
             return {"error": f"Error fetching single image, bad response: {response.status_code}, {breed_data}"}

    except requests.exceptions.RequestException as e:
        logger.error(f"Request exception occurred while fetching breed '{breed}' images: {e}")
        return {"error": f"Request error: {e}"}
    except ValueError as e:
        logger.error(f"JSON decoding error occurred while processing breed '{breed}' images: {e}")
        return {"error": f"JSON decoding error: {e}"}
    except Exception as e:
        logger.error(f"An unexpected error occurred while fetching breed '{breed}' images: {e}")
        return {"error": f"An unexpected error occurred: {e}"}
```