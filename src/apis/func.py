from src.config.logging import logger
from typing import Optional
from typing import Dict 
from typing import List 
from typing import Any 
import requests


def get_cat_fact(max_length: Optional[int] = None) -> Dict[str, Any]:
    """
    Retrieve a random cat fact. Optionally, specify a maximum length for the fact.

    :param max_length: Maximum length of the cat fact (optional).
    :return: A dictionary containing the cat fact.
    :raises requests.HTTPError: If the request fails.
    """
    base_url = "https://catfact.ninja/fact"
    params = {"max_length": max_length} if max_length else {}
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        fact = response.json()
        logger.info(f"Retrieved cat fact: {fact}")
        return fact
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve cat fact: {e}")
        raise


def get_multiple_cat_facts(limit: int) -> Dict[str, Any]:
    """
    Retrieve multiple cat facts.

    :param limit: Number of cat facts to retrieve.
    :return: A dictionary containing the cat facts.
    :raises requests.HTTPError: If the request fails.
    """
    base_url = "https://catfact.ninja/facts"
    params = {"limit": limit}
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        facts = response.json()
        logger.info(f"Retrieved {limit} cat facts: {facts}")
        return facts
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve multiple cat facts: {e}")
        raise


def get_cat_breeds(limit: Optional[int] = None) -> Dict[str, Any]:
    """
    Retrieve a list of cat breeds.

    :param limit: Number of cat breeds to retrieve (optional).
    :return: A dictionary containing the list of cat breeds.
    :raises requests.HTTPError: If the request fails.
    """
    base_url = "https://catfact.ninja/breeds"
    params = {"limit": limit} if limit else {}
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        breeds = response.json()
        logger.info(f"Retrieved cat breeds: {breeds}")
        return breeds
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve cat breeds: {e}")
        raise


def get_random_dog_image() -> Dict[str, Any]:
    """
    Retrieve a random dog image.

    :return: A dictionary containing the dog image URL.
    :raises requests.HTTPError: If the request fails.
    """
    base_url = "https://dog.ceo/api/breeds/image/random"
    try:
        response = requests.get(base_url)
        response.raise_for_status()
        image = response.json()
        logger.info(f"Retrieved dog image: {image}")
        return image
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve dog image: {e}")
        raise


def get_multiple_dog_images(number: int) -> Dict[str, Any]:
    """
    Retrieve multiple random dog images.

    :param number: Number of dog images to retrieve.
    :return: A dictionary containing the dog image URLs.
    :raises requests.HTTPError: If the request fails.
    """
    base_url = f"https://dog.ceo/api/breeds/image/random/{number}"
    try:
        response = requests.get(base_url)
        response.raise_for_status()
        images = response.json()
        logger.info(f"Retrieved {number} random dog images: {images}")
        return images
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve random dog images: {e}")
        raise


def get_random_dog_breed_image(breed: str) -> Dict[str, Any]:
    """
    Retrieve a random image of a specific dog breed.

    :param breed: The breed of the dog.
    :return: A dictionary containing the dog image URL.
    :raises requests.HTTPError: If the request fails.
    """
    base_url = f"https://dog.ceo/api/breed/{breed}/images/random"
    try:
        response = requests.get(base_url)
        response.raise_for_status()
        image = response.json()
        logger.info(f"Retrieved random dog image for breed '{breed}': {image}")
        return image
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve random dog image for breed '{breed}': {e}")
        raise


def get_random_joke() -> Dict[str, Any]:
    """
    Retrieve a random joke.

    :return: A dictionary containing the joke.
    :raises requests.HTTPError: If the request fails.
    """
    base_url = "https://official-joke-api.appspot.com/random_joke"
    try:
        response = requests.get(base_url)
        response.raise_for_status()
        joke = response.json()
        logger.info(f"Retrieved random joke: {joke}")
        return joke
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve random joke: {e}")
        raise


def get_ten_random_jokes() -> List[Dict[str, Any]]:
    """
    Retrieve ten random jokes.

    :return: A list of dictionaries containing jokes.
    :raises requests.HTTPError: If the request fails.
    """
    base_url = "https://official-joke-api.appspot.com/random_ten"
    try:
        response = requests.get(base_url)
        response.raise_for_status()
        jokes = response.json()
        logger.info(f"Retrieved ten random jokes: {jokes}")
        return jokes
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve ten random jokes: {e}")
        raise


def get_random_joke_by_type(joke_type: str) -> Dict[str, Any]:
    """
    Retrieve a random joke of a specific type.

    :param joke_type: The type of joke to retrieve (e.g., 'programming').
    :return: A dictionary containing the joke.
    :raises requests.HTTPError: If the request fails.
    """
    base_url = f"https://official-joke-api.appspot.com/jokes/{joke_type}/random"
    try:
        response = requests.get(base_url)
        response.raise_for_status()
        joke = response.json()
        logger.info(f"Retrieved random joke of type '{joke_type}': {joke}")
        return joke
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve random joke of type '{joke_type}': {e}")
        raise


def get_predicted_age_by_name(name: str, country_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Predict the age based on a given name.

    :param name: The name to predict age for.
    :param country_id: (Optional) The country code.
    :return: A dictionary containing the predicted age information.
    :raises requests.HTTPError: If the request fails.
    """
    base_url = "https://api.agify.io"
    params = {"name": name}
    if country_id:
        params["country_id"] = country_id
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        prediction = response.json()
        logger.info(f"Predicted age for name '{name}': {prediction}")
        return prediction
    except requests.RequestException as e:
        logger.error(f"Failed to predict age for name '{name}': {e}")
        raise


def get_gender_by_name(name: str, country_id: Optional[str] = None, language_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Predicts gender based on a given name.

    :param name: The name to predict gender for.
    :param country_id: (Optional) The country code.
    :param language_id: (Optional) The language code.
    :return: A dictionary containing the predicted gender information.
    :raises requests.HTTPError: If the request fails.
    """
    base_url = "https://api.genderize.io"
    params = {"name": name}
    if country_id:
        params["country_id"] = country_id
    if language_id:
        params["language_id"] = language_id
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        gender_info = response.json()
        logger.info(f"Predicted gender for name '{name}': {gender_info}")
        return gender_info
    except requests.RequestException as e:
        logger.error(f"Failed to predict gender for name '{name}': {e}")
        raise


def get_nationality_by_name(name: str, country_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Predicts nationality based on a given name.

    :param name: The name to predict nationality for.
    :param country_id: (Optional) The country code.
    :return: A dictionary containing the predicted nationality information.
    :raises requests.HTTPError: If the request fails.
    """
    base_url = "https://api.nationalize.io"
    params = {"name": name}
    if country_id:
        params["country_id"] = country_id
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        nationality_info = response.json()
        logger.info(f"Predicted nationality for name '{name}': {nationality_info}")
        return nationality_info
    except requests.RequestException as e:
        logger.error(f"Failed to predict nationality for name '{name}': {e}")
        raise


def get_zip_info(zip_code: str) -> Dict[str, Any]:
    """
    Provides location data for U.S. ZIP codes.

    :param zip_code: The ZIP code to retrieve information for.
    :return: A dictionary containing location data.
    :raises requests.HTTPError: If the request fails.
    """
    base_url = f"https://api.zippopotam.us/us/{zip_code}"
    try:
        response = requests.get(base_url)
        response.raise_for_status()
        zip_info = response.json()
        logger.info(f"Retrieved ZIP info for '{zip_code}': {zip_info}")
        return zip_info
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve ZIP info for '{zip_code}': {e}")
        raise


def get_public_ip() -> Dict[str, Any]:
    """
    Returns the public IP address of the requester.

    :return: A dictionary containing the public IP address.
    :raises requests.HTTPError: If the request fails.
    """
    base_url = "https://api.ipify.org"
    params = {"format": "json"}
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        ip_info = response.json()
        logger.info(f"Retrieved public IP: {ip_info}")
        return ip_info
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve public IP: {e}")
        raise


def get_artwork_data(limit: Optional[int] = None, page: Optional[int] = None, fields: Optional[str] = None) -> Dict[str, Any]:
    """
    Access artwork data from the Art Institute of Chicago's collection.

    :param limit: (Optional) Number of artworks to retrieve.
    :param page: (Optional) Page number to retrieve.
    :param fields: (Optional) Specific fields to include in the response.
    :return: A dictionary containing artwork data.
    :raises requests.HTTPError: If the request fails.
    """
    base_url = "https://api.artic.edu/api/v1/artworks"
    params = {}
    if limit:
        params["limit"] = limit
    if page:
        params["page"] = page
    if fields:
        params["fields"] = fields
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        artwork_data = response.json()
        logger.info(f"Retrieved artwork data: {artwork_data}")
        return artwork_data
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve artwork data: {e}")
        raise


def get_iss_location() -> Dict[str, Any]:
    """
    Get the current location of the International Space Station.

    :return: A dictionary containing the ISS position.
    :raises requests.HTTPError: If the request fails.
    """
    base_url = "http://api.open-notify.org/iss-now.json"
    try:
        response = requests.get(base_url)
        response.raise_for_status()
        iss_location = response.json()
        logger.info(f"Retrieved ISS location: {iss_location}")
        return iss_location
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve ISS location: {e}")
        raise


def get_lyrics(artist: str, title: str) -> Dict[str, Any]:
    """
    Fetch song lyrics by artist and title.

    :param artist: The artist's name.
    :param title: The song title.
    :return: A dictionary containing the song lyrics.
    :raises requests.HTTPError: If the request fails.
    """
    base_url = f"https://api.lyrics.ovh/v1/{artist}/{title}"
    try:
        response = requests.get(base_url)
        response.raise_for_status()
        lyrics = response.json()
        logger.info(f"Retrieved lyrics for '{artist} - {title}': {lyrics}")
        return lyrics
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve lyrics for '{artist} - {title}': {e}")
        raise


def get_random_fox_image() -> Dict[str, Any]:
    """
    Provides a random image of a fox.

    :return: A dictionary containing the image URL and link.
    :raises requests.HTTPError: If the request fails.
    """
    base_url = "https://randomfox.ca/floof/"
    try:
        response = requests.get(base_url)
        response.raise_for_status()
        fox_image = response.json()
        logger.info(f"Retrieved random fox image: {fox_image}")
        return fox_image
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve random fox image: {e}")
        raise

def get_trivia_questions(amount: Optional[int] = 1, category: Optional[int] = None, difficulty: Optional[str] = None, question_type: Optional[str] = None) -> Dict[str, Any]:
    """
    Offers random trivia questions.

    :param amount: Number of questions to retrieve.
    :param category: Category of trivia questions.
    :param difficulty: Difficulty level (e.g., 'easy').
    :param question_type: Type of question (e.g., 'multiple').
    :return: A dictionary containing trivia questions.
    :raises requests.HTTPError: If the request fails.
    """
    base_url = "https://opentdb.com/api.php"
    params = {"amount": amount}
    if category:
        params["category"] = category
    if difficulty:
        params["difficulty"] = difficulty
    if question_type:
        params["type"] = question_type
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        trivia_data = response.json()
        logger.info(f"Retrieved trivia questions: {trivia_data}")
        return trivia_data
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve trivia questions: {e}")
        raise

def get_exchange_rates(base: Optional[str] = "USD") -> Dict[str, Any]:
    """
    Provides current and historical exchange rates.

    :param base: The base currency code (default: 'USD').
    :return: A dictionary containing exchange rates.
    :raises requests.HTTPError: If the request fails.
    """
    base_url = f"https://open.er-api.com/v6/latest/{base}"
    try:
        response = requests.get(base_url)
        response.raise_for_status()
        exchange_data = response.json()
        logger.info(f"Retrieved exchange rates for base '{base}': {exchange_data}")
        return exchange_data
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve exchange rates for base '{base}': {e}")
        raise


if __name__ == "__main__":
    tests = [
        {"name": "get_cat_fact", "func": get_cat_fact, "args": [], "kwargs": {}},
        {"name": "get_cat_fact with max_length", "func": get_cat_fact, "args": [], "kwargs": {"max_length": 50}},
        {"name": "get_multiple_cat_facts", "func": get_multiple_cat_facts, "args": [], "kwargs": {"limit": 3}},
        {"name": "get_cat_breeds", "func": get_cat_breeds, "args": [], "kwargs": {"limit": 2}},
        {"name": "get_random_dog_image", "func": get_random_dog_image, "args": [], "kwargs": {}},
        {"name": "get_multiple_dog_images", "func": get_multiple_dog_images, "args": [], "kwargs": {"number": 3}},
        {"name": "get_random_dog_breed_image", "func": get_random_dog_breed_image, "args": [], "kwargs": {"breed": "hound"}},
        {"name": "get_random_joke", "func": get_random_joke, "args": [], "kwargs": {}},
        {"name": "get_ten_random_jokes", "func": get_ten_random_jokes, "args": [], "kwargs": {}},
        {"name": "get_random_joke_by_type", "func": get_random_joke_by_type, "args": [], "kwargs": {"joke_type": "programming"}},
        {"name": "get_predicted_age_by_name", "func": get_predicted_age_by_name, "args": [], "kwargs": {"name": "michael"}},
        {"name": "get_predicted_age_by_name with country_id", "func": get_predicted_age_by_name, "args": [], "kwargs": {"name": "michael", "country_id": "US"}},
        {"name": "get_random_fox_image", "func": get_random_fox_image, "args": [], "kwargs": {}},
        {"name": "get_trivia_questions", "func": get_trivia_questions, "args": [], "kwargs": {"amount": 1}},
        {"name": "get_exchange_rates", "func": get_exchange_rates, "args": [], "kwargs": {"base": "USD"}},
        {"name": "get_zip_info", "func": get_zip_info, "args": [], "kwargs": {"zip_code": "90210"}},
        {"name": "get_public_ip", "func": get_public_ip, "args": [], "kwargs": {}},
        {"name": "get_artwork_data", "func": get_artwork_data, "args": [], "kwargs": {"limit": 2, "fields": "title,artist_title"}},
        {"name": "get_iss_location", "func": get_iss_location, "args": [], "kwargs": {}},
        {"name": "get_lyrics", "func": get_lyrics, "args": [], "kwargs": {"artist": "Adele", "title": "Hello"}},
        {"name": "get_gender_by_name", "func": get_gender_by_name, "args": [], "kwargs": {"name": "Michael", "country_id": "US"}},
        {"name": "get_nationality_by_name", "func": get_nationality_by_name, "args": [], "kwargs": {"name": "Michael"}}
    ]

    tests_passed = 0
    tests_failed = 0

    for test in tests:
        try:
            result = test["func"](*test.get("args", []), **test.get("kwargs", {}))
            logger.info(f"Test '{test['name']}' passed. Output: {result}")
            tests_passed += 1
        except Exception as e:
            logger.error(f"Test '{test['name']}' failed. Error: {e}")
            tests_failed += 1

    logger.info(f"Tests completed. Passed: {tests_passed}, Failed: {tests_failed}")
