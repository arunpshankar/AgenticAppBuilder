import requests
from typing import Dict, List

def get_random_cat_fact() -> Dict:
    """
    Retrieves a single random cat fact from the API.

    Returns:
        Dict: A dictionary containing the cat fact data, or an empty dictionary on failure.
    """
    try:
        response = requests.get("https://catfact.ninja/fact")
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching random cat fact: {e}")
        return {}


def get_multiple_cat_facts(count: int) -> List[Dict]:
    """
    Retrieves multiple cat facts from the API.

    Args:
        count (int): The number of cat facts to retrieve.

    Returns:
        List[Dict]: A list of dictionaries, each containing a cat fact, or an empty list on failure.
    """
    try:
        response = requests.get(f"https://catfact.ninja/facts?limit={count}")
        response.raise_for_status()
        data = response.json()
        return data.get('data', [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching multiple cat facts: {e}")
        return []