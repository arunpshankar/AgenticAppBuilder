import requests
import json

def get_age_and_gender(name):
    """
    Predicts age and gender based on a given name.

    Args:
        name (str): The name to predict age and gender for.

    Returns:
        dict: A dictionary containing age and gender predictions.
             Returns None if there is an error with the API
    """
    age_url = f"https://api.agify.io?name={name}"
    gender_url = f"https://api.genderize.io?name={name}"

    try:
        age_response = requests.get(age_url)
        age_response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        age_data = age_response.json()
    
        gender_response = requests.get(gender_url)
        gender_response.raise_for_status()
        gender_data = gender_response.json()
    except requests.exceptions.RequestException as e:
         print(f"Error during API request: {e}")
         return None
    

    return {
        "age": age_data.get("age"),
        "gender": gender_data.get("gender")
    }


def get_public_ip():
    """
    Retrieves the public IP address of the requester.

    Returns:
        str: The public IP address. Returns None if there is an error with the API
    """
    url = "https://api.ipify.org?format=json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error during API request: {e}")
        return None
    return data.get("ip")

def get_location_from_ip(ip_address):
    """
    Retrieves location information from a given IP address

    Args:
        ip_address (str): the public ip address to search for location

    Returns:
        dict: A dictionary with the location data. Returns None if there is an error with the API
    """
    url = f"https://ipapi.co/{ip_address}/json/"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error during API request: {e}")
        return None
    return data

def get_nearby_art(latitude, longitude):
    """
    Fetches nearby art from the Art Institute of Chicago API.

    Args:
       latitude (float): latitude of location to search by.
       longitude (float): longitude of location to search by.

    Returns:
        list: A list of art objects. Returns None if there is an error with the API
    """
    url = "https://api.artic.edu/api/v1/artworks"
    params = {
      "limit": 3, # Get top 3 results
      "fields": "id,title,artist_display,image_id",
      "latitude": latitude,
      "longitude": longitude
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
         print(f"Error during API request: {e}")
         return None
    return data.get("data", [])


def get_transportation_info(latitude, longitude):
    """
     Fetches transport information based on location. If in London, use TFL API,
    otherwise use Open Charge Map for driving.

    Args:
      latitude (float): latitude of location to search by.
      longitude (float): longitude of location to search by.

    Returns:
      dict: A dictionary containing the results from either the TFL API or Open Charge Map.
           Returns None if there is an error with the API
    """

    #Check if location is in London (approximate coordinates of London for demo purposes)
    london_latitude_min = 51.2
    london_latitude_max = 51.8
    london_longitude_min = -0.5
    london_longitude_max = 0.3

    if (london_latitude_min <= float(latitude) <= london_latitude_max) and \
            (london_longitude_min <= float(longitude) <= london_longitude_max):
          
      tfl_url = "https://api.tfl.gov.uk/Line/Mode/tube/Status"
      try:
          tfl_response = requests.get(tfl_url)
          tfl_response.raise_for_status()
          tfl_data = tfl_response.json()
      except requests.exceptions.RequestException as e:
          print(f"Error during API request: {e}")
          return None

      return {"transport_type": "London Underground", "data": tfl_data}
    
    else:
        # use open charge map api
        open_charge_map_url = "https://api.openchargemap.io/v3/poi/"
        params = {
            "output": "json",
            "latitude": latitude,
            "longitude": longitude,
            "distance": 10,
            "maxresults": 3,
        }
        try:
            open_charge_map_response = requests.get(open_charge_map_url, params=params)
            open_charge_map_response.raise_for_status()
            open_charge_map_data = open_charge_map_response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error during API request: {e}")
            return None

        return {"transport_type": "Electric Vehicle Charging", "data": open_charge_map_data}

def get_location_info(latitude, longitude):
  """
    Fetches location information from Nominatim API

    Args:
       latitude (float): latitude of location to search by.
       longitude (float): longitude of location to search by.

    Returns:
       dict: A dictionary of location information. Returns None if there is an error with the API
  """
  nominatim_url = "https://nominatim.openstreetmap.org/reverse"
  params = {
      "format": "json",
      "lat": latitude,
      "lon": longitude,
  }
  try:
      response = requests.get(nominatim_url, params=params)
      response.raise_for_status()
      data = response.json()
  except requests.exceptions.RequestException as e:
      print(f"Error during API request: {e}")
      return None

  return data


def get_trivia():
    """
    Fetches a random trivia question.

    Returns:
        dict: A dictionary containing a trivia question and answer. Returns None if there is an error with the API
    """
    trivia_url = "https://opentdb.com/api.php?amount=1"

    try:
        response = requests.get(trivia_url)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
      print(f"Error during API request: {e}")
      return None

    if data and data.get("results"):
      return data["results"][0]
    return None

def generate_trip_plan(user_name):
    """
    Generates a personalized day trip plan for the user.

    Args:
        user_name (str): The name of the user.

    Returns:
        dict: A dictionary containing the trip plan data.
    """
    trip_plan = {}

    # 1. Predict age and gender
    age_gender_info = get_age_and_gender(user_name)
    if age_gender_info:
      trip_plan["demographics"] = age_gender_info
    else:
      trip_plan["demographics"] = {"error": "Could not get age and gender"}
   

    # 2. Get public IP address
    public_ip = get_public_ip()
    if public_ip:
        trip_plan["ip_address"] = public_ip
        # 3. Get location from IP address
        location_info = get_location_from_ip(public_ip)
        if location_info:
          trip_plan["location"] = {
            "city": location_info.get("city"),
            "region": location_info.get("region"),
             "country": location_info.get("country_name"),
            "latitude": location_info.get("latitude"),
            "longitude": location_info.get("longitude")
          }
        
          #4. Fetch nearby art
          nearby_art = get_nearby_art(location_info.get("latitude"), location_info.get("longitude"))
          if nearby_art:
             trip_plan["nearby_art"] = nearby_art
          else:
             trip_plan["nearby_art"] = {"error": "Could not get nearby art"}

          #5. Fetch Transportation info
          transport_info = get_transportation_info(location_info.get("latitude"), location_info.get("longitude"))
          if transport_info:
            trip_plan["transportation"] = transport_info
          else:
             trip_plan["transportation"] = {"error": "Could not get transportation info"}
            
          #6. Get Detailed Location info
          detailed_location_info = get_location_info(location_info.get("latitude"), location_info.get("longitude"))
          if detailed_location_info:
            trip_plan["detailed_location"] = detailed_location_info
          else:
             trip_plan["detailed_location"] = {"error": "Could not get detailed location info"}

        else:
            trip_plan["location"] = {"error": "Could not get location"}


    else:
        trip_plan["ip_address"] = {"error": "Could not get public IP"}

    # 7. Get trivia
    trivia = get_trivia()
    if trivia:
        trip_plan["trivia"] = trivia
    else:
      trip_plan["trivia"] = {"error": "Could not get trivia question"}


    return trip_plan