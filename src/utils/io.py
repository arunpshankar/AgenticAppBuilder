from src.config.setup import PROJECT_ROOT
from src.config.setup import CSV_PATH
from src.config.logging import logger 
from typing import Dict 
from typing import Any 
import yaml
import os


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


def save_app_code(app_name_slug: str, frontend_code: str, backend_code: str) -> None:
    """
    Save the generated frontend and backend code to the appropriate location.

    Args:
        app_name_slug (str): The slugified app name.
        frontend_code (str): The frontend code as a string.
        backend_code (str): The backend code as a string.
    """
    apps_dir = os.path.join(PROJECT_ROOT, 'src', 'apps', app_name_slug)
    os.makedirs(apps_dir, exist_ok=True)

    frontend_path = os.path.join(apps_dir, 'frontend.py')
    backend_path = os.path.join(apps_dir, 'backend.py')

    try:
        with open(frontend_path, 'w', encoding='utf-8') as f:
            f.write(frontend_code)
        with open(backend_path, 'w', encoding='utf-8') as f:
            f.write(backend_code)
        logger.info("App code saved to: %s and %s", frontend_path, backend_path)
    except Exception as e:
        logger.error("Failed to save app code: %s", e)