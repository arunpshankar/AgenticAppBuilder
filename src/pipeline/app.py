from src.llm.generate import generate_app_code_with_llm
from src.llm.generate import generate_ideas_with_llm
from src.config.setup import GOOGLE_ICON_PATH
from src.db.crud import purge_and_load_csv
from src.config.setup import PROJECT_ROOT
from src.utils.io import save_app_code
from src.config.setup import CSV_PATH
from src.config.logging import logger
from src.db.crud import get_entries
import streamlit as st
import time
import os


def run_ideation():
    """
    Run the ideation process with step-by-step logs and generate ideas using a Gemini LLM.
    Yields:
        str or tuple:
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

    ideas = generate_ideas_with_llm(num_ideas=3)
    yield ("IDEAS_RESULT", ideas)


def run():
    """
    Streamlit application entry point.
    Sets up the page configuration, handles CSV uploads, triggers ideation,
    displays available entries, allows selecting ideas, and builds the app code.
    """
    st.set_page_config(
        page_title="Agentic App Builder",
        layout="wide",
        page_icon="💡",
        initial_sidebar_state="expanded"
    )

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
        for step in run_ideation():
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

    # Display and select ideas
    if st.session_state["ideas"]:
        st.subheader("Ideation Results")
        st.write("Select one or more ideas to build into an app:")

        ideas = st.session_state["ideas"]
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

        # Build the selected app(s)
        if st.button("Build App"):
            if not st.session_state["selected_ideas"]:
                st.warning("Please select at least one idea before building.")
            else:
                st.info("Preparing to generate application code. Please wait...")

                if st.session_state["selected_ideas"]:
                    app_name = st.session_state["selected_ideas"][0]['title']
                else:
                    app_name = "my_new_app"
                app_name_slug = app_name.lower().replace(" ", "_")
                apps_dir = os.path.join(PROJECT_ROOT, 'src', 'apps', app_name_slug)
                os.makedirs(apps_dir, exist_ok=True)

                st.info("Generating application code. Please wait...")
                frontend_code, backend_code = generate_app_code_with_llm(st.session_state["selected_ideas"], app_name_slug)
                save_app_code(app_name_slug, frontend_code, backend_code)
                st.success(f"App code generated and saved in `src/apps/{app_name_slug}/`!")
                st.session_state["app_built"] = True

    if st.session_state["app_built"]:
        st.subheader("Your App is Ready!")
        st.markdown("The generated code has been saved in the `./src/apps/<app_name>/` directory.")
        st.markdown("You can now integrate and run it locally, or further refine the code.")

if __name__ == "__main__":
    try:
        run()
    except Exception as e:
        logger.error("Unhandled exception in main: %s", e)
        st.error(f"An unexpected error occurred: {e}")
