from src.config.serp import get_api_key
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


def get_google_search_results(q: str, location: Optional[str] = None, google_domain: Optional[str] = None, gl: Optional[str] = None, hl: Optional[str] = None, safe: Optional[str] = None, num: Optional[int] = None, start: Optional[int] = None, api_key: str = "") -> Dict[str, Any]:
    """
    Retrieve Google search results using SerpApi.

    :param q: Search query (required).
    :param location: Location for the search (optional).
    :param google_domain: Google domain to use (optional).
    :param gl: Country code for the search (optional).
    :param hl: Language for the search (optional).
    :param safe: Safe search setting (optional).
    :param num: Number of results to return (optional).
    :param start: Starting index for results (optional).
    :param api_key: SerpApi API key (required).
    :return: A dictionary containing the search results.
    :raises requests.HTTPError: If the request fails.
    """
    base_url = "https://serpapi.com/search"
    params = {"q": q, "api_key": api_key}
    if location:
        params["location"] = location
    if google_domain:
        params["google_domain"] = google_domain
    if gl:
        params["gl"] = gl
    if hl:
        params["hl"] = hl
    if safe:
        params["safe"] = safe
    if num:
        params["num"] = num
    if start:
        params["start"] = start
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        search_results = response.json()
        logger.info(f"Retrieved Google search results for query '{q}': {search_results}")
        return search_results
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve Google search results for query '{q}': {e}")
        raise


def get_google_image_search_results(q: str, tbm: str = "isch", gl: Optional[str] = None, hl: Optional[str] = None, api_key: str = "") -> Dict[str, Any]:
    """
    Retrieve Google Images search results using SerpApi.

    :param q: Search query (required).
    :param tbm: Specifies image search (required, default is 'isch').
    :param gl: Country code for the search (optional).
    :param hl: Language for the search (optional).
    :param api_key: SerpApi API key (required).
    :return: A dictionary containing the image search results.
    :raises requests.HTTPError: If the request fails.
    """
    base_url = "https://serpapi.com/search"
    params = {"q": q, "tbm": tbm, "api_key": api_key}
    if gl:
        params["gl"] = gl
    if hl:
        params["hl"] = hl
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        image_results = response.json()
        logger.info(f"Retrieved Google Images search results for query '{q}': {image_results}")
        return image_results
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve Google Images search results for query '{q}': {e}")
        raise


def get_google_location_specific_search(q: str, location: Optional[str] = None, hl: Optional[str] = None, gl: Optional[str] = None, api_key: str = "") -> Dict[str, Any]:
    """
    Retrieve Google search results simulating queries from a given geographic location.

    :param q: Search query (required).
    :param location: Geographic location (optional).
    :param hl: Language for the search (optional).
    :param gl: Country code for the search (optional).
    :param api_key: SerpApi API key (required).
    :return: A dictionary containing location-specific search results.
    :raises requests.HTTPError: If the request fails.
    """
    base_url = "https://serpapi.com/search"
    params = {"q": q, "api_key": api_key}
    if location:
        params["location"] = location
    if hl:
        params["hl"] = hl
    if gl:
        params["gl"] = gl
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        location_results = response.json()
        logger.info(f"Retrieved location-specific search results for query '{q}': {location_results}")
        return location_results
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve location-specific search results for query '{q}': {e}")
        raise


def get_google_news_search(q: str, tbm: str = "nws", hl: Optional[str] = None, gl: Optional[str] = None, num: Optional[int] = None, start: Optional[int] = None, api_key: str = "") -> Dict[str, Any]:
    """
    Retrieve Google News search results using SerpApi.

    :param q: Search query (required).
    :param tbm: Specifies news search (required, default is 'nws').
    :param hl: Language for the search (optional).
    :param gl: Country code for the search (optional).
    :param num: Number of results to return (optional).
    :param start: Starting index for results (optional).
    :param api_key: SerpApi API key (required).
    :return: A dictionary containing the news search results.
    :raises requests.HTTPError: If the request fails.
    """
    base_url = "https://serpapi.com/search"
    params = {"q": q, "tbm": tbm, "api_key": api_key}
    if hl:
        params["hl"] = hl
    if gl:
        params["gl"] = gl
    if num:
        params["num"] = num
    if start:
        params["start"] = start
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        news_results = response.json()
        logger.info(f"Retrieved Google News search results for query '{q}': {news_results}")
        return news_results
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve Google News search results for query '{q}': {e}")
        raise


def get_google_maps_search(q: Optional[str] = None, ll: Optional[str] = None, hl: Optional[str] = None, gl: Optional[str] = None, start: Optional[int] = None, api_key: str = "") -> Dict[str, Any]:
    """
    Retrieve Google Maps search results from SerpApi.

    :param q: Search query (optional).
    :param ll: Latitude and longitude coordinates (optional).
    :param hl: Language for the search (optional).
    :param gl: Country code for the search (optional).
    :param start: Starting index for results (optional).
    :param api_key: SerpApi API key (required).
    :return: A dictionary containing Google Maps search results.
    :raises requests.HTTPError: If the request fails.
    """
    base_url = "https://serpapi.com/search"
    params = {"engine": "google_maps", "api_key": api_key}
    if q:
        params["q"] = q
    if ll:
        params["ll"] = ll
    if hl:
        params["hl"] = hl
    if gl:
        params["gl"] = gl
    if start:
        params["start"] = start
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        maps_results = response.json()
        logger.info(f"Retrieved Google Maps search results for query '{q}': {maps_results}")
        return maps_results
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve Google Maps search results for query '{q}': {e}")
        raise


def get_google_maps_place(place_id: str, hl: Optional[str] = None, gl: Optional[str] = None, api_key: str = "") -> Dict[str, Any]:
    """
    Retrieve details of a specific place on Google Maps using place_id.

    :param place_id: The place ID (required).
    :param hl: Language for the search (optional).
    :param gl: Country code for the search (optional).
    :param api_key: SerpApi API key (required).
    :return: A dictionary containing place details.
    :raises requests.HTTPError: If the request fails.
    """
    base_url = "https://serpapi.com/search"
    params = {"engine": "google_maps", "place_id": place_id, "api_key": api_key}
    if hl:
        params["hl"] = hl
    if gl:
        params["gl"] = gl
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        place_details = response.json()
        logger.info(f"Retrieved place details for place ID '{place_id}': {place_details}")
        return place_details
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve place details for place ID '{place_id}': {e}")
        raise


def get_google_jobs_search(q: str, location: Optional[str] = None, hl: Optional[str] = None, gl: Optional[str] = None, lrad: Optional[int] = None, ltype: Optional[str] = None, next_page_token: Optional[str] = None, api_key: str = "") -> Dict[str, Any]:
    """
    Retrieve Google Jobs search results from SerpApi.

    :param q: Search query (required).
    :param location: Location for the job search (optional).
    :param hl: Language for the search (optional).
    :param gl: Country code for the search (optional).
    :param lrad: Search radius in miles (optional).
    :param ltype: Location type (e.g., 'city') (optional).
    :param next_page_token: Token for the next page of results (optional).
    :param api_key: SerpApi API key (required).
    :return: A dictionary containing job search results.
    :raises requests.HTTPError: If the request fails.
    """
    base_url = "https://serpapi.com/search"
    params = {"engine": "google_jobs", "q": q, "api_key": api_key}
    if location:
        params["location"] = location
    if hl:
        params["hl"] = hl
    if gl:
        params["gl"] = gl
    if lrad:
        params["lrad"] = lrad
    if ltype:
        params["ltype"] = ltype
    if next_page_token:
        params["next_page_token"] = next_page_token
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        jobs_results = response.json()
        logger.info(f"Retrieved Google Jobs search results for query '{q}': {jobs_results}")
        return jobs_results
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve Google Jobs search results for query '{q}': {e}")
        raise


def get_google_shopping_search(q: str, location: Optional[str] = None, google_domain: Optional[str] = None, gl: Optional[str] = None, hl: Optional[str] = None, api_key: str = "") -> Dict[str, Any]:
    """
    Retrieve Google Shopping search results from SerpApi.

    :param q: Search query (required).
    :param location: Location for the search (optional).
    :param google_domain: Google domain to use (optional).
    :param gl: Country code for the search (optional).
    :param hl: Language for the search (optional).
    :param api_key: SerpApi API key (required).
    :return: A dictionary containing shopping search results.
    :raises requests.HTTPError: If the request fails.
    """
    base_url = "https://serpapi.com/search"
    params = {"engine": "google_shopping", "q": q, "api_key": api_key}
    if location:
        params["location"] = location
    if google_domain:
        params["google_domain"] = google_domain
    if gl:
        params["gl"] = gl
    if hl:
        params["hl"] = hl
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        shopping_results = response.json()
        logger.info(f"Retrieved Google Shopping search results for query '{q}': {shopping_results}")
        return shopping_results
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve Google Shopping search results for query '{q}': {e}")
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
        global tests_passed, tests_failed
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
    run_test("get_random_fox_image", get_random_fox_image)
    run_test("get_trivia_questions", get_trivia_questions, amount=1)
    run_test("get_exchange_rates", get_exchange_rates, base="USD")
    run_test("get_zip_info", get_zip_info, zip_code="90210")
    run_test("get_public_ip", get_public_ip)
    run_test("get_artwork_data", get_artwork_data, limit=2, fields="title,artist_title")
    run_test("get_iss_location", get_iss_location)
    run_test("get_lyrics", get_lyrics, artist="Adele", title="Hello")
    run_test("get_gender_by_name", get_gender_by_name, name="Michael", country_id="US")
    run_test("get_nationality_by_name", get_nationality_by_name, name="Michael")

    API_KEY=get_api_key()
    run_test("get_google_search_results", get_google_search_results, q="coffee", location="New York,NY,United States", hl="en", gl="us", api_key=API_KEY)
    run_test("get_google_image_search_results", get_google_image_search_results, q="cat memes", hl="en", gl="us", api_key=API_KEY)
    run_test("get_google_location_specific_search", get_google_location_specific_search, q="best pizza", location="Chicago,Illinois,United States", hl="en", gl="us", api_key=API_KEY)
    run_test("get_google_news_search", get_google_news_search, q="technology news", tbm="nws", hl="en", gl="us", api_key=API_KEY)
    run_test("get_google_maps_search", get_google_maps_search, q="Coffee", ll="@40.7455096,-74.0083012,14z", api_key=API_KEY)
    run_test("get_google_maps_place", get_google_maps_place, place_id="ChIJ9Sto4ahZwokRXpWiQYiOOOo", api_key=API_KEY)
    run_test("get_google_jobs_search", get_google_jobs_search, q="software engineer", location="New York,NY", hl="en", gl="us", api_key=API_KEY)
    run_test("get_google_shopping_search", get_google_shopping_search, q="coffee mug", gl="us", hl="en", api_key=API_KEY)

    logger.info(f"Tests completed. Passed: {tests_passed}, Failed: {tests_failed}")