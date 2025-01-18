import streamlit as st
from typing import Dict, List
from src.apps.image_source_verification import backend
from src.llm.gemini_text import generate_content
from src.config.setup import initialize_genai_client
from src.config.logging import logger

gemini_client = initialize_genai_client()
MODEL_ID = "gemini-2.0-flash-exp"

def process_with_gemini(prompt: str) -> str:
    """
    Processes a text prompt using the Gemini model.

    Args:
        prompt: The text prompt to send to the Gemini model.

    Returns:
        The text response from the Gemini model.
    """
    try:
        response = generate_content(gemini_client, MODEL_ID, prompt)
        return response.text
    except Exception as e:
        logger.error(f"Error processing with Gemini: {e}")
        return "Error processing text with Gemini."

def main():
    """
    Primary entry point for the Streamlit application.
    Responsibilities:
    - Configure and render the user interface
    - Handle user inputs and interactions
    - Process and display data from backend
    - Format JSON responses using Gemini
    """
    st.title("Image Source Verification")

    image_query = st.text_input("Enter image search query:", "cat memes")

    if st.button("Verify Image Source"):
        if not image_query:
            st.warning("Please enter an image search query.")
            return

        try:
            image_search_results = backend.search_images(image_query)
            if image_search_results and image_search_results.get('images_results'):
                st.subheader("Image Search Results:")
                for image in image_search_results['images_results'][:5]:  # Limit to 5 for display
                    st.image(image['thumbnail'], caption=f"Position: {image['position']}", width=200)
                    
                keywords = backend.extract_keywords_from_image_results(image_search_results)
                if keywords:
                  st.subheader("Extracted Keywords for Text Search")
                  st.write(", ".join(keywords))

                  text_search_results = backend.search_text_from_keywords(keywords)

                  if text_search_results and text_search_results.get('organic_results'):
                      st.subheader("Text Search Results:")
                      for result in text_search_results['organic_results'][:5]: # Limit to 5 for display
                          st.write(f"**Title:** {result['title']}")
                          st.write(f"**Link:** {result['link']}")
                          st.write("---")
                  else:
                       st.error("No text search results found.")

            else:
                st.error("No image search results found.")

        except Exception as e:
            logger.error(f"Error during verification process: {e}")
            st.error("An error occurred. Please check the logs for details.")

if __name__ == "__main__":
    main()