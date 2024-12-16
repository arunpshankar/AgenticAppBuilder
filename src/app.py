
from sqlalchemy.exc import OperationalError
from sqlalchemy.exc import SQLAlchemyError
from agents.ideation import run_ideation
from src.config.logging import logger 
from sqlalchemy import create_engine
from sqlalchemy import text 
from typing import Tuple
import streamlit as st
import pandas as pd
import time
import os


# Configuration 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')
DB_DIR = os.path.join(PROJECT_ROOT, 'db')
DB_PATH = os.path.join(DB_DIR, 'apis.db')  # Ensure this line appears before using DB_PATH
CSV_PATH = os.path.join(DATA_DIR, 'apis.csv')
IMAGES_DIR = os.path.join(BASE_DIR, 'images')
GOOGLE_ICON_PATH = os.path.join(IMAGES_DIR, 'google_icon.png')

# Ensure DB directory exists
os.makedirs(DB_DIR, exist_ok=True)

# Create engine
engine = create_engine(f'sqlite:///{DB_PATH}', echo=False)

def validate_csv(df: pd.DataFrame) -> Tuple[bool, str]:
    """
    Validate the CSV DataFrame to ensure required columns are present.

    :param df: DataFrame loaded from the CSV.
    :return: A tuple (is_valid, message) indicating whether validation succeeded and a related message.
    """
    required_columns = [
        "name", "category", "base_url", "endpoint", 
        "description", "query_parameters", "example_request", "example_response"
    ]
    for col in required_columns:
        if col not in df.columns:
            return False, f"Missing required column: {col}"
    return True, "CSV is valid"


def purge_and_load_csv(csv_path: str) -> Tuple[bool, str]:
    """
    Load CSV into the database, replacing any existing table.

    :param csv_path: Path to the CSV file.
    :return: (success, message) indicating if the operation was successful and a description message.
    """
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
        logger.error("General error loading CSV into DB: %s", e)
        return False, f"Unknown error loading CSV: {e}"


def get_entries() -> pd.DataFrame:
    """
    Retrieve all entries from the 'apientry' table in the database.

    :return: DataFrame containing the entries, or an empty DataFrame if none.
    """
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
        # Save the uploaded file temporarily
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

    # Refresh entries if triggered
    if refresh_trigger:
        st.session_state["entries_df"] = get_entries()
        logger.debug("Entries refreshed from the database.")

    # Handle ideation process
    if ideate_trigger:
        st.session_state["ideas"] = []
        st.session_state["logs"] = []

        # Run ideation in a streaming manner
        logs_area = logs_container.empty()
        st.info("Ideation process started...")

        # Stream logs from the ideation generator
        for log_line in run_ideation(engine=engine):
            st.session_state["logs"].append(log_line)
            logs_area.write("\n".join(map(str, st.session_state["logs"])))

            logger.debug("Ideation step: %s", log_line)

        # After streaming logs, simulate finalization and idea generation
        st.warning("Ideation completed. Generating ideas...")
        time.sleep(1)  # simulate loading

        # Mock final ideas
        st.session_state["ideas"] = [
            {
                "title": "Cat Weather Trivia App",
                "description": "Displays cat facts alongside current weather info.",
                "apis_used": ["cat facts", "7timer!"]
            },
            {
                "title": "Dog Jokes in Your Area",
                "description": "Shows dog images and localized jokes from your ZIP code.",
                "apis_used": ["dog facts", "zip info", "jokes"]
            },
            {
                "title": "Geo Demographics Artist Insights",
                "description": "Presents artworks filtered by nationality and predicted age.",
                "apis_used": ["age by name", "nationality by name", "art institute of chicago"]
            }
        ]
        st.success("Ideas generated!")
        logger.debug("Ideas generated successfully.")

    # Show entries
    st.subheader("Available Entries")
    if st.session_state["entries_df"] is not None and not st.session_state["entries_df"].empty:
        st.dataframe(st.session_state["entries_df"])
    else:
        st.write("No entries available. Please upload a CSV.")

    # Show ideas if available
    if st.session_state["ideas"]:
        st.subheader("Ideation Results")
        col1, col2, col3 = st.columns(3)
        columns = [col1, col2, col3]
        for i, idea in enumerate(st.session_state["ideas"]):
            with columns[i]:
                st.markdown(f"**{idea['title']}**")
                st.write(idea["description"])
                st.write("APIs Used:")
                for api in idea["apis_used"]:
                    st.markdown(f"- {api}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error("Unhandled exception in main: %s", e)
        st.error(f"An unexpected error occurred: {e}")
