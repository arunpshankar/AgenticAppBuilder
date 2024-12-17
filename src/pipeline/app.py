from src.config.setup import GOOGLE_ICON_PATH
from src.llm.generate import generate_ideas
from src.llm.generate import build_app_code
from src.db.crud import purge_and_load_csv
from src.config.setup import PROJECT_ROOT
from src.utils.io import save_app_code
from src.config.setup import CSV_PATH
from src.config.logging import logger
from src.db.crud import get_entries
from typing import Generator, Union, Tuple, List
import streamlit as st
import pandas as pd
import time
import os
import importlib.util
from concurrent.futures import ThreadPoolExecutor

def load_available_apps():
    """
    Scan the `src/apps/` directory for any subdirectories containing a `frontend.py`
    file and update st.session_state["available_apps"].
    """
    apps_base_dir = os.path.join(PROJECT_ROOT, 'src', 'apps')
    if "available_apps" not in st.session_state:
        st.session_state["available_apps"] = {}

    # Clear existing to avoid duplicates if running multiple times
    st.session_state["available_apps"].clear()

    if os.path.exists(apps_base_dir):
        for entry in os.listdir(apps_base_dir):
            d_path = os.path.join(apps_base_dir, entry)
            if os.path.isdir(d_path):
                frontend_path = os.path.join(d_path, "frontend.py")
                if os.path.exists(frontend_path):
                    # Store relative path so run_app can locate it
                    st.session_state["available_apps"][entry] = os.path.relpath(frontend_path, start='.')

def run_ideation(num_ideas: int = 3) -> Generator[Union[str, Tuple[str, List[dict]]], None, None]:
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

    # Generate ideas using the LLM
    try:
        ideas = generate_ideas(num_ideas=num_ideas)
        logger.debug(f"{len(ideas)} ideas generated successfully.")
    except Exception as e:
        logger.error(f"Error during idea generation: {e}")
        ideas = []
    
    yield ("IDEAS_RESULT", ideas)

def handle_csv_upload(uploaded_file) -> None:
    if uploaded_file is not None:
        try:
            logger.debug("Uploading CSV file to disk.")
            with open(CSV_PATH, 'wb') as f:
                f.write(uploaded_file.read())
        except Exception as e:
            logger.error(f"Failed to save uploaded CSV: {e}")
            st.error(f"Failed to save uploaded CSV: {e}")
            return

        logger.debug("CSV file uploaded successfully. Attempting to load into DB.")
        success, message = purge_and_load_csv(CSV_PATH)
        if success:
            st.success(message)
        else:
            st.error(message)

def display_entries(entries_df: pd.DataFrame) -> None:
    st.subheader("Available Entries")
    if entries_df is not None and not entries_df.empty:
        st.dataframe(entries_df)
    else:
        st.write("No entries available. Please upload a CSV.")

def display_ideas(ideas: List[dict]) -> None:
    st.subheader("Ideation Results")
    st.write("Select one or more ideas to build into separate apps:")

    rows = (len(ideas) // 3) + (1 if len(ideas) % 3 > 0 else 0)
    current_selected_ideas = []

    for row_i in range(rows):
        cols = st.columns(3, gap="small")
        for col_i in range(3):
            idea_index = row_i * 3 + col_i
            if idea_index < len(ideas):
                idea = ideas[idea_index]
                with cols[col_i]:
                    st.markdown(f"""
                    <div style="border:1px solid #ddd; border-radius:5px; padding:10px; margin-bottom:15px;">
                        <h4 style="margin-top:0; margin-bottom:5px;">{idea['title']}</h4>
                        <p style="margin-top:0; margin-bottom:10px;">{idea['description']}</p>
                        <p style="margin-bottom:5px;"><strong>APIs Used:</strong> {", ".join(idea['apis_used'])}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    selected = st.checkbox("Select this idea", key=f"idea_select_{idea_index}")
                    if selected:
                        current_selected_ideas.append(idea)

    st.session_state["selected_ideas"] = current_selected_ideas

def build_app_for_idea(idea: dict):
    """
    Build a single app for a given idea.
    Returns the slug of the built app or raises an exception on failure.
    """
    app_name = idea['title']
    app_name_slug = app_name.lower().replace(" ", "_").replace("-", "_")
    apps_dir = os.path.join(PROJECT_ROOT, 'src', 'apps', app_name_slug)
    os.makedirs(apps_dir, exist_ok=True)
    frontend_code, backend_code = build_app_code([idea], app_name_slug)
    save_app_code(app_name_slug, frontend_code, backend_code)
    return app_name_slug

def build_selected_apps(selected_ideas: List[dict]) -> None:
    if not selected_ideas:
        st.warning("Please select at least one idea before building.")
        return

    st.info("Preparing to generate application code. Please wait...")
    logger.info(f"Building apps for selected ideas: {[idea['title'] for idea in selected_ideas]}")

    # If multiple ideas are selected, build each one as a separate app in parallel
    try:
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(build_app_for_idea, idea) for idea in selected_ideas]
            results = [f.result() for f in futures]
        
        # Store success message in session state
        st.session_state["app_build_success_message"] = f"Apps generated for these ideas: {', '.join(results)}"
        
        # After building the apps, reload the available apps and then rerun
        load_available_apps()
        st.rerun()

    except Exception as e:
        logger.error(f"Error building the app(s): {e}")
        st.error(f"An error occurred while building the app(s): {e}")

def run_app(app_path: str) -> None:
    spec = importlib.util.spec_from_file_location("generated_app", app_path)
    generated_app = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(generated_app)

    if hasattr(generated_app, 'main'):
        generated_app.main()
    else:
        st.error("The selected app does not have a main() function to run.")

def run():
    st.set_page_config(
        page_title="Agentic App Builder",
        layout="wide",
        page_icon="💡",
        initial_sidebar_state="expanded"
    )

    # Initialize session states if not present
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
    if "available_apps" not in st.session_state:
        st.session_state["available_apps"] = {}
    if "sidebar_width" not in st.session_state:
        st.session_state["sidebar_width"] = 300  # default width

    # Load available apps at startup
    load_available_apps()

    # Sidebar
    with st.sidebar:
        if os.path.exists(GOOGLE_ICON_PATH):
            st.image(GOOGLE_ICON_PATH, width=40)
        st.title("Agentic App Builder")

        # Sidebar width slider
        st.session_state["sidebar_width"] = st.slider(
            "Adjust Sidebar Width",
            min_value=200,
            max_value=600,
            value=st.session_state["sidebar_width"],
            help="Use this slider to adjust the sidebar width"
        )

        # Sidebar buttons
        ideate_trigger = st.button("Ideate", help="Start the ideation process to generate API combination ideas.")
        refresh_trigger = st.button("Refresh Entries", help="Refresh the entries table from the database.")

        # Run Generated App
        st.subheader("Run Generated App")
        available_apps = st.session_state.get("available_apps", {})
        if available_apps:
            selected_app = st.selectbox("Select an app to run", ["None"] + list(available_apps.keys()))
            if selected_app != "None":
                app_path = available_apps[selected_app]
                st.info(f"Running app: {selected_app}")
                run_app(app_path)
        else:
            st.write("No generated apps available yet.")

    # Apply custom CSS for sidebar width
    st.markdown(f"""
    <style>
    [data-testid="stSidebar"] {{
        min-width: {st.session_state["sidebar_width"]}px;
        max-width: {st.session_state["sidebar_width"]}px;
    }}
    </style>
    """, unsafe_allow_html=True)

    st.header("Welcome to Agentic App Builder")

    # CSV Upload Section
    st.subheader("Upload CSV")
    uploaded_file = st.file_uploader("Select your CSV file", type=['csv'])
    handle_csv_upload(uploaded_file)

    # Logs Section
    logs_expander = st.expander("Logs / Traces", expanded=False)
    logs_container = logs_expander.empty()

    # Refresh entries if triggered
    if refresh_trigger:
        try:
            st.session_state["entries_df"] = get_entries()
            logger.debug("Entries refreshed successfully from the database.")
        except Exception as e:
            logger.error(f"Failed to refresh entries: {e}")
            st.error(f"Failed to refresh entries: {e}")

    # Handle Ideation process
    if ideate_trigger:
        st.session_state["ideas"] = []
        st.session_state["logs"] = []
        st.session_state["selected_ideas"] = []
        st.session_state["app_built"] = False

        st.info("Ideation process started...")
        logs_area = logs_container.empty()

        # Run the ideation generator
        for step in run_ideation():
            if isinstance(step, tuple) and step[0] == "IDEAS_RESULT":
                st.session_state["ideas"] = step[1]
            else:
                st.session_state["logs"].append(step)
                logs_area.write("\n".join(map(str, st.session_state["logs"])))

        # Check if ideas were generated
        if st.session_state["ideas"]:
            st.success("Ideas generated!")
            logger.debug("Ideas generated successfully.")
        else:
            st.warning("No ideas generated.")

    # Display entries
    display_entries(st.session_state["entries_df"])

    # Display and select ideas
    if st.session_state["ideas"]:
        display_ideas(st.session_state["ideas"])

        # Build the selected app(s)
        if st.button("Build App"):
            build_selected_apps(st.session_state["selected_ideas"])

    # Display the success message (if any) just before "Your App(s) are Ready!"
    if "app_build_success_message" in st.session_state:
        st.success(st.session_state["app_build_success_message"])
        del st.session_state["app_build_success_message"]
        st.session_state["app_built"] = True

    # If app is built, inform the user
    if st.session_state["app_built"]:
        st.subheader("Your App(s) are Ready!")
        st.markdown("The generated code has been saved in the `./src/apps/<app_name>/` directories.")
        st.markdown("You can now select them from the sidebar to run them inline.")


if __name__ == "__main__":
    try:
        run()
    except Exception as e:
        logger.error("Unhandled exception in main: %s", e)
        st.error(f"An unexpected error occurred: {e}")
