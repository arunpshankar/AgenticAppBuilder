import streamlit as st
from typing import Dict, List
from src.apps.event_location_visualizer import backend
from src.llm.gemini_text import generate_content
from src.config.setup import initialize_genai_client

gemini_client = initialize_genai_client()
MODEL_ID = "gemini-2.0-flash-exp"

def process_with_gemini(prompt: str) -> str:
    """
    Processes a prompt with Gemini to format text.

    Args:
        prompt (str): The prompt to process.

    Returns:
        str: The formatted response from Gemini.
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
    st.title("Event Location Visualizer")

    query = st.text_input("Enter event query (e.g., 'Events in Austin, TX'):", "Events in Austin, TX")
    if st.button("Search"):
        with st.spinner("Searching for events..."):
            try:
                event_data = backend.search_events(query)
                if event_data and "events_results" in event_data and event_data["events_results"]:
                    for event in event_data["events_results"]:
                        st.subheader(event.get("title", "No Title"))
                        st.write(f"**Date:** {event.get('date', 'Not specified')}")
                        st.write(f"**Venue:** {event.get('venue', 'Not specified')}")
                        st.write(f"**Address:** {event.get('address', 'Not specified')}")

                        if "address" in event and event["address"]:
                          map_data = backend.search_maps(event["address"])
                          if map_data and "local_results" in map_data and map_data["local_results"]:
                              first_result = map_data["local_results"][0]
                              st.write(f"**Map Location: {first_result.get('title', 'No Title')}**")
                              
                          
                        if "title" in event and event["title"]:
                            image_data = backend.search_images(event["title"])
                            if image_data and "images_results" in image_data and image_data["images_results"]:
                              first_image = image_data["images_results"][0]
                              st.image(first_image.get("thumbnail", None), caption=f"Image related to {event['title']}", use_container_width=True)


                else:
                    st.warning("No events found for the given query.")

            except Exception as e:
                st.error(f"An error occurred: {e}")


if __name__ == "__main__":
    main()