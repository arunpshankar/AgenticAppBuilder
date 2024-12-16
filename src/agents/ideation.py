from src.config.client import initialize_genai_client
from src.llm.gemini import generate_content
from sqlalchemy.engine.base import Engine
from src.config.logging import logger
from sqlalchemy import create_engine, text
from typing import Dict, List, Generator
import pandas as pd
import time

def run_ideation(engine: Engine) -> Generator[str | tuple[str, List[Dict]], None, None]:
    """
    Run the ideation process with step-by-step logs and generate ideas using a Gemini LLM.

    This function yields status messages (steps) during the ideation process.
    After yielding the steps, it fetches API entries from the database, constructs a prompt,
    and uses the Gemini LLM to produce application ideas.

    :param engine: A SQLAlchemy Engine instance connected to the database.
    :yield: 
        - str: Log messages for each step of the process.
        - tuple: ("IDEAS_RESULT", ideas), where ideas is a list of dictionaries.
    """
    steps = [
        "Initiating ideation process...",
        "Analyzing available APIs from the database...",
        "Formulating a prompt for Gemini LLM...",
        "Asking Gemini for innovative API combination ideas...",
        "Finalizing ideas..."
    ]

    for step in steps:
        yield step
        time.sleep(1)

    ideas = generate_ideas_with_llm(engine, num_ideas=3)
    yield "IDEAS_RESULT", ideas

def generate_ideas_with_llm(engine: Engine, num_ideas: int = 3) -> List[Dict]:
    """
    Generate application ideas from APIs stored in the database using a Gemini LLM.

    :param engine: A SQLAlchemy Engine for database access.
    :param num_ideas: The number of ideas to request from the LLM.
    :return: A list of idea dictionaries with keys: "title", "description", and "apis_used".
    """
    entries = fetch_db_entries(engine)
    if not entries:
        logger.warning("No entries found in the database. Returning fallback idea.")
        return [{
            "title": "No APIs Found",
            "description": "No entries available in the database to generate ideas.",
            "apis_used": []
        }]

    prompt = construct_llm_prompt(entries, num_ideas)
    model_id = "gemini-2.0-flash-exp"
    gemini_client = initialize_genai_client()

    try:
        ideas = generate_content(gemini_client, model_id, prompt)
        logger.info("LLM successfully returned ideas.")
        return ideas
    except Exception as e:
        logger.error("Failed to get ideas from LLM: %s", e)
        return [{
            "title": "LLM Error",
            "description": "There was an error generating ideas using the LLM.",
            "apis_used": []
        }]

def fetch_db_entries(engine: Engine) -> List[Dict]:
    """
    Retrieve API entries from the 'apientry' table in the database.

    Each entry contains: name, category, base_url, endpoint, and description.

    :param engine: A SQLAlchemy Engine for database access.
    :return: A list of dictionaries containing API data. Returns an empty list if an error occurs.
    """
    try:
        with engine.connect() as conn:
            result = conn.execute(text(
                "SELECT name, category, base_url, endpoint, description FROM apientry"
            ))
            rows = result.fetchall()
        entries = [{
            "name": row.name,
            "category": row.category,
            "base_url": row.base_url,
            "endpoint": row.endpoint,
            "description": row.description
        } for row in rows]
        logger.info("Fetched %d entries from the database.", len(entries))
        return entries
    except Exception as e:
        logger.error("Failed to fetch entries from the database: %s", e)
        return []

def construct_llm_prompt(entries: List[Dict], num_ideas: int) -> str:
    """
    Construct a prompt for the LLM based on the API entries from the database.

    :param entries: A list of API entry dictionaries.
    :param num_ideas: The number of ideas to request from the LLM.
    :return: A formatted prompt string.
    """
    apis_summary_lines = [
        f"- Name: {e['name']} | Category: {e['category']} | Description: {e['description']}"
        for e in entries
    ]
    apis_summary = "\n".join(apis_summary_lines)

    prompt = f"""
You have access to a set of APIs. Each API has a name, category, and description:

{apis_summary}

Please propose {num_ideas} innovative application ideas that combine these APIs in interesting ways.
For each idea, provide:
- A short title
- A concise description of what the application does
- A list of the APIs (by name) that it would use

Return your answer as a JSON list, where each element is a dictionary with keys: "title", "description", and "apis_used".
    """.strip()

    logger.debug("Constructed LLM prompt.")
    return prompt

if __name__ == '__main__':
    try:
        # Create an in-memory SQLite DB for testing. Adjust connection as needed.
        engine = create_engine('sqlite:///test.db', echo=False)

        # Load data into the database
        df = pd.read_csv('data/apis.csv')
        df.to_sql('apientry', con=engine, if_exists='replace', index=False)
        logger.info("Loaded API data into the database.")

        # Run the ideation process
        ideation_generator = run_ideation(engine)
        final_ideas = []

        for step in ideation_generator:
            if isinstance(step, tuple) and step[0] == "IDEAS_RESULT":
                final_ideas = step[1]  # Capture the ideas
            else:
                logger.info(step)

        logger.info("Final Ideas: %s", final_ideas)

    except Exception as e:
        logger.error("Error during ideation process: %s", e)
