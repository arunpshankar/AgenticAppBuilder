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



if __name__ == "__main__":
    tests_passed = 0
    tests_failed = 0

    def run_test(test_name: str, func, *args, **kwargs):
        """
        Run a test case and log the result.

        :param test_name: Name of the test.
        :param func: Function to test.
        :param args: Positional arguments for the function.
        :param kwargs: Keyword arguments for the function.
        """
        global tests_passed, tests_failed  # Declare as global
        try:
            result = func(*args, **kwargs)
            logger.info(f"Test '{test_name}' passed. Output: {result}")
            tests_passed += 1
        except Exception as e:
            logger.error(f"Test '{test_name}' failed. Error: {e}")
            tests_failed += 1

    # Running tests
    run_test("get_cat_fact", get_cat_fact)
    run_test("get_cat_fact with max_length", get_cat_fact, max_length=50)
    run_test("get_multiple_cat_facts", get_multiple_cat_facts, limit=3)
    run_test("get_cat_breeds", get_cat_breeds, limit=2)
    run_test("get_random_dog_image", get_random_dog_image)
    run_test("get_multiple_dog_images", get_multiple_dog_images, number=3)
    run_test("get_random_dog_breed_image", get_random_dog_breed_image, breed="hound")
    run_test("get_random_joke", get_random_joke)
    run_test("get_ten_random_jokes", get_ten_random_jokes)
    run_test("get_random_joke_by_type", get_random_joke_by_type, joke_type="programming")
    run_test("get_predicted_age_by_name", get_predicted_age_by_name, name="michael")
    run_test("get_predicted_age_by_name with country_id", get_predicted_age_by_name, name="michael", country_id="US")

    logger.info(f"Tests completed. Passed: {tests_passed}, Failed: {tests_failed}")
