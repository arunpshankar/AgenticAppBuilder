import requests
import random
import json
from typing import Dict, List, Optional, Any


def get_user_info(name: str) -> Optional[Dict[str, Any]]:
    """
    Fetches user information including age, gender, and nationality based on the provided name.

    Args:
        name (str): The name of the user.

    Returns:
        Optional[Dict[str, Any]]: A dictionary containing the user's name, age, gender, and nationality
                                   or None if any API request fails.
    """
    try:
      age_data = _get_age_by_name(name)
      gender_data = _get_gender_by_name(name)
      nationality_data = _get_nationality_by_name(name)
      
      if age_data and gender_data and nationality_data:
            
            return {
                "name": name,
                "age": age_data.get('age', 'N/A'),
                "gender": gender_data.get('gender', 'N/A'),
                "nationality": _get_top_nationality(nationality_data),
            }
      else:
           return None
    except Exception as e:
      print(f"Error fetching user info: {e}")
      return None



def _get_age_by_name(name: str) -> Optional[Dict[str, Any]]:
    """
    Fetches age prediction data for a given name.

    Args:
        name (str): The name to get the age prediction for.

    Returns:
        Optional[Dict[str, Any]]: A dictionary containing the age prediction or None if the request fails.
    """
    url = f"https://api.agify.io?name={name}"
    try:
      response = requests.get(url)
      response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
      return response.json()
    except requests.exceptions.RequestException as e:
      print(f"Error fetching age: {e}")
      return None
    except json.JSONDecodeError as e:
      print(f"Error decoding age JSON: {e}")
      return None


def _get_gender_by_name(name: str) -> Optional[Dict[str, Any]]:
    """
    Fetches gender prediction data for a given name.

    Args:
        name (str): The name to get the gender prediction for.

    Returns:
        Optional[Dict[str, Any]]: A dictionary containing the gender prediction or None if the request fails.
    """
    url = f"https://api.genderize.io?name={name}"
    try:
      response = requests.get(url)
      response.raise_for_status()
      return response.json()
    except requests.exceptions.RequestException as e:
      print(f"Error fetching gender: {e}")
      return None
    except json.JSONDecodeError as e:
      print(f"Error decoding gender JSON: {e}")
      return None


def _get_nationality_by_name(name: str) -> Optional[Dict[str, Any]]:
    """
    Fetches nationality prediction data for a given name.

    Args:
        name (str): The name to get nationality prediction for.

    Returns:
        Optional[Dict[str, Any]]: A dictionary containing the nationality prediction or None if the request fails.
    """
    url = f"https://api.nationalize.io?name={name}"
    try:
      response = requests.get(url)
      response.raise_for_status()
      return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching nationality: {e}")
        return None
    except json.JSONDecodeError as e:
      print(f"Error decoding nationality JSON: {e}")
      return None



def _get_top_nationality(nationality_data: Dict[str, Any]) -> str:
    """
    Extracts the highest probability nationality from the API response.

    Args:
        nationality_data (Dict[str, Any]): The dictionary containing nationality data.

    Returns:
        str: The top predicted nationality as a string.
    """
    if nationality_data and 'country' in nationality_data and nationality_data['country']:
        top_country = max(nationality_data['country'], key=lambda x: x['probability'])
        return top_country.get('country_id', 'N/A')
    return 'N/A'



def suggest_pet(user_info: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Suggests a pet breed based on the user's demographic information.

    Args:
        user_info (Dict[str, Any]): A dictionary containing the user's demographic information.

    Returns:
         Optional[Dict[str, Any]]: A dictionary containing the suggested animal_type and breed or None if no suitable suggestion.
    """
    if not user_info:
         return None

    gender = user_info.get("gender", "N/A")
    age = user_info.get("age", 0)
    nationality = user_info.get("nationality", "N/A")

    # Simple logic to decide on a pet type and breed
    if gender == "male" and age < 30:
      return {"animal_type": "dog", "breed": "golden retriever"}
    elif gender == "female" and age > 40:
      return {"animal_type": "cat", "breed": "persian"}
    elif nationality in ["US","GB", "CA"]:
       return {"animal_type":"dog", "breed":"labrador"}
    else:
      
       if random.choice([True,False]):
            return {"animal_type":"cat", "breed":"siamese"}
       else:
            return {"animal_type": "dog", "breed": "bulldog"}



def get_cat_fact() -> Optional[str]:
    """
    Fetches a random cat fact.

    Returns:
       Optional[str]: A string containing the random cat fact or None if the request fails.
    """
    url = "https://catfact.ninja/fact"
    try:
      response = requests.get(url)
      response.raise_for_status()
      data = response.json()
      return data.get("fact", None)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching cat fact: {e}")
        return None
    except json.JSONDecodeError as e:
      print(f"Error decoding cat fact JSON: {e}")
      return None

def get_dog_image(breed: str) -> Optional[str]:
    """
    Fetches a random dog image URL for a specific breed.

    Args:
        breed (str): The breed of dog to fetch the image for.

    Returns:
        Optional[str]: A string containing the URL of a random dog image or None if the request fails.
    """
    url = f"https://dog.ceo/api/breed/{breed}/images/random"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data.get("message", None)
    except requests.exceptions.RequestException as e:
      print(f"Error fetching dog image: {e}")
      return None
    except json.JSONDecodeError as e:
        print(f"Error decoding dog image JSON: {e}")
        return None
```