from src.config.client import initialize_genai_client
from src.config.logging import logger
from pathlib import Path
from PIL import Image
import requests
import time


def process_image_from_url(image_url: str) -> Image.Image:
    """
    Downloads an image from a given URL and processes it.

    Args:
        image_url (str): URL of the image to process.

    Returns:
        Image.Image: Processed PIL Image object.
    """
    logger.info("Downloading image from URL: %s", image_url)
    try:
        response = requests.get(image_url, timeout=10)
        response.raise_for_status()
        img_bytes = response.content

        img_path = Path("downloaded_image.png")
        img_path.write_bytes(img_bytes)
        logger.info("Image downloaded and saved to %s", img_path)

        image = Image.open(img_path)
        # image.thumbnail([512, 512])
        logger.info("Image processed successfully")
        return image
    except requests.exceptions.RequestException as e:
        logger.error("Failed to download image from URL: %s", e)
        raise


def process_image_from_path(file_path: str) -> Image.Image:
    """
    Loads and processes an image from a local file path.

    Args:
        file_path (str): Local file path of the image to process.

    Returns:
        Image.Image: Processed PIL Image object.
    """
    logger.info("Loading image from local file path: %s", file_path)
    try:
        img_path = Path(file_path)
        if not img_path.exists():
            logger.error("File not found: %s", file_path)
            raise FileNotFoundError(f"File not found: {file_path}")

        image = Image.open(img_path)
        # image.thumbnail([512, 512])
        logger.info("Image processed successfully")
        return image
    except Exception as e:
        logger.error("Failed to process image from path: %s", e)
        raise


def generate_content(client, model_id: str, image: Image.Image, prompt: str) -> str:
    """
    Generates content based on a given image and text prompt using the model.

    Args:
        client: Initialized Generative AI client.
        model_id (str): Model ID for content generation.
        image (Image.Image): PIL Image object.
        prompt (str): Text prompt to guide the content generation.

    Returns:
        str: Generated content text.
    """
    logger.info("Starting content generation with the provided image and text prompt")
    try:
        start_time = time.time()
        response = client.models.generate_content(
            model=model_id,
            contents=[image, prompt]
        )
        elapsed_time = time.time() - start_time
        logger.info("Content generated successfully in %.2f seconds", elapsed_time)
        return response.text
    except Exception as e:
        logger.error("Failed to generate content: %s", e)
        raise


if __name__ == "__main__":
    try:
        # Process image from URL
        image_url = "https://images.arigatotravel.com/wp-content/uploads/2019/06/27234354/shutterstock_119011768-e1560143978361.jpg"
        # image = process_image_from_url(image_url)

        # Alternatively, process image from local path 
        file_path = "./data/sample.png"
        image = process_image_from_path(file_path)

        # Generate content
        prompt = "Write a short and engaging blog post based on this picture."

        MODEL_ID: str = "gemini-2.0-flash-exp"

        # Initialize the client
        client = initialize_genai_client()

        content = generate_content(client, MODEL_ID, image, prompt)

        # Display the output
        logger.info("Generated Content:\n%s", content)
    except Exception as e:
        logger.error("An error occurred during execution: %s", e)
