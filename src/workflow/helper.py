from concurrent.futures import ThreadPoolExecutor 
from src.agents.builder import build_app_code
from src.agents.builder import generate_ideas
from src.db.crud import purge_and_load_csv  
from src.config.setup import PROJECT_ROOT
from src.config.setup import CSV_PATH 
from src.config.logging import logger
from typing import Generator
from typing import Optional 
from typing import Tuple
from typing import Union
from typing import Dict 
from typing import List 
import streamlit as st 
import importlib.util 
import pandas as pd
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


def handle_csv_upload(uploaded_file: Optional[st.runtime.uploaded_file_manager.UploadedFile]) -> None:
    """
    Handles the upload of a CSV file, saves it to disk, and attempts to load it into the database.

    Args:
        uploaded_file (Optional[UploadedFile]): The file uploaded via Streamlit's file uploader.

    Raises:
        Exception: If file operations or database loading fail, appropriate errors are logged and displayed.
    """
    if uploaded_file is not None:
        try:
            logger.debug("Uploading CSV file to disk.")
            with open(CSV_PATH, 'wb') as f:
                f.write(uploaded_file.read())
            logger.info("CSV file uploaded and saved successfully.")
        except Exception as e:
            logger.error(f"Failed to save uploaded CSV: {e}")
            st.error(f"Failed to save uploaded CSV: {e}")
            return

        logger.debug("CSV file uploaded successfully. Attempting to load into the database.")
        try:
            success, message = purge_and_load_csv(CSV_PATH)
            if success:
                logger.info("CSV file loaded into the database successfully.")
                st.success(message)
            else:
                logger.warning(f"CSV file loading into the database failed: {message}")
                st.error(message)
        except Exception as e:
            logger.error(f"Error while loading CSV into the database: {e}")
            st.error(f"Error while loading CSV into the database: {e}")


def display_entries(entries_df: Optional[pd.DataFrame]) -> None:
    """
    Displays available entries in a Streamlit application, allowing users to select rows for further processing.

    Args:
        entries_df (Optional[pd.DataFrame]): DataFrame containing the entries to be displayed. Must include a 'name' column.

    Raises:
        ValueError: If the provided DataFrame does not contain a 'name' column.
    """
    st.subheader("Available Entries")

    if entries_df is None or entries_df.empty:
        st.write("No entries available. Please upload a CSV.")
        return

    st.markdown(
        """
        <p style='color:gray;font-size:13px;'>If you do not select any rows, random APIs will be chosen for you. 
        Selected rows will be used for ideation and code generation. To avoid scrolling resets, select multiple rows 
        first and then click 'Submit Selections'.</p>
        """,
        unsafe_allow_html=True
    )

    try:
        if "display_df" not in st.session_state or \
           st.session_state["display_df"].shape[0] != entries_df.shape[0]:
            display_df = entries_df.copy().reset_index(drop=True)
            if 'name' not in display_df.columns:
                logger.warning("No 'name' column found in entries DataFrame.")
                st.warning("No 'name' column found in entries. Please ensure CSV has a 'name' column.")
                return
            display_df.insert(0, 'Select', False)
            st.session_state["display_df"] = display_df

        with st.form("selection_form"):
            edited_df = st.data_editor(
                st.session_state["display_df"],
                num_rows="dynamic",
                use_container_width=True,
                key="entries_editor"
            )
            submit = st.form_submit_button("Submit Selections")

        if submit:
            st.session_state["display_df"] = edited_df

        selected_rows = st.session_state["display_df"][st.session_state["display_df"]["Select"]]
        if not selected_rows.empty:
            st.write("**Selected Entries:**")
            styled_selected = selected_rows.style.apply(
                lambda row: ['background-color: #A5D6A7' for _ in row],
                axis=1
            )
            st.dataframe(styled_selected, use_container_width=True)
        else:
            st.write("No entries selected.")

    except Exception as e:
        logger.error(f"Error while displaying entries: {e}")
        st.error(f"An error occurred while displaying entries: {e}")


def display_ideas(ideas: List[dict]) -> None:
    """
    Displays a list of ideation results in a grid format and allows users to select one or more ideas.

    Args:
        ideas (List[dict]): A list of dictionaries, where each dictionary contains the idea details such as title,
                            description, and APIs used.

    Raises:
        ValueError: If the input `ideas` list contains malformed dictionaries missing required keys.
    """
    st.subheader("Ideation Results")
    st.write("Select one or more ideas to build into separate apps:")

    if not ideas:
        st.warning("No ideas available to display.")
        logger.warning("The ideas list is empty. Nothing to display.")
        return

    try:
        rows = (len(ideas) // 3) + (1 if len(ideas) % 3 > 0 else 0)
        current_selected_ideas = []

        for row_i in range(rows):
            cols = st.columns(3, gap="small")
            for col_i in range(3):
                idea_index = row_i * 3 + col_i
                if idea_index < len(ideas):
                    idea = ideas[idea_index]

                    if not all(key in idea for key in ['title', 'description', 'apis_used']):
                        logger.error(f"Malformed idea at index {idea_index}: {idea}")
                        raise ValueError("Each idea must have 'title', 'description', and 'apis_used' keys.")

                    with cols[col_i]:
                        st.markdown(f"""
                        <div style="border:1px solid #ddd; border-radius:5px; padding:10px; margin-bottom:15px;">
                            <h4 style="margin-top:0; margin-bottom:5px;">{idea['title']}</h4>
                            <p style="margin-top:0; margin-bottom:10px;">{idea['description']}</p>
                            <p style="margin-bottom:5px;"><strong>APIs Used:</strong> {', '.join(idea['apis_used'])}</p>
                        </div>
                        """, unsafe_allow_html=True)

                        selected = st.checkbox("Select this idea", key=f"idea_select_{idea_index}")
                        if selected:
                            current_selected_ideas.append(idea)

        st.session_state["selected_ideas"] = current_selected_ideas
        logger.info(f"{len(current_selected_ideas)} ideas selected.")

    except Exception as e:
        logger.error(f"Error displaying ideas: {e}")
        st.error(f"An error occurred while displaying ideas: {e}")


def build_app_for_idea(idea: Dict, selected_entries: pd.DataFrame) -> str:
    """
    Builds an app for the given idea by generating and saving the corresponding frontend and backend code.

    Args:
        idea (Dict): A dictionary containing details about the idea, including its title.
        selected_entries (pd.DataFrame): A DataFrame of selected entries to be used in the app.

    Returns:
        str: The slugified name of the app directory where the code is saved.

    Raises:
        KeyError: If the 'title' key is missing in the idea dictionary.
        Exception: For any errors during app directory creation or code generation.
    """
    try:
        if 'title' not in idea:
            logger.error("The idea dictionary is missing the 'title' key.")
            raise KeyError("The idea dictionary must contain a 'title' key.")

        app_name = idea['title']
        app_name_slug = app_name.lower().replace(" ", "_").replace("-", "_")
        apps_dir = os.path.join(PROJECT_ROOT, 'src', 'apps', app_name_slug)
        print(f"PROJECT_ROOT = {PROJECT_ROOT}")

        os.makedirs(apps_dir, exist_ok=True)
        logger.info(f"Created or verified app directory: {apps_dir}")

        # Build code for this idea
        frontend_code, backend_code = build_app_code([idea], app_name_slug, entries=selected_entries)
        save_app_code(app_name_slug, frontend_code, backend_code)

        logger.info(f"App '{app_name}' built successfully with slug '{app_name_slug}'.")
        return app_name_slug

    except KeyError as e:
        logger.error(f"Key error: {e}")
        raise
    except Exception as e:
        logger.error(f"An error occurred while building the app: {e}")
        raise


def build_selected_apps(selected_ideas: List[dict]) -> None:
    """
    Builds applications for the selected ideas by generating application code for each.

    Args:
        selected_ideas (List[dict]): A list of dictionaries representing selected ideas, each containing details such as the title.

    Raises:
        Exception: If any errors occur during the app-building process.
    """
    if not selected_ideas:
        st.warning("Please select at least one idea before building.")
        return

    st.info("Preparing to generate application code. Please wait...")
    logger.info(f"Building apps for selected ideas: {[idea['title'] for idea in selected_ideas]}")

    selected_entries = st.session_state.get("display_df", pd.DataFrame())
    selected_entries_df = (
        selected_entries[selected_entries["Select"]]
        if "Select" in selected_entries.columns else pd.DataFrame()
    )

    try:
        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(build_app_for_idea, idea, selected_entries_df)
                for idea in selected_ideas
            ]
            results = [f.result() for f in futures]

        st.session_state["app_build_success_message"] = (
            f"Apps generated for these ideas: {', '.join(results)}"
        )
        logger.info("All selected apps were built successfully.")

        load_available_apps()
        st.rerun()
    except Exception as e:
        logger.error(f"Error building the app(s): {e}")
        st.error(f"An error occurred while building the app(s): {e}")


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


def run_app(app_path: str) -> None:
    """
    Executes a dynamically loaded app from the given file path.

    Args:
        app_path (str): Path to the app's Python file.

    Raises:
        AttributeError: If the app does not have a `main()` function.
        Exception: For any errors during the app execution process.
    """
    try:
        logger.info(f"Attempting to run app from path: {app_path}")

        # Dynamically load the module from the given app path
        spec = importlib.util.spec_from_file_location("generated_app", app_path)
        generated_app = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(generated_app)

        # Check and execute the main function
        if hasattr(generated_app, 'main'):
            logger.info("Executing main() function of the generated app.")
            generated_app.main()
        else:
            logger.error("The selected app does not have a main() function to run.")
            raise AttributeError("The selected app does not have a main() function to run.")

    except Exception as e:
        app_name_slug = os.path.basename(os.path.dirname(app_path))
        error_message = str(e)

        logger.error(f"Error running app '{app_name_slug}': {error_message}")

        # Store error details in session state
        st.session_state["run_error"] = {
            "app_name_slug": app_name_slug,
            "error_message": error_message
        }

        st.error(f"An error occurred while running the app: {error_message}")
