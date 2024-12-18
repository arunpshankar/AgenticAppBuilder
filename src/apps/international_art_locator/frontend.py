import streamlit as st
from typing import Dict, List
from src.apps.international_art_locator import backend
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
    st.title("International Art Locator")
    st.markdown("This service locates your approximate location and recommends art from the Art Institute of Chicago.")
    
    with st.spinner("Getting your location..."):
        location_data = backend.get_location_data()
    
    if location_data and "city" in location_data:
        st.success(f"Location Detected: {location_data['city']}, {location_data['region']}, {location_data['country']}")
    else:
         st.error("Could not determine location. Please ensure location services are enabled.")
         return
    
    with st.spinner("Fetching art..."):
       art_data = backend.get_art_data(location_data)

    if art_data and art_data["data"]:
          st.header("Recommended Artworks:")
          for artwork in art_data["data"]:
              st.subheader(artwork["title"])
              st.markdown(f"**Artist:** {artwork.get('artist_display', 'Unknown')}")
              st.markdown(f"**Date:** {artwork.get('date_display', 'Unknown')}")
              if artwork.get("image_id"):
                image_url = f"https://www.artic.edu/iiif/2/{artwork['image_id']}/full/843,/0/default.jpg"
                st.image(image_url, caption=artwork["title"], use_column_width=True)
              if artwork.get("description"):
                 formatted_description = process_with_gemini(f"Format this as markdown, use proper paragraph breaks, do not use numbered lists or bullet points: {artwork['description']}")
                 st.markdown(formatted_description, unsafe_allow_html=True)
              st.markdown("---")
    else:
          st.error("Could not retrieve artwork data. Please try again.")
          
if __name__ == "__main__":
    main()