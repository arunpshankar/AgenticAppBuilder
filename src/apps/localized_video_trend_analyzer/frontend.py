import streamlit as st
from typing import Dict, List
from src.apps.localized_video_trend_analyzer import backend
from src.llm.gemini_text import generate_content
from src.config.setup import initialize_genai_client

gemini_client = initialize_genai_client()
MODEL_ID = "gemini-2.0-flash-exp"

def process_with_gemini(prompt: str) -> str:
    """
    Generates content using the Gemini model.

    Args:
        prompt (str): The prompt to send to Gemini.

    Returns:
        str: The text response from Gemini.
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
    st.title("Localized Video Trend Analyzer")

    query = st.text_input("Enter search query (e.g., funny cats):")
    geo = st.text_input("Enter geo code (e.g., US, GB):", "US")
    region = st.text_input("Enter region (e.g., CITY, STATE):", "CITY")

    if st.button("Analyze"):
        if query:
            try:
                trends_data, video_results = backend.fetch_trending_videos(query, geo, region)

                if trends_data and video_results:
                  st.subheader("Trending Regions and Topics")
                  
                  gemini_prompt_trends = f"""
                      Please format the following JSON data into a user-friendly list of trending regions and their interest values:
                      {trends_data}
                      Format this like "Region: Value" on a new line per region.
                  """

                  formatted_trends = process_with_gemini(gemini_prompt_trends)
                  st.write(formatted_trends)

                  st.subheader("Relevant Videos")

                  gemini_prompt_videos = f"""
                    Please format the following JSON data into a user-friendly list of video titles and links:
                    {video_results}
                    Format this as "Title: Link" on a new line for each video.
                  """

                  formatted_videos = process_with_gemini(gemini_prompt_videos)
                  st.write(formatted_videos)

                else:
                    st.error("No data found for the given query and region.")

            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.warning("Please enter a search query.")


if __name__ == "__main__":
    main()