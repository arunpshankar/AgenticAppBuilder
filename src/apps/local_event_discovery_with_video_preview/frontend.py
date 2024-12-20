import streamlit as st
from src.apps.local_event_discovery_with_video_preview import backend
from src.llm.gemini_text import generate_content
from src.config.client import initialize_genai_client
from src.config.logging import logger

gemini_client = initialize_genai_client()
MODEL_ID = "gemini-2.0-flash-exp"

def process_with_gemini(prompt: str) -> str:
    """
    Processes a prompt using Gemini to format text.

    Args:
        prompt (str): The prompt to send to Gemini.

    Returns:
        str: The formatted text from Gemini, or an error message.
    """
    try:
        response = generate_content(gemini_client, MODEL_ID, prompt)
        return response.text
    except Exception as e:
        logger.error(f"Error processing with Gemini: {e}")
        return f"Error: Could not process the text. {e}"


def main():
    """
    Primary entry point for the Streamlit application.
    Responsibilities:
    - Configure and render the user interface
    - Handle user inputs and interactions
    - Process and display data from backend
    - Format JSON responses using Gemini
    """
    st.title("Local Event Discovery with Video Preview")

    country_code = st.text_input("Enter Country Code (e.g., US, GB):", "US")
    language_code = st.text_input("Enter Language Code (e.g., en, es):", "en")
    event_type = st.text_input("Enter Event Type (e.g., concert, festival):", "concert")

    if st.button("Search Events"):
        try:
            with st.spinner("Fetching Events and Videos..."):
                events_data, video_data = backend.fetch_events_and_videos(country_code, language_code, event_type)

            if events_data and events_data.get("events"):
                st.subheader("Upcoming Events")
                for event in events_data["events"]:
                     formatted_event = process_with_gemini(f"Format this event information as a short readable sentence: {event}")
                     st.markdown(formatted_event, use_container_width = True)
            else:
                st.info("No events found for the specified criteria.")

            if video_data and video_data.get("videos"):
                 st.subheader("Related YouTube Videos")
                 for video in video_data["videos"]:
                      formatted_video = process_with_gemini(f"Format this video info into a short readable sentence: {video}")
                      st.markdown(formatted_video, use_container_width = True)
            else:
                st.info("No videos found related to the event type")


        except Exception as e:
             logger.error(f"An error occurred: {e}")
             st.error(f"An error occurred: {e}")


if __name__ == "__main__":
    main()