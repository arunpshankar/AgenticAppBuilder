import requests
from typing import Dict, List, Optional
from llm.gemini_text import generate_content
from src.config.client import initialize_genai_client
import json

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

def get_cat_facts(limit: int = 3) -> Optional[List[Dict]]:
    """
    Retrieves multiple cat facts from the catfact.ninja API.

    Args:
        limit (int): The number of facts to retrieve. Defaults to 3.

    Returns:
        Optional[List[Dict]]: A list of cat fact dictionaries, or None if an error occurs.
    """
    url = f"https://catfact.ninja/facts?limit={limit}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        data = response.json()
        return data.get("data")
    except requests.exceptions.RequestException as e:
         print(f"Error fetching cat facts: {e}")
         return None

def get_cat_breeds() -> Optional[List[str]]:
    """
    Retrieves a list of cat breeds from a local JSON file.

    Returns:
        Optional[List[str]]: A list of cat breed names, or None if an error occurs.
    """
    try:
        # Ideally this would come from an external source
        # But, given the current API specs lack breeds, using a local file for example purposes.
        # In a real application we would use an API endpoint. 
        breeds_data = """
        {
          "breeds": [
            "Abyssinian",
            "Aegean",
            "American Bobtail",
            "American Curl",
            "American Shorthair",
            "American Wirehair",
            "Arabian Mau",
            "Australian Mist",
             "Balinese",
             "Bambino"
           ]
        }
        """
        breeds = json.loads(breeds_data).get("breeds", [])
        return breeds
    except Exception as e:
         print(f"Error loading cat breeds: {e}")
         return None