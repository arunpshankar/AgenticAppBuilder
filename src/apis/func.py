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


def get_walmart_basic_search(query: str, page: Optional[int] = None, api_key: str = "") -> Dict[str, Any]:
    """
    Retrieve Walmart search results using a query from SerpApi.

    :param query: Search query (required).
    :param page: Page number for results (optional).
    :param api_key: SerpApi API key (required).
    :return: A dictionary containing Walmart search results.
    :raises requests.HTTPError: If the request fails.
    """
    base_url = "https://serpapi.com/search"
    params = {"engine": "walmart", "query": query, "api_key": api_key}
    if page:
        params["page"] = page
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        search_results = response.json()
        logger.info(f"Retrieved Walmart search results for query '{query}': {search_results}")
        return search_results
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve Walmart search results for query '{query}': {e}")
        raise

def get_walmart_category_search(cat_id: str, page: Optional[int] = None, api_key: str = "") -> Dict[str, Any]:
    """
    Retrieve Walmart search results by category ID from SerpApi.

    :param cat_id: Category ID (required).
    :param page: Page number for results (optional).
    :param api_key: SerpApi API key (required).
    :return: A dictionary containing category search results.
    :raises requests.HTTPError: If the request fails.
    """
    base_url = "https://serpapi.com/search"
    params = {"engine": "walmart", "cat_id": cat_id, "api_key": api_key}
    if page:
        params["page"] = page
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        category_results = response.json()
        logger.info(f"Retrieved Walmart category search results for category ID '{cat_id}': {category_results}")
        return category_results
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve Walmart category search results for category ID '{cat_id}': {e}")
        raise

def get_google_trends_interest_over_time(q: str, date: Optional[str] = None, hl: Optional[str] = None, geo: Optional[str] = None, tz: Optional[int] = None, gprop: Optional[str] = None, api_key: str = "") -> Dict[str, Any]:
    """
    Retrieve 'Interest over time' data for a given query using SerpApi's Google Trends API.

    :param q: Search query (required).
    :param date: Date range for the trends (optional).
    :param hl: Language for the search (optional).
    :param geo: Geographic region (optional).
    :param tz: Timezone offset (optional).
    :param gprop: Google property (optional).
    :param api_key: SerpApi API key (required).
    :return: A dictionary containing interest over time data.
    :raises requests.HTTPError: If the request fails.
    """
    base_url = "https://serpapi.com/search"
    params = {"engine": "google_trends", "q": q, "api_key": api_key}
    if date:
        params["date"] = date
    if hl:
        params["hl"] = hl
    if geo:
        params["geo"] = geo
    if tz:
        params["tz"] = tz
    if gprop:
        params["gprop"] = gprop
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        trends_data = response.json()
        logger.info(f"Retrieved Google Trends 'Interest over time' data for query '{q}': {trends_data}")
        return trends_data
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve Google Trends 'Interest over time' data for query '{q}': {e}")
        raise

def get_google_trends_compared_breakdown(q: str, data_type: str = "GEO_MAP", geo: Optional[str] = None, region: Optional[str] = None, date: Optional[str] = None, api_key: str = "") -> Dict[str, Any]:
    """
    Retrieve 'Compared breakdown by region' data for multiple queries using SerpApi's Google Trends API.

    :param q: Comma-separated queries (required).
    :param data_type: Data type (e.g., 'GEO_MAP', required).
    :param geo: Geographic region (optional).
    :param region: Specific region (optional).
    :param date: Date range for the trends (optional).
    :param api_key: SerpApi API key (required).
    :return: A dictionary containing compared breakdown data by region.
    :raises requests.HTTPError: If the request fails.
    """
    base_url = "https://serpapi.com/search"
    params = {"engine": "google_trends", "q": q, "data_type": data_type, "api_key": api_key}
    if geo:
        params["geo"] = geo
    if region:
        params["region"] = region
    if date:
        params["date"] = date
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        breakdown_data = response.json()
        logger.info(f"Retrieved Google Trends 'Compared breakdown by region' data for queries '{q}': {breakdown_data}")
        return breakdown_data
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve Google Trends 'Compared breakdown by region' data for queries '{q}': {e}")
        raise


def get_google_trends_interest_by_region(q: str, data_type: str = "GEO_MAP_0", geo: Optional[str] = None, region: Optional[str] = None, date: Optional[str] = None, api_key: str = "") -> Dict[str, Any]:
    """
    Retrieve 'Interest by region' data for a single query using SerpApi's Google Trends API.

    :param q: Search query (required).
    :param data_type: Data type (required, default is 'GEO_MAP_0').
    :param geo: Geographic region (optional).
    :param region: Specific region (optional).
    :param date: Date range for the trends (optional).
    :param api_key: SerpApi API key (required).
    :return: A dictionary containing interest by region data.
    :raises requests.HTTPError: If the request fails.
    """
    base_url = "https://serpapi.com/search"
    params = {"engine": "google_trends", "q": q, "data_type": data_type, "api_key": api_key}
    if geo:
        params["geo"] = geo
    if region:
        params["region"] = region
    if date:
        params["date"] = date
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        region_data = response.json()
        logger.info(f"Retrieved Google Trends 'Interest by region' data for query '{q}': {region_data}")
        return region_data
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve Google Trends 'Interest by region' data for query '{q}': {e}")
        raise

def get_google_hotels_basic_search(q: str, check_in_date: str, check_out_date: str, hl: Optional[str] = None, gl: Optional[str] = None, currency: Optional[str] = None, api_key: str = "") -> Dict[str, Any]:
    """
    Retrieve hotel listings by location and date range from SerpApi's Google Hotels API.

    :param q: Search query (required).
    :param check_in_date: Check-in date (required).
    :param check_out_date: Check-out date (required).
    :param hl: Language for the search (optional).
    :param gl: Geographic region for the search (optional).
    :param currency: Currency for prices (optional).
    :param api_key: SerpApi API key (required).
    :return: A dictionary containing hotel listings.
    :raises requests.HTTPError: If the request fails.
    """
    base_url = "https://serpapi.com/search"
    params = {"engine": "google_hotels", "q": q, "check_in_date": check_in_date, "check_out_date": check_out_date, "api_key": api_key}
    if hl:
        params["hl"] = hl
    if gl:
        params["gl"] = gl
    if currency:
        params["currency"] = currency
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        hotel_data = response.json()
        logger.info(f"Retrieved Google Hotels listings for query '{q}': {hotel_data}")
        return hotel_data
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve Google Hotels listings for query '{q}': {e}")
        raise

def get_google_vacation_rentals(q: str, check_in_date: str, check_out_date: str, vacation_rentals: Optional[bool] = None, bedrooms: Optional[int] = None, bathrooms: Optional[int] = None, api_key: str = "") -> Dict[str, Any]:
    """
    Retrieve vacation rental listings instead of hotels by using SerpApi's Google Hotels API.

    :param q: Search query (required).
    :param check_in_date: Check-in date (required).
    :param check_out_date: Check-out date (required).
    :param vacation_rentals: Whether to retrieve vacation rentals (optional).
    :param bedrooms: Number of bedrooms (optional).
    :param bathrooms: Number of bathrooms (optional).
    :param api_key: SerpApi API key (required).
    :return: A dictionary containing vacation rental listings.
    :raises requests.HTTPError: If the request fails.
    """
    base_url = "https://serpapi.com/search"
    params = {"engine": "google_hotels", "q": q, "check_in_date": check_in_date, "check_out_date": check_out_date, "api_key": api_key}
    if vacation_rentals:
        params["vacation_rentals"] = vacation_rentals
    if bedrooms:
        params["bedrooms"] = bedrooms
    if bathrooms:
        params["bathrooms"] = bathrooms
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        rental_data = response.json()
        logger.info(f"Retrieved Google Vacation Rentals listings for query '{q}': {rental_data}")
        return rental_data
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve Google Vacation Rentals listings for query '{q}': {e}")
        raise

def get_google_hotels_property_details(property_token: str, api_key: str = "") -> Dict[str, Any]:
    """
    Retrieve detailed information about a specific property by using property_token.

    :param property_token: Property token (required).
    :param api_key: SerpApi API key (required).
    :return: A dictionary containing property details.
    :raises requests.HTTPError: If the request fails.
    """
    base_url = "https://serpapi.com/search"
    params = {"engine": "google_hotels", "property_token": property_token, "api_key": api_key}
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        property_details = response.json()
        logger.info(f"Retrieved property details for token '{property_token}': {property_details}")
        return property_details
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve property details for token '{property_token}': {e}")
        raise

def get_google_local_basic_search(q: str, location: Optional[str] = None, hl: Optional[str] = None, gl: Optional[str] = None, api_key: str = "") -> Dict[str, Any]:
    """
    Retrieve local business results by query using SerpApi's Google Local API.

    :param q: Search query (required).
    :param location: Location for the search (optional).
    :param hl: Language for the search (optional).
    :param gl: Geographic region for the search (optional).
    :param api_key: SerpApi API key (required).
    :return: A dictionary containing local business results.
    :raises requests.HTTPError: If the request fails.
    """
    base_url = "https://serpapi.com/search"
    params = {"engine": "google_local", "q": q, "api_key": api_key}
    if location:
        params["location"] = location
    if hl:
        params["hl"] = hl
    if gl:
        params["gl"] = gl
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        local_results = response.json()
        logger.info(f"Retrieved Google Local search results for query '{q}': {local_results}")
        return local_results
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve Google Local search results for query '{q}': {e}")
        raise



def get_google_finance_basic_search(q: str, hl: Optional[str] = None, api_key: str = "") -> Dict[str, Any]:
    """
    Retrieve Google Finance data for a given ticker or search query from SerpApi.

    :param q: Search query or ticker (required).
    :param hl: Language for the search (optional).
    :param api_key: SerpApi API key (required).
    :return: A dictionary containing Google Finance data.
    :raises requests.HTTPError: If the request fails.
    """
    base_url = "https://serpapi.com/search"
    params = {"engine": "google_finance", "q": q, "api_key": api_key}
    if hl:
        params["hl"] = hl
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        finance_data = response.json()
        logger.info(f"Retrieved Google Finance data for query '{q}': {finance_data}")
        return finance_data
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve Google Finance data for query '{q}': {e}")
        raise

def get_google_finance_currency_exchange(q: str, hl: Optional[str] = None, api_key: str = "") -> Dict[str, Any]:
    """
    Retrieve exchange rate data for a currency pair using SerpApi.

    :param q: Currency pair (e.g., 'USD/EUR') (required).
    :param hl: Language for the search (optional).
    :param api_key: SerpApi API key (required).
    :return: A dictionary containing currency exchange rate data.
    :raises requests.HTTPError: If the request fails.
    """
    base_url = "https://serpapi.com/search"
    params = {"engine": "google_finance", "q": q, "api_key": api_key}
    if hl:
        params["hl"] = hl
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        exchange_data = response.json()
        logger.info(f"Retrieved currency exchange data for query '{q}': {exchange_data}")
        return exchange_data
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve currency exchange data for query '{q}': {e}")
        raise

def get_google_product_offers(product_id: str, offers: int = 1, start: Optional[int] = None, filter: Optional[str] = None, api_key: str = "") -> Dict[str, Any]:
    """
    Retrieve online sellers (offers) for a given product_id using SerpApi.

    :param product_id: Product ID (required).
    :param offers: Indicates offers are to be retrieved (default: 1).
    :param start: Starting page or index for results (optional).
    :param filter: Additional filters for the search (optional).
    :param api_key: SerpApi API key (required).
    :return: A dictionary containing product offers data.
    :raises requests.HTTPError: If the request fails.
    """
    base_url = "https://serpapi.com/search"
    params = {"engine": "google_product", "product_id": product_id, "offers": offers, "api_key": api_key}
    if start:
        params["start"] = start
    if filter:
        params["filter"] = filter
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        offers_data = response.json()
        logger.info(f"Retrieved product offers for product ID '{product_id}': {offers_data}")
        return offers_data
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve product offers for product ID '{product_id}': {e}")
        raise

def get_google_product_specs(product_id: str, specs: int = 1, hl: Optional[str] = None, gl: Optional[str] = None, api_key: str = "") -> Dict[str, Any]:
    """
    Retrieve detailed specifications for a given product_id using SerpApi.

    :param product_id: Product ID (required).
    :param specs: Indicates specifications are to be retrieved (default: 1).
    :param hl: Language for the search (optional).
    :param gl: Geographic region for the search (optional).
    :param api_key: SerpApi API key (required).
    :return: A dictionary containing product specifications data.
    :raises requests.HTTPError: If the request fails.
    """
    base_url = "https://serpapi.com/search"
    params = {"engine": "google_product", "product_id": product_id, "specs": specs, "api_key": api_key}
    if hl:
        params["hl"] = hl
    if gl:
        params["gl"] = gl
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        specs_data = response.json()
        logger.info(f"Retrieved product specifications for product ID '{product_id}': {specs_data}")
        return specs_data
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve product specifications for product ID '{product_id}': {e}")
        raise

def get_google_product_reviews(product_id: str, reviews: int = 1, filter: Optional[str] = None, api_key: str = "") -> Dict[str, Any]:
    """
    Retrieve reviews for a given product_id using SerpApi.

    :param product_id: Product ID (required).
    :param reviews: Indicates reviews are to be retrieved (default: 1).
    :param filter: Additional filters for the reviews (optional).
    :param api_key: SerpApi API key (required).
    :return: A dictionary containing product reviews data.
    :raises requests.HTTPError: If the request fails.
    """
    base_url = "https://serpapi.com/search"
    params = {"engine": "google_product", "product_id": product_id, "reviews": reviews, "api_key": api_key}
    if filter:
        params["filter"] = filter
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        reviews_data = response.json()
        logger.info(f"Retrieved product reviews for product ID '{product_id}': {reviews_data}")
        return reviews_data
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve product reviews for product ID '{product_id}': {e}")
        raise

def get_google_events_basic_search(q: str, hl: Optional[str] = None, gl: Optional[str] = None, location: Optional[str] = None, api_key: str = "") -> Dict[str, Any]:
    """
    Retrieve events based on a query using SerpApi's Google Events API.

    :param q: Search query (e.g., 'Events in Austin, TX') (required).
    :param hl: Language for the search (optional).
    :param gl: Geographic region for the search (optional).
    :param location: Location for the events (optional).
    :param api_key: SerpApi API key (required).
    :return: A dictionary containing events data.
    :raises requests.HTTPError: If the request fails.
    """
    base_url = "https://serpapi.com/search"
    params = {"engine": "google_events", "q": q, "api_key": api_key}
    if hl:
        params["hl"] = hl
    if gl:
        params["gl"] = gl
    if location:
        params["location"] = location
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        events_data = response.json()
        logger.info(f"Retrieved events for query '{q}': {events_data}")
        return events_data
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve events for query '{q}': {e}")
        raise

def get_google_flights_round_trip(departure_id: Optional[str] = None, arrival_id: Optional[str] = None, outbound_date: Optional[str] = None, return_date: str = "", hl: Optional[str] = None, gl: Optional[str] = None, currency: Optional[str] = None, api_key: str = "") -> Dict[str, Any]:
    """
    Retrieve round-trip flight results using SerpApi's Google Flights API.

    :param departure_id: Departure location (optional).
    :param arrival_id: Arrival location (optional).
    :param outbound_date: Outbound flight date (optional).
    :param return_date: Return flight date (required for round trip).
    :param hl: Language for the search (optional).
    :param gl: Geographic region for the search (optional).
    :param currency: Currency for prices (optional).
    :param api_key: SerpApi API key (required).
    :return: A dictionary containing round-trip flight data.
    :raises requests.HTTPError: If the request fails.
    """
    base_url = "https://serpapi.com/search"
    params = {"engine": "google_flights", "type": 1, "return_date": return_date, "api_key": api_key}
    if departure_id:
        params["departure_id"] = departure_id
    if arrival_id:
        params["arrival_id"] = arrival_id
    if outbound_date:
        params["outbound_date"] = outbound_date
    if hl:
        params["hl"] = hl
    if gl:
        params["gl"] = gl
    if currency:
        params["currency"] = currency
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        flights_data = response.json()
        logger.info(f"Retrieved round-trip flight results: {flights_data}")
        return flights_data
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve round-trip flight results: {e}")
        raise

def get_google_flights_one_way(departure_id: Optional[str] = None, arrival_id: Optional[str] = None, outbound_date: Optional[str] = None, stops: int = 1, max_price: Optional[int] = None, hl: Optional[str] = None, gl: Optional[str] = None, currency: Optional[str] = None, api_key: str = "") -> Dict[str, Any]:
    """
    Retrieve one-way flight results with filters using SerpApi's Google Flights API.

    :param departure_id: Departure location (optional).
    :param arrival_id: Arrival location (optional).
    :param outbound_date: Outbound flight date (optional).
    :param stops: Number of stops (default is 1 for nonstop).
    :param max_price: Maximum price for flights (optional).
    :param hl: Language for the search (optional).
    :param gl: Geographic region for the search (optional).
    :param currency: Currency for prices (optional).
    :param api_key: SerpApi API key (required).
    :return: A dictionary containing one-way flight data.
    :raises requests.HTTPError: If the request fails.
    """
    base_url = "https://serpapi.com/search"
    params = {"engine": "google_flights", "type": 2, "stops": stops, "api_key": api_key}
    if departure_id:
        params["departure_id"] = departure_id
    if arrival_id:
        params["arrival_id"] = arrival_id
    if outbound_date:
        params["outbound_date"] = outbound_date
    if max_price:
        params["max_price"] = max_price
    if hl:
        params["hl"] = hl
    if gl:
        params["gl"] = gl
    if currency:
        params["currency"] = currency
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        flights_data = response.json()
        logger.info(f"Retrieved one-way flight results: {flights_data}")
        return flights_data
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve one-way flight results: {e}")
        raise

def get_google_flights_multi_city(multi_city_json: List[Dict[str, str]], hl: Optional[str] = None, gl: Optional[str] = None, currency: Optional[str] = None, api_key: str = "") -> Dict[str, Any]:
    """
    Retrieve multi-city flight results using SerpApi's Google Flights API.

    :param multi_city_json: JSON list of segments specifying departure, arrival, and date (required).
    :param hl: Language for the search (optional).
    :param gl: Geographic region for the search (optional).
    :param currency: Currency for prices (optional).
    :param api_key: SerpApi API key (required).
    :return: A dictionary containing multi-city flight data.
    :raises requests.HTTPError: If the request fails.
    """
    base_url = "https://serpapi.com/search"
    params = {"engine": "google_flights", "type": 3, "multi_city_json": multi_city_json, "api_key": api_key}
    if hl:
        params["hl"] = hl
    if gl:
        params["gl"] = gl
    if currency:
        params["currency"] = currency
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        flights_data = response.json()
        logger.info(f"Retrieved multi-city flight results: {flights_data}")
        return flights_data
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve multi-city flight results: {e}")
        raise

def get_google_flights_with_airline_filters(departure_id: Optional[str] = None, arrival_id: Optional[str] = None, outbound_date: Optional[str] = None, return_date: Optional[str] = None, include_airlines: Optional[str] = None, exclude_airlines: Optional[str] = None, hl: Optional[str] = None, gl: Optional[str] = None, currency: Optional[str] = None, api_key: str = "") -> Dict[str, Any]:
    """
    Retrieve flight results including or excluding specific airlines or alliances using SerpApi's Google Flights API.

    :param departure_id: Departure location (optional).
    :param arrival_id: Arrival location (optional).
    :param outbound_date: Outbound flight date (optional).
    :param return_date: Return flight date (optional).
    :param include_airlines: Airlines to include in the search (optional).
    :param exclude_airlines: Airlines to exclude from the search (optional).
    :param hl: Language for the search (optional).
    :param gl: Geographic region for the search (optional).
    :param currency: Currency for prices (optional).
    :param api_key: SerpApi API key (required).
    :return: A dictionary containing filtered flight data.
    :raises requests.HTTPError: If the request fails.
    """
    base_url = "https://serpapi.com/search"
    params = {"engine": "google_flights", "type": 1, "api_key": api_key}
    if departure_id:
        params["departure_id"] = departure_id
    if arrival_id:
        params["arrival_id"] = arrival_id
    if outbound_date:
        params["outbound_date"] = outbound_date
    if return_date:
        params["return_date"] = return_date
    if include_airlines:
        params["include_airlines"] = include_airlines
    if exclude_airlines:
        params["exclude_airlines"] = exclude_airlines
    if hl:
        params["hl"] = hl
    if gl:
        params["gl"] = gl
    if currency:
        params["currency"] = currency
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        flights_data = response.json()
        logger.info(f"Retrieved filtered flight results: {flights_data}")
        return flights_data
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve filtered flight results: {e}")
        raise


def get_google_flights_booking_options(booking_token: str, api_key: str = "") -> Dict[str, Any]:
    """
    Retrieve booking options for a selected flight itinerary using SerpApi's Google Flights API.

    :param booking_token: Booking token for the selected flight itinerary (required).
    :param api_key: SerpApi API key (required).
    :return: A dictionary containing booking options.
    :raises requests.HTTPError: If the request fails.
    """
    base_url = "https://serpapi.com/search"
    params = {"engine": "google_flights", "booking_token": booking_token, "api_key": api_key}
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        booking_data = response.json()
        logger.info(f"Retrieved booking options for booking token '{booking_token}': {booking_data}")
        return booking_data
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve booking options for booking token '{booking_token}': {e}")
        raise

def get_google_lens_basic_search(url: str, hl: Optional[str] = None, country: Optional[str] = None, api_key: str = "") -> Dict[str, Any]:
    """
    Retrieve Google Lens results by providing an image URL using SerpApi.

    :param url: URL of the image (required).
    :param hl: Language for the search (optional).
    :param country: Country for the search (optional).
    :param api_key: SerpApi API key (required).
    :return: A dictionary containing Google Lens results.
    :raises requests.HTTPError: If the request fails.
    """
    base_url = "https://serpapi.com/search"
    params = {"engine": "google_lens", "url": url, "api_key": api_key}
    if hl:
        params["hl"] = hl
    if country:
        params["country"] = country
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        lens_data = response.json()
        logger.info(f"Retrieved Google Lens results for image URL '{url}': {lens_data}")
        return lens_data
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve Google Lens results for image URL '{url}': {e}")
        raise

def get_google_play_query_search(q: Optional[str] = None, hl: Optional[str] = None, gl: Optional[str] = None, api_key: str = "") -> Dict[str, Any]:
    """
    Retrieve app listings from the Google Play Store by search query using SerpApi.

    :param q: Search query (optional).
    :param hl: Language for the search (optional).
    :param gl: Geographic region for the search (optional).
    :param api_key: SerpApi API key (required).
    :return: A dictionary containing app listings.
    :raises requests.HTTPError: If the request fails.
    """
    base_url = "https://serpapi.com/search"
    params = {"engine": "google_play", "api_key": api_key}
    if q:
        params["q"] = q
    if hl:
        params["hl"] = hl
    if gl:
        params["gl"] = gl
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        play_data = response.json()
        logger.info(f"Retrieved Google Play app listings for query '{q}': {play_data}")
        return play_data
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve Google Play app listings for query '{q}': {e}")
        raise

def get_google_play_category_search(apps_category: Optional[str] = None, hl: Optional[str] = None, gl: Optional[str] = None, api_key: str = "") -> Dict[str, Any]:
    """
    Retrieve apps from a specific Google Play category using SerpApi.

    :param apps_category: Category of apps (optional).
    :param hl: Language for the search (optional).
    :param gl: Geographic region for the search (optional).
    :param api_key: SerpApi API key (required).
    :return: A dictionary containing apps from the specified category.
    :raises requests.HTTPError: If the request fails.
    """
    base_url = "https://serpapi.com/search"
    params = {"engine": "google_play", "api_key": api_key}
    if apps_category:
        params["apps_category"] = apps_category
    if hl:
        params["hl"] = hl
    if gl:
        params["gl"] = gl
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        category_data = response.json()
        logger.info(f"Retrieved Google Play apps for category '{apps_category}': {category_data}")
        return category_data
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve Google Play apps for category '{apps_category}': {e}")
        raise

def get_google_reverse_image_search(image_url: str, hl: Optional[str] = None, gl: Optional[str] = None, google_domain: Optional[str] = None, api_key: str = "") -> Dict[str, Any]:
    """
    Retrieve Google reverse image search results by providing an image URL using SerpApi.

    :param image_url: URL of the image (required).
    :param hl: Language for the search (optional).
    :param gl: Geographic region for the search (optional).
    :param google_domain: Google domain to use for the search (optional).
    :param api_key: SerpApi API key (required).
    :return: A dictionary containing reverse image search results.
    :raises requests.HTTPError: If the request fails.
    """
    base_url = "https://serpapi.com/search"
    params = {"engine": "google_reverse_image", "image_url": image_url, "api_key": api_key}
    if hl:
        params["hl"] = hl
    if gl:
        params["gl"] = gl
    if google_domain:
        params["google_domain"] = google_domain
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        reverse_image_data = response.json()
        logger.info(f"Retrieved reverse image search results for image URL '{image_url}': {reverse_image_data}")
        return reverse_image_data
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve reverse image search results for image URL '{image_url}': {e}")
        raise


def get_google_videos_basic_search(q: str, hl: Optional[str] = None, gl: Optional[str] = None, api_key: str = "") -> Dict[str, Any]:
    """
    Retrieve video search results from Google Videos by query using SerpApi.

    :param q: Search query (required).
    :param hl: Language for the search (optional).
    :param gl: Geographic region for the search (optional).
    :param api_key: SerpApi API key (required).
    :return: A dictionary containing video search results.
    :raises requests.HTTPError: If the request fails.
    """
    base_url = "https://serpapi.com/search"
    params = {"engine": "google_videos", "q": q, "api_key": api_key}
    if hl:
        params["hl"] = hl
    if gl:
        params["gl"] = gl
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        video_data = response.json()
        logger.info(f"Retrieved Google Videos results for query '{q}': {video_data}")
        return video_data
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve Google Videos results for query '{q}': {e}")
        raise

def get_youtube_basic_search(search_query: str, hl: Optional[str] = None, gl: Optional[str] = None, api_key: str = "") -> Dict[str, Any]:
    """
    Retrieve YouTube search results by providing a search query using SerpApi.

    :param search_query: Search query (required).
    :param hl: Language for the search (optional).
    :param gl: Geographic region for the search (optional).
    :param api_key: SerpApi API key (required).
    :return: A dictionary containing YouTube search results.
    :raises requests.HTTPError: If the request fails.
    """
    base_url = "https://serpapi.com/search"
    params = {"engine": "youtube", "search_query": search_query, "api_key": api_key}
    if hl:
        params["hl"] = hl
    if gl:
        params["gl"] = gl
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        youtube_data = response.json()
        logger.info(f"Retrieved YouTube results for query '{search_query}': {youtube_data}")
        return youtube_data
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve YouTube results for query '{search_query}': {e}")
        raise

def get_yelp_basic_search(find_loc: str, find_desc: Optional[str] = None, yelp_domain: Optional[str] = None, api_key: str = "") -> Dict[str, Any]:
    """
    Retrieve Yelp search results by location and optional query using SerpApi.

    :param find_loc: Location for the search (required).
    :param find_desc: Description of the search (optional).
    :param yelp_domain: Yelp domain to use for the search (optional).
    :param api_key: SerpApi API key (required).
    :return: A dictionary containing Yelp search results.
    :raises requests.HTTPError: If the request fails.
    """
    base_url = "https://serpapi.com/search"
    params = {"engine": "yelp", "find_loc": find_loc, "api_key": api_key}
    if find_desc:
        params["find_desc"] = find_desc
    if yelp_domain:
        params["yelp_domain"] = yelp_domain
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        yelp_data = response.json()
        logger.info(f"Retrieved Yelp results for location '{find_loc}': {yelp_data}")
        return yelp_data
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve Yelp results for location '{find_loc}': {e}")
        raise

def get_yelp_category_search(find_loc: str, cflt: Optional[str] = None, api_key: str = "") -> Dict[str, Any]:
    """
    Retrieve Yelp results for a specific category by location using SerpApi.

    :param find_loc: Location for the search (required).
    :param cflt: Category filter (optional).
    :param api_key: SerpApi API key (required).
    :return: A dictionary containing Yelp category search results.
    :raises requests.HTTPError: If the request fails.
    """
    base_url = "https://serpapi.com/search"
    params = {"engine": "yelp", "find_loc": find_loc, "api_key": api_key}
    if cflt:
        params["cflt"] = cflt
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        category_data = response.json()
        logger.info(f"Retrieved Yelp category results for location '{find_loc}' with category '{cflt}': {category_data}")
        return category_data
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve Yelp category results for location '{find_loc}': {e}")
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

    run_test("get_walmart_basic_search", get_walmart_basic_search, query="coffee maker", page=1, api_key="YOUR_API_KEY")
    run_test("get_walmart_category_search", get_walmart_category_search, cat_id="976759_976787", page=1, api_key="YOUR_API_KEY")
    run_test("get_google_trends_interest_over_time", get_google_trends_interest_over_time, q="coffee", date="today 12-m", geo="US", api_key="YOUR_API_KEY")
    run_test("get_google_trends_compared_breakdown", get_google_trends_compared_breakdown, q="coffee,tea", data_type="GEO_MAP", geo="US", date="today 3-m", api_key="YOUR_API_KEY")
    run_test("get_google_trends_interest_by_region", get_google_trends_interest_by_region, q="chocolate", data_type="GEO_MAP_0", geo="GB", region="CITY", date="today 5-y", api_key="YOUR_API_KEY")
    run_test("get_google_hotels_basic_search", get_google_hotels_basic_search, q="New York", check_in_date="2024-12-21", check_out_date="2024-12-22", hl="en", gl="us", currency="USD", api_key="YOUR_API_KEY")
    run_test("get_google_vacation_rentals", get_google_vacation_rentals, q="Hawaii", check_in_date="2024-12-21", check_out_date="2024-12-22", vacation_rentals=True, bedrooms=2, bathrooms=1, api_key="YOUR_API_KEY")
    run_test("get_google_hotels_property_details", get_google_hotels_property_details, property_token="AB123XYZ", api_key="YOUR_API_KEY")
    run_test("get_google_local_basic_search", get_google_local_basic_search, q="coffee shops", location="New York,NY", hl="en", gl="us", api_key="YOUR_API_KEY")

    run_test("get_google_finance_basic_search", get_google_finance_basic_search, q="NASDAQ:GOOGL", hl="en", api_key="YOUR_API_KEY")
    run_test("get_google_finance_currency_exchange", get_google_finance_currency_exchange, q="USD/EUR", hl="en", api_key="YOUR_API_KEY")
    run_test("get_google_product_offers", get_google_product_offers, product_id="1234567890123456789", offers=1, filter="scoring:p", api_key="YOUR_API_KEY")
    run_test("get_google_product_specs", get_google_product_specs, product_id="1234567890123456789", specs=1, hl="en", gl="us", api_key="YOUR_API_KEY")
    run_test("get_google_product_reviews", get_google_product_reviews, product_id="1234567890123456789", reviews=1, filter="rnum:50", api_key="YOUR_API_KEY")

    run_test("get_google_events_basic_search", get_google_events_basic_search, q="Events in Austin TX", hl="en", gl="us", location="Austin,Texas,United States", api_key="YOUR_API_KEY")
    run_test("get_google_flights_round_trip", get_google_flights_round_trip, departure_id="AUS", arrival_id="CDG", outbound_date="2024-12-21", return_date="2024-12-27", hl="en", gl="us", currency="USD", api_key="YOUR_API_KEY")
    run_test("get_google_flights_one_way", get_google_flights_one_way, departure_id="JFK", arrival_id="SFO", outbound_date="2024-12-21", stops=1, max_price=500, hl="en", gl="us", currency="USD", api_key="YOUR_API_KEY")
    run_test("get_google_flights_multi_city", get_google_flights_multi_city, multi_city_json=[{"departure_id":"CDG","arrival_id":"NRT","date":"2024-12-27"},{"departure_id":"NRT","arrival_id":"LAX,SEA","date":"2025-01-03"},{"departure_id":"LAX,SEA","arrival_id":"AUS","date":"2025-01-10"}], hl="en", gl="us", currency="USD", api_key="YOUR_API_KEY")
    run_test("get_google_flights_with_airline_filters", get_google_flights_with_airline_filters, departure_id="LHR", arrival_id="JFK", outbound_date="2024-12-21", return_date="2024-12-30", include_airlines="ONEWORLD", hl="en", gl="us", currency="USD", api_key="YOUR_API_KEY")

    run_test("get_google_flights_booking_options", get_google_flights_booking_options, booking_token="ABC123xyz", api_key="YOUR_API_KEY")
    run_test("get_google_lens_basic_search", get_google_lens_basic_search, url="https://i.imgur.com/HBrB8p0.png", hl="en", country="us", api_key="YOUR_API_KEY")
    run_test("get_google_play_query_search", get_google_play_query_search, q="weather apps", hl="en", gl="us", api_key="YOUR_API_KEY")
    run_test("get_google_play_category_search", get_google_play_category_search, apps_category="GAME_ACTION", hl="en", gl="us", api_key="YOUR_API_KEY")
    run_test("get_google_reverse_image_search", get_google_reverse_image_search, image_url="https://i.imgur.com/5bGzZi7.jpg", hl="en", gl="us", google_domain="google.com", api_key="YOUR_API_KEY")

    run_test("get_google_videos_basic_search", get_google_videos_basic_search, q="funny cats", hl="en", gl="us", api_key="YOUR_API_KEY")
    run_test("get_youtube_basic_search", get_youtube_basic_search, search_query="star wars", hl="en", gl="us", api_key="YOUR_API_KEY")
    run_test("get_yelp_basic_search", get_yelp_basic_search, find_loc="San Francisco, CA", find_desc="pizza", yelp_domain="yelp.com", api_key="YOUR_API_KEY")
    run_test("get_yelp_category_search", get_yelp_category_search, find_loc="Los Angeles, CA", cflt="restaurants", api_key="YOUR_API_KEY")

    logger.info(f"Tests completed. Passed: {tests_passed}, Failed: {tests_failed}")