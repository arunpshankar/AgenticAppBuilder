import streamlit as st
from typing import Dict, List
from src.apps.space_event_tracker import backend
from src.llm.gemini_text import generate_content
from src.config.client import initialize_genai_client
from src.config.logging import logger

gemini_client = initialize_genai_client()
MODEL_ID = "gemini-2.0-flash-exp"

def process_with_gemini(prompt: str) -> str:
    """
    Uses Gemini to process a given prompt.

    Args:
        prompt (str): The prompt to send to Gemini.

    Returns:
        str: The processed text response from Gemini.
    """
    try:
        response = generate_content(gemini_client, MODEL_ID, prompt)
        return response.text
    except Exception as e:
        logger.error(f"Error processing with Gemini: {e}")
        return f"Error: Could not format data using Gemini. {e}"

def main():
    """
    Primary entry point for the Streamlit application.
    Responsibilities:
    - Configure and render the user interface
    - Handle user inputs and interactions
    - Process and display data from backend
    - Format JSON responses using Gemini
    """
    st.title("Space Event Tracker")
    st.markdown("Get notified of events happening near the International Space Station.")

    try:
        with st.spinner("Fetching ISS location..."):
            iss_location = backend.get_iss_location()
        
        if iss_location:
            st.success("ISS location fetched successfully!")
            latitude = iss_location.get("latitude")
            longitude = iss_location.get("longitude")
            
            if latitude is not None and longitude is not None:
                st.write(f"ISS Latitude: {latitude}, Longitude: {longitude}")
                with st.spinner("Searching for events near ISS..."):
                    events_data = backend.search_events_near_location(latitude, longitude)
                
                if events_data and events_data.get("events"):
                    
                    formatted_events = process_with_gemini(f"Format the following JSON data as markdown to be displayed to a user, only include information on the title, date, and location of the event: {events_data['events']}")
                    
                    st.subheader("Events Near ISS:")
                    st.markdown(formatted_events)
                
                elif events_data and events_data.get('error'):
                   st.error(f"Error fetching event data: {events_data.get('error')}")
                
                else:
                     st.info("No events found near the ISS location.")
            else:
                st.error("Error: Could not extract latitude or longitude from ISS location data.")

        else:
           st.error("Error: Could not fetch ISS location.")
    
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        st.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()