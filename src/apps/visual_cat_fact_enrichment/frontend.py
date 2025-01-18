import streamlit as st
from src.apps.visual_cat_fact_enrichment import backend
from src.llm.gemini_text import generate_content
from src.config.setup import initialize_genai_client
from src.config.logging import logger
import json

gemini_client = initialize_genai_client()
MODEL_ID = "gemini-2.0-flash-exp"

def process_with_gemini(prompt: str) -> str:
    """
    Formats the given prompt using Gemini.

    Args:
        prompt (str): The prompt to process.

    Returns:
        str: The formatted text from Gemini.
    """
    try:
        response = generate_content(gemini_client, MODEL_ID, prompt)
        return response.text
    except Exception as e:
        logger.error(f"Error processing with Gemini: {e}")
        return "Failed to format response with Gemini."

def display_cat_fact_and_image(cat_fact_data: dict) -> None:
    """
    Displays a cat fact and corresponding image using Streamlit.

    Args:
        cat_fact_data (dict): A dictionary containing the cat fact and image URL.
    """
    try:
        if not cat_fact_data or "fact" not in cat_fact_data or "image_url" not in cat_fact_data:
            st.error("Invalid data format received.")
            return
        
        fact = cat_fact_data["fact"]
        image_url = cat_fact_data["image_url"]

        st.subheader("Cat Fact:")
        st.write(fact)

        if image_url:
           st.subheader("Related Image:")
           st.image(image_url, use_container_width=True)
        else:
            st.warning("No image found for this cat fact.")
            
    except Exception as e:
        logger.error(f"Error displaying cat fact and image: {e}")
        st.error("Failed to display cat fact and image.")

def main():
    """
    Primary entry point for the Streamlit application.
    Responsibilities:
    - Configure and render the user interface
    - Handle user inputs and interactions
    - Process and display data from backend
    - Format JSON responses using Gemini
    """
    st.title("Visual Cat Fact Enrichment")
    st.write("Get a random cat fact and an image related to the fact.")

    if st.button("Get a Cat Fact"):
        try:
            with st.spinner("Fetching cat fact and image..."):
                cat_data = backend.get_cat_fact_and_image()
                if cat_data and isinstance(cat_data, dict):
                   display_cat_fact_and_image(cat_data)
                else:
                    st.error("Failed to fetch data or invalid response format.")
        except Exception as e:
             logger.error(f"An error occurred in main: {e}")
             st.error("An error occurred while processing your request.")

if __name__ == "__main__":
    main()