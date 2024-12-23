import streamlit as st
from typing import Dict, List
from src.apps.vacation_planning_assistant import backend
from src.llm.gemini_text import generate_content
from src.config.client import initialize_genai_client

gemini_client = initialize_genai_client()
MODEL_ID = "gemini-2.0-flash-exp"

def process_with_gemini(prompt: str) -> str:
    """
    Processes a prompt using the Gemini model and returns the formatted text response.

    Args:
        prompt (str): The prompt to send to the Gemini model.

    Returns:
        str: The formatted text response from the Gemini model.
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
    st.title("Vacation Planning Assistant")

    location = st.text_input("Enter Location (e.g., New York):")
    check_in_date = st.text_input("Enter Check-in Date (YYYY-MM-DD):")
    check_out_date = st.text_input("Enter Check-out Date (YYYY-MM-DD):")

    if st.button("Search Hotels"):
        if location and check_in_date and check_out_date:
            try:
                hotels_data = backend.search_hotels(location, check_in_date, check_out_date)
                if hotels_data and "properties" in hotels_data:
                    formatted_hotel_data = process_with_gemini(f"Please format this hotel JSON into a user-friendly list of hotel names and prices: {hotels_data}")
                    st.subheader("Hotel Options:")
                    st.markdown(formatted_hotel_data)
                else:
                    st.error("No hotel results found or an error occurred.")

            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.warning("Please enter location, check-in date, and check-out date.")

    hotel_name_for_videos = st.text_input("Enter Hotel Name for Video Search (optional):")
    if st.button("Search Videos"):
       if hotel_name_for_videos and location:
            try:
                video_data = backend.search_youtube_videos(f"{hotel_name_for_videos} {location} hotel reviews")
                if video_data and "video_results" in video_data:
                    formatted_video_data = process_with_gemini(f"Please format this youtube JSON into a user-friendly list of video titles and links: {video_data}")
                    st.subheader("Relevant Video Reviews:")
                    st.markdown(formatted_video_data)
                else:
                  st.error("No video results found or an error occurred.")
            except Exception as e:
                st.error(f"An error occurred: {e}")
       elif not hotel_name_for_videos and location:
           st.warning("Please enter hotel name")
       else:
           st.warning("Please enter a location and a hotel name")

if __name__ == "__main__":
    main()