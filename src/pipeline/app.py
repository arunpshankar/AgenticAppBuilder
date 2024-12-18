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

    # Determine selected names
    if "display_df" in st.session_state and "entries_df" in st.session_state:
        selected_df = st.session_state["display_df"]
        if "Select" in selected_df and selected_df["Select"].any():
            selected_names = selected_df.loc[selected_df["Select"], "name"].tolist()
        else:
            selected_names = []
    else:
        selected_names = []

    # Generate ideas using the LLM based on selected_names
    try:
        ideas = generate_ideas(num_ideas=num_ideas, selected_names=selected_names)
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

    if entries_df is None or entries_df.empty:
        st.write("No entries available. Please upload a CSV.")
        return

    st.markdown(
        "<p style='color:gray;font-size:13px;'>If you do not select any rows, random APIs will be chosen for you. "
        "Selected rows will be used for ideation and code generation. To avoid scrolling resets, select multiple rows first and then click 'Submit Selections'.</p>",
        unsafe_allow_html=True
    )

    # Initialize display_df in session state if needed
    if "display_df" not in st.session_state or \
       st.session_state["display_df"].shape[0] != entries_df.shape[0]:
        display_df = entries_df.copy().reset_index(drop=True)
        if 'name' not in display_df.columns:
            st.warning("No 'name' column found in entries. Please ensure CSV has a 'name' column.")
            return
        # Add a "Select" column with boolean checkboxes
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

    # Update session_state after the user submits the form
    if submit:
        st.session_state["display_df"] = edited_df

    # Highlight selected rows below the editor
    selected_rows = st.session_state["display_df"][st.session_state["display_df"]["Select"]]
    if not selected_rows.empty:
        st.write("**Selected Entries:**")
        # Apply a background color to highlight selected rows
        styled_selected = selected_rows.style.apply(
            lambda row: ['background-color: #D9F2E6' for _ in row],
            axis=1
        )
        st.dataframe(styled_selected, use_container_width=True)
    else:
        st.write("No entries selected.")



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
    app_name = idea['title']
    app_name_slug = app_name.lower().replace(" ", "_").replace("-", "_")
    apps_dir = os.path.join(PROJECT_ROOT, 'src', 'apps', app_name_slug)
    os.makedirs(apps_dir, exist_ok=True)

    # Use only the selected entries
    selected_entries = st.session_state.get("selected_entries_df", pd.DataFrame())

    frontend_code, backend_code = build_app_code([idea], app_name_slug, entries=selected_entries)
    save_app_code(app_name_slug, frontend_code, backend_code)
    return app_name_slug

def build_selected_apps(selected_ideas: List[dict]) -> None:
    if not selected_ideas:
        st.warning("Please select at least one idea before building.")
        return

    st.info("Preparing to generate application code. Please wait...")
    logger.info(f"Building apps for selected ideas: {[idea['title'] for idea in selected_ideas]}")

    try:
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(build_app_for_idea, idea) for idea in selected_ideas]
            results = [f.result() for f in futures]
        
        st.session_state["app_build_success_message"] = f"Apps generated for these ideas: {', '.join(results)}"
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

    # Modern, unique, pretty, and polished font and styling + green checkboxes
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
    body {
        font-family: 'Inter', sans-serif;
        font-size: 14px;
        color: #333;
        background-color: #f8f8f8;
    }
    h1, h2, h3, h4 {
        font-family: 'Inter', sans-serif;
        color: #222;
    }
    /* Make checked checkboxes green in data_editor */
    [data-testid="stDataFrameContainer"] div[data-baseweb="checkbox"] input:checked ~ div {
        background-color: #4CAF50 !important;
        border-color: #4CAF50 !important;
    }
    </style>
    """, unsafe_allow_html=True)

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
    # display_df initialized in display_entries if needed

    load_available_apps()

    # Sidebar
    with st.sidebar:
        if os.path.exists(GOOGLE_ICON_PATH):
            st.image(GOOGLE_ICON_PATH, width=40)
        st.title("Agentic App Builder")

        sidebar_width = st.slider(
            "Adjust Sidebar Width",
            min_value=200,
            max_value=600,
            value=300,
            help="Use this slider to adjust the sidebar width"
        )

        ideate_trigger = st.button("Ideate", help="Start the ideation process to generate API combination ideas.")
        refresh_trigger = st.button("Refresh Entries", help="Refresh the entries table from the database.")

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

    st.markdown(f"""
    <style>
    [data-testid="stSidebar"] {{
        min-width: {sidebar_width}px;
        max-width: {sidebar_width}px;
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
            if "display_df" in st.session_state:
                del st.session_state["display_df"]
            logger.debug("Entries refreshed successfully from the database.")
        except Exception as e:
            logger.error(f"Failed to refresh entries: {e}")
            st.error(f"Failed to refresh entries: {e}")

    # Display entries and selection
    display_entries(st.session_state["entries_df"])

    # Handle Ideation process
    if ideate_trigger:
        st.session_state["ideas"] = []
        st.session_state["logs"] = []
        st.session_state["selected_ideas"] = []
        st.session_state["app_built"] = False

        st.info("Ideation process started...")
        logs_area = logs_container.empty()

        for step in run_ideation():
            if isinstance(step, tuple) and step[0] == "IDEAS_RESULT":
                st.session_state["ideas"] = step[1]
            else:
                st.session_state["logs"].append(step)
                logs_area.write("\n".join(map(str, st.session_state["logs"])))

        if st.session_state["ideas"]:
            st.success("Ideas generated!")
            logger.debug("Ideas generated successfully.")
        else:
            st.warning("No ideas generated.")

    # Display and select ideas
    if st.session_state["ideas"]:
        display_ideas(st.session_state["ideas"])

        # Build the selected app(s)
        if st.button("Build App"):
            build_selected_apps(st.session_state["selected_ideas"])

    # Display success message if apps built
    if "app_build_success_message" in st.session_state:
        st.success(st.session_state["app_build_success_message"])
        del st.session_state["app_build_success_message"]
        st.session_state["app_built"] = True

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
