import streamlit as st
from typing import Dict, List
from src.apps.dynamic_travel_demand_planner import backend
from src.llm.gemini_text import generate_content
from src.config.client import initialize_genai_client

gemini_client = initialize_genai_client()
MODEL_ID = "gemini-2.0-flash-exp"

def process_with_gemini(prompt: str) -> str:
    """
    Processes a prompt using the Gemini model and returns the response text.

    Args:
        prompt: The input prompt for Gemini.

    Returns:
        The text response from Gemini.
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
    st.title("Dynamic Travel Demand Planner")

    with st.expander("Google Trends Analysis", expanded=True):
         
        region = st.text_input("Enter Region for Google Trends Analysis", "United States")
        if st.button("Get Trends", key="trends"):
           try:
                with st.spinner("Fetching trends..."):
                    trends_data = backend.get_google_trends_data(region)
                    if trends_data:
                        formatted_data = process_with_gemini(f"Format this JSON to be human readable and display only the title and the percentage of interest per region: {trends_data}")
                        st.markdown(formatted_data)
                    else:
                       st.error("Failed to fetch trends data.")
           except Exception as e:
               st.error(f"An error occurred: {e}")
            
    with st.expander("Flight Search", expanded=False):
        origin = st.text_input("Enter Origin Airport", "JFK")
        destination = st.text_input("Enter Destination Airport", "LAX")
        airline = st.text_input("Enter Airline (optional, use comma to separate airlines", "")
        if st.button("Search Flights", key="flights"):
             try:
                with st.spinner("Searching flights..."):
                    flights_data = backend.search_flights(origin, destination, airline.split(',') if airline else [])
                    if flights_data:
                        formatted_flights = process_with_gemini(f"Format this JSON to be human readable and display the airlines, departure time, arrival time, price and carrier: {flights_data}")
                        st.markdown(formatted_flights)
                    else:
                        st.error("No flights found for the specified criteria.")
             except Exception as e:
                st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()