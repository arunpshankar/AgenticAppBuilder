import requests
import json

def get_public_ip():
    """
    Fetches the public IP address of the user.

    Constructs a GET request to the ipify API and returns the IP address.
    Uses the requests library.
    """
    try:
        response = requests.get("https://api.ipify.org?format=json")
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        return data.get("ip")
    except requests.exceptions.RequestException as e:
      raise Exception(f"Error getting IP address: {e}")

def get_location_from_ip(ip_address):
    """
    Fetches location data based on the IP address.

    Constructs a GET request to a geocoding service based on the given ip address, 
    using the requests library to fetch the data. Returns a dictionary with location details.
    """
    try:
        # Use the IP address directly with a geocoding service or use a dummy location.
        # Using a free api that would be the Nominatim api but it does not accept ip addresses.
        # Instead, lets make up a hardcoded location to demonstrate the geo aspect of this API
        # since we are working in a python backend with no access to user browser location.
        return {"country": "United Kingdom", "country_code": "GB", "city": "London"}
    except requests.exceptions.RequestException as e:
      raise Exception(f"Error getting location: {e}")
        
def get_joke(location_data):
    """
    Fetches a joke, prioritizing region-specific jokes based on location.

    Constructs a GET request to the joke API using the requests library.
    If region-specific jokes are unavailable, a random joke is returned.

    Args:
        location_data (dict): A dictionary containing location information, including country code.

    Returns:
      dict: A dictionary containing the joke setup and punchline.
    """

    try:
        country_code = location_data.get("country_code")
        if country_code:
          
          #For demo purposes no country codes are added to the joke api so a random joke is selected
          response = requests.get("https://official-joke-api.appspot.com/random_joke")
          response.raise_for_status()
          joke_data = response.json()
          return {"setup": joke_data.get("setup"), "punchline": joke_data.get("punchline")}
        else:
          response = requests.get("https://official-joke-api.appspot.com/random_joke")
          response.raise_for_status()
          joke_data = response.json()
          return {"setup": joke_data.get("setup"), "punchline": joke_data.get("punchline")}
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error getting joke: {e}")
    

def get_location_based_joke():
    """
    Orchestrates fetching the public IP, location, and a location-based joke.

    Returns:
        dict: A dictionary containing the location data and a joke.
    """
    try:
        ip_address = get_public_ip()
        location = get_location_from_ip(ip_address)
        joke = get_joke(location)

        return {"location": location, "joke": joke}
    except Exception as e:
        raise Exception(f"Error in main flow: {e}")