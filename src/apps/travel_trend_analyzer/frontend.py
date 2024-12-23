import streamlit as st
from typing import Dict, List
from src.apps.travel_trend_analyzer import backend
from src.llm.gemini_text import generate_content
from src.config.client import initialize_genai_client

gemini_client = initialize_genai_client()
MODEL_ID = "gemini-2.0-flash-exp"

def process_with_gemini(prompt: str) -> str:
    """
    Uses Gemini to process and format text.

    Args:
        prompt (str): The prompt for Gemini.

    Returns:
        str: The processed text from Gemini.
    """
    response = generate_content(gemini_client, MODEL_ID, prompt)
    return response.text

def main():
    """
    Primary entry point for the Streamlit application.
    Responsibilities:
    - Configure and render the user interface
    - Handle user inputs and interactions
    - Process and display data from backend
    - Format JSON responses using Gemini
    """
    st.title("Travel Trend Analyzer")

    destinations_input = st.text_input("Enter destinations (comma-separated):")
    airlines_to_include = st.text_input("Airlines to include (comma-separated, optional):")
    airlines_to_exclude = st.text_input("Airlines to exclude (comma-separated, optional):")


    if st.button("Analyze"):
        if not destinations_input:
            st.error("Please enter at least one destination.")
            return

        destinations = [dest.strip() for dest in destinations_input.split(",")]
        airlines_include = [airline.strip() for airline in airlines_to_include.split(",")] if airlines_to_include else []
        airlines_exclude = [airline.strip() for airline in airlines_to_exclude.split(",")] if airlines_to_exclude else []


        try:
            trends_data, flights_data = backend.fetch_travel_data(destinations, airlines_include, airlines_exclude)

            if trends_data:
                st.subheader("Trending Destinations:")
                formatted_trends = process_with_gemini(f"Format the following trends data in a user-friendly way: {trends_data}")
                st.write(formatted_trends)
            else:
                st.warning("No trend data found for provided destinations.")

            if flights_data:
                st.subheader("Flight Options:")
                formatted_flights = process_with_gemini(f"Format the following flight data in a user-friendly way: {flights_data}")
                st.write(formatted_flights)
            else:
                st.warning("No flight data found based on the given criteria.")

        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()