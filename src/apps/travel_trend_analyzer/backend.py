import requests
from typing import Dict, List, Tuple
from src.config.serp import get_api_key
from src.config.logging import logger
import json

def fetch_travel_data(destinations: List[str], airlines_include: List[str] = [], airlines_exclude: List[str] = []) -> Tuple[Dict, Dict]:
    """
    Fetches travel trend and flight data based on provided destinations and airline preferences.
    
    Args:
        destinations (List[str]): List of destination names.
        airlines_include (List[str], optional): List of airlines to include in search. Defaults to [].
        airlines_exclude (List[str], optional): List of airlines to exclude from search. Defaults to [].

    Returns:
        Tuple[Dict, Dict]: A tuple containing trend data and flight data.
    """
    trends_data = fetch_trends_data(destinations)
    flights_data = {}

    if trends_data:
      trending_locations = [location for location, _ in trends_data.items() if _ > 0] # Use only locations where trends are > 0
      if trending_locations:
          flights_data = fetch_flights_data(trending_locations, airlines_include, airlines_exclude)

    return trends_data, flights_data

def fetch_trends_data(destinations: List[str]) -> Dict:
  """
  Fetches travel trend data for the given destinations using the Google Trends API.
  
  Args:
      destinations (List[str]): List of destination names.

  Returns:
      Dict: A dictionary containing trend data for each destination, or empty dictionary if error
  """
  api_key = get_api_key()
  if not api_key:
        logger.error("SERP API key not found.")
        return {}

  base_url = "https://serpapi.com/trends.json"
  trends_data = {}

  for destination in destinations:
    params = {
      "api_key": api_key,
      "q": destination,
      "region": "US",
      "output": "json",
      "type": "related_queries",
    }
    
    try:
      response = requests.get(base_url, params=params)
      response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)

      data = response.json()
      
      if data and 'related_queries' in data and data['related_queries']:
          # Get the top trending query (assuming its the first one in the list)
          top_query = data['related_queries'][0]
          trends_data[destination] = top_query.get('value',0)
      else:
        trends_data[destination] = 0
        logger.warning(f"No trend data found for {destination}.")

    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching trends for {destination}: {e}")
        trends_data[destination] = 0
    
    except json.JSONDecodeError as e:
        logger.error(f"JSON decoding error for trends {destination}: {e}")
        trends_data[destination] = 0
    except Exception as e:
        logger.error(f"An unexpected error occurred when fetching trends for {destination}: {e}")
        trends_data[destination] = 0

  return trends_data

def fetch_flights_data(destinations: List[str], airlines_include: List[str], airlines_exclude: List[str]) -> Dict:
    """
    Fetches flight data for the given destinations using the Google Flights API.

    Args:
        destinations (List[str]): List of destination names.
        airlines_include (List[str]): List of airlines to include in the search.
        airlines_exclude (List[str]): List of airlines to exclude from the search.

    Returns:
        Dict: A dictionary containing flight data for each destination, or empty dictionary if error
    """
    api_key = get_api_key()
    if not api_key:
        logger.error("SERP API key not found.")
        return {}

    base_url = "https://serpapi.com/search.json"
    flights_data = {}


    for destination in destinations:
      params = {
        "api_key": api_key,
        "engine": "google_flights",
        "q": f"flights to {destination}",
        "hl": "en",
      }
    
      if airlines_include:
          params["airline_inclusion"] = ",".join(airlines_include)
      if airlines_exclude:
          params["airline_exclusion"] = ",".join(airlines_exclude)

      try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        flights_data[destination] = data.get("flights", [])

      except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching flights for {destination}: {e}")
        flights_data[destination] = []
      except json.JSONDecodeError as e:
        logger.error(f"JSON decoding error for flights to {destination}: {e}")
        flights_data[destination] = []
      except Exception as e:
          logger.error(f"An unexpected error occurred when fetching flights for {destination}: {e}")
          flights_data[destination] = []


    return flights_data