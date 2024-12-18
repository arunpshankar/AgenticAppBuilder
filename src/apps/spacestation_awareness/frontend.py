import streamlit as st
from typing import Dict, List
from src.apps.spacestation_awareness import backend
from src.llm.gemini import generate_content
from src.config.client import initialize_genai_client

gemini_client = initialize_genai_client()
MODEL_ID = "gemini-2.0-flash-exp"

def process_with_gemini(prompt: str) -> str:
    """
    Process content through Gemini and format as markdown.
    
    Args:
        prompt (str): Input prompt for Gemini
        
    Returns:
        str: Formatted markdown response
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
    st.title("ISS Real-Time Location Tracker")

    location_input = st.text_input("Enter your location (e.g., city, address):", "")

    if location_input:
        try:
            iss_location = backend.get_iss_location()
            if iss_location:
                st.subheader("Current ISS Location")
                
                # Format JSON using Gemini
                prompt = f"Format the following JSON as a human-readable markdown: {iss_location}"
                formatted_location = process_with_gemini(prompt)

                st.markdown(formatted_location)
            else:
                st.error("Could not fetch ISS location data.")
        except Exception as e:
           st.error(f"An error occurred: {e}")
        try:
           location_coords = backend.get_coordinates_from_location(location_input)
           if location_coords:
                st.subheader(f"Coordinates of {location_input}")
                prompt = f"Format the following JSON as a human-readable markdown: {location_coords}"
                formatted_coords = process_with_gemini(prompt)
                st.markdown(formatted_coords)
                # Display map
                st.map(location_coords)

           else:
               st.error("Could not fetch coordinates for your location.")
        except Exception as e:
            st.error(f"An error occurred: {e}")
if __name__ == "__main__":
    main()