import streamlit as st
from typing import Dict, List
from src.apps.local_event_trend_analyzer import backend
from src.llm.gemini_text import generate_content
from src.config.client import initialize_genai_client
from src.config.logging import logger

gemini_client = initialize_genai_client()
MODEL_ID = "gemini-2.0-flash-exp"

def process_with_gemini(prompt: str) -> str:
    """
    Processes the given prompt with Gemini to format the response.

    Args:
        prompt (str): The prompt to send to Gemini.

    Returns:
        str: The text response from Gemini.
    """
    try:
        response = generate_content(gemini_client, MODEL_ID, prompt)
        return response.text
    except Exception as e:
        logger.error(f"Error processing with Gemini: {e}")
        return "Error processing with Gemini."

def main():
    """
    Primary entry point for the Streamlit application.
    Responsibilities:
    - Configure and render the user interface
    - Handle user inputs and interactions
    - Process and display data from backend
    - Format JSON responses using Gemini
    """
    st.title("Local Event Trend Analyzer")

    location = st.text_input("Enter Location (e.g., New York, NY):")
    query = st.text_input("Enter Search Query (e.g., coffee shops):")

    if location and query:
        try:
            with st.spinner("Fetching data..."):
                local_results, events_results, trends_results = backend.fetch_local_data(location, query)

                st.subheader("Local Business Results:")
                if local_results and isinstance(local_results, dict) and "local_results" in local_results:
                    prompt = f"Format this JSON data into a user-friendly list of local business results. The json data is: {local_results['local_results']}"
                    formatted_local_results = process_with_gemini(prompt)
                    st.write(formatted_local_results)
                else:
                   st.write("No local business results found.")
    
                st.subheader("Event Results:")
                if events_results and isinstance(events_results, dict) and "events_results" in events_results:
                    prompt = f"Format this JSON data into a user-friendly list of local event results. The json data is: {events_results['events_results']}"
                    formatted_events_results = process_with_gemini(prompt)
                    st.write(formatted_events_results)
                else:
                   st.write("No event results found.")
    
                st.subheader("Trend Analysis:")
                if trends_results and isinstance(trends_results, dict) and "compared_breakdown_by_region" in trends_results:
                    prompt = f"Format this JSON data into a user-friendly analysis of trending events by region. The json data is: {trends_results['compared_breakdown_by_region']}"
                    formatted_trends_results = process_with_gemini(prompt)
                    st.write(formatted_trends_results)
                else:
                   st.write("No trend analysis found.")


        except Exception as e:
            logger.error(f"Error processing data: {e}")
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()