from src.config.logging import logger 
from typing import Dict 
from typing import Any 
import yaml


def load_api_key(file_path: str) -> str:
    """
    Loads the API key from a YAML file.

    Args:
        file_path (str): Path to the YAML file containing the API key.

    Returns:
        str: The API key.

    Raises:
        FileNotFoundError: If the credentials file is not found.
        ValueError: If the API key is missing in the YAML file.
        yaml.YAMLError: If there is an error parsing the YAML file.
    """
    try:
        logger.info("Loading API key from file.")
        with open(file_path, 'r') as file:
            credentials: Dict[str, Any] = yaml.safe_load(file)
        
        api_key: str = credentials.get("GOOGLE_API_KEY", "")
        if not api_key:
            raise ValueError("API key not found in the YAML file.")

        logger.info("API key successfully loaded.")
        return api_key

    except FileNotFoundError:
        logger.error(f"Credentials file not found at: {file_path}")
        raise
    except yaml.YAMLError as e:
        logger.error(f"Error parsing YAML file: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error while loading API key: {e}")
        raise
