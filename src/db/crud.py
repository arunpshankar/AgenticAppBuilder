from sqlalchemy.exc import OperationalError
from sqlalchemy.exc import SQLAlchemyError
from src.config.logging import logger
from src.config.setup import DB_PATH
from src.config.setup import engine
from sqlalchemy import text
from typing import Tuple, List, Dict
import pandas as pd
import os


def validate_csv(df: pd.DataFrame) -> Tuple[bool, str]:
    """
    Validate that the given DataFrame contains all required columns.
    """
    required_columns = [
        "name", "category", "base_url", "endpoint",
        "description", "query_parameters", "example_request", "example_response"
    ]

    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        return False, f"Missing required columns: {', '.join(missing_columns)}"
    return True, "CSV is valid"


def purge_and_load_csv(csv_path: str) -> Tuple[bool, str]:
    """
    Drop the existing 'apientry' table (if it exists) and load the CSV file data into it.
    """
    logger.debug("Attempting to load CSV from path: %s", csv_path)

    # Step 1: Read the CSV
    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        logger.error("Failed to read CSV file: %s", e)
        return False, f"Error reading CSV file: {e}"

    # Step 2: Validate the CSV structure
    is_valid, validation_msg = validate_csv(df)
    if not is_valid:
        logger.error("CSV validation failed: %s", validation_msg)
        return False, validation_msg

    # Step 3: Reload the data into the database
    try:
        with engine.connect() as conn:
            logger.debug("Dropping existing 'apientry' table if it exists.")
            conn.execute(text("DROP TABLE IF EXISTS apientry"))
            logger.debug("Inserting new data into 'apientry' table.")
        
        df.to_sql('apientry', con=engine, if_exists='replace', index=False)
        logger.info("CSV successfully loaded into the database.")
        return True, "CSV uploaded and database reloaded successfully!"

    except OperationalError as oe:
        logger.error("Database operational error: %s", oe)
        return False, f"Database operational error: {oe}"

    except SQLAlchemyError as sqle:
        logger.error("SQLAlchemy error occurred: %s", sqle)
        return False, f"SQLAlchemy error: {sqle}"

    except Exception as e:
        logger.error("Unexpected error occurred while loading CSV: %s", e)
        return False, f"Unknown error: {e}"


def get_entries() -> pd.DataFrame:
    """
    Retrieve all entries from the 'apientry' table and return them as a DataFrame.
    """
    if not os.path.exists(DB_PATH):
        logger.warning("Database file not found at path: %s", DB_PATH)
        return pd.DataFrame()

    try:
        with engine.connect() as conn:
            logger.debug("Fetching all entries from 'apientry' table.")
            result = conn.execute(text("SELECT * FROM apientry"))
            df = pd.DataFrame(result.fetchall(), columns=result.keys())
        logger.info("Successfully fetched entries from the database.")
        return df

    except Exception as e:
        logger.error("Error while fetching entries from database: %s", e)
        return pd.DataFrame()


def fetch_db_entries() -> List[Dict]:
    """
    Retrieve API entries from the 'apientry' table in the database.
    Returns a list of dicts with keys: name, category, base_url, endpoint, description.
    """
    try:
        with engine.connect() as conn:
            logger.debug("Fetching specific columns from 'apientry' table.")
            result = conn.execute(text(
                "SELECT name, category, base_url, endpoint, description FROM apientry"
            ))
            entries = [
                {
                    "name": row["name"],
                    "category": row["category"],
                    "base_url": row["base_url"],
                    "endpoint": row["endpoint"],
                    "description": row["description"]
                }
                for row in result.mappings()
            ]

        logger.info("Fetched %d entries from the database.", len(entries))
        return entries

    except Exception as e:
        logger.error("Error while fetching API entries: %s", e)
        return []


def fetch_db_entries_by_names(names: List[str]) -> List[Dict]:
    """
    Retrieve API entries from 'apientry' table for the given list of names.
    """
    if not names:
        return []

    try:
        placeholders = ", ".join([f":name{i}" for i in range(len(names))])
        params = {f"name{i}": name for i, name in enumerate(names)}
        with engine.connect() as conn:
            query = text(f"SELECT name, category, base_url, endpoint, description FROM apientry WHERE name IN ({placeholders})")
            result = conn.execute(query, params)
            entries = [
                {
                    "name": row["name"],
                    "category": row["category"],
                    "base_url": row["base_url"],
                    "endpoint": row["endpoint"],
                    "description": row["description"]
                }
                for row in result.mappings()
            ]
        return entries
    except Exception as e:
        logger.error("Error while fetching entries by names: %s", e)
        return []
