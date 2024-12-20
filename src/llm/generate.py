from src.config.client import initialize_genai_client
from src.llm.gemini_text import generate_content
from src.config.setup import TEMPLATES_DIR
from src.db.crud import fetch_db_entries, fetch_db_entries_by_names
from src.config.logging import logger
from typing import Tuple, Dict, List
import os
import re
import random
import pandas as pd 

MODEL_ID = "gemini-2.0-flash-exp"
IDEATE_TEMPLATE_PATH = os.path.join(TEMPLATES_DIR, 'ideate.txt')
BUILD_TEMPLATE_PATH = os.path.join(TEMPLATES_DIR, 'build.txt')
FRONTEND_MARKERS = ("---BEGIN FRONTEND CODE---", "---END FRONTEND CODE---")
BACKEND_MARKERS = ("---BEGIN BACKEND CODE---", "---END BACKEND CODE---")


def build_prompt(entries: List[Dict], num_ideas: int) -> str:
    apis_summary = "\n".join([
        f"- Name: {entry['name']} | Category: {entry['category']} | Description: {entry['description']}"
        for entry in entries
    ])

    with open(IDEATE_TEMPLATE_PATH, 'r', encoding='utf-8') as f:
        template = f.read()

    return template.format(apis_summary=apis_summary, num_ideas=num_ideas).strip()


def extract_ideas_from_response(response: str) -> List[Dict]:
    # Regex pattern that:
    # 1. Matches Title line: "Title: <some_title>"
    #    - <some_title> must be alphabetic/underscore only, per instructions
    # 2. Matches Description line: "Description: <some_description>"
    # 3. Matches APIs Used line: "APIs Used: <API_1, API_2, ...>"
    # This pattern assumes each idea block is separated by a blank line.
    pattern = re.compile(
        r"^Title:\s*([A-Za-z_]+)\r?\n"      # Title line with allowed chars
        r"Description:\s*(.+?)\r?\n"         # Description line (non-greedy)
        r"APIs Used:\s*(.+)$",               # APIs Used line
        re.IGNORECASE | re.MULTILINE
    )

    ideas = []
    # Split the entire response by double newlines to handle each idea block
    raw_ideas = [block.strip() for block in response.strip().split("\n\n") if block.strip()]

    for idea_text in raw_ideas:
        match = pattern.search(idea_text)
        if match:
            title = match.group(1).strip()
            description = match.group(2).strip()
            apis_used_line = match.group(3).strip()
            # Split the APIs by comma and strip whitespace from each API name
            apis_used = [api.strip() for api in apis_used_line.split(",") if api.strip()]

            # Only add this idea if all fields are present and valid
            # (If needed, add any additional validation checks here)
            if title and description and apis_used:
                ideas.append({
                    "title": title,
                    "description": description,
                    "apis_used": apis_used
                })

    # Return extracted ideas or a fallback if none found
    return ideas if ideas else [{
        "title": "LLM Error",
        "description": "No valid ideas could be extracted.",
        "apis_used": []
    }]



def generate_ideas(num_ideas: int = 3, selected_names: List[str] = None) -> List[Dict]:
    """
    Generate ideas using the LLM based on selected_names.
    If selected_names is provided, fetch those entries from DB.
    If not, fetch all and choose a random subset.
    """
    if selected_names and len(selected_names) > 0:
        entries = fetch_db_entries_by_names(selected_names)
    else:
        # No selected names, fetch all entries and pick random if needed
        all_entries = fetch_db_entries()
        if not all_entries:
            logger.info("No entries found in the database. Returning fallback idea.")
            return [{
                "title": "No APIs Found",
                "description": "No entries available in the database to generate ideas.",
                "apis_used": []
            }]
        sample_size = min(3, len(all_entries))
        entries = random.sample(all_entries, sample_size)

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


def build_app_code(selected_ideas: List[Dict], app_name_slug: str, entries: pd.DataFrame) -> Tuple[str, str]:
    client = initialize_genai_client()

    ideas_summary = "\n\n".join([
        f"Title: {idea['title']}\nDescription: {idea['description']}\nAPIs Used: {', '.join(idea['apis_used'])}"
        for idea in selected_ideas
    ])

    # Convert only the provided 'entries' DataFrame to CSV if not empty
    if not entries.empty:
        apis_summary = "APIs Table:\n" + entries.to_csv(index=False)
    else:
        apis_summary = "No entries found."

    with open(BUILD_TEMPLATE_PATH, 'r', encoding='utf-8') as f:
        template = f.read()

    prompt = template.format(ideas_text=ideas_summary, entries_text=apis_summary, app_name_slug=app_name_slug)
    
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
    start_marker, end_marker = markers
    try:
        # Extract section between markers
        code_section = response.split(start_marker, 1)[1].split(end_marker, 1)[0]
        
        # First try to find code block with backticks
        code_block = re.search(r"```(.*?)```", code_section, re.DOTALL)
        
        if code_block:
            # Extract content from triple backticks
            code = code_block.group(1).strip()
        else:
            # Use the whole section if no backticks found
            code = code_section.strip()
        
        # Clean any stray backticks at start or end
        # Handle single and double backticks that might be left
        code = re.sub(r'^`{1,2}', '', code)  # Remove 1-2 backticks at start
        code = re.sub(r'`{1,2}$', '', code)  # Remove 1-2 backticks at end
        
        # Handle case where there might be a language identifier
        if code.split('\n', 1)[0].strip().lower() in ['python', 'javascript', 'java', 'cpp', 'typescript']:
            code = code.split('\n', 1)[1] if '\n' in code else code
            
        return code.strip()
        
    except (IndexError, AttributeError):
        return f"# No code block found for section: {start_marker}"
    