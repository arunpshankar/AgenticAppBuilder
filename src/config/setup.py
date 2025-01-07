from src.config.logging import logger
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from src.utils.io import load_yaml
from google import genai
from typing import Dict
from typing import Any 
import os


# Configuration Constants
BASE_DIR: str = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT: str = os.path.dirname(os.path.dirname(BASE_DIR))
DATA_DIR: str = os.path.join(PROJECT_ROOT, 'data')
DB_DIR: str = os.path.join(PROJECT_ROOT, 'db')
DB_PATH: str = os.path.join(DB_DIR, 'apis.db')
CSV_PATH: str = os.path.join(DATA_DIR, 'apis.csv')
IMAGES_DIR: str = os.path.join(PROJECT_ROOT, 'img')
GOOGLE_ICON_PATH: str = os.path.join(IMAGES_DIR, 'google_logo.svg')
TEMPLATES_DIR: str = os.path.join(PROJECT_ROOT, 'templates')
CREDENTIALS_FILE: str = os.path.join(PROJECT_ROOT, 'credentials', 'api.yml')
MODEL = "gemini-2.0-flash-exp"

# Global Configuration
CONFIG: Dict[str, Any] = load_yaml(CREDENTIALS_FILE)
engine: Engine

def get_google_api_key(config: Dict[str, Any] = CONFIG) -> str:
    """
    Extract the Google API key from the configuration.

    Args:
        config (Dict[str, Any]): The loaded configuration dictionary.

    Returns:
        str: The Google API key.

    Raises:
        ValueError: If the Google API key is missing.
    """
    api_key = config.get("GOOGLE_API_KEY", "")
    if not api_key:
        logger.error("Google API key is missing in the configuration.")
        raise ValueError("Google API key not found in the configuration.")
    return api_key


def get_serp_api_key(config: Dict[str, Any] = CONFIG) -> str:
    """
    Extract the SERP API key from the configuration.

    Args:
        config (Dict[str, Any]): The loaded configuration dictionary.

    Returns:
        str: The SERP API key.

    Raises:
        ValueError: If the SERP API key is missing.
    """
    api_key = config.get("SERP_API_KEY", "")
    if not api_key:
        logger.error("SERP API key is missing in the configuration.")
        raise ValueError("SERP API key not found in the configuration.")
    return api_key


def initialize_genai_client(config: Dict[str, Any] = CONFIG) -> genai.Client:
    """
    Initializes the GenAI client using the Google API key from the configuration.

    Args:
        config (Dict[str, Any]): The loaded configuration dictionary.

    Returns:
        genai.Client: The initialized GenAI client.

    Raises:
        Exception: If the client initialization fails.
    """
    try:
        logger.info("Extracting Google API key from configuration.")
        google_api_key = get_google_api_key(config)

        logger.info("Initializing GenAI client.")
        client = genai.Client(api_key=google_api_key)
        logger.info("GenAI client initialized successfully.")
        return client
    except Exception as e:
        logger.error(f"Failed to initialize GenAI client: {e}")
        raise


def setup_directories() -> None:
    """
    Create necessary directories for the project.
    Ensures `db` and `data` directories exist.
    Logs any issues during directory creation.
    """
    try:
        os.makedirs(DB_DIR, exist_ok=True)
        os.makedirs(DATA_DIR, exist_ok=True)
        logger.info(f"Directories ensured: {DB_DIR}, {DATA_DIR}")
    except OSError as e:
        logger.error(f"Error creating directories: {e}")
        raise


def initialize_database(db_path: str) -> Engine:
    """
    Initialize a SQLite database using SQLAlchemy.

    Args:
        db_path (str): Path to the SQLite database file.

    Returns:
        Engine: SQLAlchemy database engine.
    
    Logs database initialization status.
    """
    try:
        engine = create_engine(f'sqlite:///{db_path}', echo=False)
        logger.info(f"Database initialized at {db_path}")
        return engine
    except Exception as e:
        logger.error(f"Failed to initialize database at {db_path}: {e}")
        raise

# Setup happens when the module is imported
try:
    setup_directories()
    engine = initialize_database(DB_PATH)
    logger.info("Module setup complete. Database and directories are ready.")
except Exception as e:
    logger.critical(f"Module setup failed: {e}")
    raise
