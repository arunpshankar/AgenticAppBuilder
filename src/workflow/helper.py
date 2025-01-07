
from src.llm.generate import generate_ideas
from src.config.setup import PROJECT_ROOT
from src.config.logging import logger
from typing import Generator
from typing import Tuple
from typing import Union
from typing import List 
import streamlit as st 
import time 
import os 


def load_available_apps() -> None:
    """
    Loads all available applications from the 'src/apps' directory and updates the Streamlit session state.

    Each application's frontend script (frontend.py) is checked for existence. If found, the application
    name and its relative path are stored in `st.session_state["available_apps"]`.

    Exceptions encountered during the directory traversal are logged and skipped gracefully.

    Raises:
        OSError: If there are issues accessing the directory structure.
    """
    apps_base_dir = os.path.join(PROJECT_ROOT, 'src', 'apps')

    if "available_apps" not in st.session_state:
        st.session_state["available_apps"] = {}
    
    st.session_state["available_apps"].clear()

    try:
        if os.path.exists(apps_base_dir):
            for entry in os.listdir(apps_base_dir):
                d_path = os.path.join(apps_base_dir, entry)
                if os.path.isdir(d_path):
                    frontend_path = os.path.join(d_path, "frontend.py")
                    if os.path.exists(frontend_path):
                        relative_path = os.path.relpath(frontend_path, start='.')
                        st.session_state["available_apps"][entry] = relative_path
                        logger.info(f"App '{entry}' loaded successfully with frontend path '{relative_path}'.")
        else:
            logger.warning(f"Apps base directory does not exist: {apps_base_dir}")
    except OSError as e:
        logger.error(f"Error accessing apps directory '{apps_base_dir}': {e}")
        raise


def run_ideation(num_ideas: int = 3) -> Generator[Union[str, Tuple[str, List[dict]]], None, None]:
    """
    Executes the ideation process by guiding through a sequence of steps and generating innovative API combination ideas using Gemini LLM.

    Args:
        num_ideas (int, optional): The number of ideas to generate. Defaults to 3.

    Yields:
        Union[str, Tuple[str, List[dict]]]:
            - Each step in the ideation process as a string.
            - Final result as a tuple containing the key 'IDEAS_RESULT' and a list of ideas.

    Raises:
        Exception: Propagates exceptions encountered during idea generation.
    """
    steps = [
        "Initiating ideation process...",
        "Analyzing available APIs from the database...",
        "Formulating a prompt for Gemini LLM...",
        "Asking Gemini for innovative API combination ideas...",
        "Finalizing ideas..."
    ]

    for step in steps:
        logger.debug(f"Ideation step: {step}")
        yield step
        time.sleep(1)

    selected_names = []
    try:
        if "display_df" in st.session_state and "entries_df" in st.session_state:
            selected_df = st.session_state["display_df"]
            if "Select" in selected_df and selected_df["Select"].any():
                selected_names = selected_df.loc[selected_df["Select"], "name"].tolist()
    except KeyError as e:
        logger.warning(f"Key error while accessing session state data: {e}")

    try:
        ideas = generate_ideas(num_ideas=num_ideas, selected_names=selected_names)
        logger.debug(f"{len(ideas)} ideas generated successfully.")
    except Exception as e:
        logger.error(f"Error during idea generation: {e}")
        ideas = []

    yield ("IDEAS_RESULT", ideas)

