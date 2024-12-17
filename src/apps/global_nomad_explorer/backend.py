import requests
import json
from src.llm.gemini import generate_content 
from src.config.client import initialize_genai_client

gemini_client = initialize_genai_client()
MODEL_ID = "gemini-2.0-flash-exp"


def get_age_by_name(name):
    """
    Predicts age based on a given name using the Agify API.

    Args:
        name (str): The name to predict the age for.

    Returns:
        dict: A dictionary containing the predicted age, or None if an error occurs.
    """
    url = f"https://api.agify.io?name={name}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching age data: {e}")
        return None


def get_nationality_by_name(name):
    """
    Predicts nationality based on a given name using the Nationalize API.

    Args:
        name (str): The name to predict the nationality for.

    Returns:
        dict: A dictionary containing the predicted nationality, or None if an error occurs.
    """
    url = f"https://api.nationalize.io?name={name}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching nationality data: {e}")
        return None


def recommend_locations(country_code):
    """
    Recommends locations based on a country code using the Nominatim API.

    Args:
        country_code (str): The two-letter country code to find locations in

    Returns:
         list: list of dicts containing the location data or None if error.

    """
    url = f"https://nominatim.openstreetmap.org/search?countrycodes={country_code}&format=json&limit=3"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching location data: {e}")
        return None


def get_trivia():
    """
    Retrieves a random trivia question using the Open Trivia Database API.

    Returns:
        dict: A dictionary containing a trivia question or None if error
    """
    url = "https://opentdb.com/api.php?amount=1"
    try:
       response = requests.get(url)
       response.raise_for_status()
       return response.json()
    except requests.exceptions.RequestException as e:
       print(f"Error fetching trivia data: {e}")
       return None


def recommend_music(country_code):
    """
    Recommends music based on a country code using the Openwhyd API and Gemini LLM to craft a description

    Args:
       country_code (str): The two-letter country code
    Returns:
       str: text with the recomendation or None if error
    """
    try:
        prompt = f"""Given the country code {country_code} what would be the music genre you recommend and 
         what is your rationale, limit the description to 100 words? """
        response = generate_content(gemini_client, MODEL_ID, prompt)
        text_response = response.text
        return text_response
    except Exception as e:
        print(f"Error processing music recommendations: {e}")
        return None


def get_charge_points(lat, lon, country_code):
    """
    Fetches nearby electric vehicle charging stations using the Open Charge Map API.

    Args:
        lat (float): Latitude of the location.
        lon (float): Longitude of the location.
        country_code (str): The two-letter country code.
    Returns:
       list: list of dicts containing charge point information or None if error
    """
    url = f"https://api.openchargemap.io/v3/poi/?output=json&latitude={lat}&longitude={lon}&countrycode={country_code}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching charge point data: {e}")
        return None

def get_iss_location(lat, lon):
    """
    Fetches the current location of the International Space Station using the Open Notify API,
    and compares it to the given location using Gemini
    Args:
        lat (float): Latitude of the location.
        lon (float): Longitude of the location.

    Returns:
      dict: dictionary containing the ISS location and comparision
    """
    url = "http://api.open-notify.org/iss-now.json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        iss_lat = data['iss_position']['latitude']
        iss_lon = data['iss_position']['longitude']
        prompt = f"The ISS is located at latitude {iss_lat} and longitude {iss_lon} the place is located at lat {lat} and lon {lon} could you describe how far is the space station from the place? limit the description to 50 words"
        response_gemini = generate_content(gemini_client, MODEL_ID, prompt)
        text_response = response_gemini.text
        return {"iss_location":data, "comparision":text_response}

    except requests.exceptions.RequestException as e:
        print(f"Error fetching ISS data: {e}")
        return None
```