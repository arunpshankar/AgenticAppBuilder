import requests
import random

def fetch_cat_or_dog_fact():
    """Fetches a random cat or dog fact using the catfact.ninja and dog.ceo APIs.
    Chooses randomly between cat and dog facts.
    Returns:
        str: A string containing the fact.
    """
    if random.choice([True, False]): # Randomly choose cat or dog
      response = requests.get("https://catfact.ninja/fact")
      response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
      data = response.json()
      return data["fact"]
    else:
        response = requests.get("https://dog.ceo/api/breeds/image/random")
        response.raise_for_status()
        data = response.json()
        return f"Here's a dog image url: {data['message']}"


def fetch_random_fox_image():
    """Fetches a random fox image using the randomfox.ca API.
    Returns:
        str: URL of the random fox image.
    """
    response = requests.get("https://randomfox.ca/floof/")
    response.raise_for_status()
    data = response.json()
    return data["image"]


def fetch_art_institute_artwork():
    """Fetches a random piece of art from the Art Institute of Chicago API.
     Returns:
        dict: Dictionary containing data for the random art work.
    """
    response = requests.get("https://api.artic.edu/api/v1/artworks?limit=1")
    response.raise_for_status()
    data = response.json()
    return data


def generate_adventure_prompt(animal_fact, fox_image_url, art_institute_data):
      """
      Generates a creative narrative prompt by combining animal facts,
      a fox image URL, and the feel of artwork from the Art Institute.

      Args:
        animal_fact (str): A fact about a cat or a dog
        fox_image_url (str): URL of the fox image
        art_institute_data (dict): Data dictionary from the Art Institute of Chicago.

      Returns:
            str: A creative prompt.
      """
      artwork_title = art_institute_data["data"][0].get("title","an unknown artwork")
      return (
        f"Imagine a scene where {animal_fact.lower()}, "
        f"a mischievous fox from {fox_image_url.split('/')[-1].split('.')[0]} "
        f"is found gazing at {artwork_title.lower()}. "
        "What whimsical adventure unfolds?"
      )

def create_adventure():
  """Orchestrates the fetching of data from the APIs and returns a combined response.
      Returns:
        dict: Dictionary with all data of the adventure.
    """
  try:
        animal_fact = fetch_cat_or_dog_fact()
        fox_image_url = fetch_random_fox_image()
        art_institute_data = fetch_art_institute_artwork()
        adventure_prompt = generate_adventure_prompt(animal_fact, fox_image_url, art_institute_data)


        return {
            "animal_fact": animal_fact,
            "fox_image": fox_image_url,
            "art_institute_data": art_institute_data,
            "adventure_prompt": adventure_prompt
        }

  except requests.exceptions.RequestException as e:
        print(f"An error occurred during API request: {e}")
        return None

if __name__ == "__main__":
    adventure_data = create_adventure()
    if adventure_data:
        print("Animal Fact:", adventure_data["animal_fact"])
        print("Fox Image:", adventure_data["fox_image"])
        print("Art Institute Data:", adventure_data["art_institute_data"])
        print("Adventure Prompt:", adventure_data["adventure_prompt"])
    else:
      print("Could not create adventure.")