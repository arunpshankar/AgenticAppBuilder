import requests
import json
from src.llm.gemini import generate_content
from src.config.client import initialize_genai_client


gemini_client = initialize_genai_client()
MODEL_ID = "gemini-2.0-flash-exp"


def get_iss_location_and_city():
    """
    Fetches the current location of the International Space Station (ISS) and the nearest city.

    Returns:
        tuple: A tuple containing the ISS location data (dict) and the nearest city name (str).
               Returns (None, None) if there is an error fetching the data.
    """
    try:
        # Fetch ISS location
        iss_url = "http://api.open-notify.org/iss-now.json"
        iss_response = requests.get(iss_url)
        iss_response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        iss_data = iss_response.json()
        
        iss_latitude = iss_data["iss_position"]["latitude"]
        iss_longitude = iss_data["iss_position"]["longitude"]
        
        # Fetch nearest city name using Nominatim API
        nominatim_url = "https://nominatim.openstreetmap.org/reverse"
        params = {
            "format": "json",
            "lat": iss_latitude,
            "lon": iss_longitude,
            "zoom": 10,
            "accept-language": "en"
        }
        nominatim_response = requests.get(nominatim_url, params=params)
        nominatim_response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        nominatim_data = nominatim_response.json()

        if nominatim_data and "address" in nominatim_data:
            city_name = nominatim_data["address"].get("city") or nominatim_data["address"].get("town") or nominatim_data["address"].get("village")
            return iss_data, city_name
        else:
            return iss_data, None

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None, None

def get_song_lyrics(artist, title):
    """
    Fetches song lyrics for a given artist and title using the Lyrics.ovh API.

    Args:
        artist (str): The name of the artist.
        title (str): The title of the song.

    Returns:
        str: The lyrics of the song, or None if there was an error.
    """
    try:
        lyrics_url = f"https://api.lyrics.ovh/v1/{artist}/{title}"
        lyrics_response = requests.get(lyrics_url)
        lyrics_response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
        lyrics_data = lyrics_response.json()
        return lyrics_data.get("lyrics")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching lyrics: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding lyrics JSON: {e}")
        return None

def get_openwhyd_playlists(city_name):
    """
    Fetches openwhyd playlists related to a city.

    Args:
        city_name (str): The name of the city.

     Returns:
        list: list of dictionaries containing playlist information or None if an error occurred
    """
    try:
      #First, find a user in openwhyd based on the city
      prompt = f"""
      You are an AI that will look at a list of openwhyd user descriptions, and based on the city name provided, you will provide the username of the most relevant openwhyd user. Return ONLY the username.
      City name: {city_name}
      User descriptions:
      - london_beats : I love creating playlists related to London!
      - paris_vibes : playlists for the parisian nightlife.
      - nyc_grooves: New York City has some incredible beats. 
      - global_tunes : Global music from all over the world
      """
      playlist_response = generate_content(gemini_client, MODEL_ID, prompt)
      username_text_response = playlist_response.text
      
      # if there is no username then return none
      if not username_text_response:
           return None

      
      #now get the user's playlists
      openwhyd_url = f"https://openwhyd.org/user/{username_text_response}"
      openwhyd_response = requests.get(openwhyd_url)
      openwhyd_response.raise_for_status()

      # Use Gemini to extract playlist information
      prompt = f"""
      You are an AI that will analyze HTML content of an openwhyd user's page and extract a list of all playlists by looking for the playlist titles, playlist urls and playlist usernames associated with each playlist. Return a python list of dictionaries with each dictionary containing a "title" , "url", and "username" key. Only return the list.

      HTML Content: {openwhyd_response.text}
      """

      playlist_extraction_response = generate_content(gemini_client, MODEL_ID, prompt)
      playlist_extraction_response_text = playlist_extraction_response.text
      # Attempt to parse the response, handle invalid JSON cases
      try:
        playlists = json.loads(playlist_extraction_response_text)
      except json.JSONDecodeError:
            return None # or handle the error
      
      return playlists

    except requests.exceptions.RequestException as e:
        print(f"Error fetching Openwhyd data: {e}")
        return None
```