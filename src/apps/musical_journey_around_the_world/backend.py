import requests
import json
from src.llm.gemini import generate_content
from src.config.client import initialize_genai_client

gemini_client = initialize_genai_client()
MODEL_ID = "gemini-2.0-flash-exp"

def get_location_info():
    """
    Fetches the user's public IP address and then uses it to determine their country.

    Returns:
        dict: A dictionary containing the user's country, or None if the location cannot be determined.
    """
    try:
        ip_response = requests.get("https://api.ipify.org?format=json")
        ip_response.raise_for_status()
        ip_data = ip_response.json()
        ip_address = ip_data.get("ip")

        if ip_address:
           location_response = requests.get(f"http://ip-api.com/json/{ip_address}")
           location_response.raise_for_status()
           location_data = location_response.json()
           country = location_data.get("country")
           if country:
               return {"country": country}
        return None

    except requests.exceptions.RequestException as e:
        print(f"Error fetching location data: {e}")
        return None


def get_artists_from_country(country):
    """
    Retrieves popular artists and song themes from a given country using the provided API.

    Args:
        country (str): The country to fetch music information for.

    Returns:
        dict: A dictionary containing a list of artists with themes and lyrics, or None if an error occurs.
    """
    try:
        prompt = f"""
        Given the country "{country}", please provide 3 popular musical artists from this location. 
        For each artist, please provide a list of up to 3 song themes they are known for.
        Return the result as a JSON object with the following structure:
        {{
        "artists": [
          {{
           "name": "artist name",
           "themes": ["theme 1", "theme 2", "theme 3"]
          }}
         ]
        }}
        """
        response = generate_content(gemini_client, MODEL_ID, prompt)
        text_response = response.text

        try:
             artist_data = json.loads(text_response)

             if not isinstance(artist_data, dict) or "artists" not in artist_data or not isinstance(artist_data['artists'], list):
                  print("Invalid response format from Gemini for artist data.")
                  return None

             
             for artist in artist_data['artists']:
                  if 'name' in artist:
                      artist_name = artist['name']
                      sample_lyrics = get_sample_lyrics(artist_name)
                      artist["lyrics"] = sample_lyrics
             return artist_data
        except json.JSONDecodeError:
             print("Error decoding JSON from Gemini for artist data.")
             return None

    except Exception as e:
      print(f"Error getting artist data: {e}")
      return None


def get_sample_lyrics(artist_name):
    """
        Fetches sample lyrics for a given artist and returns the lyrics string or None

        Args:
        artist_name (str): The name of the artist.

        Returns:
        str or None: A string containing sample lyrics or None if error.
    """
    try:
        prompt = f"""
        Given the artist "{artist_name}", please provide a popular song and related lyrics.
        Return the response as a JSON object with the following structure:
            {{
            "song_title": "title",
             "lyrics": "lyrics string"
            }}
        """
        response = generate_content(gemini_client, MODEL_ID, prompt)
        text_response = response.text
        try:
            lyrics_data = json.loads(text_response)
            if "lyrics" in lyrics_data:
                return lyrics_data["lyrics"]
            else:
               return None
        except json.JSONDecodeError:
             print("Error decoding JSON from Gemini for lyrics data.")
             return None
    except Exception as e:
      print(f"Error fetching lyrics: {e}")
      return None


def get_playlists():
    """
    Fetches and processes playlist data.

    Returns:
        dict or None: A dictionary containing playlist data, or None if an error occurs.
    """
    try:
         response = requests.get("https://openwhyd.org/")
         response.raise_for_status()
         # For now, since openwhyd html content and parsing is too complex for this context, just send basic response
         return {"message":"OpenWhyd API is HTML content - no JSON can be parsed for this API."}
    except requests.exceptions.RequestException as e:
        print(f"Error fetching playlist data: {e}")
        return None


def get_currency_exchange(country):
    """
    Fetches currency exchange data for a given country.

    Args:
        country (str): The country to fetch currency data for.

    Returns:
        dict or None: A dictionary containing currency exchange data, or None if an error occurs.
    """
    try:
        prompt = f"""
        Given the country "{country}", provide the currency code and current exchange rate to USD.
        Return a JSON object with the following structure:
          {{
            "currency_code": "currency_code",
            "exchange_rate_to_usd": "exchange_rate"
          }}
        """
        response = generate_content(gemini_client, MODEL_ID, prompt)
        text_response = response.text
        try:
            currency_data = json.loads(text_response)
            return currency_data
        except json.JSONDecodeError:
            print("Error decoding JSON from Gemini for currency data.")
            return None
    except Exception as e:
      print(f"Error fetching currency data: {e}")
      return None
    

def get_country_info(country):
    """
    Fetches country data based on the given name.
    Args:
        country (str): The name of the country
    Returns:
         dict or None: A dictionary containing the retrieved data or None
    """
    try:
       prompt = f"""
       Given the country "{country}", please provide a summary of information about the country.
       Return the result as a JSON object with the following structure:
          {{
           "summary": "country summary",
           "population": "population in number",
           "capital": "capital of the country",
           "languages": ["language1", "language2", ...]
          }}
       """
       response = generate_content(gemini_client, MODEL_ID, prompt)
       text_response = response.text
       try:
           country_data = json.loads(text_response)
           return country_data
       except json.JSONDecodeError:
           print("Error decoding JSON from Gemini for country info data.")
           return None
    except Exception as e:
       print(f"Error fetching country info data: {e}")
       return None