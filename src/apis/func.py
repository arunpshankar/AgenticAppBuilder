from src.config.logging import logger
from typing import Optional, Dict, Any
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

    logger.info(f"Tests completed. Passed: {tests_passed}, Failed: {tests_failed}")
