import requests
import json

def fetch_trivia_questions(amount=1):
    """
    Fetches trivia questions from the Open Trivia DB API.

    Args:
        amount (int): The number of trivia questions to fetch. Defaults to 1.

    Returns:
        dict: A dictionary containing the trivia question data, or None if the request fails.
    """
    url = "https://opentdb.com/api.php"
    params = {"amount": amount}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching trivia questions: {e}")
        return None


def fetch_location_by_country(country_name):
    """
    Fetches location data based on a country name using Nominatim API.

    Args:
        country_name (str): The name of the country to search for.

    Returns:
        list: A list of dictionaries containing location data, or None if the request fails.
    """
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": country_name, "format": "json"}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching location data: {e}")
        return None
    

def fetch_ip_location():
    """
    Fetches the public IP address of the requester and returns it as json.

    Returns:
      dict: A dictionary containing the IP address or None if request fails.
    """
    url = "https://api.ipify.org"
    params = {"format": "json"}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching IP location: {e}")
        return None


def fetch_geocoding_data(query):
    """
    Fetches geocoding data based on the provided query using Nominatim API.

    Args:
        query (str): The location query (e.g., city, landmark).

    Returns:
        list: A list of dictionaries containing geocoding data, or None if the request fails.
    """
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": query, "format": "json"}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching geocoding data: {e}")
        return None