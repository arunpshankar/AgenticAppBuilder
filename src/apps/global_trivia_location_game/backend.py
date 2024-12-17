import requests
import json

def get_public_ip():
    """
    Fetches the public IP address of the user.

    Returns:
        str: The public IP address as a string, or None if an error occurs.
    """
    try:
        response = requests.get("https://api.ipify.org?format=json")
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        ip_data = response.json()
        return ip_data.get("ip")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching IP address: {e}")
        return None

def get_location_from_ip(ip_address):
    """
    Retrieves location information based on the provided IP address using the Nominatim API.

    Args:
        ip_address (str): The IP address to lookup.

    Returns:
        dict: A dictionary containing location data, or None if an error occurs.
    """
    if not ip_address:
        return None

    try:
        #Use ipinfo.io to get location first
        response = requests.get(f"https://ipinfo.io/{ip_address}/json")
        response.raise_for_status()
        ip_info = response.json()
        
        latitude = ip_info.get("latitude")
        longitude = ip_info.get("longitude")
        if latitude and longitude:
            nominatim_url = "https://nominatim.openstreetmap.org/reverse"
            params = {
            "format": "json",
            "lat": latitude,
            "lon": longitude,
            }
            response = requests.get(nominatim_url, params=params)
            response.raise_for_status()
            location_data = response.json()
            if location_data:
                return location_data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching location from IP: {e}")
    return None


def fetch_trivia_question():
    """
    Fetches a random trivia question from the Open Trivia Database API.

    Returns:
        dict: A dictionary containing the trivia question data, or None if an error occurs.
    """
    try:
        response = requests.get("https://opentdb.com/api.php?amount=1")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching trivia question: {e}")
        return None


def fetch_trivia_and_location():
    """
    Combines fetching a trivia question and location data based on the user's IP.

    Returns:
         tuple: A tuple containing the trivia data (dict) and location data (dict), both may be None
    """
    trivia_data = fetch_trivia_question()
    ip_address = get_public_ip()
    location_data = get_location_from_ip(ip_address)

    # Check if location_data is a list and extract the first element if it is
    if isinstance(location_data, list) and location_data:
         location_data = location_data[0]

    return trivia_data, location_data