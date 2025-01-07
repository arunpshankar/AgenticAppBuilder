from src.config.setup import GOOGLE_ICON_PATH
from src.config.logging import logger 
from src.db.crud import get_entries 
from src.workflow.helper import * 
import streamlit as st 
import os 


def run() -> None:
    """
    Main entry point for the Agentic App Builder Streamlit application. Sets up the page configuration,
    loads session state variables, and provides UI functionality for uploading CSV files, generating
    ideas, and running or building apps.

    Raises:
        Exception: Handles exceptions for refreshing entries, running apps, or other UI interactions.
    """
    # Configure the page
    st.set_page_config(
        page_title="Agentic App Builder",
        layout="wide",
        page_icon="💡",
        initial_sidebar_state="expanded"
    )

    # Load CSS styles
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
        body {
            font-family: 'Nunito Sans', 'Helvetica', sans-serif;
            font-size: 14px;
            color: #333;
            background-color: #f8f8f8;
        }
        h1, h2, h3, h4 {
            font-family: 'Cascadia Code', 'Monaco', monospace;
            color: #222;
        }
        [data-testid="stDataFrameContainer"] div[data-baseweb="checkbox"] input:checked ~ div {
            background-color: #4CAF50 !important;
            border-color: #4CAF50 !important;
        }

        .rainbow-title {
        font-size: 2.5em;
        font-weight: 800;
        background: linear-gradient(to right, red, orange, yellow, green, blue, indigo, violet);
        background-clip: text;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        color: transparent;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Initialize session state variables
    for key, default in {
        "logs": [],
        "ideas": [],
        "entries_df": get_entries(),
        "selected_ideas": [],
        "app_built": False,
        "available_apps": {}
    }.items():
        if key not in st.session_state:
            st.session_state[key] = default

    load_available_apps()

    # Sidebar setup
    with st.sidebar:
        if os.path.exists(GOOGLE_ICON_PATH):
            st.image(GOOGLE_ICON_PATH, width=40)

        st.markdown("<h2 style='font-family: Inter, sans-serif; color:#ea4335;'>Test Panel</h2>", unsafe_allow_html=True)

        ideate_trigger = st.button("Ideate", help="Start the ideation process to generate API combination ideas.", type="primary")
        refresh_trigger = st.button("Refresh Entries", help="Refresh the entries table from the database.", type="secondary")

        st.subheader("Run Generated App")
        available_apps = st.session_state.get("available_apps", {})
        if available_apps:
            selected_app = st.selectbox("Select an app to run", ["None"] + list(available_apps.keys()))
            if selected_app != "None":
                app_path = available_apps[selected_app]
                run_app(app_path)
        else:
            st.write("No generated apps available yet.")

        if "run_error" in st.session_state:
            app_name_slug = st.session_state["run_error"]["app_name_slug"]
            error_message = st.session_state["run_error"]["error_message"]
            st.error(f"Error running the app: {error_message}")

    # Main content
    st.markdown("<h1 class='rainbow-title'>Agentic App Builder</h1>", unsafe_allow_html=True)

    st.subheader("Upload CSV")
    uploaded_file = st.file_uploader("Select your CSV file", type=['csv'])
    handle_csv_upload(uploaded_file)

    logs_expander = st.expander("Logs / Traces", expanded=False)
    logs_container = logs_expander.empty()

    if refresh_trigger:
        try:
            st.session_state["entries_df"] = get_entries()
            if "display_df" in st.session_state:
                del st.session_state["display_df"]
            logger.debug("Entries refreshed successfully from the database.")
        except Exception as e:
            logger.error(f"Failed to refresh entries: {e}")
            st.error(f"Failed to refresh entries: {e}")

    display_entries(st.session_state["entries_df"])

    if ideate_trigger:
        st.session_state.update({
            "ideas": [],
            "logs": [],
            "selected_ideas": [],
            "app_built": False
        })

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

    if st.session_state["ideas"]:
        display_ideas(st.session_state["ideas"])

        if st.button("Build App", type="primary"):
            build_selected_apps(st.session_state["selected_ideas"])

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
