from src.config.client import initialize_genai_client
from src.config.logging import logger
from google import genai
import time

def generate_content(client: genai.Client, model_id: str, prompt: str) -> str:
    """
    Generates content using the GenAI client and specified model.

    Args:
        client (genai.Client): The GenAI client.
        model_id (str): The model ID to use for generation.
        prompt (str): The prompt for content generation.

    Returns:
        str: The generated content.

    Raises:
        Exception: If content generation fails.
    """
    try:
        logger.info(f"Generating content using model: {model_id}")
        start_time = time.time()  # Start the timer
        response = client.models.generate_content(model=model_id, contents=prompt)
        end_time = time.time()  # End the timer
        elapsed_time = end_time - start_time  # Calculate elapsed time
        logger.info(f"Content generated successfully in {elapsed_time:.2f} seconds.")
        logger.info(f"Response: {response.text.strip()}")
        return response
    except Exception as e:
        logger.error(f"Failed to generate content: {e}")
        raise

def count_tokens(client: genai.Client, model_id: str, prompt: str) -> int:
    """
    Counts the number of tokens in the input prompt using the GenAI client.

    Args:
        client (genai.Client): The GenAI client.
        model_id (str): The model ID to use for token counting.
        prompt (str): The input prompt for token counting.

    Returns:
        int: The number of tokens in the input prompt.

    Raises:
        Exception: If token counting fails.
    """
    try:
        logger.info(f"Counting tokens for model: {model_id}")
        response = client.models.count_tokens(model=model_id, contents=prompt)
        logger.info(f"Token count: {response.total_tokens}")
        return response.total_tokens
    except Exception as e:
        logger.error(f"Failed to count tokens: {e}")
        raise

if __name__ == "__main__":
    try:
        gemini_client: genai.Client = initialize_genai_client()

        MODEL_ID: str = "gemini-2.0-flash-exp"
        prompt: str = "What's the largest planet in our solar system?"

        # Generate content
        generate_content(gemini_client, MODEL_ID, prompt)

        # Count tokens
        count_tokens(gemini_client, MODEL_ID, "What's the highest mountain in Africa?")

    except Exception as e:
        logger.error(f"An error occurred in the main process: {e}")
