import streamlit as st
from typing import Dict, List
from src.apps.london_commute_playlist import backend
from src.llm.gemini_text import generate_content
from src.config.client import initialize_genai_client

gemini_client = initialize_genai_client()
MODEL_ID = "gemini-2.0-flash-exp"

def process_with_gemini(prompt: str) -> str:
    """
    Processes a prompt with Gemini and returns the generated text.

    Args:
        prompt (str): The prompt to send to Gemini.

    Returns:
        str: The generated text response.
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
    st.title("London Commute Playlist Generator")

    st.header("Travel Information")
    start_location = st.text_input("Enter Starting Location (e.g., 'London Bridge')")
    destination = st.text_input("Enter Destination (e.g., 'Waterloo')")
    travel_mode = st.selectbox("Select Travel Mode", ["tube", "bus", "dlr"])

    st.header("Music Preferences")
    mood = st.selectbox("Select Commute Mood", ["Energetic", "Relaxing", "Upbeat", "Chill"])
    artist_preference = st.text_input("Enter preferred artists (comma separated)", "")

    if st.button("Generate Playlist"):
        if not start_location or not destination:
          st.error("Please enter both start and destination locations.")
          return
        
        with st.spinner("Fetching travel and music data..."):
           try:
             travel_data = backend.get_travel_info(travel_mode)
             if not travel_data or not travel_data.get('lineStatuses'):
                 st.error("Could not retrieve travel data. Please try again later.")
                 return
             
             estimated_travel_time = backend.calculate_travel_time(start_location,destination)
             
             if estimated_travel_time == None:
                st.error("Could not estimate travel time. Please try different locations.")
                return
             
             prompt_for_playlist = f"""
             Generate a playlist for a London commute, based on the following criteria:
             - Commute Mood: {mood}
             - Commute Travel Time: {estimated_travel_time} minutes
             - Artist Preference: {artist_preference}
             - Transport Mode: {travel_mode}
             The response must be a JSON list of songs with the following format:
              [ {{"artist": "...", "title": "...", "lyrics": "..."}} , ...]
             """
             
             playlist_json = process_with_gemini(prompt_for_playlist)
             
             if not playlist_json:
                 st.error("Could not generate a playlist using LLM.")
                 return
             
             st.subheader("Generated Playlist")
             st.json(playlist_json, expanded=False)

           except Exception as e:
              st.error(f"An error occurred: {e}")
              
if __name__ == "__main__":
    main()