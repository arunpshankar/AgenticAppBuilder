import requests
from typing import Dict, List, Optional
from src.config.serp import get_api_key
from src.config.logging import logger
import json

def search_travel_options(search_term: str, include_airlines: str = "", exclude_airlines: str = "") -> Dict:
    """
    Searches for travel options using the Serp API.

    Args:
        search_term (str): The user's search query.
        include_airlines (str): Comma-separated airlines to include.
        exclude_airlines (str): Comma-separated airlines to exclude.

    Returns:
        Dict: A dictionary containing search results, including AI overview and flight details.
        Returns an empty dictionary on error or if no results are found.
    """
    api_key = get_api_key()
    if not api_key:
        logger.error("SERP API key not found.")
        return {}

    params = {
        "api_key": api_key,
        "q": search_term,
        "location": "United States",
        "gl": "us",
        "hl": "en",
        "serp_api_params": json.dumps({"ai_overview": True, "flights":True }) #enable ai overview and flights parameter
    }

    if include_airlines:
        params["serp_api_params"] = json.dumps({"ai_overview": True, "flights":True, "include_airlines": include_airlines})

    if exclude_airlines:
         params["serp_api_params"] = json.dumps({"ai_overview": True, "flights":True, "exclude_airlines": exclude_airlines})

    try:
        response = requests.get("https://serpapi.com/search", params=params)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        data = response.json()

        ai_overview = {}
        if 'ai_overview' in data:
           ai_overview = data['ai_overview']


        flights_data = []
        if 'flights' in data and 'flights' in data['flights'] :
            for flight_item in data['flights']['flights']:
              try:
                flights_data.append({
                'airline': flight_item.get('airline', 'N/A'),
                'departure_airport': flight_item.get('departure_airport', 'N/A'),
                'arrival_airport': flight_item.get('arrival_airport', 'N/A'),
                'price': flight_item.get('price', 'N/A')
                })
              except Exception as e:
                  logger.error(f"Error parsing flight data: {e}")


        return {'ai_overview': ai_overview, 'flights': flights_data}

    except requests.exceptions.RequestException as e:
        logger.error(f"Request error: {e}")
        return {}
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {e}")
        return {}
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return {}