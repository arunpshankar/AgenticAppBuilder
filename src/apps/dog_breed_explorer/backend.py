import requests
from typing import Dict, Optional

def fetch_dog_image(breed_name: str) -> Dict:
    """
    Fetches a random image URL of the specified dog breed from the Dog API.

    Args:
        breed_name (str): The name of the dog breed.

    Returns:
        Dict: A dictionary containing the status and the image URL (if successful),
              or an error message.
    """
    url = f"https://dog.ceo/api/breed/{breed_name}/images/random"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        return {"status": "error", "message": f"Request failed: {e}"}
    except ValueError as e:
         return {"status": "error", "message": f"Failed to decode JSON: {e}"}
    except Exception as e:
        return {"status": "error", "message": f"An unexpected error occurred: {e}"}