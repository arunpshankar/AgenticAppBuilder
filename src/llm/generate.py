from src.config.client import initialize_genai_client
from src.llm.gemini import generate_content
from src.config.setup import TEMPLATES_DIR
from src.db.io import fetch_db_entries
from src.config.logging import logger
from src.db.io import get_entries
from typing import Tuple
from typing import Dict 
from typing import List 
import os
import re

# Static variables
MODEL_ID = "gemini-2.0-flash-exp"
IDEATE_TEMPLATE_PATH = os.path.join(TEMPLATES_DIR, 'ideate.txt')
BUILD_TEMPLATE_PATH = os.path.join(TEMPLATES_DIR, 'build.txt')
FRONTEND_MARKERS = ("---BEGIN FRONTEND CODE---", "---END FRONTEND CODE---")
BACKEND_MARKERS = ("---BEGIN BACKEND CODE---", "---END BACKEND CODE---")


def build_prompt(entries: List[Dict], num_ideas: int) -> str:
    """
    Build a prompt for generating ideas using the LLM.

    Args:
        entries (List[Dict]): A list of API entries.
        num_ideas (int): The number of ideas to generate.

    Returns:
        str: The constructed prompt string.
    """
    apis_summary = "\n".join([
        f"- Name: {entry['name']} | Category: {entry['category']} | Description: {entry['description']}"
        for entry in entries
    ])

    with open(IDEATE_TEMPLATE_PATH, 'r', encoding='utf-8') as f:
        template = f.read()

    return template.format(apis_summary=apis_summary, num_ideas=num_ideas).strip()


def extract_ideas_from_response(response: str) -> List[Dict]:
    """
    Extract ideas from the LLM response text.

    Args:
        response (str): The response text from the LLM.

    Returns:
        List[Dict]: A list of ideas as dictionaries.
    """
    ideas = []
    raw_ideas = [idea.strip() for idea in response.split("\n\n") if idea.strip()]

    for idea_text in raw_ideas:
        fields = {
            "title": re.search(r"^Title:\s*(.+)", idea_text, re.IGNORECASE | re.MULTILINE),
            "description": re.search(r"^Description:\s*(.+)", idea_text, re.IGNORECASE | re.MULTILINE),
            "apis_used": re.search(r"^APIs Used:\s*(.+)", idea_text, re.IGNORECASE | re.MULTILINE)
        }

        if fields["title"] and fields["description"]:
            ideas.append({
                "title": fields["title"].group(1).strip(),
                "description": fields["description"].group(1).strip(),
                "apis_used": [api.strip() for api in fields["apis_used"].group(1).split(",")] if fields["apis_used"] else []
            })

    return ideas if ideas else [{
        "title": "LLM Error",
        "description": "No valid ideas could be extracted.",
        "apis_used": []
    }]


def generate_ideas(num_ideas: int = 3) -> List[Dict]:
    """
    Generate ideas using the LLM based on database entries.

    Args:
        num_ideas (int, optional): Number of ideas to generate. Defaults to 3.

    Returns:
        List[Dict]: A list of generated ideas as dictionaries.
    """
    entries = fetch_db_entries()
    if not entries:
        logger.info("No entries found in the database. Returning fallback idea.")
        return [{
            "title": "No APIs Found",
            "description": "No entries available in the database to generate ideas.",
            "apis_used": []
        }]

    prompt = build_prompt(entries, num_ideas)
    client = initialize_genai_client()

    try:
        response = generate_content(client, MODEL_ID, prompt)
        return extract_ideas_from_response(response.text)
    except Exception as e:
        logger.error("Failed to generate ideas: %s", e)
        return [{
            "title": "LLM Error",
            "description": "Error occurred while generating ideas.",
            "apis_used": []
        }]


def build_app_code(selected_ideas: List[Dict], app_slug: str) -> Tuple[str, str]:
    """
    Generate frontend and backend code for an app based on selected ideas.

    Args:
        selected_ideas (List[Dict]): A list of selected ideas.
        app_slug (str): The slugified name of the app.

    Returns:
        Tuple[str, str]: Frontend and backend code as strings.
    """
    client = initialize_genai_client()

    ideas_summary = "\n\n".join([
        f"Title: {idea['title']}\nDescription: {idea['description']}\nAPIs Used: {', '.join(idea['apis_used'])}"
        for idea in selected_ideas
    ])

    df = get_entries()
    apis_summary = "APIs Table:\n" + df.to_csv(index=False) if not df.empty else "No entries found in the database."

    with open(BUILD_TEMPLATE_PATH, 'r', encoding='utf-8') as f:
        template = f.read()

    prompt = template.format(ideas_summary=ideas_summary, apis_summary=apis_summary, app_slug=app_slug)

    logger.info("Generating app code.")
    try:
        response = generate_content(client, MODEL_ID, prompt)
        return (
            extract_code_block(response.text, FRONTEND_MARKERS),
            extract_code_block(response.text, BACKEND_MARKERS)
        )
    except Exception as e:
        logger.error("Failed to generate app code: %s", e)
        return "# Error generating frontend code", "# Error generating backend code"


def extract_code_block(response: str, markers: Tuple[str, str]) -> str:
    """
    Extract a specific code block (frontend or backend) from the response.

    Args:
        response (str): The response text containing code blocks.
        markers (Tuple[str, str]): Start and end markers for the code block.

    Returns:
        str: The extracted code as a string.
    """
    start_marker, end_marker = markers

    try:
        # Extract the section between the markers
        code_section = response.split(start_marker, 1)[1].split(end_marker, 1)[0]
        # Extract code within backticks if present
        code_block = re.search(r"```(.*?)```", code_section, re.DOTALL)
        return code_block.group(1).strip() if code_block else code_section.strip()
    except (IndexError, AttributeError):
        # Return a clear error message if markers or code block are not found
        return f"# No code block found for section: {start_marker}"
