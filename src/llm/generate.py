import re
import random
import pandas as pd
from typing import List, Dict, Tuple
from src.config.client import initialize_genai_client
from src.llm.gemini_text import generate_content
from src.config.setup import TEMPLATES_DIR
from src.db.crud import fetch_db_entries, fetch_db_entries_by_names
from src.config.logging import logger

MODEL_ID = "gemini-2.0-flash-exp"
IDEATE_TEMPLATE_PATH = TEMPLATES_DIR + '/ideate.txt'
BUILD_TEMPLATE_PATH = TEMPLATES_DIR + '/build.txt'
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
    pattern = re.compile(
        r"^Title:\s*([A-Za-z_]+)\r?\n"
        r"Description:\s*(.+?)\r?\n"
        r"APIs Used:\s*(.+)$",
        re.IGNORECASE | re.MULTILINE
    )

    ideas = []
    raw_ideas = [block.strip() for block in response.strip().split("\n\n") if block.strip()]

    for idea_text in raw_ideas:
        match = pattern.search(idea_text)
        if match:
            title = match.group(1).strip()
            description = match.group(2).strip()
            apis_used_line = match.group(3).strip()
            apis_used = [api.strip() for api in apis_used_line.split(",") if api.strip()]

            if title and description and apis_used:
                ideas.append({
                    "title": title,
                    "description": description,
                    "apis_used": apis_used
                })

    return ideas if ideas else [{
        "title": "LLM Error",
        "description": "No valid ideas could be extracted.",
        "apis_used": []
    }]

def generate_ideas(num_ideas: int = 3, selected_names: List[str] = None) -> List[Dict]:
    if selected_names and len(selected_names) > 0:
        entries = fetch_db_entries_by_names(selected_names)
    else:
        all_entries = fetch_db_entries()
        if not all_entries:
            return [{
                "title": "No APIs Found",
                "description": "No entries available.",
                "apis_used": []
            }]
        sample_size = min(3, len(all_entries))
        entries = random.sample(all_entries, sample_size)

    prompt = build_prompt(entries, num_ideas)
    client = initialize_genai_client()

    response = generate_content(client, MODEL_ID, prompt)
    return extract_ideas_from_response(response.text)

def extract_code_block(response: str, markers: Tuple[str, str]) -> str:
    start_marker, end_marker = markers
    try:
        code_section = response.split(start_marker, 1)[1].split(end_marker, 1)[0]
        code_block = re.search(r"```(.*?)```", code_section, re.DOTALL)
        if code_block:
            code = code_block.group(1).strip()
        else:
            code = code_section.strip()
        return code.strip()
    except (IndexError, AttributeError):
        return f"# No code block found for section: {start_marker}"

def build_app_code(selected_ideas: List[Dict], app_name_slug: str, entries: pd.DataFrame) -> Tuple[str, str]:
    client = initialize_genai_client()
    ideas_summary = "\n\n".join([
        f"Title: {idea['title']}\nDescription: {idea['description']}\nAPIs Used: {', '.join(idea['apis_used'])}"
        for idea in selected_ideas
    ])
    apis_summary = "No entries found."
    if not entries.empty:
        apis_summary = "APIs Table:\n" + entries.to_csv(index=False)

    with open(BUILD_TEMPLATE_PATH, 'r', encoding='utf-8') as f:
        template = f.read()

    prompt = template.format(ideas_text=ideas_summary, entries_text=apis_summary, app_name_slug=app_name_slug)
    
    response = generate_content(client, MODEL_ID, prompt)
    return (
        extract_code_block(response.text, FRONTEND_MARKERS),
        extract_code_block(response.text, BACKEND_MARKERS)
    )

def fix_app_code(selected_ideas: List[Dict], app_name_slug: str, entries: pd.DataFrame, error_message: str) -> Tuple[str, str, str]:
    client = initialize_genai_client()

    ideas_summary = "\n\n".join([
        f"Title: {idea['title']}\nDescription: {idea['description']}\nAPIs Used: {', '.join(idea['apis_used'])}"
        for idea in selected_ideas
    ])

    apis_summary = "No entries found."
    if not entries.empty:
        apis_summary = "APIs Table:\n" + entries.to_csv(index=False)

    fix_prompt = f"""
We generated an app named '{app_name_slug}' from these ideas:

{ideas_summary}

APIs available:

{apis_summary}

We got this runtime error:

{error_message}

Fix the code so it runs without errors. Return updated code in the same format:
{FRONTEND_MARKERS[0]} ```\n<frontend code>\n```
{FRONTEND_MARKERS[1]}
{BACKEND_MARKERS[0]} ```\n<backend code>\n```
{BACKEND_MARKERS[1]}

After code blocks, give a one-sentence summary of what was fixed.
    """

    response = generate_content(client, MODEL_ID, fix_prompt)
    response_text = response.text

    new_frontend = extract_code_block(response_text, FRONTEND_MARKERS)
    new_backend = extract_code_block(response_text, BACKEND_MARKERS)

    summary_pattern = re.compile(rf"{BACKEND_MARKERS[1]}\s*(.*)", re.DOTALL)
    summary_match = summary_pattern.search(response_text)
    fix_summary = summary_match.group(1).strip() if summary_match else "No summary provided."

    return new_frontend, new_backend, fix_summary
