import os
import time
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine, text
from agents.ideation import run_ideation

# Configurations
DATA_DIR = 'data'
DB_PATH = 'db/apis.db'
CSV_PATH = os.path.join(DATA_DIR, 'apis.csv')

# Setup the database engine
engine = create_engine(f'sqlite:///{DB_PATH}', echo=False)

def purge_and_load_csv(csv_path):
    # Purge DB: drop table if exists
    with engine.connect() as conn:
        conn.execute(text("DROP TABLE IF EXISTS apientry"))

    # Load CSV into DataFrame
    df = pd.read_csv(csv_path)
    # Rename columns if needed. Assumes CSV columns match exactly:
    # name, category, base_url, endpoint, description, query_parameters, example_request, example_response

    # Load DataFrame into SQL table
    df.to_sql('apientry', con=engine, if_exists='replace', index=False)

def get_entries():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM apientry"))
        df = pd.DataFrame(result.fetchall(), columns=result.keys())
    return df

def main():
    st.set_page_config(page_title="Agentic App Builder", layout="centered", page_icon="💡")

    st.title("Agentic App Builder")

    # Upload CSV Section
    st.subheader("Upload CSV")
    uploaded_file = st.file_uploader("Select your CSV file", type=['csv'])
    if uploaded_file is not None:
        # Save the uploaded file temporarily
        with open(CSV_PATH, 'wb') as f:
            f.write(uploaded_file.read())
        # Purge and load
        purge_and_load_csv(CSV_PATH)
        st.success("CSV uploaded and database reloaded!")

    # Actions Section
    st.subheader("Actions")
    col1, col2 = st.columns([1,1])
    with col1:
        ideate_trigger = st.button("Ideate")
    with col2:
        refresh_trigger = st.button("Refresh Entries")

    logs_expanded = st.expander("Logs / Traces", expanded=False)
    logs_area = logs_expanded.empty()

    # State to hold logs
    if "logs" not in st.session_state:
        st.session_state.logs = []

    if ideate_trigger:
        # Run ideation
        logs = run_ideation()
        st.session_state.logs = logs
        # Display logs in the expander
        for log in logs:
            logs_area.write(log)

    # Refresh Entries or load them initially
    if refresh_trigger or "entries_df" not in st.session_state:
        if os.path.exists(DB_PATH):
            st.session_state.entries_df = get_entries()
        else:
            st.session_state.entries_df = pd.DataFrame()

    # Show entries
    st.subheader("Available Entries")
    if st.session_state.entries_df is not None and not st.session_state.entries_df.empty:
        st.dataframe(st.session_state.entries_df)
    else:
        st.write("No entries available. Please upload a CSV.")

    # If logs are already present in the session state, display them
    if st.session_state.logs:
        with logs_expanded:
            for log in st.session_state.logs:
                logs_area.write(log)

if __name__ == "__main__":
    main()
