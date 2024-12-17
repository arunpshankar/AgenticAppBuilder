import requests
import json
from src.llm.gemini import generate_content
from src.config.client import initialize_genai_client

gemini_client = initialize_genai_client()
MODEL_ID = "gemini-2.0-flash-exp"



def get_cat_fact():
    """
    Fetches a random cat fact from the catfact.ninja API.

    Returns:
        dict: A dictionary containing the cat fact, or None if the request fails.
    """
    try:
        url = "https://catfact.ninja/fact"
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching cat fact: {e}")
        return None


def get_dog_image():
    """
    Fetches a random dog image URL from the dog.ceo API.

    Returns:
        dict: A dictionary containing the dog image URL, or None if the request fails.
    """
    try:
        url = "https://dog.ceo/api/breeds/image/random"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching dog image: {e}")
        return None

def get_public_ip():
    """
    Fetches the public IP address of the user using the api.ipify.org service.

    Returns:
         str: A string containing the public IP address, or None if the request fails.
    """
    try:
        url = "https://api.ipify.org?format=json"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching IP address: {e}")
        return None

def get_open_charge_map_data(ip_address):
    """
    Retrieves charging station data using Open Charge Map API using a general location from an IP address

    Returns:
        dict: A dict containing the charging data or None if the request fails
    """
    try:
          # Use another API to geolocate the IP address since it is too complex
          geo_url = f"http://ip-api.com/json/{ip_address}"
          geo_response = requests.get(geo_url)
          geo_response.raise_for_status()
          geo_data = geo_response.json()
          
          latitude = geo_data.get("lat")
          longitude = geo_data.get("lon")
          if latitude is None or longitude is None:
                print("Could not find lat/long")
                return None
          
          charge_url = "https://api.openchargemap.io/v3/poi/"
          params = {
                "output": "json",
                "latitude": latitude,
                "longitude": longitude,
                "distance": 20, #20km 
                "distanceunit": "km",
                "maxresults": 5,
          }
          response = requests.get(charge_url, params=params)
          response.raise_for_status()
          return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching charging station data: {e}")
        return None
    

def get_location_and_charge_data():
    """
    Fetches the user's IP address, uses this to find geo location then fetches nearby charging station data.

    Returns:
      dict: A dictionary containing the IP address and charging station data, or None if the requests fail.
    """
    ip_data = get_public_ip()
    if ip_data and "ip" in ip_data:
        ip_address = ip_data["ip"]
        charge_data = get_open_charge_map_data(ip_address)
        return {"ip_address": ip_data, "charge_data": charge_data}
    else:
       return None
    
def get_fox_image():
    """
    Fetches a random fox image URL from randomfox.ca API.

    Returns:
        dict: A dictionary containing the fox image URL, or None if the request fails.
    """
    try:
        url = "https://randomfox.ca/floof/"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching fox image: {e}")
        return None

if __name__ == '__main__':
    # Example usage:
    cat_fact = get_cat_fact()
    if cat_fact:
        print("Cat Fact:", cat_fact)

    dog_image = get_dog_image()
    if dog_image:
        print("Dog Image URL:", dog_image)

    location_data = get_location_and_charge_data()
    if location_data:
         print("Location and Charge data:", location_data)

    fox_image = get_fox_image()
    if fox_image:
        print("Fox Image URL:", fox_image)