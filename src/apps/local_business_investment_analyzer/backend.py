import requests
from typing import Dict, Optional, List
from src.config.setup import get_serp_api_key
from src.config.logging import logger
import json

def fetch_data_from_serp(url: str, params: Dict) -> Optional[dict]:
    """
    Fetches data from the SERP API.

    Args:
        url (str): The API endpoint URL.
        params (Dict): The query parameters for the API request.

    Returns:
        Optional[dict]: A dictionary containing the API response data or None if an error occurs.
    """
    api_key = get_serp_api_key()
    if not api_key:
        logger.error("SERP API key not found.")
        return None

    params['api_key'] = api_key
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error during API request: {e}")
        return None
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON response: {e}")
        return None

def search_local_businesses(business_type: str, location: str) -> Optional[List[dict]]:
    """
    Searches for local businesses using the Google Maps Search API.

    Args:
        business_type (str): The type of business to search for.
        location (str): The location to search in.

    Returns:
        Optional[List[dict]]: A list of dictionaries containing local business information, or None if an error occurs.
    """
    url = "https://serpapi.com/search"
    params = {
        "engine": "google_maps",
        "q": f"{business_type} in {location}",
    }
    response_data = fetch_data_from_serp(url, params)

    if response_data and 'local_results' in response_data:
        return response_data.get('local_results',[])
    else:
        logger.warning(f"No local business results found for {business_type} in {location}")
        return None

def get_business_details(place_id: str) -> Optional[dict]:
    """
    Retrieves detailed business information using the Google Local Basic Search API.

    Args:
        place_id (str): The place ID of the business.

    Returns:
        Optional[dict]: A dictionary containing detailed business information, or None if an error occurs.
    """
    url = "https://serpapi.com/search"
    params = {
        "engine": "google_local",
        "place_id": place_id,
    }
    response_data = fetch_data_from_serp(url, params)

    if response_data and 'place_results' in response_data and response_data['place_results']:
        return response_data.get('place_results')[0]
    else:
         logger.warning(f"No business details found for place ID: {place_id}")
         return None

def get_finance_data(business_type: str) -> Optional[List[dict]]:
    """
    Retrieves financial data using the Google Finance Basic Search API.

    Args:
        business_type (str): The type of business to fetch financial data for.

    Returns:
        Optional[List[dict]]: A list of dictionaries containing financial data, or None if an error occurs.
    """
    url = "https://serpapi.com/search"
    params = {
        "engine": "google_finance",
        "q": business_type,
    }

    response_data = fetch_data_from_serp(url, params)

    if response_data and 'markets' in response_data:
        return response_data.get('markets',[])
    else:
        logger.warning(f"No finance data found for {business_type}")
        return None

def get_business_investment_data(business_type: str, location: str) -> Optional[Dict]:
    """
    Orchestrates the retrieval of business information and financial data.

    Args:
        business_type (str): The type of business to analyze.
        location (str): The location to search in.

    Returns:
        Optional[Dict]: A dictionary containing business information and financial data.
                        Returns None if an error occurs.
    """
    local_results = search_local_businesses(business_type, location)
    if not local_results:
        return None

    business_details_list = []
    for result in local_results:
        place_id = result.get('place_id')
        if place_id:
            business_details = get_business_details(place_id)
            business_details_list.append(business_details)
        else:
           logger.warning(f"No place ID found for result: {result}")

    finance_data = get_finance_data(business_type)


    response = {
         "local_results": local_results,
         "finance_data": finance_data,
    }

    return response