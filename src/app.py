import os
import json
import time
import pandas as pd
import streamlit as st
from typing import Tuple, List, Dict
from sqlalchemy.exc import OperationalError, SQLAlchemyError
from sqlalchemy import create_engine, text
from src.config.logging import logger
from src.config.client import initialize_genai_client
from src.llm.gemini import generate_content

# Configuration 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')
DB_DIR = os.path.join(PROJECT_ROOT, 'db')
DB_PATH = os.path.join(DB_DIR, 'apis.db')
CSV_PATH = os.path.join(DATA_DIR, 'apis.csv')
IMAGES_DIR = os.path.join(BASE_DIR, 'images')
GOOGLE_ICON_PATH = os.path.join(IMAGES_DIR, 'google_icon.png')
TEMPLATES_DIR = os.path.join(PROJECT_ROOT, 'templates')

os.makedirs(DB_DIR, exist_ok=True)
engine = create_engine(f'sqlite:///{DB_PATH}', echo=False)

def validate_csv(df: pd.DataFrame) -> Tuple[bool, str]:
    required_columns = [
        "name", "category", "base_url", "endpoint",
        "description", "query_parameters", "example_request", "example_response"
    ]
    for col in required_columns:
        if col not in df.columns:
            return False, f"Missing required column: {col}"
    return True, "CSV is valid"

def purge_and_load_csv(csv_path: str) -> Tuple[bool, str]:
    logger.debug("Loading CSV from path: %s", csv_path)
    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        logger.error("Failed to read CSV: %s", e)
        return False, f"Failed to read CSV: {e}"

    is_valid, msg = validate_csv(df)
    if not is_valid:
        logger.error("CSV validation failed: %s", msg)
        return False, msg

    try:
        with engine.connect() as conn:
            conn.execute(text("DROP TABLE IF EXISTS apientry"))
        df.to_sql('apientry', con=engine, if_exists='replace', index=False)
        logger.debug("CSV successfully loaded into the database.")
        return True, "CSV uploaded and database reloaded successfully!"
    except OperationalError as oe:
        logger.error("Database operational error: %s", oe)
        return False, f"Database error: {oe}"
    except SQLAlchemyError as sqle:
        logger.error("SQLAlchemy error: %s", sqle)
        return False, f"Database error: {sqle}"
    except Exception as e:
        logger.error("Unknown error loading CSV into DB: %s", e)
        return False, f"Unknown error loading CSV: {e}"

def get_entries() -> pd.DataFrame:
    if not os.path.exists(DB_PATH):
        logger.debug("Database file does not exist. Returning empty DataFrame.")
        return pd.DataFrame()
    logger.debug("Fetching entries from the database.")
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT * FROM apientry"))
            df = pd.DataFrame(result.fetchall(), columns=result.keys())
        return df
    except Exception as e:
        logger.error("Failed to fetch entries: %s", e)
        return pd.DataFrame()

def fetch_db_entries(engine) -> List[Dict]:
    """
    Retrieve API entries from the 'apientry' table in the database.
    Each entry is a dictionary with keys: name, category, base_url, endpoint, description.
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
    apis_summary_lines = [
        f"- Name: {e['name']} | Category: {e['category']} | Description: {e['description']}"
        for e in entries
    ]
    apis_summary = "\n".join(apis_summary_lines)

    # Load template
    prompt_template_path = os.path.join(TEMPLATES_DIR, 'ideate.txt')
    with open(prompt_template_path, 'r', encoding='utf-8') as f:
        prompt_template = f.read()

    prompt = prompt_template.format(apis_summary=apis_summary, num_ideas=num_ideas)
    return prompt.strip()

def generate_ideas_with_llm(engine, num_ideas: int = 3) -> List[Dict]:
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
        response = generate_content(gemini_client, model_id, prompt)
        response_str = response.text
        
        # Parse ideas from the text
        raw_ideas = [idea.strip() for idea in response_str.split("\n\n") if idea.strip()]
        
        parsed_ideas = []
        for idea_text in raw_ideas:
            lines = idea_text.splitlines()
            title_line = next((l for l in lines if l.lower().startswith("title:")), None)
            desc_line = next((l for l in lines if l.lower().startswith("description:")), None)
            apis_line = next((l for l in lines if l.lower().startswith("apis used:")), None)

            if title_line and desc_line and apis_line:
                title = title_line.split(":", 1)[1].strip() if ":" in title_line else "Untitled"
                description = desc_line.split(":", 1)[1].strip() if ":" in desc_line else ""
                apis_used = [a.strip() for a in apis_line.split(":", 1)[1].split(",")] if ":" in apis_line else []
                parsed_ideas.append({
                    "title": title,
                    "description": description,
                    "apis_used": apis_used
                })
        
        if not parsed_ideas:
            return [{
                "title": "LLM Error",
                "description": "No valid ideas could be extracted.",
                "apis_used": []
            }]
        
        return parsed_ideas

    except Exception as e:
        logger.error("Failed to get ideas from LLM: %s", e)
        return [{
            "title": "LLM Error",
            "description": "There was an error generating ideas using the LLM.",
            "apis_used": []
        }]

def generate_app_code_with_llm(selected_ideas: List[Dict]) -> Tuple[str, str]:
    gemini_client = initialize_genai_client()
    model_id = "gemini-2.0-flash-exp"

    idea_descriptions = []
    for idea in selected_ideas:
        idea_descriptions.append(f"""
Title: {idea['title']}
Description: {idea['description']}
APIs Used: {", ".join(idea['apis_used'])}
        """.strip())

    ideas_text = "\n\n".join(idea_descriptions)

    # Load code generation prompt template
    prompt_template_path = os.path.join(TEMPLATES_DIR, 'build.txt')
    with open(prompt_template_path, 'r', encoding='utf-8') as f:
        prompt_template = f.read()

    prompt = prompt_template.format(ideas_text=ideas_text)

    logger.debug("Constructing prompt for app code generation.")
    try:
        response = generate_content(gemini_client, model_id, prompt)
        response_str = response.text

        # Extract code between markers
        frontend_code = "# No frontend code returned"
        backend_code = "# No backend code returned"

        # Find frontend code
        if "---BEGIN FRONTEND CODE---" in response_str and "---END FRONTEND CODE---" in response_str:
            frontend_section = response_str.split("---BEGIN FRONTEND CODE---", 1)[-1].split("---END FRONTEND CODE---", 1)[0]
            if "```" in frontend_section:
                frontend_section = frontend_section.split("```", 1)[-1]
                frontend_section = frontend_section.rsplit("```", 1)[0]
            frontend_code = frontend_section.strip()

        # Find backend code
        if "---BEGIN BACKEND CODE---" in response_str and "---END BACKEND CODE---" in response_str:
            backend_section = response_str.split("---BEGIN BACKEND CODE---", 1)[-1].split("---END BACKEND CODE---", 1)[0]
            if "```" in backend_section:
                backend_section = backend_section.split("```", 1)[-1]
                backend_section = backend_section.rsplit("```", 1)[0]
            backend_code = backend_section.strip()

        return frontend_code, backend_code
    except Exception as e:
        logger.error("Failed to generate app code with LLM: %s", e)
        return "# Error generating frontend code", "# Error generating backend code"

def save_app_code(frontend_code: str, backend_code: str):
    apps_dir = os.path.join(PROJECT_ROOT, 'src', 'apps')
    os.makedirs(apps_dir, exist_ok=True)

    frontend_path = os.path.join(apps_dir, 'my_new_app_frontend.py')
    backend_path = os.path.join(apps_dir, 'my_new_app_backend.py')

    with open(frontend_path, 'w', encoding='utf-8') as f:
        f.write(frontend_code)

    with open(backend_path, 'w', encoding='utf-8') as f:
        f.write(backend_code)

    logger.info("App code saved to: %s and %s", frontend_path, backend_path)

def run_ideation(engine):
    """
    Run the ideation process with step-by-step logs and generate ideas using a Gemini LLM.
    Yields:
        - str for each step
        - ("IDEAS_RESULT", ideas) tuple with the final ideas
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
    yield ("IDEAS_RESULT", ideas)

def main():
    st.set_page_config(
        page_title="Agentic App Builder",
        layout="wide",
        page_icon="💡",
        initial_sidebar_state="expanded"
    )

    # Inject custom CSS for fonts & styling
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css?family=Open+Sans:400,600&display=swap');
    body {
        font-family: 'Open Sans', sans-serif;
    }
    .stProgress > div > div > div > div {
        background-color: #4285F4;
    }
    </style>
    """, unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        if os.path.exists(GOOGLE_ICON_PATH):
            st.image(GOOGLE_ICON_PATH, width=40)
        st.title("Agentic App Builder")

        ideate_trigger = st.button("Ideate", help="Start the ideation process to generate API combination ideas.")
        refresh_trigger = st.button("Refresh Entries", help="Refresh the entries table from the database.")

    st.header("Welcome to Agentic App Builder")

    # Upload CSV Section
    st.subheader("Upload CSV")
    uploaded_file = st.file_uploader("Select your CSV file", type=['csv'])

    if uploaded_file is not None:
        try:
            with open(CSV_PATH, 'wb') as f:
                f.write(uploaded_file.read())
        except Exception as e:
            st.error(f"Failed to save uploaded CSV: {e}")
            logger.error("Failed to save uploaded CSV: %s", e)
        else:
            logger.debug("CSV file uploaded successfully, attempting to load into DB.")
            success, message = purge_and_load_csv(CSV_PATH)
            if success:
                st.success(message)
            else:
                st.error(message)

    # Logs Section
    logs_expander = st.expander("Logs / Traces", expanded=False)
    logs_container = logs_expander.empty()

    # Initialize session states
    if "logs" not in st.session_state:
        st.session_state["logs"] = []
    if "ideas" not in st.session_state:
        st.session_state["ideas"] = []
    if "entries_df" not in st.session_state:
        st.session_state["entries_df"] = get_entries()
    if "selected_ideas" not in st.session_state:
        st.session_state["selected_ideas"] = []
    if "app_built" not in st.session_state:
        st.session_state["app_built"] = False

    # Refresh entries if triggered
    if refresh_trigger:
        st.session_state["entries_df"] = get_entries()
        logger.debug("Entries refreshed from the database.")

    # Handle ideation process
    if ideate_trigger:
        st.session_state["ideas"] = []
        st.session_state["logs"] = []
        st.session_state["selected_ideas"] = []
        st.session_state["app_built"] = False

        logs_area = logs_container.empty()
        st.info("Ideation process started...")

        # Run the ideation generator
        for step in run_ideation(engine=engine):
            if isinstance(step, tuple) and step[0] == "IDEAS_RESULT":
                # step[1] contains the final ideas
                st.session_state["ideas"] = step[1]
            else:
                st.session_state["logs"].append(step)
                logs_area.write("\n".join(map(str, st.session_state["logs"])))

        if st.session_state["ideas"]:
            st.success("Ideas generated!")
            logger.debug("Ideas generated successfully.")
        else:
            st.warning("No ideas generated.")

    # Show entries
    st.subheader("Available Entries")
    if st.session_state["entries_df"] is not None and not st.session_state["entries_df"].empty:
        st.dataframe(st.session_state["entries_df"])
    else:
        st.write("No entries available. Please upload a CSV.")

    # Show ideas if available
    if st.session_state["ideas"]:
        st.subheader("Ideation Results")
        st.write("Select one or more ideas to build into an app:")

        current_selected_ideas = []
        for i, idea in enumerate(st.session_state["ideas"]):
            if isinstance(idea, dict) and all(k in idea for k in ["title", "description", "apis_used"]):
                selected = st.checkbox(idea['title'], value=False, key=f"idea_select_{i}")
                if selected:
                    current_selected_ideas.append(idea)

                st.markdown(f"**{idea['title']}**")
                st.write(idea["description"])
                st.write("APIs Used:")
                for api in idea["apis_used"]:
                    st.markdown(f"- {api}")
            else:
                st.write("Idea format is invalid. Cannot display.")

        st.session_state["selected_ideas"] = current_selected_ideas

        # Add a button to build the selected app(s)
        if st.button("Build App"):
            if not st.session_state["selected_ideas"]:
                st.warning("Please select at least one idea before building.")
            else:
                st.info("Generating application code. Please wait...")
                frontend_code, backend_code = generate_app_code_with_llm(st.session_state["selected_ideas"])
                save_app_code(frontend_code, backend_code)
                st.success("App code generated and saved!")
                st.session_state["app_built"] = True

    if st.session_state["app_built"]:
        st.subheader("Your App is Ready!")
        st.markdown("The generated code has been saved in `./src/apps/` directory.")
        st.markdown("You can now integrate and run it locally, or further refine the code.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error("Unhandled exception in main: %s", e)
        st.error(f"An unexpected error occurred: {e}")