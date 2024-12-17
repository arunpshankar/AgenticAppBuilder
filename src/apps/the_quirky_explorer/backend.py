import requests
import json
import random

def get_ip_address():
    """
    Fetches the public IP address of the requester.

    API Endpoint: https://api.ipify.org?format=json
    Method: GET
    Returns:
    - dict: A dictionary containing the IP address {"ip": "192.0.2.1"}.
    """
    try:
        response = requests.get("https://api.ipify.org?format=json")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
         return {"error": f"Error fetching IP address: {e}"}

def get_location_from_ip(ip_address):
    """
    Fetches location data based on the provided IP address.

    Uses ipinfo.io to get location details.
    API Endpoint: https://ipinfo.io/{ip}/json
    Method: GET

     Parameters:
        - ip_address (str): The IP address to lookup.
     Returns:
        - dict: A dictionary containing location details or an error message.
            
    """
    try:
        response = requests.get(f"https://ipinfo.io/{ip_address}/json")
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Error fetching location data: {e}"}
    
def get_joke():
    """
    Fetches a random joke.

    API Endpoint: https://official-joke-api.appspot.com/random_joke
    Method: GET
     Returns:
      - dict: A dictionary containing the joke data
            (e.g., {"id": 1, "type": "general", "setup": "...", "punchline": "..."}).
    """
    try:
        response = requests.get("https://official-joke-api.appspot.com/random_joke")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Error fetching joke: {e}"}
    
def get_trivia():
    """
    Fetches a random trivia question related to art from the Art Institute of Chicago.
    It first gets a random artwork id from the API and then it will extract the data.

    API Endpoint: https://api.artic.edu/api/v1/artworks?limit=1
                 https://api.artic.edu/api/v1/artworks/{id}
    Method: GET
     Returns:
      - dict: A dictionary containing the trivia question and answer
            (e.g., {"question": "Who painted...", "correct_answer": "Pablo Picasso"}).
    """
    try:
        #get the random artwork
        response_artworks = requests.get("https://api.artic.edu/api/v1/artworks?limit=1")
        response_artworks.raise_for_status()
        artwork_data = response_artworks.json()
        artwork_id = artwork_data['data'][0]['id']
        
        #get the artwork data for the trivia
        response_artwork_details = requests.get(f"https://api.artic.edu/api/v1/artworks/{artwork_id}")
        response_artwork_details.raise_for_status()
        artwork_details = response_artwork_details.json()
        
        #create the trivia question based on the data
        title = artwork_details['data']['title']
        artist = artwork_details['data'].get('artist_title','Unknown Artist')
        question = f"Who is the artist of the artwork '{title}'?"
        correct_answer = artist
        return {"question": question, "correct_answer": correct_answer}

    except requests.exceptions.RequestException as e:
        return {"error": f"Error fetching trivia data: {e}"}
    except KeyError as e:
         return {"error": f"Error parsing trivia data: {e}"}
    
def get_cat_fact():
    """
    Fetches a random cat fact.

    API Endpoint: https://catfact.ninja/fact
    Method: GET
     Returns:
        - dict: A dictionary containing the cat fact
            (e.g., {"fact": "Cats have five toes on their front paws, but only four on the back ones.", "length": 74}).
    """
    try:
      response = requests.get("https://catfact.ninja/fact")
      response.raise_for_status()
      return response.json()
    except requests.exceptions.RequestException as e:
      return {"error": f"Error fetching cat fact: {e}"}
```