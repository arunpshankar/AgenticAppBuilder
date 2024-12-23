import streamlit as st
from typing import Dict, List
from src.apps.astro_weather_lyric_match import backend
from src.llm.gemini_text import generate_content
from src.config.client import initialize_genai_client
from src.config.logging import logger

gemini_client = initialize_genai_client()
MODEL_ID = "gemini-2.0-flash-exp"

def process_with_gemini(prompt: str) -> str:
    """
    Processes a prompt using the Gemini model.

    Args:
        prompt (str): The prompt to send to Gemini.

    Returns:
        str: The response from Gemini.
    """
    try:
        response = generate_content(gemini_client, MODEL_ID, prompt)
        return response.text
    except Exception as e:
        logger.error(f"Error processing with Gemini: {e}")
        return "Error processing response."

def main():
    """
    Primary entry point for the Streamlit application.
    Responsibilities:
    - Configure and render the user interface
    - Handle user inputs and interactions
    - Process and display data from backend
    - Format JSON responses using Gemini
    """
    st.title("Astro Weather Lyric Match")

    with st.container(use_container_width=True):
        col1, col2 = st.columns(2)
        with col1:
            latitude = st.number_input("Enter Latitude", value=51.5074, step=0.0001)
        with col2:
            longitude = st.number_input("Enter Longitude", value=0.1278, step=0.0001)

    if st.button("Get Astro Weather and Lyrics"):
        try:
            with st.spinner("Fetching astronomical weather data..."):
                weather_data = backend.get_astro_weather(latitude, longitude)
            
            if weather_data:
                st.subheader("Astronomical Weather Data")
                formatted_weather_data = process_with_gemini(f"Format the following weather data to be human-readable and easily understood, highlight the key celestial information: {weather_data}")
                st.markdown(formatted_weather_data)

                with st.spinner("Finding matching lyrics..."):
                  # Example usage to find lyrics matching celestial event keywords
                  celestial_event = formatted_weather_data # Use the formatted text as keywords 
                  lyrics_result = backend.search_lyrics_by_theme(celestial_event)

                  if lyrics_result:
                    st.subheader("Matching Lyrics")
                    formatted_lyrics = process_with_gemini(f"Format the following lyrics to be human-readable, extract key lyrical themes: {lyrics_result}")
                    st.markdown(formatted_lyrics)
                  else:
                      st.error("Could not find matching lyrics.")
            else:
                st.error("Could not fetch weather data.")
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            st.error(f"An unexpected error occurred: {e}")
            
if __name__ == "__main__":
    main()